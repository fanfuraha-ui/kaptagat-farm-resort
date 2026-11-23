/* Kaptagat Farm Resort: site script (no dependencies).
   Edit CONFIG to update phone numbers, rates and the exchange rate. */
{
const CONFIG = {
  phone: "254725859860",       // main line (Google listing)
  whatsapp: "254706508637",    // confirm this number is on WhatsApp before launch
  email: "",                   // add the resort's email to show email buttons
  usdRate: 129,                // KES per 1 USD: update by hand
  formEndpoint: "",            // e.g. "https://formspree.io/f/xxxxxx"; empty = WhatsApp hand-off
  rooms: {                     // rates are indicative: confirm with the resort
    standard: { name: "Standard Room",   kes: 4900,  max: 2,  img: "room",          tag: "Garden block · river balcony" },
    cottage:  { name: "Decagon Cottage", kes: 7700,  max: 2,  img: "cottage",       tag: "Free-standing · bush stone" },
    pond:     { name: "Pond Cottage",    kes: 9500,  max: 2,  img: "pond-cottage",  tag: "Built in the middle of a pond" },
    cabin:    { name: "Deluxe Cabin",    kes: 9500,  max: 2,  img: "cabin",         tag: "Secluded corner of the grounds" },
    villa:    { name: "Garden Villa",    kes: 15000, max: 4,  img: "villa",         tag: "The most space on the farm" },
    dorm:     { name: "Dormitory",       kes: 1500,  max: 20, img: "dorm", tag: "Groups and training camps", perPerson: true }
  }
};

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const store = {
  get(k) { try { return sessionStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { sessionStorage.setItem(k, v); } catch {} },
  lget(k) { try { return localStorage.getItem(k); } catch { return null; } },
  lset(k, v) { try { localStorage.setItem(k, v); } catch {} }
};
const fmtKES = n => "KES " + Math.round(n).toLocaleString("en-KE");
const fmtUSD = n => "US$" + Math.round(n / CONFIG.usdRate).toLocaleString("en-US");
const fmtPhone = n => "+" + n.replace(/^(\d{3})(\d{3})(\d{3})(\d{3})$/, "$1 $2 $3 $4");
const waLink = text => `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(text)}`;
const mailLink = (subject, body) => `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
const iso = d => d.toISOString().slice(0, 10);
const nightsBetween = (a, b) => Math.round((new Date(b) - new Date(a)) / 864e5);
const niceDate = s => new Date(s + "T00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
const plural = (n, w) => `${n} ${w}${n == 1 ? "" : "s"}`;

/* Navigation */
const btn = $(".menu-btn"), nav = $("#nav");
if (btn && nav) {
  btn.addEventListener("click", () => btn.setAttribute("aria-expanded", nav.classList.toggle("open")));
  document.addEventListener("keydown", e => { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); } });
}
const here = location.pathname.split("/").pop() || "index.html";
$$("#nav a:not(.btn)").forEach(a => { if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page"); });

/* Contact details from CONFIG */
$$("[data-year]").forEach(el => el.textContent = new Date().getFullYear());
$$("[data-wa]").forEach(a => a.href = waLink(a.dataset.wa || "Hello Kaptagat Farm Resort, I'd like to ask about a stay."));
$$("[data-wa-text]").forEach(el => el.textContent = fmtPhone(CONFIG.whatsapp));
$$("[data-tel]").forEach(a => { a.href = "tel:+" + CONFIG.phone; a.textContent = fmtPhone(CONFIG.phone); });
$$("[data-needs-email]").forEach(el => el.hidden = !CONFIG.email);
$$("[data-email]").forEach(a => { a.href = "mailto:" + CONFIG.email; a.textContent = CONFIG.email; });

/* Prices and currency toggle */
let currency = store.lget("kfr-cur") || "KES";
const paintPrices = () => {
  $$("[data-kes]").forEach(el => {
    const kes = +el.dataset.kes;
    el.textContent = currency === "KES" ? fmtKES(kes) : fmtUSD(kes);
    const alt = el.parentElement.querySelector("[data-alt]");
    if (alt) alt.textContent = "≈ " + (currency === "KES" ? fmtUSD(kes) : fmtKES(kes)) + " · " + (el.dataset.unit || "per night");
  });
  $$(".cur button").forEach(b => b.setAttribute("aria-pressed", b.dataset.cur === currency));
};
$$(".cur button").forEach(b => b.addEventListener("click", () => { currency = b.dataset.cur; store.lset("kfr-cur", currency); paintPrices(); }));
paintPrices();

/* Dates: no past dates; check-out follows check-in */
const today = iso(new Date(new Date().setHours(12, 0, 0, 0)));
$$("input[type=date]").forEach(i => i.min = today);
const setErr = (input, msg) => {
  const box = $("#" + input.id + "-err");
  (input._t || input).setAttribute("aria-invalid", msg ? "true" : "false");
  if (box) box.textContent = msg || "";
  return !msg;
};
const totalFor = (roomId, nights, guests) => {
  const r = CONFIG.rooms[roomId];
  return r.perPerson ? r.kes * nights * guests : r.kes * nights;
};
const buildMessage = d => [
  "Booking inquiry: Kaptagat Farm Resort",
  d.name && `Name: ${d.name}`,
  `Stay: ${CONFIG.rooms[d.room].name}`,
  `Check-in: ${niceDate(d.checkin)}`,
  `Check-out: ${niceDate(d.checkout)} (${plural(d.nights, "night")})`,
  `Guests: ${d.guests}`,
  `Estimate: ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)})`,
  d.phone && `Phone: ${d.phone}`,
  d.email && `Email: ${d.email}`,
  d.message && `Message: ${d.message}`
].filter(Boolean).join("\n");

/* Premium pickers: select panel, guests stepper, range calendar */
const esc = t => String(t).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const svg = p => `<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
const ICON = { chev: '<path d="m6 9 6 6 6-6"/>', tick: '<path d="m5 12 5 5 9-10"/>', cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>', user: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.9c1.7.8 2.7 2.4 3 5.1"/>' };
const roomMeta = v => {
  const r = CONFIG.rooms[v];
  return { t: r.name, s: r.tag, thumb: `img/${r.img}.svg`, r: `From ${fmtKES(r.kes)} <span>${r.perPerson ? "per bed, per night" : "per night"} · sleeps ${r.max}</span>` };
};
const UI = (() => {
  const mq = matchMedia("(max-width:719px)");
  const fire = (el, t) => el.dispatchEvent(new Event(t, { bubbles: true }));
  const back = document.createElement("div"); back.className = "ui-back"; document.body.append(back);
  let cur = null;
  const closeAll = focus => {
    if (!cur) return; const c = cur; cur = null;
    c.panel.classList.remove("on"); back.classList.remove("on"); document.documentElement.classList.remove("ui-lock");
    $$(".strig[aria-expanded=true],.dtrig[aria-expanded=true]").forEach(t => t.setAttribute("aria-expanded", "false"));
    $$(".dtrig.act").forEach(t => t.classList.remove("act"));
    setTimeout(() => c.panel.remove(), 280);
    if (focus) c.trigger.focus({ preventScroll: true });
  };
  const place = (panel, anchor) => {
    if (mq.matches) { panel.classList.add("sheet"); back.classList.add("on"); document.documentElement.classList.add("ui-lock"); return; }
    const r = anchor.getBoundingClientRect(), w = panel.offsetWidth, h = panel.offsetHeight;
    const left = Math.min(Math.max(12, r.left), innerWidth - w - 12);
    const above = r.bottom + h + 16 > innerHeight && r.top > h + 90;
    panel.style.left = left + scrollX + "px";
    panel.style.top = (above ? r.top - h - 10 : r.bottom + 10) + scrollY + "px";
    panel.style.transformOrigin = `${Math.max(20, r.left - left + 40)}px ${above ? "100%" : "0"}`;
  };
  const open = (trigger, anchor, cls, build) => {
    closeAll(false);
    const panel = document.createElement("div"); panel.className = "ui-pop " + cls; document.body.append(panel);
    cur = { panel, trigger }; build(panel);
    trigger.setAttribute("aria-expanded", "true"); place(panel, anchor);
    requestAnimationFrame(() => requestAnimationFrame(() => panel.classList.add("on")));
    if (!mq.matches) setTimeout(() => { const r = panel.getBoundingClientRect(); if (r.bottom > innerHeight - 12) scrollBy({ top: Math.min(r.bottom - innerHeight + 24, r.top - 90), behavior: "smooth" }); }, 40);
    return cur;
  };
  document.addEventListener("pointerdown", e => { if (cur && !cur.panel.contains(e.target) && !e.target.closest(".strig,.dtrig")) closeAll(false); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && cur) { e.preventDefault(); closeAll(true); } });
  back.addEventListener("click", () => closeAll(true));
  addEventListener("resize", () => { if (cur && !mq.matches) closeAll(false); });
  const hook = (input, trig, label) => {
    input.hidden = true; input.tabIndex = -1; input._t = trig; trig.id = input.id + "-t";
    const l = input.id && document.querySelector(`label[for="${input.id}"]`); if (l) l.htmlFor = trig.id;
    input.after(trig);
  };

  /* select */
  const select = (sel, meta, eyebrow, title) => {
    const t = document.createElement("button"); t.type = "button"; t.className = "strig";
    t.setAttribute("aria-haspopup", "listbox"); t.setAttribute("aria-expanded", "false");
    const paint = () => { const m = meta(sel.value); t.innerHTML = `${m.thumb ? `<img src="${m.thumb}" alt="">` : ""}<span>${esc(m.t)}</span>${svg(ICON.chev)}`; t.setAttribute("aria-label", `${eyebrow}: ${m.t}`); };
    hook(sel, t); paint(); sel.addEventListener("change", paint);
    t.addEventListener("click", () => {
      if (cur && cur.trigger === t) return closeAll(true);
      open(t, sel.closest(".field"), "ui-sel", panel => {
        panel.setAttribute("role", "listbox"); panel.setAttribute("aria-label", title);
        panel.innerHTML = `<div class="ui-grab"></div><div class="ui-h"><small>${esc(eyebrow)}</small><b>${esc(title)}</b></div><div class="ui-list">` +
          [...sel.options].map((o, i) => { const m = meta(o.value);
            return `<div class="ui-o" role="option" tabindex="-1" data-v="${esc(o.value)}" aria-selected="${o.value === sel.value}" style="--i:${i}"><img src="${m.thumb}" alt=""><span class="ui-t"><b>${esc(m.t)}</b><em>${esc(m.s)}</em>${m.r ? `<i>${m.r}</i>` : ""}</span><span class="ui-k">${svg(ICON.tick)}</span></div>`; }).join("") + "</div>";
        const choose = o => { sel.value = o.dataset.v; fire(sel, "change"); $$(".ui-o", panel).forEach(x => x.setAttribute("aria-selected", x === o)); setTimeout(() => closeAll(true), 200); };
        panel.addEventListener("click", e => { const o = e.target.closest(".ui-o"); if (o) choose(o); });
        panel.addEventListener("keydown", e => {
          const it = $$(".ui-o", panel), i = it.indexOf(document.activeElement);
          if (e.key === "ArrowDown") { e.preventDefault(); it[Math.min(it.length - 1, i + 1)].focus(); }
          else if (e.key === "ArrowUp") { e.preventDefault(); it[Math.max(0, i - 1)].focus(); }
          else if ((e.key === "Enter" || e.key === " ") && i > -1) { e.preventDefault(); choose(it[i]); }
        });
        setTimeout(() => ($('[aria-selected="true"]', panel) || $(".ui-o", panel)).focus({ preventScroll: true }), 60);
      });
    });
  };

  /* guests stepper */
  const stepper = (inp, roomOf) => {
    const min = +inp.min || 1, max = +inp.max || 40;
    const t = document.createElement("button"); t.type = "button"; t.className = "strig";
    t.setAttribute("aria-haspopup", "dialog"); t.setAttribute("aria-expanded", "false");
    const word = n => `${n} guest${n == 1 ? "" : "s"}`;
    const paint = () => { t.innerHTML = `${svg(ICON.user)}<span>${word(+inp.value || min)}</span>${svg(ICON.chev)}`; t.setAttribute("aria-label", `Guests: ${word(+inp.value || min)}`); };
    hook(inp, t); paint(); inp.addEventListener("change", paint);
    t.addEventListener("click", () => {
      if (cur && cur.trigger === t) return closeAll(true);
      open(t, inp.closest(".field"), "ui-gst", panel => {
        panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Number of guests");
        const draw = () => {
          const n = +inp.value || min, r = roomOf(), over = n > r.max;
          panel.innerHTML = `<div class="ui-grab"></div><div class="ui-h"><small>Who's coming</small><b>Number of guests</b></div>
            <div class="gst"><button type="button" data-s="-1" aria-label="One fewer guest" ${n <= min ? "disabled" : ""}>−</button><div><output aria-live="polite">${n}</output><small>guest${n == 1 ? "" : "s"}</small></div><button type="button" data-s="1" aria-label="One more guest" ${n >= max ? "disabled" : ""}>+</button></div>
            <p class="gst-note">${over ? `<b>${esc(r.name)}</b> sleeps up to ${r.max}. Pick another stay or message us for a group booking.` : `<b>${esc(r.name)}</b> sleeps up to ${r.max}${r.perPerson ? " beds" : ""}.`}</p>
            <div class="gst-go"><button type="button" class="btn btn-sm" data-done>Done</button></div>`;
        };
        draw();
        panel.addEventListener("click", e => {
          const s = e.target.closest("[data-s]");
          if (s) { inp.value = Math.min(max, Math.max(min, (+inp.value || min) + +s.dataset.s)); fire(inp, "input"); fire(inp, "change"); draw(); const b = $(`[data-s="${s.dataset.s}"]`, panel); if (b && !b.disabled) b.focus({ preventScroll: true }); }
          if (e.target.closest("[data-done]")) closeAll(true);
        });
        setTimeout(() => $("[data-s='1']", panel).focus({ preventScroll: true }), 60);
      });
    });
  };

  /* range calendar */
  const MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const dObj = v => new Date(v + "T12:00:00");
  const short = v => dObj(v).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
  const pair = (inEl, outEl) => {
    const P = { stage: "in", view: null, hover: "" };
    const mk = el => { const b = document.createElement("button"); b.type = "button"; b.className = "dtrig"; b.setAttribute("aria-haspopup", "dialog"); b.setAttribute("aria-expanded", "false"); hook(el, b); return b; };
    P.bi = mk(inEl); P.bo = mk(outEl);
    const paint = () => [[P.bi, inEl, "Check-in"], [P.bo, outEl, "Check-out"]].forEach(([b, el, l]) => { b.innerHTML = `${svg(ICON.cal)}<span class="${el.value ? "" : "ph"}">${el.value ? short(el.value) : "Add date"}</span>`; b.setAttribute("aria-label", `${l}: ${el.value ? niceDate(el.value) : "not chosen"}`); });
    [inEl, outEl].forEach(el => el.addEventListener("change", paint)); paint();
    const thisMonth = new Date(); thisMonth.setDate(1); thisMonth.setHours(12);
    const render = () => {
      const panel = P.panel, ci = inEl.value, co = outEl.value, n = mq.matches ? 1 : 2;
      const canBack = P.view > thisMonth;
      let h = `<div class="ui-grab"></div><div class="cal-top"><div class="ui-h"><small>${P.stage === "in" ? "Step 1 of 2" : "Step 2 of 2"}</small><b>${P.stage === "in" ? "Choose your check-in" : "Now your check-out"}</b></div>
        <div class="cal-nav"><button type="button" data-nav="-1" aria-label="Previous month" ${canBack ? "" : "disabled"}>‹</button><button type="button" data-nav="1" aria-label="Next month">›</button></div></div><div class="cal-months">`;
      for (let k = 0; k < n; k++) {
        const m = new Date(P.view.getFullYear(), P.view.getMonth() + k, 1, 12);
        h += `<div class="cal-m"><h4>${MON[m.getMonth()]} <em>${m.getFullYear()}</em></h4><div class="cal-w">${["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map(d => `<span>${d}</span>`).join("")}</div><div class="cal-g">` + "<i></i>".repeat((m.getDay() + 6) % 7);
        const days = new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
        for (let d = 1; d <= days; d++) {
          const v = iso(new Date(m.getFullYear(), m.getMonth(), d, 12));
          const end = co || (P.stage === "out" && P.hover > ci ? P.hover : "");
          const cls = [v === ci && "s", v === co && "e", ci && end && v > ci && v < end && "r", ci && end && v === end && !co && "hv", v === today && "t"].filter(Boolean).join(" ");
          const dis = v < today || (P.stage === "out" && ci && v === ci);
          h += `<button type="button" class="${cls}" data-d="${v}" ${dis ? "disabled" : ""} aria-label="${niceDate(v)}" aria-pressed="${v === ci || v === co}">${d}</button>`;
        }
        h += "</div></div>";
      }
      const nn = ci && co ? nightsBetween(ci, co) : 0;
      h += `</div><div class="cal-foot"><div class="cal-sum"><span><small>Check-in</small>${ci ? short(ci) : "—"}</span><i></i><span><small>Check-out</small>${co ? short(co) : "—"}</span>${nn ? `<strong>${nn}<small>night${nn > 1 ? "s" : ""}</small></strong>` : ""}</div>
        <div class="cal-act"><button type="button" class="cal-clear">Clear</button><button type="button" class="btn cal-done" ${nn ? "" : "disabled"}>Done</button></div></div>`;
      panel.innerHTML = h;
      P.bi.classList.toggle("act", P.stage === "in"); P.bo.classList.toggle("act", P.stage === "out");
    };
    const onClick = e => {
      const nav = e.target.closest("[data-nav]");
      if (nav) { P.view = new Date(P.view.getFullYear(), P.view.getMonth() + +nav.dataset.nav, 1, 12); render(); return; }
      const d = e.target.closest("[data-d]");
      if (d) {
        const v = d.dataset.d;
        if (P.stage === "in" || !inEl.value || v < inEl.value) { inEl.value = v; outEl.value = ""; P.stage = "out"; paint(); fire(inEl, "input"); render(); }
        else { outEl.value = v; paint(); fire(inEl, "change"); fire(outEl, "change"); render(); setTimeout(() => closeAll(true), 420); }
        return;
      }
      if (e.target.closest(".cal-clear")) { inEl.value = outEl.value = ""; P.stage = "in"; P.hover = ""; paint(); fire(inEl, "input"); render(); }
      if (e.target.closest(".cal-done")) closeAll(true);
    };
    const onHover = e => {
      if (P.stage !== "out" || !inEl.value || outEl.value) return;
      const d = e.target.closest("[data-d]"); const v = d ? d.dataset.d : "";
      if (v === P.hover) return; P.hover = v;
      $$("[data-d]", P.panel).forEach(b => { const x = b.dataset.d; b.classList.toggle("r", !!v && v > inEl.value && x > inEl.value && x < v); b.classList.toggle("hv", !!v && v > inEl.value && x === v); });
    };
    const show = stage => {
      const st = stage === "out" && !inEl.value ? "in" : stage;
      if (cur && cur.pair === P) { P.stage = st; render(); return; }
      P.stage = st; P.hover = "";
      const base = inEl.value ? dObj(inEl.value) : new Date(); P.view = new Date(base.getFullYear(), base.getMonth(), 1, 12);
      const c = open(st === "in" ? P.bi : P.bo, inEl.closest(".field"), "ui-cal", panel => {
        P.panel = panel; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Choose your dates");
        panel.addEventListener("click", onClick); panel.addEventListener("mouseover", onHover); render();
      });
      c.pair = P;
      setTimeout(() => { const f = $(".s,[data-d]:not([disabled])", P.panel); f && f.focus({ preventScroll: true }); }, 80);
    };
    P.bi.addEventListener("click", () => show("in")); P.bo.addEventListener("click", () => show("out"));
    return { show };
  };
  return { select, stepper, pair, closeAll };
})();

