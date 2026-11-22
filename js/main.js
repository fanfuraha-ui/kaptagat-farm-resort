/* Kaptagat Farm Resort: site script (no dependencies)
   Edit CONFIG to update contact details, rates and the exchange rate. */
{
const CONFIG = {
  whatsapp: "254700000000",            // SAMPLE: international format, no + or spaces
  email: "stay@kaptagatfarmresort.co.ke", // SAMPLE
  usdRate: 129,                        // KES per 1 USD: update by hand
  formEndpoint: "",                    // e.g. "https://formspree.io/f/xxxxxx"; empty = WhatsApp/email hand-off
  rooms: {
    garden:   { name: "Garden Room",     kes: 9500,  max: 2 },
    suite:    { name: "Farmhouse Suite", kes: 13500, max: 2 },
    cottage:  { name: "Family Cottage",  kes: 18000, max: 5 }
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
const waLink = text => `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(text)}`;
const mailLink = (subject, body) => `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
const iso = d => d.toISOString().slice(0, 10);
const nightsBetween = (a, b) => Math.round((new Date(b) - new Date(a)) / 864e5);
const niceDate = s => new Date(s + "T00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", year: "numeric" });

/* Navigation */
const btn = $(".menu-btn"), nav = $("#nav");
if (btn && nav) {
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); } });
}
const here = location.pathname.split("/").pop() || "index.html";
$$("#nav a:not(.btn)").forEach(a => { if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page"); });
$$("[data-year]").forEach(el => el.textContent = new Date().getFullYear());
$$("[data-wa]").forEach(a => a.href = waLink(a.dataset.wa || "Hello Kaptagat Farm Resort, I'd like to ask about a stay."));
$$("[data-email]").forEach(a => { a.href = "mailto:" + CONFIG.email; if (!a.textContent.trim()) a.textContent = CONFIG.email; });
$$("[data-email-text]").forEach(el => el.textContent = CONFIG.email);
$$("[data-phone-text]").forEach(el => el.textContent = "+" + CONFIG.whatsapp.replace(/^(\d{3})(\d{3})(\d{3})(\d{3})$/, "$1 $2 $3 $4"));

/* Prices and currency toggle */
let currency = store.lget("kfr-cur") || "KES";
const paintPrices = () => {
  $$("[data-kes]").forEach(el => {
    const kes = +el.dataset.kes;
    el.textContent = currency === "KES" ? fmtKES(kes) : fmtUSD(kes);
    const alt = el.parentElement.querySelector("[data-alt]");
    if (alt) alt.textContent = "≈ " + (currency === "KES" ? fmtUSD(kes) : fmtKES(kes)) + " · per night, B&B for two";
  });
  $$(".cur button").forEach(b => b.setAttribute("aria-pressed", b.dataset.cur === currency));
};
$$(".cur button").forEach(b => b.addEventListener("click", () => { currency = b.dataset.cur; store.lset("kfr-cur", currency); paintPrices(); }));
paintPrices();

/* Date inputs: no past dates */
const today = iso(new Date());
$$('input[type=date]').forEach(i => i.min = today);
const linkDates = (inEl, outEl) => {
  if (!inEl || !outEl) return;
  inEl.addEventListener("change", () => {
    if (!inEl.value) return;
    const next = new Date(inEl.value); next.setDate(next.getDate() + 1);
    outEl.min = iso(next);
    if (!outEl.value || outEl.value <= inEl.value) outEl.value = iso(next);
  });
};

const setErr = (input, msg) => {
  const box = $("#" + input.id + "-err");
  input.setAttribute("aria-invalid", msg ? "true" : "false");
  if (box) box.textContent = msg || "";
  return !msg;
};

const buildMessage = d => [
  "Booking inquiry: Kaptagat Farm Resort",
  d.name ? `Name: ${d.name}` : "",
  `Room: ${CONFIG.rooms[d.room].name}`,
  `Check-in: ${niceDate(d.checkin)}`,
  `Check-out: ${niceDate(d.checkout)} (${d.nights} night${d.nights > 1 ? "s" : ""})`,
  `Guests: ${d.guests}`,
  `Estimate: ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)})`,
  d.phone ? `Phone: ${d.phone}` : "",
  d.email ? `Email: ${d.email}` : "",
  d.message ? `Message: ${d.message}` : ""
].filter(Boolean).join("\n");

/* Booking bar */
const bf = $("#booking-form");
if (bf) {
  const ci = $("#bk-in"), co = $("#bk-out"), gu = $("#bk-guests"), rm = $("#bk-room"), q = $("#quote");
  linkDates(ci, co);
  bf.addEventListener("submit", e => {
    e.preventDefault();
    let ok = setErr(ci, ci.value ? "" : "Choose a check-in date");
    ok = setErr(co, co.value && co.value > ci.value ? "" : "Check-out must be after check-in") && ok;
    const room = CONFIG.rooms[rm.value];
    ok = setErr(gu, +gu.value <= room.max ? "" : `${room.name} sleeps up to ${room.max}`) && ok;
    if (!ok) { $("[aria-invalid=true]", bf).focus(); return; }
    const nights = nightsBetween(ci.value, co.value);
    const d = { room: rm.value, checkin: ci.value, checkout: co.value, guests: gu.value, nights, total: nights * room.kes };
    store.set("kfr-booking", JSON.stringify(d));
    const msg = buildMessage(d);
    $("#q-total").textContent = fmtKES(d.total);
    $("#q-detail").textContent = `${room.name} · ${nights} night${nights > 1 ? "s" : ""} · ${gu.value} guest${gu.value > 1 ? "s" : ""} · ≈ ${fmtUSD(d.total)}`;
    $("#q-wa").href = waLink(msg);
    $("#q-mail").href = mailLink("Booking inquiry", msg);
    q.classList.add("show");
    q.focus();
  });
}

/* Inquiry form */
const inf = $("#inquiry-form");
if (inf) {
  const f = id => $("#" + id);
  linkDates(f("iq-in"), f("iq-out"));
  try {
    const saved = JSON.parse(store.get("kfr-booking") || "null");
    if (saved) { f("iq-in").value = saved.checkin; f("iq-out").value = saved.checkout; f("iq-guests").value = saved.guests; f("iq-room").value = saved.room; }
  } catch {}
  inf.addEventListener("submit", async e => {
    e.preventDefault();
    if (f("iq-company").value) return; // honeypot: bots fill hidden field
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f("iq-email").value);
    let ok = setErr(f("iq-name"), f("iq-name").value.trim().length > 1 ? "" : "Please enter your name");
    ok = setErr(f("iq-email"), emailOk ? "" : "Enter a valid email address") && ok;
    ok = setErr(f("iq-phone"), /^[+\d][\d\s-]{6,}$/.test(f("iq-phone").value) ? "" : "Enter a phone number, e.g. +254 712 345 678") && ok;
    ok = setErr(f("iq-in"), f("iq-in").value ? "" : "Choose a check-in date") && ok;
    ok = setErr(f("iq-out"), f("iq-out").value > f("iq-in").value ? "" : "Check-out must be after check-in") && ok;
    ok = setErr(f("iq-consent"), f("iq-consent").checked ? "" : "Please agree so we can reply to you") && ok;
    if (!ok) { $("[aria-invalid=true]", inf).focus(); return; }
    const room = CONFIG.rooms[f("iq-room").value];
    const nights = nightsBetween(f("iq-in").value, f("iq-out").value);
    const d = { name: f("iq-name").value.trim(), email: f("iq-email").value.trim(), phone: f("iq-phone").value.trim(), room: f("iq-room").value, checkin: f("iq-in").value, checkout: f("iq-out").value, guests: f("iq-guests").value, nights, total: nights * room.kes, message: f("iq-msg").value.trim() };
    const msg = buildMessage(d);
    const box = $("#iq-success");
    $("#iq-wa").href = waLink(msg);
    $("#iq-mail").href = mailLink(`Booking inquiry: ${d.name}`, msg);
    $("#iq-summary").textContent = `${room.name}, ${niceDate(d.checkin)} to ${niceDate(d.checkout)}, ${nights} night${nights > 1 ? "s" : ""}. Estimate ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)}).`;
    if (CONFIG.formEndpoint) {
      try {
        const r = await fetch(CONFIG.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(d) });
        if (!r.ok) throw new Error(r.status);
        $("#iq-title").textContent = "Thank you, your inquiry has been received.";
        $("#iq-note").textContent = "We'll confirm availability by email or WhatsApp within a few hours. For a faster reply, you can also message us now:";
      } catch {
        $("#iq-title").textContent = "We couldn't send the form just now.";
        $("#iq-note").textContent = "Please send your inquiry on WhatsApp or email instead. Everything is filled in for you:";
      }
    } else {
      $("#iq-title").textContent = "Your inquiry is ready to send.";
      $("#iq-note").textContent = "Choose WhatsApp or email. Your details are already filled in. We confirm availability within a few hours.";
    }
    box.classList.add("show");
    box.focus();
  });
}

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
  const dlg = $("#lightbox"), img = $("#lb-img"), cap = $("#lb-cap");
  let idx = 0;
  const visible = () => items.filter(x => !x.hidden);
  const show = i => {
    const v = visible(); idx = (i + v.length) % v.length;
    const fi = $("img", v[idx]);
    img.src = fi.src; img.alt = fi.alt; cap.textContent = $("figcaption", v[idx]).textContent;
  };
  items.forEach(fig => $("button", fig).addEventListener("click", () => { show(visible().indexOf(fig)); dlg.showModal(); }));
  $("#lb-prev").addEventListener("click", () => show(idx - 1));
  $("#lb-next").addEventListener("click", () => show(idx + 1));
  $("#lb-close").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("keydown", e => { if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1); });
}
}
