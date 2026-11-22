#!/usr/bin/env python3
"""Builds the static Kaptagat Farm Resort site (pages and line drawings). Run: python3 tools/build.py <output folder>

Copy is limited to what public listings and visitor accounts say about the resort. Anything not yet
confirmed (rates for four stay types, email address, the real site plan) is left out or marked as
"on request" rather than invented."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import art

OUT = pathlib.Path(sys.argv[1])
SITE = "https://kaptagatfarmresort.co.ke"   # placeholder domain: replace before launch
GOOGLE = "https://www.google.co.ke/travel/hotels/entity/CgoIy7v0kISag-1pEAE"
FB = "https://www.facebook.com/Kaptagatfarmresort/"
IG = "https://www.instagram.com/kaptagat_farm_resort/"
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=CFG8%2B65C+Kaptarakwa%2C+Kenya"

WA_ICON = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.6 3.6 0 0 0-1.1 2.7 6.3 6.3 0 0 0 1.3 3.3 14.4 14.4 0 0 0 5.5 4.9c2 .9 2.8.9 3.8.8a3.3 3.3 0 0 0 2.2-1.5 2.7 2.7 0 0 0 .2-1.5c-.1-.2-.3-.3-.6-.5z"/></svg>'
NAV = [("index.html", "Home"), ("accommodations.html", "Stay"), ("experiences.html", "Dine &amp; explore"), ("contact.html", "Contact")]

def url(path): return f"{SITE}/{'' if path == 'index.html' else path}"

def head(title, desc, path, extra=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url(path)}">
<meta name="theme-color" content="#1C3427">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kaptagat Farm Resort">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(path)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&amp;family=Public+Sans:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="Kaptagat Farm Resort, home">{art.mark()}<span>Kaptagat Farm Resort</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" aria-label="Main">
      {''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}
      <a class="btn" href="contact.html">Book a stay</a>
    </nav>
  </div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="site-foot on-forest">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand">Kaptagat Farm Resort</div>
        <p style="color:rgba(236,233,221,.8);max-width:30ch">Kaptarakwa, beside the Kaptagat road, about 25&nbsp;km from Eldoret.</p>
      </div>
      <div><h2>Explore</h2><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
      <div><h2>Contact</h2><ul>
        <li><a data-tel href="#"></a></li>
        <li><a data-wa="" href="#">WhatsApp</a></li>
        <li data-needs-email><a data-email href="#"></a></li>
      </ul></div>
      <div><h2>Elsewhere</h2><ul>
        <li><a href="{GOOGLE}">Google reviews</a></li>
        <li><a href="{FB}">Facebook</a></li>
        <li><a href="{IG}">Instagram</a></li>
      </ul></div>
    </div>
    <div class="foot-base"><span>© <span data-year></span> Kaptagat Farm Resort</span><span>Plus code CFG8+65C Kaptarakwa</span></div>
  </div>
</footer>
<a class="wa" data-wa="" href="#">{WA_ICON}<span>WhatsApp</span></a>
<script src="js/main.js" defer></script>
</body>
</html>
'''

def page_head(h1, lede):
    return f'''<section class="page-head on-forest" aria-labelledby="h1">
  <div class="wrap"><div><h1 id="h1">{h1}</h1><p class="lede">{lede}</p></div>{art.plan_small()}</div>
</section>
'''

# Stays: only what public sources say. kes=None means "rate on request".
STAYS = [
    dict(id="cottage", name="Decagon Cottage", kes=7700,
         short="Single bush-stone cottages in the ten-sided design, with full-view windows from the ground to the roof frame.",
         long="Bush-stone cottages in the ten-sided design, with full-view windows from the ground to the roof frame, so there is a view on every side. Each cottage stands on its own for privacy."),
    dict(id="pond", name="Pond Cottage", kes=None,
         short="A cottage built in the middle of a pond, with papyrus on one side and a trail around the water.",
         long="A cottage built in the middle of a pond, with papyrus on one side and a trail around the water."),
    dict(id="standard", name="Standard Room", kes=4900,
         short="Twin beds for sharing, or a double bed, with a separate bathroom and hot shower.",
         long="Twin beds for two people sharing, or a double bed, with a separate bathroom and hot shower. The rooms are in a single-storey block with a shared balcony that looks over the river."),
    dict(id="cabin", name="Deluxe Cabin", kes=None,
         short="Isolated cabins in the quieter parts of the grounds, suited to couples.",
         long="Isolated cabins in the quieter parts of the grounds, suited to couples."),
    dict(id="villa", name="Villa", kes=None,
         short="Luxury villas for a longer stay in the countryside.",
         long="Luxury villas for a premium stay in the countryside. Ask us about layout and availability."),
    dict(id="dorm", name="Dormitory", kes=None,
         short="Dormitory-style rooms for groups, clubs and training camps.",
         long="Dormitory-style rooms for groups, athletic organisations and training camps. All rooms have hot showers."),
]
ROOM_OPTS = "".join(f'<option value="{r["id"]}">{r["name"]}</option>' for r in STAYS)
CUR = '<div class="cur" role="group" aria-label="Show prices in"><button type="button" data-cur="KES" aria-pressed="true">KES</button><span aria-hidden="true">/</span><button type="button" data-cur="USD" aria-pressed="false">USD</button></div>'
RATE_NOTE = '<p class="note" style="margin-top:14px">Rates are indicative. We confirm the price when we confirm your dates.</p>'

def stay_row(r, long=False):
    if r["kes"]:
        rate = f'<b data-kes="{r["kes"]}" data-from="1" data-unit="per night">From KES {r["kes"]:,}</b><small data-alt></small>'
    else:
        rate = '<b>On request</b><small>Rate confirmed with your dates</small>'
    return f'''<li class="stay" id="{r["id"]}">
  <div><h3>{r["name"]}</h3><p>{r["long"] if long else r["short"]}</p></div>
  <div class="rate">{rate}<a class="more" href="contact.html">Enquire</a></div>
</li>'''

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Hotel", "name": "Kaptagat Farm Resort",
    "description": "Bush-stone decagon cottages in a botanical garden at the edge of the forest near Eldoret, Kenya, with a restaurant, bar, conference hall and event grounds.",
    "url": SITE, "telephone": "+254725859860", "starRating": {"@type": "Rating", "ratingValue": "3"},
    "address": {"@type": "PostalAddress", "streetAddress": "CFG8+65C Kaptarakwa", "addressLocality": "Eldoret", "addressRegion": "Uasin Gishu", "addressCountry": "KE"},
    "checkinTime": "14:00", "checkoutTime": "10:00", "sameAs": [FB, IG],
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Restaurant", "Bar", "Room service", "Free parking", "Conference facilities"]],
}, indent=1)

def key_list():
    return "".join(f'<li data-pin="{n}" tabindex="0"><span class="n">{n}</span><span><b>{t}</b><span>{d}</span></span></li>' for n, _, _, t, d in art.PINS)

BOOKING = f'''<section class="booking" id="booking" aria-labelledby="h-book">
  <div class="wrap">
    <h2 id="h-book" class="sr">Check availability</h2>
    <form id="booking-form" novalidate>
      <div class="field"><label for="bk-in">Check-in</label><input id="bk-in" type="date" required><div class="err" id="bk-in-err" aria-live="polite"></div></div>
      <div class="field"><label for="bk-out">Check-out</label><input id="bk-out" type="date" required><div class="err" id="bk-out-err" aria-live="polite"></div></div>
      <div class="field"><label for="bk-room">Stay</label><select id="bk-room">{ROOM_OPTS}</select></div>
      <div class="field"><label for="bk-guests">Guests</label><input id="bk-guests" type="number" inputmode="numeric" min="1" max="200" value="2"><div class="err" id="bk-guests-err" aria-live="polite"></div></div>
      <div class="field go"><button class="btn" type="submit">Check availability</button></div>
    </form>
    <div class="quote" id="quote" tabindex="-1" aria-live="polite">
      <div><span class="sr">Estimate:</span><strong id="q-total"></strong><span id="q-detail" class="muted"></span>
        <p class="note" style="margin:8px 0 0">Send your dates and we confirm availability and the final price. There is nothing to pay to ask.</p></div>
      <div class="acts"><a class="btn" id="q-wa" href="#">Send on WhatsApp</a><a class="btn line" id="q-mail" href="#" data-needs-email>Email us</a></div>
    </div>
  </div>
</section>'''

# ---------------- Home ----------------
home = head("Kaptagat Farm Resort | Garden cottages near Eldoret, Kenya",
            "Bush-stone decagon cottages, a restaurant, the Mill Bar and event grounds in a botanical garden at the edge of the Kaptagat forest, about 25 km from Eldoret.",
            "index.html", f'<script type="application/ld+json">{JSONLD}</script>\n') + f'''
<section class="hero on-forest" aria-labelledby="h-hero">
  <div class="wrap">
    <div>
      <h1 id="h-hero">Garden cottages at the edge of the Kaptagat forest</h1>
      <p class="lede">Bush-stone cottages, a restaurant and the Mill Bar in a botanical garden, about 25&nbsp;km from Eldoret.</p>
      <div class="acts"><a class="btn" href="#booking">Check availability</a><a class="btn line" href="accommodations.html">See the stays</a></div>
    </div>
    {art.hero_drawing()}
  </div>
</section>
{BOOKING}

<div class="wrap">
  <section class="row" aria-labelledby="h-res">
    <h2 id="h-res">The resort</h2>
    <div>
      <p class="statement">Kaptagat Farm Resort is a garden property at Kaptarakwa, beside the Kaptagat road. The cottages are built in local bush stone on a ten-sided plan, with windows from the ground to the roof frame. Around them are hedged gardens, ponds and picnic terraces, and the forest begins at the edge of the grounds.</p>
      <dl class="facts">
        <div><dt>Location</dt><dd>Kaptarakwa, beside the Kaptagat road</dd></div>
        <div><dt>From Eldoret</dt><dd>About 25&nbsp;km by road</dd></div>
        <div><dt>Airport</dt><dd>About 30 minutes to Eldoret International</dd></div>
        <div><dt>Plus code</dt><dd>CFG8+65C Kaptarakwa</dd></div>
        <div><dt>Check-in</dt><dd>From 2:00&nbsp;pm</dd></div>
        <div><dt>Check-out</dt><dd>By 10:00&nbsp;am</dd></div>
        <div><dt>Breakfast</dt><dd>6:30 to 10:00&nbsp;am</dd></div>
        <div><dt>On site</dt><dd>Restaurant, bar, room service, parking</dd></div>
      </dl>
    </div>
  </section>

  <section class="row" aria-labelledby="h-stay">
    <h2 id="h-stay">Stay</h2>
    <div>
      <div class="tools"><p class="muted" style="margin:0">Six kinds of accommodation, each with its own bathroom and hot shower.</p>{CUR}</div>
      <ul class="stays">{''.join(stay_row(r) for r in STAYS)}</ul>
      {RATE_NOTE}
      <p style="margin-top:18px"><a class="more" href="accommodations.html">Details and policies</a></p>
    </div>
  </section>

  <section class="row" id="grounds" aria-labelledby="h-map">
    <h2 id="h-map">The grounds</h2>
    <div>
      <div class="mapwrap">
        <div>{art.estate_map()}<p class="note" style="margin-top:10px">Schematic plan, not to scale. Positions are indicative.</p></div>
        <ol class="key">{key_list()}</ol>
      </div>
    </div>
  </section>

  <section class="row" aria-labelledby="h-food">
    <h2 id="h-food">Food, drink and the garden</h2>
    <div>
      <div class="cols">
        <div><h3>Restaurant</h3><p>Meals are cooked from scratch to order and served outdoors, on the lawns or in the bandas. Allow time, or pre-order when you book.</p></div>
        <div><h3>The Mill Bar</h3><p>A ten-sided bar at the centre of the garden, with a large screen and plenty of seating.</p></div>
        <div><h3>Garden and forest</h3><p>Walks through the hedged gardens, birdwatching, and picnics in the shade of the acacias.</p></div>
      </div>
      <p style="margin-top:28px"><a class="more" href="experiences.html">Dine and explore</a></p>
    </div>
  </section>

  <section class="row" aria-labelledby="h-ev">
    <h2 id="h-ev">Events and groups</h2>
    <div>
      <p class="statement">A two-storey decagon conference room for up to 200 people, a seminar block, six bush-stone bandas for private dining, and open lawns for weddings and team building. The dormitories suit clubs and training camps.</p>
      <div class="acts"><a class="btn" href="contact.html">Ask about an event</a><a class="more" href="experiences.html#events">What we host</a></div>
    </div>
  </section>

  <section class="row" aria-labelledby="h-visit">
    <h2 id="h-visit">Visit</h2>
    <div>
      <p class="statement">From Eldoret, take the Kaptagat road. The resort is beside it at Kaptarakwa, about 25&nbsp;km out. Eldoret International Airport is about 30 minutes away.</p>
      <div class="acts gap-lg"><a class="btn" data-tel href="#"></a><a class="btn line" data-wa="" href="#">WhatsApp</a><a class="more" href="{MAPS}">Open in Google Maps</a></div>
    </div>
  </section>
</div>
''' + FOOT

# ---------------- Stay ----------------
acc = head("Stay | Kaptagat Farm Resort",
           "Decagon cottages, a pond cottage, standard rooms, deluxe cabins, villas and dormitories at Kaptagat Farm Resort near Eldoret.",
           "accommodations.html") + page_head("Stay", "Six kinds of accommodation in the garden, from standard rooms to a cottage built in a pond.") + f'''
<div class="wrap">
  <section class="row" aria-labelledby="h-all">
    <h2 id="h-all">Accommodation</h2>
    <div>
      <div class="tools"><p class="muted" style="margin:0">Every room has its own bathroom with a hot shower.</p>{CUR}</div>
      <ul class="stays">{''.join(stay_row(r, True) for r in STAYS)}</ul>
      {RATE_NOTE}
    </div>
  </section>
  <section class="row" aria-labelledby="h-know">
    <h2 id="h-know">Good to know</h2>
    <div>
      <table class="tbl">
        <caption class="sr">Stay details</caption>
        <tbody>
          <tr><th scope="row">Check-in</th><td>From 2:00&nbsp;pm</td></tr>
          <tr><th scope="row">Check-out</th><td>By 10:00&nbsp;am</td></tr>
          <tr><th scope="row">Breakfast</th><td>6:30 to 10:00&nbsp;am</td></tr>
          <tr><th scope="row">Meals</th><td>Cooked to order. Pre-order lunch or dinner when you book, or message us an hour ahead.</td></tr>
          <tr><th scope="row">Room service</th><td>Available</td></tr>
          <tr><th scope="row">Parking</th><td>Free, on site</td></tr>
          <tr><th scope="row">Wi-Fi</th><td>In the rooms. Coverage in the garden is limited.</td></tr>
          <tr><th scope="row">Pets</th><td>Please ask before you book</td></tr>
          <tr><th scope="row">Day visitors</th><td>A gate fee applies. Ask what it covers.</td></tr>
          <tr><th scope="row">Groups</th><td>Dormitory and group rates on request</td></tr>
        </tbody>
      </table>
    </div>
  </section>
</div>
''' + FOOT

# ---------------- Dine & explore ----------------
exp = head("Dine and explore | Kaptagat Farm Resort",
           "The restaurant, the Mill Bar, gardens, birdwatching, forest walks, farm life, conferences and events at Kaptagat Farm Resort near Eldoret.",
           "experiences.html") + page_head("Dine and explore", "Meals outdoors, a bar at the centre of the garden, and walks into the forest.") + '''
<div class="wrap">
  <section class="row" id="dining" aria-labelledby="h-dine">
    <h2 id="h-dine">Restaurant</h2>
    <div class="prose">
      <p class="statement">The kitchen cooks from scratch and to order. Eat on the lawns, under the acacias, or in a banda.</p>
      <p>Guests mention nyama choma, kienyeji chicken, chips and tea. Because everything is made to order, meals take time. Pre-order lunch or dinner when you book, or message us an hour ahead and it will be ready when you are.</p>
      <ul class="plain">
        <li><b>Breakfast</b> for stay guests, 6:30 to 10:00&nbsp;am</li>
        <li><b>Room service</b> available</li>
        <li><b>Outdoor dining</b> on the lawns and in the bandas</li>
      </ul>
    </div>
  </section>
  <section class="row" id="millbar" aria-labelledby="h-bar">
    <h2 id="h-bar">The Mill Bar</h2>
    <div class="prose">
      <p>A ten-sided bar at the centre of the garden, with a large flat-screen television and seating inside and out.</p>
      <p><a class="more" data-wa="Hello, I'd like to reserve a table at the Mill Bar." href="#">Reserve by WhatsApp</a></p>
    </div>
  </section>
  <section class="row" id="nature" aria-labelledby="h-nat">
    <h2 id="h-nat">Garden and forest</h2>
    <div class="prose">
      <h3>The garden</h3>
      <p>Hedged sitting areas, ponds between the trails, and plants growing on logs, walls and trees: gazania, agapanthus, euphorbia, peace lilies and giant papyrus. Terraces step down towards the river, with a picnic area in the shade of acacias. The river runs along the edge of the grounds and can be seen from the seating, but not entered.</p>
      <h3>Birds and walks</h3>
      <p>The forest is next to the grounds, and forest birds come close to the garden. Staff can point you to the walking trails.</p>
      <h3>The farm</h3>
      <p>The resort sits on a family farm with greenhouses, poultry and fish ponds, and keeps its own geese and dogs. Ask at reception what you can see.</p>
    </div>
  </section>
  <section class="row" id="events" aria-labelledby="h-ev">
    <h2 id="h-ev">Events and groups</h2>
    <div>
      <table class="tbl">
        <caption class="sr">Event spaces</caption>
        <tbody>
          <tr><th scope="row">Conference room</th><td>In a two-storey decagon, for up to 200 people</td></tr>
          <tr><th scope="row">Seminar block</th><td>With a shared balcony over the river</td></tr>
          <tr><th scope="row">Bandas</th><td>Six bush-stone bandas in a U-shape, for private dining and receptions</td></tr>
          <tr><th scope="row">Lawns</th><td>Open ground for weddings, parties and team building</td></tr>
          <tr><th scope="row">Camps</th><td>Dormitories for clubs and athletes training at altitude</td></tr>
        </tbody>
      </table>
      <div class="acts" style="margin-top:26px"><a class="btn" href="contact.html">Request a quote</a><a class="btn line" data-wa="Hello, I'd like a quote for an event at Kaptagat Farm Resort." href="#">WhatsApp</a></div>
    </div>
  </section>
  <section class="row" aria-labelledby="h-near">
    <h2 id="h-near">Nearby</h2>
    <div>
      <table class="tbl">
        <caption class="sr">Places nearby</caption>
        <tbody>
          <tr><th scope="row">Kaptagat Forest</th><td class="r">Next to the grounds</td></tr>
          <tr><th scope="row">Naiberi River Campsite &amp; Resort</th><td class="r">About 5&nbsp;km</td></tr>
          <tr><th scope="row">Eldoret town</th><td class="r">About 25&nbsp;km</td></tr>
          <tr><th scope="row">Eldoret International Airport</th><td class="r">About 30 minutes</td></tr>
          <tr><th scope="row">Chepkorio</th><td class="r">Next town along the B54</td></tr>
        </tbody>
      </table>
    </div>
  </section>
</div>
''' + FOOT

# ---------------- Contact ----------------
con = head("Book and find us | Kaptagat Farm Resort",
           "Send a booking inquiry, call or WhatsApp Kaptagat Farm Resort, and get directions from Eldoret, the airport and Nairobi.",
           "contact.html") + page_head("Book a stay", "Send your dates and we confirm availability and the final price. You pay once your stay is confirmed.") + f'''
<div class="wrap">
  <section class="contact" aria-label="Booking and contact">
    <div>
      <h2>Booking inquiry</h2>
      <form id="inquiry-form" novalidate>
        <div class="form-grid">
          <div class="field"><label for="iq-name">Full name</label><input id="iq-name" autocomplete="name" required><div class="err" id="iq-name-err" aria-live="polite"></div></div>
          <div class="field"><label for="iq-phone">Phone or WhatsApp</label><input id="iq-phone" type="tel" autocomplete="tel" placeholder="+254 712 345 678" required><div class="err" id="iq-phone-err" aria-live="polite"></div></div>
          <div class="field"><label for="iq-email">Email (optional)</label><input id="iq-email" type="email" autocomplete="email"><div class="err" id="iq-email-err" aria-live="polite"></div></div>
          <div class="field"><label for="iq-room">Stay</label><select id="iq-room">{ROOM_OPTS}</select></div>
          <div class="field"><label for="iq-in">Check-in</label><input id="iq-in" type="date" required><div class="err" id="iq-in-err" aria-live="polite"></div></div>
          <div class="field"><label for="iq-out">Check-out</label><input id="iq-out" type="date" required><div class="err" id="iq-out-err" aria-live="polite"></div></div>
          <div class="field"><label for="iq-guests">Guests</label><input id="iq-guests" type="number" inputmode="numeric" min="1" max="200" value="2"></div>
          <div class="field full"><label for="iq-msg">Anything we should know? (optional)</label><textarea id="iq-msg" placeholder="Arrival time, meals to pre-order, events, group bookings"></textarea></div>
          <div class="hp" aria-hidden="true"><label for="iq-company">Company</label><input id="iq-company" tabindex="-1" autocomplete="off"></div>
          <div class="field full"><label class="check" for="iq-consent"><input id="iq-consent" type="checkbox"> I agree that Kaptagat Farm Resort may contact me about this inquiry.</label><div class="err" id="iq-consent-err" aria-live="polite"></div></div>
          <div class="full"><button class="btn" type="submit">Send inquiry</button></div>
        </div>
      </form>
      <div class="success" id="iq-success" tabindex="-1" aria-live="polite">
        <h3 id="iq-title"></h3>
        <p id="iq-summary" style="margin-top:8px"></p><p id="iq-note"></p>
        <div class="acts"><a class="btn" id="iq-wa" href="#">Send on WhatsApp</a><a class="btn line" id="iq-mail" href="#" data-needs-email>Send by email</a></div>
      </div>
    </div>
    <div>
      <h2>Talk to us</h2>
      <dl class="facts" style="grid-template-columns:minmax(0,1fr);margin-top:22px">
        <div><dt>Call</dt><dd><a data-tel href="#"></a></dd></div>
        <div><dt>WhatsApp</dt><dd><a data-wa="" href="#"><span data-wa-text></span></a></dd></div>
        <div data-needs-email><dt>Email</dt><dd><a data-email href="#"></a></dd></div>
        <div><dt>Elsewhere</dt><dd><a href="{FB}">Facebook</a>, <a href="{IG}">Instagram</a>, <a href="{GOOGLE}">Google reviews</a></dd></div>
      </dl>
      <p class="note" style="margin-top:22px">Meals are cooked to order, so please pre-order lunch or dinner when you book. Evenings in Kaptagat are cool; bring a warm layer.</p>
    </div>
  </section>

  <section class="row" id="directions" aria-labelledby="h-dir">
    <h2 id="h-dir">Getting here</h2>
    <div class="mapwrap" style="align-items:start">
      <div>
        <ol class="route">
          <li><span><b>Eldoret town</b><small>Take the Kaptagat road out of town</small></span><em>start</em></li>
          <li><span><b>Kaptagat road</b><small>Continue towards Kaptagat and Chepkorio</small></span><em>about 25&nbsp;km</em></li>
          <li><span><b>Kaptagat Farm Resort</b><small>Beside the road at Kaptarakwa</small></span><em>arrive</em></li>
        </ol>
        <p style="margin-top:20px"><b>By air.</b> Eldoret International Airport is about 30 minutes from the resort by road.</p>
        <p><b>From Nairobi.</b> Take the A104 through Nakuru to Eldoret, then the Kaptagat road.</p>
      </div>
      <div>
        <p class="muted" style="margin:0">Google plus code</p>
        <p class="pluscode">CFG8+65C Kaptarakwa</p>
        <div class="acts gap-lg"><a class="btn" href="{MAPS}">Open in Google Maps</a><a class="more" href="{GOOGLE}">Google listing</a></div>
      </div>
    </div>
  </section>
</div>
''' + FOOT

pages = [("index.html", home), ("accommodations.html", acc), ("experiences.html", exp), ("contact.html", con)]
(OUT / "img").mkdir(parents=True, exist_ok=True)
art.write_assets(OUT / "img")
for name, html in pages:
    (OUT / name).write_text(html, encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 + "".join(f"  <url><loc>{url(p)}</loc></url>\n" for p, _ in pages) + "</urlset>\n")
print("built", sorted(p.name for p in OUT.iterdir()))