/* Booking bar */
const bf = $("#booking-form");
if (bf) {
  const ci = $("#bk-in"), co = $("#bk-out"), gu = $("#bk-guests"), rm = $("#bk-room");
  UI.select(rm, roomMeta, "Where to stay", "Choose your stay");
  const cal = UI.pair(ci, co);
  UI.stepper(gu, () => CONFIG.rooms[rm.value]);
  const rvw = $("#rvw");
  const review = d => {
    const r = CONFIG.rooms[d.room], msg = buildMessage(d);
    const part = (v, l) => { const t = new Date(v + "T12:00:00"); return `<div><small>${l}</small><b>${t.getDate()}</b><span>${t.toLocaleDateString("en-GB", { month: "short" })} · ${t.toLocaleDateString("en-GB", { weekday: "short" })}</span></div>`; };
    $("#rvwImg").innerHTML = `<img src="img/${r.img}.svg" alt=""><div class="rvw-cap"><small>Your stay</small><b>${esc(r.name)}</b><span>${esc(r.tag)}</span></div>`;
    $("#rvwDates").innerHTML = part(d.checkin, "Check-in") + `<div class="tk-n"><i>${d.nights}</i><em>night${d.nights > 1 ? "s" : ""}</em></div>` + part(d.checkout, "Check-out");
    $("#rvwList").innerHTML = [["Stay", r.name], ["Guests", plural(d.guests, "guest")]].map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join("")
      + `<div class="tot"><dt>Estimate</dt><dd>${fmtKES(d.total)}<small>≈ ${fmtUSD(d.total)} · indicative</small></dd></div>`;
    $("#rvwWa").href = waLink(msg);
    const m = $("#rvwMail"); if (m) m.href = mailLink("Booking inquiry", msg);
    rvw.showModal();
  };
  if (rvw) {
    $("#rvwEdit").addEventListener("click", () => { rvw.close(); $("#booking").scrollIntoView({ behavior: "smooth" }); });
    $("#rvwX").addEventListener("click", () => rvw.close());
    rvw.addEventListener("click", e => { if (e.target === rvw) rvw.close(); });
  }
  bf.addEventListener("submit", e => {
    e.preventDefault();
    let ok = setErr(ci, ci.value ? "" : "Choose a check-in date");
    ok = setErr(co, co.value && co.value > ci.value ? "" : "Choose a check-out date") && ok;
    const room = CONFIG.rooms[rm.value];
    ok = setErr(gu, +gu.value <= room.max ? "" : `${room.name} sleeps up to ${room.max}`) && ok;
    if (!ok) { if (!ci.value || !co.value) cal.show(ci.value ? "out" : "in"); else $("[aria-invalid=true]", bf).focus(); return; }
    const nights = nightsBetween(ci.value, co.value);
    const d = { room: rm.value, checkin: ci.value, checkout: co.value, guests: +gu.value, nights, total: totalFor(rm.value, nights, +gu.value) };
    store.set("kfr-booking", JSON.stringify(d));
    review(d);
  });
  [ci, co, gu, rm].forEach(el => el.addEventListener("change", () => setErr(el, "")));
}

