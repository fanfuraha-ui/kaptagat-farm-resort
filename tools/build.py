#!/usr/bin/env python3
"""Builds the static Kaptagat Farm Resort site: pages from shared partials, plus generated illustrations."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import art

OUT = pathlib.Path(sys.argv[1])
SITE = "https://kaptagatfarmresort.co.ke"   # placeholder domain: replace before launch
GOOGLE = "https://www.google.co.ke/travel/hotels/entity/CgoIy7v0kISag-1pEAE"
FB = "https://www.facebook.com/Kaptagatfarmresort/"
IG = "https://www.instagram.com/kaptagat_farm_resort/"
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=CFG8%2B65C+Kaptarakwa%2C+Kenya"

LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1F3A2C"/>'
        + art.deca_roof(32, 32, 22, "#B4552F") + '</svg>')
WA_ICON = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.6 3.6 0 0 0-1.1 2.7 6.3 6.3 0 0 0 1.3 3.3 14.4 14.4 0 0 0 5.5 4.9c2 .9 2.8.9 3.8.8a3.3 3.3 0 0 0 2.2-1.5 2.7 2.7 0 0 0 .2-1.5c-.1-.2-.3-.3-.6-.5z"/></svg>'
NAV = [("index.html", "Home"), ("accommodations.html", "Stay"), ("experiences.html", "Dine &amp; explore"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]

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
<meta name="theme-color" content="#1F3A2C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kaptagat Farm Resort">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{SITE}/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&amp;family=Instrument+Sans:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="Kaptagat Farm Resort, home">{LOGO}<span>Kaptagat<small>Farm Resort</small></span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" aria-label="Main">
      {''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}
      <a class="btn btn-sm" href="contact.html">Book your stay</a>
    </nav>
  </div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html" style="color:#F5F0E6">{LOGO}<span>Kaptagat<small style="color:#A9B4A6">Farm Resort</small></span></a>
        <p style="margin-top:14px">Bush-stone cottages in a botanical garden at the edge of the forest. Kaptarakwa, off the Kaptagat road, about 25 km from Eldoret.</p>
      </div>
      <div><h3>Explore</h3><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
      <div><h3>Contact</h3><ul>
        <li>Call <a data-tel href="#"></a></li>
        <li><a data-wa="" href="#">WhatsApp us</a></li>
        <li data-needs-email><a data-email href="#"></a></li>
      </ul></div>
      <div><h3>Follow</h3><ul>
        <li><a href="{FB}">Facebook</a></li>
        <li><a href="{IG}">Instagram</a></li>
        <li><a href="{GOOGLE}">Reviews on Google</a></li>
      </ul></div>
    </div>
    <div class="foot-base"><span>© <span data-year></span> Kaptagat Farm Resort</span><span>Plus code CFG8+65C Kaptarakwa · Rates shown are indicative</span></div>
  </div>
</footer>
<a class="wa-float" data-wa="" href="#" aria-label="Chat with us on WhatsApp">{WA_ICON}</a>
<script src="js/main.js" defer></script>
</body>
</html>
'''

ROOMS = [
    dict(id="cottage", name="Decagon Cottage", kes=7700, cap="2", capl="guests", img="cottage",
         blurb="A free-standing ten-sided cottage in bush stone, glazed from floor to roof frame, so the garden surrounds you on every side.",
         amen=["Garden views all round", "Private bathroom", "Hot shower", "Wi-Fi"]),
    dict(id="pond", name="Pond Cottage", kes=9500, cap="2", capl="guests", img="pond-cottage",
         blurb="Built in the middle of a pond, with papyrus along one bank and a trail around the water. The quietest view in the garden.",
         amen=["On the water", "Private bathroom", "Hot shower", "Wi-Fi"]),
    dict(id="standard", name="Standard Room", kes=4900, cap="2", capl="guests", img="room",
         blurb="Simple, clean rooms in the garden block with twin or double beds, a private bathroom and a shared balcony over the river.",
         amen=["Twin or double", "Private bathroom", "Hot shower", "Wi-Fi"]),
    dict(id="cabin", name="Deluxe Cabin", kes=9500, cap="2", capl="guests", img="cabin",
         blurb="Set apart in a quieter corner of the grounds for couples who want privacy, birdsong and a slow morning.",
         amen=["Secluded", "Private bathroom", "Hot shower", "Room service"]),
    dict(id="villa", name="Garden Villa", kes=15000, cap="4", capl="guests", img="villa",
         blurb="The most spacious stay on the farm, for families or friends who want room to spread out in the countryside.",
         amen=["Most space", "Private bathroom", "Hot shower", "Room service"]),
    dict(id="dorm", name="Dormitory", kes=1500, cap="20", capl="beds", img="dorm", unit="per bed, per night",
         blurb="Shared rooms for school trips, clubs and athletes' training camps at altitude. Ask about full-board group rates.",
         amen=["Bunk beds", "Hot showers", "Group meals", "Training camps"]),
]
ROOM_OPTS = "".join(f'<option value="{r["id"]}">{r["name"]}</option>' for r in ROOMS)

def room_card(r):
    unit = r.get("unit", "per night")
    return f'''<article class="room" id="{r["id"]}">
  <img src="img/{r["img"]}.svg" alt="{r["name"]}: illustration in place of a photo" width="800" height="600" loading="lazy">
  <div class="cap" aria-label="Sleeps {r["cap"]}">{r["cap"]}<small>{r["capl"]}</small></div>
  <div class="room-body">
    <h3>{r["name"]}</h3>
    <p>{r["blurb"]}</p>
    <ul class="amen">{''.join(f"<li>{a}</li>" for a in r["amen"])}</ul>
    <div class="price"><div><b data-kes="{r["kes"]}" data-unit="{unit}">KES {r["kes"]:,}</b><small data-alt></small></div>
      <a class="btn btn-sm" href="contact.html">Enquire</a></div>
  </div>
</article>'''

CUR = '<div class="cur" role="group" aria-label="Show prices in"><button type="button" data-cur="KES" aria-pressed="true">KES</button><button type="button" data-cur="USD" aria-pressed="false">USD</button></div>'
RATE_NOTE = '<p class="note">Indicative rates. Confirm current prices and what is included when you book.</p>'

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Hotel", "name": "Kaptagat Farm Resort",
    "description": "Bush-stone decagon cottages in a botanical garden at the edge of the forest near Eldoret, Kenya. Restaurant, the Mill Bar, conference hall and event grounds.",
    "url": SITE, "telephone": "+254725859860", "starRating": {"@type": "Rating", "ratingValue": "3"},
    "address": {"@type": "PostalAddress", "streetAddress": "CFG8+65C Kaptarakwa", "addressLocality": "Eldoret", "addressRegion": "Uasin Gishu", "addressCountry": "KE"},
    "geo": {"@type": "GeoCoordinates", "latitude": 0.4256, "longitude": 35.4654},
    "checkinTime": "14:00", "checkoutTime": "10:00", "sameAs": [FB, IG],
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Free parking", "Restaurant", "Bar", "Room service", "Free Wi-Fi", "Conference facilities"]],
}, indent=1)

def map_section():
    legend = "".join(f'<li data-pin="{n}" tabindex="0"><span>{n}</span><span><b>{t}</b><small>{d}</small></span></li>' for n, _, _, t, d in art.PINS)
    return f'''<section class="band tint" id="grounds" aria-labelledby="h-map">
  <div class="wrap">
    <div class="sec-head"><div><h2 id="h-map">Find your way around the garden</h2><p class="lede">Paths fan out from the Mill Bar to the cottages, the pond, the picnic terrace and the forest trails.</p></div></div>
    <div class="mapgrid">
      <div>{art.estate_map()}<p class="note">Illustrated map, not to scale.</p></div>
      <ol class="legend">{legend}</ol>
    </div>
  </div>
</section>'''

BOOKING = f'''<section class="booking" id="booking" aria-labelledby="h-book">
  <div class="wrap">
    <h2 id="h-book" class="sr">Check availability</h2>
    <form id="booking-form" novalidate>
      <div class="field"><label for="bk-in">Check-in</label><input id="bk-in" type="date" required><div class="err" id="bk-in-err" aria-live="polite"></div></div>
      <div class="field"><label for="bk-out">Check-out</label><input id="bk-out" type="date" required><div class="err" id="bk-out-err" aria-live="polite"></div></div>
      <div class="field"><label for="bk-room">Stay</label><select id="bk-room">{ROOM_OPTS}</select></div>
      <div class="field"><label for="bk-guests">Guests</label><input id="bk-guests" type="number" inputmode="numeric" min="1" max="40" value="2"><div class="err" id="bk-guests-err" aria-live="polite"></div></div>
      <div class="field go"><button class="btn" type="submit">Check availability</button></div>
    </form>
    <ul class="facts" aria-label="At a glance">
      <li>3-star hotel</li><li>Check-in from 2 pm</li><li>Restaurant and the Mill Bar</li><li>Room service</li>
      <li>Free secure parking</li><li>Wi-Fi</li><li>Conference hall for 200</li><li>30 min from Eldoret airport</li>
    </ul>
  </div>
</section>
<dialog class="rvw" id="rvw" aria-labelledby="rvwT">
  <div class="rvw-img" id="rvwImg"></div>
  <div class="rvw-body">
    <button type="button" class="rvw-x" id="rvwX" aria-label="Close">×</button>
    <h3 id="rvwT">Your <em>stay</em></h3>
    <div class="tk"><div class="tk-d" id="rvwDates"></div><dl id="rvwList"></dl></div>
    <p class="rvw-fine">Send this on WhatsApp and we confirm availability and the final price. Nothing to pay to ask.</p>
    <div class="rvw-act"><button type="button" class="btn ghost" id="rvwEdit">Edit</button><a class="btn wa" id="rvwWa" href="#">Send on WhatsApp</a><a class="btn ghost" id="rvwMail" href="#" data-needs-email>Email us</a></div>
  </div>
</dialog>'''

# ---------------- Home ----------------
home = head("Kaptagat Farm Resort | Garden cottages near Eldoret, Kenya",
            "Ten-sided bush-stone cottages in a botanical garden at the edge of the forest, 25 km from Eldoret. Restaurant, the Mill Bar, conference hall for 200 and wedding grounds. Book direct.",
            "index.html", f'<script type="application/ld+json">{JSONLD}</script>\n') + f'''
<section class="hero" aria-labelledby="h-hero">
  <img class="scene" src="img/hero.svg" alt="" width="1600" height="900" fetchpriority="high">
  <div class="wrap">
    <h1 id="h-hero">A garden stay at the edge of the Kaptagat forest</h1>
    <p class="lede">Ten-sided bush-stone cottages with windows from floor to roof, ponds ringed with papyrus, and birdsong all day. About 25 km from Eldoret.</p>
    <div class="acts"><a class="btn" href="#booking">Check dates</a><a class="btn ghost" href="accommodations.html">See the cottages</a></div>
  </div>
</section>
{BOOKING}

<section class="band" aria-labelledby="h-sig">
  <div class="wrap sig">
    <div class="deca-frame"><img src="img/cottage.svg" alt="Illustration of a decagon cottage at dusk with its windows lit" width="800" height="600" loading="lazy"></div>
    <div>
      <h2 id="h-sig">Ten walls of stone and glass</h2>
      <p class="lede">Our cottages are built in local bush stone on a ten-sided plan. Glass runs from the floor to the roof frame, so you wake up inside the garden.</p>
      <ul class="points">
        <li><span class="ico" aria-hidden="true">360</span><span><b>Views on every side</b><span>Full-height windows look out on hedged gardens, ponds and the forest line.</span></span></li>
        <li><span class="ico" aria-hidden="true">1</span><span><b>Each cottage stands alone</b><span>Set apart along garden paths for privacy, with one built on its own pond.</span></span></li>
        <li><span class="ico" aria-hidden="true">2.5k</span><span><b>Cool highland air</b><span>Kaptagat sits about 2,500 m up, so mornings are crisp and evenings call for a jumper.</span></span></li>
      </ul>
      <a class="btn" href="accommodations.html">Choose your stay</a>
    </div>
  </div>
</section>

<section class="band" style="padding-top:0" aria-labelledby="h-rooms">
  <div class="wrap">
    <div class="sec-head"><div><h2 id="h-rooms">Where you'll sleep</h2><p class="lede">From simple garden rooms to a cottage on the water.</p></div>{CUR}</div>
    <div class="rooms">{''.join(room_card(r) for r in ROOMS[:3])}</div>
    <div class="acts" style="margin-top:24px"><a class="btn ghost" href="accommodations.html">All six ways to stay</a></div>
    {RATE_NOTE}
  </div>
</section>

{map_section()}

<section class="band dark" aria-labelledby="h-ev">
  <div class="wrap events">
    <div>
      <div class="big" aria-hidden="true">200</div>
      <h2 id="h-ev">Guests in the conference hall, and room to celebrate outside</h2>
      <p class="lede">Meetings in a two-storey decagon hall, weddings on the garden lawns and private dinners in the bandas.</p>
      <div class="acts"><a class="btn" href="contact.html">Plan an event</a><a class="btn ghost" href="experiences.html#events">What we host</a></div>
    </div>
    <ul class="ev-list">
      <li><b>Conferences and seminars</b><span>Hall for up to 200, plus a seminar block with river views.</span></li>
      <li><b>Weddings and parties</b><span>Garden ceremonies and receptions among the hedges and acacias.</span></li>
      <li><b>Team building</b><span>Open lawns, trails and picnic areas for a day out of the office.</span></li>
      <li><b>Training camps</b><span>Dormitories for clubs and athletes who come to Kaptagat to train at altitude.</span></li>
    </ul>
  </div>
</section>

<section class="band" aria-labelledby="h-do">
  <div class="wrap">
    <div class="sec-head"><div><h2 id="h-do">Eat slowly, walk far</h2><p class="lede">Food cooked to order, a bar at the heart of the garden, and trails into the forest.</p></div><a class="btn ghost" href="experiences.html">Dine and explore</a></div>
    <div class="exp-grid">
      <a class="exp" href="experiences.html#dining" style="text-decoration:none;color:inherit"><img src="img/dining.svg" alt="Illustration of outdoor dining under an acacia" width="800" height="600" loading="lazy"><div><h3>Outdoor dining</h3><p>Nyama choma, kienyeji chicken and tea, served in the garden.</p></div></a>
      <a class="exp" href="experiences.html#millbar" style="text-decoration:none;color:inherit"><img src="img/millbar.svg" alt="Illustration of the Mill Bar at night" width="800" height="600" loading="lazy"><div><h3>The Mill Bar</h3><p>A ten-sided bar in the middle of the garden, with a big screen for the match.</p></div></a>
      <a class="exp" href="experiences.html#nature" style="text-decoration:none;color:inherit"><img src="img/forest.svg" alt="Illustration of a forest trail with a sunbird" width="800" height="600" loading="lazy"><div><h3>Birds and forest walks</h3><p>Sunbirds in the flowers and trails into the indigenous forest.</p></div></a>
    </div>
  </div>
</section>

<section class="band tint" aria-labelledby="h-rev">
  <div class="wrap">
    <div class="sec-head"><div><h2 id="h-rev">Hear it from guests</h2><p class="lede">Read reviews and see recent photos where guests post them.</p></div></div>
    <div class="social">
      <a href="{GOOGLE}"><b>Google</b><span>Guest reviews and photos on our Google listing</span></a>
      <a href="{FB}"><b>Facebook</b><span>News, events and guest posts</span></a>
      <a href="{IG}"><b>Instagram</b><span>@kaptagat_farm_resort</span></a>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-cta">
  <div class="wrap cta">
    <h2 id="h-cta">Tell us your dates. We'll take it from there.</h2>
    <div class="acts"><a class="btn wa" data-wa="" href="#">Chat on WhatsApp</a><a class="btn ghost" href="contact.html">Send an inquiry</a></div>
  </div>
</section>
''' + FOOT

# ---------------- Stay ----------------
acc = head("Cottages and rooms | Kaptagat Farm Resort",
           "Decagon bush-stone cottages, a pond cottage, deluxe cabins, a garden villa, standard rooms and dormitories at Kaptagat Farm Resort. Rates in KES and USD.",
           "accommodations.html") + f'''
<section class="page-hero" aria-labelledby="h1">
  <img class="scene" src="img/banner.svg" alt="" width="1600" height="420">
  <div class="wrap"><h1 id="h1">Six ways to stay</h1><p class="lede">Decagon cottages, a cottage on the water, quiet cabins, a villa for families, simple rooms and dormitories for groups.</p></div>
</section>
<section class="band" aria-label="Accommodation">
  <div class="wrap">
    <div class="sec-head"><p class="lede">Prices per night. Switch currency:</p>{CUR}</div>
    <div class="rooms">{''.join(room_card(r) for r in ROOMS)}</div>
    {RATE_NOTE}
  </div>
</section>
<section class="band tint" aria-labelledby="h-pol">
  <div class="wrap split">
    <div>
      <h2 id="h-pol">Good to know</h2>
      <ul class="ticks">
        <li>Every room has its own bathroom with a hot shower</li>
        <li>Breakfast is served from 6:30 to 10:00 am</li>
        <li>Room service, a restaurant and the Mill Bar on site</li>
        <li>Free secure parking inside the gate</li>
        <li>Wi-Fi in the rooms and for events</li>
      </ul>
      <p class="tip">Meals are cooked from scratch to order. Pre-order lunch or dinner when you book, or message us an hour ahead, and it will be ready when you are.</p>
    </div>
    <div class="table-wrap">
      <table class="stack">
        <caption class="sr">Stay policies</caption>
        <thead><tr><th scope="col">Policy</th><th scope="col">Details</th></tr></thead>
        <tbody>
          <tr><td data-l="Policy">Check-in</td><td data-l="Details">From 2:00 pm</td></tr>
          <tr><td data-l="Policy">Check-out</td><td data-l="Details">By 10:00 am</td></tr>
          <tr><td data-l="Policy">Breakfast</td><td data-l="Details">6:30 to 10:00 am</td></tr>
          <tr><td data-l="Policy">Pets</td><td data-l="Details">Ask us before you book</td></tr>
          <tr><td data-l="Policy">Day visitors</td><td data-l="Details">A gate fee applies; ask what it covers</td></tr>
          <tr><td data-l="Policy">Groups</td><td data-l="Details">Dormitory and full-board rates on request</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
''' + FOOT

# ---------------- Dine & explore ----------------
exp = head("Dine and explore | Kaptagat Farm Resort",
           "Outdoor dining, the Mill Bar, garden tours, birdwatching, forest walks, picnics, farm life, conferences and weddings at Kaptagat Farm Resort near Eldoret.",
           "experiences.html") + '''
<section class="page-hero" aria-labelledby="h1">
  <img class="scene" src="img/banner.svg" alt="" width="1600" height="420">
  <div class="wrap"><h1 id="h1">Dine and explore</h1><p class="lede">Long lunches outdoors, a drink at the Mill Bar, and a garden that runs down to the river and out to the forest.</p></div>
</section>

<section class="band" id="dining" aria-labelledby="h-dine">
  <div class="wrap split">
    <div>
      <h2 id="h-dine">Cooked to order, served outdoors</h2>
      <p>The kitchen cooks everything from scratch. Eat on the lawns, under the acacias or in a private banda.</p>
      <ul class="ticks">
        <li>Nyama choma from the open grill</li>
        <li>Kienyeji chicken, chips and fresh greens</li>
        <li>Breakfast for stay guests, 6:30 to 10:00 am</li>
        <li>Tea at any hour, and room service</li>
      </ul>
      <p class="tip">Because food is made fresh, meals take time. Pre-order lunch or dinner when you book, or message us an hour ahead.</p>
    </div>
    <figure><img src="img/dining.svg" alt="Illustration of grilled meat, chips and chicken on a garden table" width="800" height="600" loading="lazy"></figure>
  </div>
</section>

<section class="band tint" id="millbar" aria-labelledby="h-bar">
  <div class="wrap split rev">
    <div>
      <h2 id="h-bar">The Mill Bar</h2>
      <p>Our ten-sided bar stands at the centre of the garden. Watch the match on the big screen, or take your drink out to the lawn as the lights come on.</p>
      <a class="btn" data-wa="Hello, I'd like to reserve a table at the Mill Bar." href="#">Reserve a table</a>
    </div>
    <figure><img src="img/millbar.svg" alt="Illustration of the Mill Bar glowing at night under string lights" width="800" height="600" loading="lazy"></figure>
  </div>
</section>

<section class="band" id="nature" aria-labelledby="h-nat">
  <div class="wrap">
    <h2 id="h-nat">A botanical garden at the forest's edge</h2>
    <p class="lede">Hedged sitting areas, ponds between the trails, and plants on every log, wall and tree.</p>
    <div class="exp-grid">
      <article class="exp"><img src="img/hero.svg" alt="Illustration of the garden with cottages and pond" width="1600" height="900" loading="lazy"><div><div class="meta"><span>Self-guided or with staff</span></div><h3>Garden tours</h3><p>Agapanthus, euphorbia, peace lilies and giant papyrus, and one great tree wrapped in vines to its crown.</p></div></article>
      <article class="exp"><img src="img/forest.svg" alt="Illustration of a sunbird on a branch over a forest trail" width="800" height="600" loading="lazy"><div><div class="meta"><span>Best early morning</span></div><h3>Birds and forest walks</h3><p>Forest birds come close to the garden, and trails lead out into the trees.</p></div></article>
      <article class="exp"><img src="img/garden.svg" alt="Illustration of a picnic table under acacias above the river" width="800" height="600" loading="lazy"><div><div class="meta"><span>Morning or late afternoon</span></div><h3>Picnics and yoga</h3><p>Terraces step down towards the river under acacia shade: a calm spot to stretch or spread a blanket.</p></div></article>
    </div>
  </div>
</section>

<section class="band tint" aria-labelledby="h-farm">
  <div class="wrap split">
    <div>
      <h2 id="h-farm">Farm life and running country</h2>
      <p>This is a working farm. Ask to see the greenhouses, the fish ponds and the poultry, and meet the geese that patrol the lawns.</p>
      <p>Kaptagat is one of Kenya's great running grounds. Clubs and athletes stay in our dormitories to train on the forest roads at altitude.</p>
      <a class="btn ghost" href="contact.html">Ask about a training camp</a>
    </div>
    <figure><img src="img/pond-cottage.svg" alt="Illustration of the pond cottage among papyrus" width="800" height="600" loading="lazy"></figure>
  </div>
</section>

<section class="band" id="events" aria-labelledby="h-ev">
  <div class="wrap split rev">
    <div>
      <h2 id="h-ev">Conferences, weddings and gatherings</h2>
      <ul class="ticks">
        <li><b>Conference hall</b> in a two-storey decagon, for up to 200 people</li>
        <li><b>Seminar block</b> with a shared balcony over the river</li>
        <li><b>Six bandas</b> in a U-shape for private dining and receptions</li>
        <li><b>Garden lawns</b> for weddings, parties and team building</li>
        <li>Wi-Fi for events and secure parking for guests</li>
      </ul>
      <div class="acts"><a class="btn" href="contact.html">Request a quote</a><a class="btn wa" data-wa="Hello, I'd like a quote for an event at Kaptagat Farm Resort." href="#">WhatsApp the events team</a></div>
    </div>
    <figure><img src="img/bandas.svg" alt="Illustration of thatched bush-stone bandas around a dining table" width="800" height="600" loading="lazy"></figure>
  </div>
</section>

<section class="band dark" aria-labelledby="h-near">
  <div class="wrap">
    <h2 id="h-near">Around Kaptagat</h2>
    <p class="lede">Easy outings from the farm. Drive times are approximate.</p>
    <ul class="attractions">
      <li><b>Kaptagat Forest</b><span>On the doorstep · indigenous forest and running trails</span></li>
      <li><b>Chepkorio</b><span>A short drive · village on the B54, home of champion runners</span></li>
      <li><b>Eldoret town</b><span>About 25 km · shops, banks, hospital</span></li>
      <li><b>Eldoret International Airport</b><span>About 30 minutes · daily flights to Nairobi</span></li>
      <li><b>Iten and the Kerio View</b><span>About 1 hr 15 min · the Rift Valley escarpment</span></li>
      <li><b>Kerio Valley</b><span>Below the escarpment · warm valley floor, viewpoints on the way</span></li>
    </ul>
  </div>
</section>
''' + FOOT

# ---------------- Gallery ----------------
G = [("rooms", "cottage", "Decagon cottage at dusk"), ("nature", "hero", "The garden, the pond and the cottages"), ("dining", "dining", "Lunch under the acacias"),
     ("rooms", "pond-cottage", "The pond cottage"), ("dining", "millbar", "The Mill Bar at night"), ("nature", "forest", "Sunbird on the forest trail"),
     ("rooms", "cabin", "A deluxe cabin after dark"), ("dining", "bandas", "Bandas for private dining"), ("nature", "garden", "Picnic terrace above the river"),
     ("rooms", "villa", "The garden villa"), ("rooms", "room", "Standard twin room"), ("rooms", "dorm", "Dormitory for groups")]
figs = "\n".join(f'<figure data-cat="{c}"><button type="button" aria-label="View larger: {t}"><img src="img/{i}.svg" alt="{t}, illustration" width="800" height="600" loading="lazy"></button><figcaption>{t}</figcaption></figure>' for c, i, t in G)
gal = head("Gallery | Kaptagat Farm Resort",
           "The decagon cottages, the pond cottage, the Mill Bar, the bandas and the gardens of Kaptagat Farm Resort near Eldoret.",
           "gallery.html") + f'''
<section class="band" aria-labelledby="h1">
  <div class="wrap">
    <div class="sec-head"><div><h1 id="h1" style="font-size:clamp(40px,5vw,62px)">Gallery</h1><p class="lede">Cottages, food and the garden around them.</p></div><a class="btn ghost" href="{IG}">More on Instagram</a></div>
    <div class="filters" role="group" aria-label="Filter pictures">
      <button type="button" data-f="all" aria-pressed="true">All</button>
      <button type="button" data-f="rooms" aria-pressed="false">Rooms</button>
      <button type="button" data-f="dining" aria-pressed="false">Dining</button>
      <button type="button" data-f="nature" aria-pressed="false">Nature &amp; grounds</button>
    </div>
    <div class="gallery">{figs}</div>
    <p class="note">Illustrations stand in for photographs until the resort's own photos are added.</p>
  </div>
</section>
<dialog class="glb" id="lightbox" aria-label="Picture viewer">
  <div class="glb-top"><div><small id="gEy"></small><b id="gTi"></b></div><span class="glb-c"><b id="gCur">01</b> / <span id="gTot">01</span></span><button type="button" class="glb-b" id="gX" aria-label="Close">×</button></div>
  <span class="glb-bar"><u id="gBar"></u></span>
  <div class="glb-stage"><img id="gImg" src="" alt=""></div>
  <div class="glb-th" id="gTh"></div>
  <button type="button" class="glb-b glb-a" id="gP" aria-label="Previous picture">‹</button><button type="button" class="glb-b glb-a" id="gN" aria-label="Next picture">›</button>
</dialog>
''' + FOOT

# ---------------- Contact ----------------
con = head("Book and find us | Kaptagat Farm Resort",
           "Send a booking inquiry, call or WhatsApp Kaptagat Farm Resort, and get directions from Eldoret, the airport and Nairobi.",
           "contact.html") + f'''
<section class="band" aria-labelledby="h1">
  <div class="wrap">
    <h1 id="h1" style="font-size:clamp(40px,5vw,62px)">Book your stay</h1>
    <p class="lede">Send your dates and we confirm availability and the final price. You only pay once your stay is confirmed.</p>
    <div class="contact-grid">
      <div class="card">
        <h2 style="font-size:30px">Booking inquiry</h2>
        <form id="inquiry-form" novalidate>
          <div class="form-grid">
            <div class="field"><label for="iq-name">Full name</label><input id="iq-name" autocomplete="name" required><div class="err" id="iq-name-err" aria-live="polite"></div></div>
            <div class="field"><label for="iq-phone">Phone or WhatsApp</label><input id="iq-phone" type="tel" autocomplete="tel" placeholder="+254 712 345 678" required><div class="err" id="iq-phone-err" aria-live="polite"></div></div>
            <div class="field"><label for="iq-email">Email (optional)</label><input id="iq-email" type="email" autocomplete="email"><div class="err" id="iq-email-err" aria-live="polite"></div></div>
            <div class="field"><label for="iq-room">Stay</label><select id="iq-room">{ROOM_OPTS}</select><div class="err"></div></div>
            <div class="field"><label for="iq-in">Check-in</label><input id="iq-in" type="date" required><div class="err" id="iq-in-err" aria-live="polite"></div></div>
            <div class="field"><label for="iq-out">Check-out</label><input id="iq-out" type="date" required><div class="err" id="iq-out-err" aria-live="polite"></div></div>
            <div class="field"><label for="iq-guests">Guests</label><input id="iq-guests" type="number" inputmode="numeric" min="1" max="200" value="2"></div>
            <div class="field full"><label for="iq-msg">Anything we should know? (optional)</label><textarea id="iq-msg" placeholder="Arrival time, meals to pre-order, events, group bookings…"></textarea></div>
            <div class="hp" aria-hidden="true"><label for="iq-company">Company</label><input id="iq-company" tabindex="-1" autocomplete="off"></div>
            <div class="field full"><label class="check" for="iq-consent"><input id="iq-consent" type="checkbox"> I agree that Kaptagat Farm Resort may contact me about this inquiry.</label><div class="err" id="iq-consent-err" aria-live="polite"></div></div>
            <div class="full"><button class="btn" type="submit">Send inquiry</button></div>
          </div>
        </form>
        <div class="success" id="iq-success" tabindex="-1" aria-live="polite">
          <h3 id="iq-title" style="font-size:24px"></h3>
          <p id="iq-summary"></p><p id="iq-note"></p>
          <div class="acts"><a class="btn wa" id="iq-wa" href="#">Send on WhatsApp</a><a class="btn ghost" id="iq-mail" href="#" data-needs-email>Send by email</a></div>
        </div>
      </div>
      <div class="stackcol">
        <div class="card">
          <h2 style="font-size:30px">Talk to us</h2>
          <ul class="contact-list">
            <li><b>Call</b><a data-tel href="#"></a></li>
            <li><b>WhatsApp</b><a data-wa="" href="#"><span data-wa-text></span></a></li>
            <li data-needs-email><b>Email</b><a data-email href="#"></a></li>
            <li><b>Social</b><a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></li>
          </ul>
          <a class="btn wa" data-wa="" href="#" style="margin-top:20px;width:100%">Chat on WhatsApp</a>
        </div>
        <div class="card">
          <h2 style="font-size:26px">Before you come</h2>
          <ul class="ticks" style="margin:0">
            <li>Pre-order meals: everything is cooked fresh to order</li>
            <li>Pack a warm layer for cool highland evenings</li>
            <li>Day visitors pay a gate fee; ask what it covers</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band tint" id="directions" aria-labelledby="h-dir">
  <div class="wrap split">
    <div>
      <h2 id="h-dir">Getting here</h2>
      <ol class="route">
        <li><div><b>Eldoret town</b><span>Take the Kaptagat road out of town</span></div><em>start</em></li>
        <li><div><b>Kaptagat road</b><span>Continue towards Kaptagat and Chepkorio</span></div><em>about 25 km</em></li>
        <li><div><b>Kaptagat Farm Resort</b><span>Beside the road at Kaptarakwa</span></div><em>arrive</em></li>
      </ol>
      <p><b>By air:</b> fly into Eldoret International Airport, about 30 minutes from the resort by road. We can help arrange a pickup.</p>
      <p><b>From Nairobi:</b> follow the A104 through Nakuru to Eldoret, then the Kaptagat road as above.</p>
    </div>
    <div class="card" style="text-align:center">
      <p class="note" style="margin:0 0 6px">Google plus code</p>
      <p class="pluscode">CFG8+65C Kaptarakwa</p>
      <div class="acts" style="justify-content:center"><a class="btn" href="{MAPS}">Open in Google Maps</a><a class="btn ghost" href="{GOOGLE}">Google listing</a></div>
      <!-- On the live site you can replace this card with a Google Maps embed:
      <iframe src="https://www.google.com/maps/embed?pb=..." title="Map to Kaptagat Farm Resort" loading="lazy" style="border:0;width:100%;aspect-ratio:16/10" referrerpolicy="no-referrer-when-downgrade"></iframe> -->
    </div>
  </div>
</section>
''' + FOOT

pages = [("index.html", home), ("accommodations.html", acc), ("experiences.html", exp), ("gallery.html", gal), ("contact.html", con)]
(OUT / "img").mkdir(parents=True, exist_ok=True)
art.write_all(OUT / "img")
for name, html in pages:
    (OUT / name).write_text(html, encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 + "".join(f"  <url><loc>{url(p)}</loc></url>\n" for p, _ in pages) + "</urlset>\n")
print("built", sorted(p.name for p in OUT.iterdir()))
