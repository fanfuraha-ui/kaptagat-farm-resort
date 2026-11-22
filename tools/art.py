"""Line drawings for the Kaptagat Farm Resort site.

The drawings are built from the real geometry of the resort's signature building, the ten-sided
(decagon) bush-stone cottage: a plan, an elevation and a schematic site plan. Strokes use
currentColor so the page's CSS decides the ink colour; nothing here pretends to be a photograph.
"""
import math, random


def deca(cx, cy, r, rot=0):
    return [(cx + r * math.cos(math.radians(rot + 36 * i)), cy + r * math.sin(math.radians(rot + 36 * i))) for i in range(10)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def poly(p, sw=1, fill="none", extra=""):
    return f'<polygon points="{pts(p)}" fill="{fill}" stroke="currentColor" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def line(x1, y1, x2, y2, sw=1, op=1, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="{sw}" opacity="{op}" {extra}/>'


def plan_group(cx, cy, r, eaves=True, ridges=True):
    """Roof plan of a ten-sided cottage: wall line, eave line, pillars at the corners and the ten hips."""
    out = []
    outer = deca(cx, cy, r)
    if eaves:
        out.append(poly(deca(cx, cy, r * 1.12), .8, extra='stroke-dasharray="5 4" opacity=".6"'))
    out.append(poly(outer, 1.5))
    out.append(poly(deca(cx, cy, r * .92), .8))
    if ridges:
        for x, y in outer:
            out.append(line(cx, cy, x, y, .6, .5))
    for x, y in outer:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(2.4, r * .028):.1f}" fill="currentColor"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="none" stroke="currentColor" stroke-width=".8"/>')
    return "".join(out)


def elevation(cx, gy, w, H, rh, seed=4):
    """Front elevation: five visible faces of full-height glass between bush-stone pillars, under a pyramid roof."""
    rnd = random.Random(seed)
    unit = w / 3.24
    widths = [.31, .81, 1.0, .81, .31]
    xs = [cx - w / 2]
    for k in widths:
        xs.append(xs[-1] + k * unit)
    top = gy - H
    base_h = H * .14
    out = []
    # ground, with hatching beneath
    gx0, gx1 = cx - w * .95, cx + w * .95
    out.append(line(gx0, gy, gx1, gy, 1.3))
    x = gx0 + 6
    while x < gx1 - 8:
        out.append(line(x, gy, x - 7, gy + 9, .6, .4))
        x += 11
    # glazed faces
    tint = [.10, .07, .045, .03, .02]
    for i in range(5):
        x0, x1 = xs[i], xs[i + 1]
        out.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1 - x0:.1f}" height="{H - base_h:.1f}" fill="currentColor" fill-opacity="{tint[i]}" stroke="currentColor" stroke-width="1"/>')
        out.append(line(x0, top + H * .24, x1, top + H * .24, .7, .8))
        if widths[i] > .7:
            out.append(line((x0 + x1) / 2, top, (x0 + x1) / 2, gy - base_h, .5, .45))
    # stone base with coursing
    out.append(f'<rect x="{xs[0]:.1f}" y="{gy - base_h:.1f}" width="{xs[-1] - xs[0]:.1f}" height="{base_h:.1f}" fill="none" stroke="currentColor" stroke-width="1"/>')
    rows = 3
    rh_ = base_h / rows
    for r in range(1, rows):
        out.append(line(xs[0], gy - base_h + r * rh_, xs[-1], gy - base_h + r * rh_, .5, .55))
    for r in range(rows):
        y0 = gy - base_h + r * rh_
        x = xs[0] + rnd.uniform(4, 16)
        while x < xs[-1] - 4:
            out.append(line(x, y0, x, y0 + rh_, .5, .5))
            x += rnd.uniform(15, 28)
    # pillars
    p = 4.2
    for x in xs:
        out.append(f'<rect x="{x - p:.1f}" y="{top:.1f}" width="{2 * p:.1f}" height="{H:.1f}" fill="currentColor" fill-opacity=".22" stroke="currentColor" stroke-width=".9"/>')
    # roof
    eave = top + H * .02
    ex = [cx + (x - cx) * 1.12 for x in xs]
    apex = (cx, top - rh)
    face = [.16, .11, .07, .04, .02]
    for i in range(5):
        out.append(f'<polygon points="{apex[0]:.1f},{apex[1]:.1f} {ex[i]:.1f},{eave:.1f} {ex[i + 1]:.1f},{eave:.1f}" fill="currentColor" fill-opacity="{face[i]}" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>')
    out.append(line(ex[0], eave + 6, ex[-1], eave + 6, .8, .7))
    out.append(line(cx, apex[1] - 16, cx, apex[1], 1.4))
    return "".join(out), dict(xs=xs, top=top, apex=apex, eave=eave, gy=gy, unit=unit, base_h=base_h)