/* Inquiry form */
const inf = $("#inquiry-form");
if (inf) {
  const f = id => $("#" + id);
  try {
    const saved = JSON.parse(store.get("kfr-booking") || "null");
    if (saved) { f("iq-in").value = saved.checkin; f("iq-out").value = saved.checkout; f("iq-guests").value = saved.guests; f("iq-room").value = saved.room; }
  } catch {}
  UI.select(f("iq-room"), roomMeta, "Where to stay", "Choose your stay");
  UI.pair(f("iq-in"), f("iq-out"));
  UI.stepper(f("iq-guests"), () => CONFIG.rooms[f("iq-room").value]);
  inf.addEventListener("submit", async e => {
    e.preventDefault();
    if (f("iq-company").value) return; // honeypot
    let ok = setErr(f("iq-name"), f("iq-name").value.trim().length > 1 ? "" : "Please enter your name");
    ok = setErr(f("iq-phone"), /^[+\d][\d\s-]{6,}$/.test(f("iq-phone").value) ? "" : "Enter a phone number, e.g. +254 712 345 678") && ok;
    const em = f("iq-email").value.trim();
    ok = setErr(f("iq-email"), !em || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em) ? "" : "Check the email address") && ok;
    ok = setErr(f("iq-in"), f("iq-in").value ? "" : "Choose a check-in date") && ok;
    ok = setErr(f("iq-out"), f("iq-out").value > f("iq-in").value ? "" : "Check-out must be after check-in") && ok;
    ok = setErr(f("iq-consent"), f("iq-consent").checked ? "" : "Please agree so we can reply to you") && ok;
    if (!ok) { $("[aria-invalid=true]", inf).focus(); return; }
    const room = CONFIG.rooms[f("iq-room").value];
    const nights = nightsBetween(f("iq-in").value, f("iq-out").value);
    const guests = +f("iq-guests").value;
    const d = { name: f("iq-name").value.trim(), email: em, phone: f("iq-phone").value.trim(), room: f("iq-room").value, checkin: f("iq-in").value, checkout: f("iq-out").value, guests, nights, total: totalFor(f("iq-room").value, nights, guests), message: f("iq-msg").value.trim() };
    const msg = buildMessage(d);
    $("#iq-wa").href = waLink(msg);
    const im = $("#iq-mail"); if (im) im.href = mailLink(`Booking inquiry: ${d.name}`, msg);
    $("#iq-summary").textContent = `${room.name}, ${niceDate(d.checkin)} to ${niceDate(d.checkout)}, ${plural(nights, "night")}, ${plural(guests, "guest")}. Estimate ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)}).`;
    if (CONFIG.formEndpoint) {
      try {
        const r = await fetch(CONFIG.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(d) });
        if (!r.ok) throw new Error(r.status);
        $("#iq-title").textContent = "Thank you, we have your inquiry.";
        $("#iq-note").textContent = "We'll confirm availability by phone or WhatsApp. For a faster reply, message us now:";
      } catch {
        $("#iq-title").textContent = "We couldn't send the form just now.";
        $("#iq-note").textContent = "Please send it on WhatsApp instead. Your details are already filled in:";
      }
    } else {
      $("#iq-title").textContent = "Your inquiry is ready to send.";
      $("#iq-note").textContent = "Tap below to send it on WhatsApp. Your details are already filled in.";
    }
    const box = $("#iq-success"); box.classList.add("show"); box.focus();
  });
}

