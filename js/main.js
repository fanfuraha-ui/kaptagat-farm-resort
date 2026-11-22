/* Kaptagat Farm Resort: site script (no dependencies).
   Edit CONFIG for phone numbers, rates and the exchange rate.
   A room with kes: null shows "rate on request" and no estimate. */
{
const CONFIG = {
  phone: "254725859860",       // main line on the resort's Google listing
  whatsapp: "254706508637",    // from the resort's Facebook page: confirm it is on WhatsApp
  email: "",                   // add the resort's email to show the email buttons
  usdRate: 129,                // KES per 1 USD: update by hand
  formEndpoint: "",            // e.g. "https://formspree.io/f/xxxxxx"; empty = hand off to WhatsApp
  rooms: {
    cottage:  { name: "Decagon Cottage", kes: 7700 },
    pond:     { name: "Pond Cottage",    kes: null },
    standard: { name: "Standard Room",   kes: 4900 },
    cabin:    { name: "Deluxe Cabin",    kes: null },
    villa:    { name: "Villa",           kes: null },
    dorm:     { name: "Dormitory",       kes: null }
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

/* Rates and currency toggle */
let currency = store.lget("kfr-cur") || "KES";
const paintPrices = () => {
  $$("[data-kes]").forEach(el => {
    const kes = +el.dataset.kes;
    el.textContent = (el.dataset.from ? "From " : "") + (currency === "KES" ? fmtKES(kes) : fmtUSD(kes));
    const alt = el.parentElement.querySelector("[data-alt]");
    if (alt) alt.textContent = (currency === "KES" ? "≈ " + fmtUSD(kes) : "≈ " + fmtKES(kes)) + " · " + (el.dataset.unit || "per night");
  });
  $$(".cur button").forEach(b => b.setAttribute("aria-pressed", b.dataset.cur === currency));
};
$$(".cur button").forEach(b => b.addEventListener("click", () => { currency = b.dataset.cur; store.lset("kfr-cur", currency); paintPrices(); }));
paintPrices();

/* Dates: no past dates; check-out follows check-in */
const today = iso(new Date());
$$("input[type=date]").forEach(i => i.min = today);
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
const totalFor = (roomId, nights) => { const r = CONFIG.rooms[roomId]; return r.kes == null ? null : r.kes * nights; };
const estimateLine = d => d.total == null ? "Rate: to be confirmed" : `Estimate: ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)})`;
const buildMessage = d => [
  "Booking inquiry: Kaptagat Farm Resort",
  d.name && `Name: ${d.name}`,
  `Stay: ${CONFIG.rooms[d.room].name}`,
  `Check-in: ${niceDate(d.checkin)}`,
  `Check-out: ${niceDate(d.checkout)} (${plural(d.nights, "night")})`,
  `Guests: ${d.guests}`,
  estimateLine(d),
  d.phone && `Phone: ${d.phone}`,
  d.email && `Email: ${d.email}`,
  d.message && `Message: ${d.message}`
].filter(Boolean).join("\n");

/* Booking strip */
const bf = $("#booking-form");
if (bf) {
  const ci = $("#bk-in"), co = $("#bk-out"), gu = $("#bk-guests"), rm = $("#bk-room"), q = $("#quote");
  linkDates(ci, co);
  bf.addEventListener("submit", e => {
    e.preventDefault();
    let ok = setErr(ci, ci.value ? "" : "Choose a check-in date");
    ok = setErr(co, co.value && co.value > ci.value ? "" : "Check-out must be after check-in") && ok;
    ok = setErr(gu, +gu.value >= 1 ? "" : "Enter the number of guests") && ok;
    if (!ok) { $("[aria-invalid=true]", bf).focus(); return; }
    const nights = nightsBetween(ci.value, co.value);
    const d = { room: rm.value, checkin: ci.value, checkout: co.value, guests: +gu.value, nights, total: totalFor(rm.value, nights) };
    store.set("kfr-booking", JSON.stringify(d));
    const msg = buildMessage(d);
    const room = CONFIG.rooms[d.room];
    $("#q-total").textContent = d.total == null ? "Rate confirmed on inquiry" : fmtKES(d.total);
    $("#q-detail").textContent = `${room.name} · ${plural(nights, "night")} · ${plural(d.guests, "guest")}` + (d.total == null ? "" : ` · ≈ ${fmtUSD(d.total)}`);
    $("#q-wa").href = waLink(msg);
    const qm = $("#q-mail"); if (qm) qm.href = mailLink("Booking inquiry", msg);
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
    if (f("iq-company").value) return; // honeypot
    let ok = setErr(f("iq-name"), f("iq-name").value.trim().length > 1 ? "" : "Please enter your name");
    ok = setErr(f("iq-phone"), /^[+\d][\d\s-]{6,}$/.test(f("iq-phone").value) ? "" : "Enter a phone number, e.g. +254 712 345 678") && ok;
    const em = f("iq-email").value.trim();
    ok = setErr(f("iq-email"), !em || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em) ? "" : "Check the email address") && ok;
    ok = setErr(f("iq-in"), f("iq-in").value ? "" : "Choose a check-in date") && ok;
    ok = setErr(f("iq-out"), f("iq-out").value > f("iq-in").value ? "" : "Check-out must be after check-in") && ok;
    ok = setErr(f("iq-consent"), f("iq-consent").checked ? "" : "Please agree so we can reply to you") && ok;
    if (!ok) { $("[aria-invalid=true]", inf).focus(); return; }
    const nights = nightsBetween(f("iq-in").value, f("iq-out").value);
    const guests = +f("iq-guests").value || 1;
    const room = CONFIG.rooms[f("iq-room").value];
    const d = { name: f("iq-name").value.trim(), email: em, phone: f("iq-phone").value.trim(), room: f("iq-room").value, checkin: f("iq-in").value, checkout: f("iq-out").value, guests, nights, total: totalFor(f("iq-room").value, nights), message: f("iq-msg").value.trim() };
    const msg = buildMessage(d);
    $("#iq-wa").href = waLink(msg);
    const im = $("#iq-mail"); if (im) im.href = mailLink(`Booking inquiry: ${d.name}`, msg);
    $("#iq-summary").textContent = `${room.name}, ${niceDate(d.checkin)} to ${niceDate(d.checkout)}, ${plural(nights, "night")}, ${plural(guests, "guest")}. ` + (d.total == null ? "We'll confirm the rate." : `Estimate ${fmtKES(d.total)} (≈ ${fmtUSD(d.total)}).`);
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
      $("#iq-note").textContent = "Send it on WhatsApp. Your details are already filled in.";
    }
    const box = $("#iq-success"); box.classList.add("show"); box.focus();
  });
}

/* Site plan: key highlights its pin */
$$(".key li[data-pin]").forEach(li => {
  const pin = $(`.estate .pin[data-pin="${li.dataset.pin}"]`);
  if (!pin) return;
  const on = () => pin.classList.add("on"), off = () => pin.classList.remove("on");
  li.addEventListener("mouseenter", on); li.addEventListener("mouseleave", off);
  li.addEventListener("focus", on); li.addEventListener("blur", off);
});
}