def ann(x, y, tx, ty, text, anchor="start"):
    dx = 7 if anchor == "start" else -7
    return (f'<g class="ann"><circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="currentColor"/>'
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="currentColor" stroke-width=".7" opacity=".7"/>'
            f'<text x="{tx + dx:.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}">{text}</text></g>')


def hero_drawing():
    """Elevation and roof plan of the decagon cottage, drawn like a sheet from an architect's set."""
    W, H = 1000, 560
    body = []
    # tall trees behind, drawn as light outlines for scale
    for tx, ty, rx, ry in [(48, 380, 16, 70), (84, 395, 13, 54)]:
        body.append(f'<ellipse cx="{tx}" cy="{ty}" rx="{rx}" ry="{ry}" fill="currentColor" fill-opacity=".05" stroke="currentColor" stroke-width=".8" opacity=".6"/>')
        body.append(line(tx, ty + ry, tx, 470, .9, .6))
    elev, g = elevation(290, 470, 340, 210, 115)
    body.append(elev)
    body.append(plan_group(830, 285, 138))
    # notes
    xs, top = g["xs"], g["top"]
    body.append(ann(xs[5], 392, 540, 392, "Bush-stone pillars"))
    body.append(ann(xs[2] + g["unit"] * .45, 330, 540, 330, "Full-height glazing"))
    body.append(ann(g["apex"][0] + 50, g["apex"][1] + 55, 540, 205, "Pyramid roof"))
    body.append('<text class="cap" x="290" y="522" text-anchor="middle">Decagon cottage, elevation</text>')
    body.append('<text class="cap" x="830" y="492" text-anchor="middle">Roof plan, ten sides</text>')
    return (f'<svg class="drawing" viewBox="0 0 {W} {H}" role="img" aria-label="Line drawing of a decagon cottage: an elevation showing bush-stone pillars, full-height glazing and a pyramid roof, beside its ten-sided roof plan">'
            + "".join(body) + '</svg>')


def plan_small():
    """Small roof-plan ornament for inner page headers."""
    return ('<svg class="drawing small" viewBox="0 0 320 320" aria-hidden="true">'
            + plan_group(160, 160, 120) + '</svg>')


def mark():
    """Brand mark: the decagon plan."""
    out = [poly(deca(32, 32, 24), 3.2, extra='stroke="currentColor"'), poly(deca(32, 32, 19), 1.4)]
    for x, y in deca(32, 32, 24):
        out.append(line(32, 32, x, y, 1.2, .7))
    return ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true">' + "".join(out) + '</svg>')