/* Estate map: legend highlights its pin */
$$(".legend li[data-pin]").forEach(li => {
  const pin = $(`.estate .pin[data-pin="${li.dataset.pin}"]`);
  if (!pin) return;
  const on = () => pin.classList.add("on"), off = () => pin.classList.remove("on");
  li.addEventListener("mouseenter", on); li.addEventListener("mouseleave", off);
  li.addEventListener("focus", on); li.addEventListener("blur", off);
});

/* Gallery: filters + lightbox */
const gal = $(".gallery");
if (gal) {
  const items = $$("figure", gal);
  $$(".filters button").forEach(b => b.addEventListener("click", () => {
    $$(".filters button").forEach(x => x.setAttribute("aria-pressed", x === b));
    items.forEach(fig => fig.hidden = b.dataset.f !== "all" && fig.dataset.cat !== b.dataset.f);
  }));
  const preset = $(`.filters [data-f="${location.hash.slice(1)}"]`);
  if (preset) preset.click();
  const dlg = $("#lightbox"), gImg = $("#gImg"), cats = { rooms: "Rooms", dining: "Dining", nature: "Nature & grounds" };
  let idx = 0, built = false;
  const visible = () => items.filter(x => !x.hidden);
  const show = i => {
    const v = visible(); idx = (i + v.length) % v.length;
    const fi = $("img", v[idx]);
    gImg.classList.remove("in");
    const done = () => requestAnimationFrame(() => gImg.classList.add("in"));
    gImg.onload = done; gImg.src = fi.src; gImg.alt = fi.alt; if (gImg.complete) done();
    $("#gEy").textContent = cats[v[idx].dataset.cat] || "Gallery";
    $("#gTi").textContent = $("figcaption", v[idx]).textContent;
    $("#gCur").textContent = String(idx + 1).padStart(2, "0");
    $("#gTot").textContent = String(v.length).padStart(2, "0");
    $("#gBar").style.width = ((idx + 1) / v.length * 100) + "%";
    $$("#gTh button").forEach((b, k) => { b.setAttribute("aria-current", k === idx); if (k === idx) b.scrollIntoView({ inline: "center", block: "nearest", behavior: "smooth" }); });
  };
  const openAt = fig => {
    const v = visible();
    $("#gTh").innerHTML = v.map((x, k) => `<button type="button" aria-label="Picture ${k + 1}"><img src="${$("img", x).src}" alt=""></button>`).join("");
    $$("#gTh button").forEach((b, k) => b.addEventListener("click", () => show(k)));
    dlg.showModal(); show(v.indexOf(fig));
  };
  items.forEach(fig => $("button", fig).addEventListener("click", () => openAt(fig)));
  $("#gP").addEventListener("click", () => show(idx - 1));
  $("#gN").addEventListener("click", () => show(idx + 1));
  $("#gX").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", e => { if (e.target === dlg || e.target.classList.contains("glb-stage")) dlg.close(); });
  dlg.addEventListener("keydown", e => { if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1); });
}
}