def favicon():
    out = ['<rect width="64" height="64" rx="12" fill="#1C3427"/>']
    p = deca(32, 32, 22)
    out.append(f'<polygon points="{pts(p)}" fill="none" stroke="#ECE9DD" stroke-width="3" stroke-linejoin="round"/>')
    for x, y in p:
        out.append(f'<line x1="32" y1="32" x2="{x:.1f}" y2="{y:.1f}" stroke="#ECE9DD" stroke-width="1.6" opacity=".75"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' + "".join(out) + '</svg>\n'


# ---------------- Schematic site plan ----------------
PINS = [
    (1, 70, 350, "Gate and parking", "Secure parking inside the gate"),
    (2, 226, 312, "Reception", "Check-in from 2:00 pm"),
    (3, 452, 236, "The Mill Bar", "A ten-sided bar at the centre of the garden"),
    (4, 305, 226, "Restaurant", "Meals cooked to order, served indoors and out"),
    (5, 700, 128, "Decagon cottages", "Bush stone, windows from ground to roof frame"),
    (6, 392, 440, "Pond cottage", "A cottage built in the middle of a pond"),
    (7, 636, 446, "Picnic terrace", "Acacia shade, stepping down towards the river"),
    (8, 806, 412, "Bandas", "Six bush-stone bandas in a U for private dining"),
    (9, 562, 312, "Conference hall", "A two-storey decagon, up to 200 people"),
    (10, 372, 134, "Standard rooms", "Twin and double rooms, with the seminar block"),
    (11, 524, 54, "Forest trails", "Paths into the forest at the edge of the grounds"),
]


def mini(cx, cy, r, sw=1.2):
    out = [f'<polygon points="{pts(deca(cx, cy, r))}" class="fp" stroke="currentColor" stroke-width="{sw}" stroke-linejoin="round"/>',
           f'<polygon points="{pts(deca(cx, cy, r * .84))}" fill="none" stroke="currentColor" stroke-width=".6"/>']
    for x, y in deca(cx, cy, r):
        out.append(line(cx, cy, x, y, .5, .5))
    return "".join(out)


def tree(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" class="fp" stroke="currentColor" stroke-width="1"/>'
            f'<circle cx="{x}" cy="{y}" r="{max(1.6, r * .1):.1f}" fill="currentColor"/>')


def estate_map():
    rnd = random.Random(99)
    b = ['<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width=".6" opacity=".4"/></pattern>'
         '<pattern id="water" width="12" height="7" patternUnits="userSpaceOnUse"><path d="M0 3.5 q3 -3.5 6 0 t6 0" fill="none" stroke="currentColor" stroke-width=".7" opacity=".5"/></pattern></defs>']
    # forest to the north
    for i in range(36):
        b.append(tree(round(i * 25.5 + rnd.uniform(-6, 6)), round(rnd.uniform(14, 56)), round(rnd.uniform(15, 25))))
    # river
    for off, op in [(0, 1), (22, 1)]:
        b.append(f'<path d="M-10 {552 + off} C150 {522 + off} 300 {577 + off} 470 {547 + off} C640 {517 + off} 760 {567 + off} 910 {532 + off}" fill="none" stroke="currentColor" stroke-width="1.1" opacity="{op}"/>')
    b.append('<path d="M-10 563 C150 533 300 588 470 558 C640 528 760 578 910 543 L910 575 C760 610 640 560 470 590 C300 620 150 565 -10 585Z" fill="url(#water)" opacity=".7"/>')
    # road
    b.append(line(8, 0, 8, 600, 1.1) + line(34, 0, 34, 600, 1.1))
    b.append('<text x="21" y="300" transform="rotate(-90 21 300)" text-anchor="middle" class="mt">Kaptagat road</text>')
    # paths
    for d in ["M34 380 C120 380 160 354 226 354 C300 354 380 304 452 304", "M452 304 C520 304 580 244 640 224 C690 209 720 194 760 204",
              "M452 304 C480 334 520 354 562 364 C640 384 720 404 800 409", "M452 304 C420 344 380 384 330 414",
              "M452 304 C500 364 560 424 630 474", "M452 304 C460 234 480 174 500 114 L520 64", "M226 354 C230 304 240 244 250 209"]:
        b.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="7 5" opacity=".75"/>')
    # parking
    for i in range(4):
        b.append(f'<rect x="{46 + i * 30}" y="412" width="24" height="44" class="fp" stroke="currentColor" stroke-width="1"/>')
    # standard rooms and seminar block
    for y in (118, 162):
        b.append(f'<rect x="150" y="{y}" width="200" height="30" class="fp" stroke="currentColor" stroke-width="1.1"/>')
        for i in range(1, 8):
            b.append(line(150 + i * 25, y, 150 + i * 25, y + 30, .6, .6))
    # reception and restaurant
    b.append('<rect x="190" y="332" width="72" height="40" fill="url(#hatch)" stroke="currentColor" stroke-width="1.2"/>')
    b.append('<rect x="258" y="246" width="96" height="44" fill="url(#hatch)" stroke="currentColor" stroke-width="1.2"/>')
    for x, y in [(272, 304), (300, 308), (328, 304)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="5" class="fp" stroke="currentColor" stroke-width="1"/>')
    # Mill Bar, conference hall, cottages
    b.append(mini(452, 304, 42, 1.4))
    b.append(f'<polygon points="{pts(deca(562, 364, 38))}" fill="url(#hatch)" stroke="currentColor" stroke-width="1.2"/>')
    b.append(mini(562, 364, 30, 1.4))
    for x, y in [(560, 174), (640, 226), (722, 176), (792, 252)]:
        b.append(mini(x, y, 22))
    # pond and its cottage
    b.append('<path d="M210 432 C220 382 300 372 360 387 C410 400 400 472 350 484 C290 498 205 482 210 432Z" fill="url(#water)" stroke="currentColor" stroke-width="1.2"/>')
    b.append(mini(310, 434, 20))
    for x in (222, 232, 242):
        b.append(line(x, 450, x + 3, 436, .9) + line(x + 5, 452, x + 2, 440, .9))
    # acacias
    for x, y, r in [(590, 474, 30), (680, 504, 30), (520, 498, 22)]:
        b.append(tree(x, y, r))
    # bandas
    for x, y in [(760, 376), (758, 412), (772, 446), (830, 446), (844, 412), (842, 376)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="11" class="fp" stroke="currentColor" stroke-width="1.1"/><circle cx="{x}" cy="{y}" r="3.5" fill="currentColor"/>')
    # north
    b.append('<g transform="translate(868 112)"><path d="M0 -20 L7 6 L0 1 L-7 6Z" fill="currentColor"/><text x="0" y="24" text-anchor="middle" class="mt">N</text></g>')
    for n, x, y, _, _ in PINS:
        b.append(f'<g class="pin" data-pin="{n}"><circle cx="{x}" cy="{y}" r="13" class="pc"/><text x="{x}" y="{y + 4.6}" text-anchor="middle">{n}</text></g>')
    return ('<svg class="estate" viewBox="0 0 900 600" role="img" aria-labelledby="map-t"><title id="map-t">Schematic plan of the resort grounds, with numbered places matching the key</title>'
            + "".join(b) + '</svg>')


def write_assets(out):
    (out / "favicon.svg").write_text(favicon(), encoding="utf-8")
