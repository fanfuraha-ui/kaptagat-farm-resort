"""Procedural SVG illustrations for the Kaptagat Farm Resort site.
The signature motif is the resort's ten-sided (decagon) bush-stone cottage."""
import math, random

FOREST = "#1F3A2C"; MOSS = "#557A46"; LEAF = "#6E8F4E"; PAPYRUS = "#8FA65B"
TERRA = "#A44E2C"; STONE = "#B8AD9B"; STONE_D = "#8F8574"; CREAM = "#F4EEE2"; MIST = "#EAE8DA"
AGAP = "#7275C9"; AGAP_L = "#A3A6E6"

def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    if f < 1: r, g, b = (int(c * f) for c in (r, g, b))
    else: r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"

def svg(w, h, body, label, defs="", par="xMidYMid slice"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="{par}" '
            f'role="img" aria-label="{label}"><defs>{defs}</defs>{body}</svg>\n')

def grad(id_, c1, c2, vertical=True):
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{id_}" {xy}><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'

GLASS = {
    "day":   ("#DDE6DA", "#7F9B8E"),
    "dusk":  ("#FFD796", "#D98744"),
    "night": ("#FFE3A8", "#E39A4C"),
}

def stones(x, y, w, h, rnd, base=STONE):
    """Bush-stone wall texture inside a rectangle."""
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{shade(base,.82)}"/>']
    rows = max(2, int(h // 9))
    rh = h / rows
    for r in range(rows):
        cx = x + rnd.uniform(-6, 0)
        while cx < x + w:
            sw = rnd.uniform(8, 18)
            sw2 = min(sw, x + w - cx)
            if sw2 > 2 and cx >= x - 1:
                out.append(f'<rect x="{max(cx,x):.1f}" y="{y + r*rh + .8:.1f}" width="{sw2 - 1.2:.1f}" height="{rh - 1.6:.1f}" rx="3" fill="{shade(base, rnd.uniform(.9,1.08))}"/>')
            cx += sw
    return "".join(out)

def cottage(cx, by, w, H, rh, mode="day", seed=1, roof=TERRA, wall=STONE):
    """Front view of a ten-sided cottage: five visible faces of full-height glass between stone pillars."""
    rnd = random.Random(seed)
    unit = w / 3.24
    widths = [.31, .81, 1.0, .81, .31]
    light = [1.0, 1.0, .93, .8, .68]
    xs = [cx - w / 2]
    for k in widths: xs.append(xs[-1] + k * unit)
    top = by - H
    g = mode
    out = [f'<ellipse cx="{cx:.1f}" cy="{by+4:.1f}" rx="{w*.62:.1f}" ry="{H*.09:.1f}" fill="#16281E" opacity=".28"/>']
    if mode != "day":
        out.append(f'<ellipse cx="{cx:.1f}" cy="{by+10:.1f}" rx="{w*.75:.1f}" ry="{H*.16:.1f}" fill="#FFC979" opacity=".18"/>')
    base_h = H * .13
    for i, k in enumerate(widths):
        x0, x1 = xs[i], xs[i+1]
        out.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1-x0:.1f}" height="{H-base_h:.1f}" fill="url(#glass-{g})"/>')
        if light[i] < 1:
            out.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1-x0:.1f}" height="{H-base_h:.1f}" fill="#0E1A14" opacity="{(1-light[i])*.9:.2f}"/>')
        # glass reflection streak
        if mode == "day" and k > .5:
            sx = x0 + (x1-x0)*.25
            out.append(f'<path d="M{sx:.1f} {top+H*.08:.1f} l{(x1-x0)*.18:.1f} 0 l-{(x1-x0)*.22:.1f} {H*.5:.1f} l-{(x1-x0)*.14:.1f} 0z" fill="#fff" opacity=".22"/>')
        # transom bar
        out.append(f'<rect x="{x0:.1f}" y="{top + H*.2:.1f}" width="{x1-x0:.1f}" height="{max(2,H*.018):.1f}" fill="{shade(wall,.55)}" opacity=".9"/>')
    if mode != "day":
        # warm interior: lamp and bed silhouettes in centre face
        x0, x1 = xs[2], xs[3]; fw = x1 - x0
        out.append(f'<rect x="{x0+fw*.12:.1f}" y="{by-base_h-H*.2:.1f}" width="{fw*.5:.1f}" height="{H*.12:.1f}" rx="4" fill="#B5653A" opacity=".55"/>')
        out.append(f'<rect x="{x0+fw*.72:.1f}" y="{by-base_h-H*.42:.1f}" width="{fw*.04:.1f}" height="{H*.3:.1f}" fill="#7A4022" opacity=".6"/>')
        out.append(f'<path d="M{x0+fw*.64:.1f} {by-base_h-H*.42:.1f} h{fw*.2:.1f} l-{fw*.04:.1f} -{H*.1:.1f} h-{fw*.12:.1f}z" fill="#FFF1C9"/>')
    # stone base band
    out.append(stones(xs[0], by - base_h, xs[-1] - xs[0], base_h, rnd, wall))
    out.append(f'<rect x="{xs[3]:.1f}" y="{by-base_h:.1f}" width="{xs[-1]-xs[3]:.1f}" height="{base_h:.1f}" fill="#0E1A14" opacity=".22"/>')
    # stone pillars
    p = unit * .085
    for i, x in enumerate(xs):
        f = 1.0 if i < 3 else .82
        out.append(f'<g>{stones(x - p/2, top, p, H - base_h, rnd, shade(wall, f))}</g>')
    # roof: decagonal pyramid
    eave = top + H * .03
    over = 1.12
    ex = [cx + (x - cx) * over for x in xs]
    apex = (cx, top - rh)
    roof_light = [1.12, 1.0, .9, .74, .62]
    for i in range(5):
        out.append(f'<path d="M{apex[0]:.1f} {apex[1]:.1f} L{ex[i]:.1f} {eave:.1f} L{ex[i+1]:.1f} {eave:.1f}Z" fill="{shade(roof, roof_light[i])}"/>')
    out.append(f'<rect x="{ex[0]:.1f}" y="{eave-1:.1f}" width="{ex[-1]-ex[0]:.1f}" height="{max(3,H*.035):.1f}" fill="{shade(roof,.5)}"/>')
    out.append(f'<rect x="{cx-unit*.04:.1f}" y="{apex[1]-rh*.12:.1f}" width="{unit*.08:.1f}" height="{rh*.14:.1f}" fill="{shade(roof,.45)}"/>')
    return "".join(out)

def tree_round(x, y, s, c=MOSS, rnd=None):
    rnd = rnd or random.Random(int(x*7+y))
    out = [f'<rect x="{x-s*.06:.1f}" y="{y-s*.55:.1f}" width="{s*.12:.1f}" height="{s*.55:.1f}" fill="#3B2A1E"/>']
    for dx, dy, r in [(-.28, -.75, .34), (.26, -.78, .36), (0, -1.0, .42), (-.05, -.68, .38)]:
        out.append(f'<circle cx="{x+dx*s:.1f}" cy="{y+dy*s:.1f}" r="{r*s:.1f}" fill="{shade(c, rnd.uniform(.9,1.06))}"/>')
    out.append(f'<path d="M{x:.1f} {y-s*1.42:.1f} A{s*.55:.1f} {s*.55:.1f} 0 0 1 {x+s*.6:.1f} {y-s*.72:.1f} L{x:.1f} {y-s*.6:.1f}Z" fill="#0E1A14" opacity=".18"/>')
    return "".join(out)

def tree_tall(x, y, s, c=FOREST):
    return (f'<rect x="{x-s*.05:.1f}" y="{y-s*.5:.1f}" width="{s*.1:.1f}" height="{s*.5:.1f}" fill="#3B2A1E"/>'
            f'<ellipse cx="{x:.1f}" cy="{y-s*1.15:.1f}" rx="{s*.3:.1f}" ry="{s*.85:.1f}" fill="{c}"/>'
            f'<path d="M{x:.1f} {y-s*2:.1f} C{x+s*.45:.1f} {y-s*1.5:.1f} {x+s*.36:.1f} {y-s*.6:.1f} {x:.1f} {y-s*.3:.1f}Z" fill="#0E1A14" opacity=".2"/>')

def acacia(x, y, s, c=MOSS):
    return (f'<path d="M{x-s*.04:.1f} {y:.1f} C{x-s*.02:.1f} {y-s*.4:.1f} {x-s*.2:.1f} {y-s*.6:.1f} {x-s*.45:.1f} {y-s*.78:.1f} M{x:.1f} {y-s*.35:.1f} C{x+s*.1:.1f} {y-s*.55:.1f} {x+s*.3:.1f} {y-s*.65:.1f} {x+s*.5:.1f} {y-s*.8:.1f} M{x-s*.02:.1f} {y-s*.4:.1f} L{x+s*.02:.1f} {y-s*.82:.1f}" stroke="#3B2A1E" stroke-width="{s*.05:.1f}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{x:.1f}" cy="{y-s*.86:.1f}" rx="{s*.78:.1f}" ry="{s*.16:.1f}" fill="{c}"/>'
            f'<ellipse cx="{x-s*.25:.1f}" cy="{y-s*.92:.1f}" rx="{s*.42:.1f}" ry="{s*.11:.1f}" fill="{shade(c,1.15)}"/>'
            f'<ellipse cx="{x+s*.1:.1f}" cy="{y-s*.8:.1f}" rx="{s*.7:.1f}" ry="{s*.07:.1f}" fill="#0E1A14" opacity=".22"/>')

def papyrus(x, y, s, rnd, n=7):
    out = []
    for i in range(n):
        bx = x + rnd.uniform(-s*.25, s*.25); tx = bx + rnd.uniform(-s*.25, s*.25); ty = y - s * rnd.uniform(.7, 1.1)
        out.append(f'<path d="M{bx:.1f} {y:.1f} Q{(bx+tx)/2:.1f} {(y+ty)/2:.1f} {tx:.1f} {ty:.1f}" stroke="#5E7F3C" stroke-width="{s*.025:.1f}" fill="none"/>')
        for a in range(-80, 81, 20):
            r = math.radians(a - 90); L = s * .16
            out.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{tx+math.cos(r)*L:.1f}" y2="{ty+math.sin(r)*L*.8:.1f}" stroke="{PAPYRUS}" stroke-width="{s*.018:.1f}" stroke-linecap="round"/>')
    return "".join(out)

def agapanthus(x, y, s, rnd):
    out = [f'<path d="M{x:.1f} {y:.1f} q{s*.05:.1f} -{s*.5:.1f} 0 -{s:.1f}" stroke="#4E6E35" stroke-width="{s*.04:.1f}" fill="none"/>']
    for _ in range(9):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(0, s*.16)
        out.append(f'<circle cx="{x+math.cos(a)*r:.1f}" cy="{y-s+math.sin(a)*r*.8:.1f}" r="{s*.05:.1f}" fill="{rnd.choice([AGAP,AGAP_L])}"/>')
    out.append(f'<path d="M{x-s*.25:.1f} {y:.1f} q{s*.2:.1f} -{s*.25:.1f} {s*.25:.1f} 0 M{x+s*.25:.1f} {y:.1f} q-{s*.2:.1f} -{s*.25:.1f} -{s*.25:.1f} 0" stroke="#4E6E35" stroke-width="{s*.05:.1f}" fill="none"/>')
    return "".join(out)

def forest_band(W, y, c, rnd, count, s0, s1, kinds=("r", "t")):
    out = []
    for i in range(count):
        x = (i + rnd.uniform(-.3, .3)) * W / (count - 1)
        s = rnd.uniform(s0, s1)
        out.append(tree_round(x, y + rnd.uniform(-6, 6), s, c, rnd) if rnd.choice(kinds) == "r" else tree_tall(x, y, s, c))
    return "".join(out)

# ---------------- Scenes ----------------
def hero():
    W, H = 1600, 900; rnd = random.Random(7)
    defs = "".join(grad(f"glass-{k}", *v) for k, v in GLASS.items()) + grad("water", "#B9CDC6", "#7E9E98") + grad("lawn", "#93AD6A", "#5F8447") + '<clipPath id="pondclip"><ellipse cx="430" cy="760" rx="330" ry="78"/></clipPath>'
    b = [f'<rect width="{W}" height="{H}" fill="{MIST}"/>',
         forest_band(W, 470, "#A9B997", rnd, 22, 70, 110),
         forest_band(W, 520, "#7C9868", rnd, 18, 90, 140),
         forest_band(W, 575, "#4C6E45", rnd, 15, 110, 160),
         f'<path d="M0 560 C300 540 600 575 900 555 C1200 535 1400 565 1600 550 L1600 900 L0 900Z" fill="url(#lawn)"/>',
         # stone path
         f'<path d="M1000 900 C960 800 900 720 860 660" stroke="#D8CDB8" stroke-width="46" fill="none" stroke-linecap="round" opacity=".85"/>',
         # back cottage
         cottage(1215, 630, 160, 96, 56, "day", 3),
         # main cottage
         cottage(900, 690, 400, 230, 130, "day", 5),
         # pond with cottage
         f'<ellipse cx="430" cy="760" rx="330" ry="78" fill="url(#water)"/>',
         f'<ellipse cx="430" cy="752" rx="300" ry="62" fill="#C9DAD3" opacity=".35"/>',
         f'<ellipse cx="430" cy="720" rx="120" ry="18" fill="#9C9180"/>',
         cottage(430, 716, 210, 125, 70, "day", 9),
         f'<g clip-path="url(#pondclip)"><g opacity=".2" transform="translate(0 1432) scale(1 -1)">{cottage(430, 716, 210, 125, 1, "day", 9)}</g></g>',
         papyrus(140, 790, 150, rnd, 9), papyrus(710, 800, 120, rnd, 6),
         acacia(1500, 800, 290, "#4C6E45"),
         ]
    for x in (1080, 1130, 1180, 600, 640):
        b.append(agapanthus(x, 830 + rnd.uniform(-10, 10), 70, rnd))
    b.append(f'<path d="M0 840 C400 820 800 860 1200 840 C1400 832 1500 846 1600 840 L1600 900 L0 900Z" fill="{FOREST}"/>')
    return svg(W, H, "".join(b), "Illustration of Kaptagat Farm Resort: ten-sided bush-stone cottages with full-height windows, a cottage on a pond among papyrus, acacia trees and the forest behind", defs, "xMidYMax slice")

def banner():
    W, H = 1600, 420; rnd = random.Random(17)
    defs = "".join(grad(f"glass-{k}", *v) for k, v in GLASS.items()) + grad("water", "#B9CDC6", "#7E9E98") + grad("lawn", "#93AD6A", "#5F8447")
    b = [f'<rect width="{W}" height="{H}" fill="{MIST}"/>',
         forest_band(W, 225, "#A9B997", rnd, 26, 45, 70),
         forest_band(W, 250, "#7C9868", rnd, 22, 55, 85),
         forest_band(W, 280, "#4C6E45", rnd, 18, 65, 95),
         f'<path d="M0 275 C400 265 800 285 1200 270 C1400 265 1500 275 1600 270 L1600 420 L0 420Z" fill="url(#lawn)"/>',
         f'<ellipse cx="330" cy="350" rx="210" ry="40" fill="url(#water)"/>',
         cottage(330, 335, 130, 78, 44, "day", 9),
         cottage(820, 340, 230, 132, 74, "day", 5),
         cottage(1180, 320, 120, 72, 42, "day", 3),
         papyrus(150, 385, 90, rnd, 7), papyrus(520, 390, 70, rnd, 5),
         acacia(1450, 370, 200, "#4C6E45")]
    for x in (980, 1020, 1060):
        b.append(agapanthus(x, 395, 45, rnd))
    b.append(f'<path d="M0 400 C400 392 800 410 1200 398 C1400 394 1500 402 1600 398 L1600 420 L0 420Z" fill="{FOREST}"/>')
    return svg(W, H, "".join(b), "Illustration of the decagon cottages, the pond and the forest", defs, "xMidYMax slice")

def cottage_scene(mode="dusk", name="cottage", pond=False, two=False, label=""):
    W, H = 800, 600; rnd = random.Random(len(name) * 11)
    skies = {"day": ("#EAE8DA", "#F4EEE2"), "dusk": ("#2B3E3A", "#D99A62"), "night": ("#0F1C1A", "#253934")}
    defs = "".join(grad(f"glass-{k}", *v) for k, v in GLASS.items()) + grad("sky", *skies[mode]) + grad("water", "#5E7B78", "#2A403E") + grad("lawn", "#4E6E40", "#2C4630")
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    if mode == "night":
        for _ in range(60):
            b.append(f'<circle cx="{rnd.uniform(0,W):.0f}" cy="{rnd.uniform(0,250):.0f}" r="{rnd.uniform(.6,1.6):.1f}" fill="#F4EEE2" opacity="{rnd.uniform(.4,.9):.2f}"/>')
    if mode == "dusk":
        b.append(f'<circle cx="610" cy="300" r="70" fill="#F2B477" opacity=".8"/>')
    fc = {"day": "#6E8F58", "dusk": "#1F3328", "night": "#132520"}[mode]
    b.append(forest_band(W, 360, shade(fc, 1.15), rnd, 12, 70, 110))
    b.append(forest_band(W, 400, fc, rnd, 10, 90, 130))
    b.append(f'<rect y="390" width="{W}" height="{H-390}" fill="url(#lawn)"/>')
    if pond:
        b.append(f'<ellipse cx="400" cy="500" rx="360" ry="80" fill="url(#water)"/>')
        b.append(f'<ellipse cx="400" cy="470" rx="150" ry="20" fill="#6D6558"/>')
        b.append(cottage(400, 466, 270, 165, 92, mode, 4))
        b.append(f'<clipPath id="pc"><ellipse cx="400" cy="500" rx="360" ry="80"/></clipPath><g clip-path="url(#pc)"><g opacity=".25" transform="translate(0 932) scale(1 -1)">{cottage(400, 466, 270, 165, 1, mode, 4)}</g></g>')
        b.append(papyrus(80, 560, 160, rnd, 8)); b.append(papyrus(720, 570, 140, rnd, 7))
    elif two:
        b.append(cottage(250, 470, 260, 160, 90, mode, 2))
        b.append(f'<rect x="360" y="400" width="90" height="62" fill="{shade(STONE,.7)}"/><rect x="360" y="392" width="90" height="10" fill="{shade(TERRA,.5)}"/>')
        b.append(cottage(560, 480, 300, 185, 100, mode, 6))
    else:
        b.append(cottage(400, 480, 380, 230, 120, mode, 8))
        b.append(tree_round(90, 470, 110, fc, rnd)); b.append(tree_tall(720, 480, 120, fc))
    if not pond:
        for x in (120, 200, 610, 690):
            b.append(agapanthus(x, 560, 60, rnd))
    return svg(W, H, "".join(b), label, defs)

def interior(kind="standard"):
    W, H = 800, 600; rnd = random.Random(3)
    defs = grad("wall", "#EFE5D2", "#E1D3BA") + grad("view", "#EAE8DA", "#7C9868")
    b = [f'<rect width="{W}" height="{H}" fill="url(#wall)"/>',
         f'<rect y="440" width="{W}" height="160" fill="#7A5236"/>',
         f'<rect x="470" y="70" width="240" height="250" fill="#5E5446"/>',
         f'<rect x="482" y="82" width="216" height="226" fill="url(#view)"/>',
         forest_band(216, 300, "#4C6E45", rnd, 5, 40, 60).replace('x="', 'x="').replace("<", "<", 1),
         ]
    b[-1] = f'<g transform="translate(482 0)"><clipPath id="vc"><rect y="82" width="216" height="226"/></clipPath><g clip-path="url(#vc)">{forest_band(216, 300, "#4C6E45", rnd, 5, 40, 60)}</g></g>'
    b.append('<rect x="586" y="82" width="8" height="226" fill="#5E5446"/>')
    if kind == "standard":
        for bx in (60, 280):
            b.append(f'<path d="M{bx+80} 60 L{bx-10} 360 L{bx+170} 360Z" fill="#FFFFFF" opacity=".5"/>')
            b.append(f'<rect x="{bx}" y="360" width="150" height="80" rx="6" fill="#F7F2E8"/>')
            b.append(f'<rect x="{bx}" y="380" width="150" height="60" fill="{TERRA}"/>')
            b.append(f'<rect x="{bx+20}" y="344" width="110" height="26" rx="12" fill="#FBF7EF"/>')
            b.append(f'<rect x="{bx+6}" y="440" width="8" height="30" fill="#4A3020"/><rect x="{bx+136}" y="440" width="8" height="30" fill="#4A3020"/>')
            b.append(f'<circle cx="{bx+80}" cy="58" r="6" fill="#B8AD9B"/>')
        b.append('<rect x="225" y="400" width="44" height="40" rx="4" fill="#6B4430"/>')
        label = "Illustration of a standard twin room with mosquito nets and a window onto the garden"
    else:
        for bx in (40, 250):
            b.append(f'<rect x="{bx}" y="200" width="12" height="270" fill="#4A3020"/><rect x="{bx+168}" y="200" width="12" height="270" fill="#4A3020"/>')
            for by in (250, 390):
                b.append(f'<rect x="{bx+12}" y="{by}" width="156" height="34" fill="#F7F2E8"/><rect x="{bx+12}" y="{by+12}" width="156" height="22" fill="{MOSS}"/><rect x="{bx+20}" y="{by-12}" width="56" height="20" rx="9" fill="#FBF7EF"/>')
            b.append(f'<rect x="{bx+150}" y="250" width="8" height="140" fill="#6B4430"/>')
        b.append('<rect x="480" y="380" width="70" height="60" fill="#6B4430"/><rect x="560" y="380" width="70" height="60" fill="#5E3B26"/>')
        label = "Illustration of a dormitory room with bunk beds for groups and athletes"
    b.append(f'<ellipse cx="400" cy="560" rx="300" ry="20" fill="{FOREST}" opacity=".7"/>')
    return svg(W, H, "".join(b), label, defs)

def dining():
    W, H = 800, 600; rnd = random.Random(12)
    defs = grad("sky", "#EAE8DA", "#F4EEE2")
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         forest_band(W, 300, "#7C9868", rnd, 10, 70, 100),
         forest_band(W, 330, "#4C6E45", rnd, 9, 80, 120),
         f'<rect y="320" width="{W}" height="280" fill="#6E8F4E"/>',
         acacia(620, 330, 300, "#4C6E45"),
         # table
         '<rect x="70" y="380" width="520" height="22" rx="6" fill="#8A5A3B"/>',
         '<rect x="90" y="402" width="16" height="130" fill="#6B4430"/><rect x="554" y="402" width="16" height="130" fill="#6B4430"/>',
         '<ellipse cx="190" cy="372" rx="78" ry="16" fill="#F7F2E8"/><ellipse cx="190" cy="368" rx="54" ry="10" fill="#C98B4E"/>',
         '<path d="M150 366 q20 -14 40 0 q18 -12 36 0" stroke="#8C4F26" stroke-width="7" fill="none" stroke-linecap="round"/>',
         '<ellipse cx="360" cy="372" rx="70" ry="15" fill="#F7F2E8"/>',
         '<path d="M318 368 l8 -14 l10 14 l8 -16 l10 16 l8 -12 l10 12" stroke="#E2B65C" stroke-width="6" fill="none"/>',
         '<path d="M470 372 q0 -38 26 -38 q26 0 26 38z" fill="#F7F2E8"/><rect x="520" y="344" width="22" height="6" rx="3" fill="#F7F2E8"/>',
         '<circle cx="496" cy="330" r="5" fill="#B8AD9B"/>',
         # grill
         '<rect x="640" y="440" width="120" height="46" rx="6" fill="#2B2B2B"/>',
         '<path d="M650 440 h100" stroke="#5C5C5C" stroke-width="6"/>',
         '<rect x="660" y="426" width="36" height="14" rx="6" fill="#8C4F26"/><rect x="704" y="426" width="36" height="14" rx="6" fill="#A3582B"/>',
         '<path d="M690 420 q-10 -24 6 -40 M716 418 q12 -22 -2 -42" stroke="#D8CDB8" stroke-width="4" fill="none" opacity=".7"/>',
         '<rect x="656" y="486" width="8" height="50" fill="#2B2B2B"/><rect x="736" y="486" width="8" height="50" fill="#2B2B2B"/>',
         ]
    return svg(W, H, "".join(b), "Illustration of outdoor dining under an acacia: grilled meat, chips, kienyeji chicken and tea", defs)

def millbar():
    W, H = 800, 600; rnd = random.Random(21)
    defs = "".join(grad(f"glass-{k}", *v) for k, v in GLASS.items()) + grad("sky", "#0F1C1A", "#28403A") + grad("lawn", "#2C4630", "#1A2C20")
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for _ in range(50):
        b.append(f'<circle cx="{rnd.uniform(0,W):.0f}" cy="{rnd.uniform(0,230):.0f}" r="{rnd.uniform(.6,1.5):.1f}" fill="#F4EEE2" opacity="{rnd.uniform(.4,.9):.2f}"/>')
    b += [forest_band(W, 380, "#132520", rnd, 11, 90, 130), f'<rect y="380" width="{W}" height="220" fill="url(#lawn)"/>',
          cottage(400, 470, 420, 200, 120, "night", 13, "#7E3B22")]
    for i in range(14):
        x = 40 + i * 55; y = 300 + 30 * math.sin(i / 13 * math.pi)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#FFE3A8"/><circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="#FFE3A8" opacity=".2"/>')
    b.append('<path d="M40 300 Q400 360 755 300" stroke="#0B1310" stroke-width="2" fill="none"/>')
    for x in (130, 670):
        b.append(f'<rect x="{x-40}" y="500" width="80" height="10" rx="4" fill="#6B4430"/><rect x="{x-4}" y="510" width="8" height="40" fill="#4A3020"/>')
    return svg(W, H, "".join(b), "Illustration of the Mill Bar at night: a ten-sided building glowing at the centre of the garden under string lights", defs)

def bandas():
    W, H = 800, 600; rnd = random.Random(5)
    defs = grad("sky", "#EAE8DA", "#F4EEE2")
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', forest_band(W, 300, "#7C9868", rnd, 10, 70, 100),
         forest_band(W, 330, "#4C6E45", rnd, 9, 90, 120), f'<rect y="320" width="{W}" height="280" fill="#7C9868"/>',
         '<path d="M0 420 C200 400 600 400 800 420 L800 600 L0 600Z" fill="#6E8F4E"/>']
    pos = [(110, 400, .7), (250, 380, .62), (400, 372, .58), (550, 380, .62), (690, 400, .7)]
    for x, y, s in pos:
        w = 150 * s; h = 90 * s
        b.append(f'<ellipse cx="{x}" cy="{y+4}" rx="{w*.6:.0f}" ry="{h*.12:.0f}" fill="#16281E" opacity=".25"/>')
        b.append(stones(x - w/2, y - h*.45, w, h*.45, rnd))
        b.append(f'<rect x="{x-w*.32:.0f}" y="{y-h*.45:.0f}" width="{w*.64:.0f}" height="{h*.45:.0f}" fill="#3B2A1E" opacity=".65"/>')
        b.append(f'<path d="M{x-w*.62:.0f} {y-h*.42:.0f} L{x:.0f} {y-h*1.25:.0f} L{x+w*.62:.0f} {y-h*.42:.0f}Z" fill="#C9A45E"/>')
        b.append(f'<path d="M{x:.0f} {y-h*1.25:.0f} L{x+w*.62:.0f} {y-h*.42:.0f} L{x:.0f} {y-h*.42:.0f}Z" fill="#A9853F"/>')
    b.append('<rect x="300" y="470" width="200" height="14" rx="5" fill="#8A5A3B"/><rect x="315" y="484" width="10" height="60" fill="#6B4430"/><rect x="475" y="484" width="10" height="60" fill="#6B4430"/>')
    for x in (330, 400, 470):
        b.append(f'<ellipse cx="{x}" cy="466" rx="24" ry="6" fill="#F7F2E8"/>')
    return svg(W, H, "".join(b), "Illustration of thatched bush-stone bandas arranged in a U-shape for events and private dining", defs)

def garden():
    W, H = 800, 600; rnd = random.Random(31)
    defs = grad("sky", "#EAE8DA", "#F4EEE2") + grad("water", "#8DAAA5", "#5E7B78")
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', forest_band(W, 260, "#7C9868", rnd, 11, 70, 110),
         f'<path d="M0 250 L800 250 L800 600 L0 600Z" fill="#7C9868"/>',
         '<path d="M0 520 C200 490 500 540 800 500 L800 600 L0 600Z" fill="url(#water)"/>',
         '<path d="M0 470 C250 440 520 480 800 450 L800 505 C500 545 200 495 0 525Z" fill="#6E8F4E"/>',
         '<path d="M0 380 C250 350 520 390 800 360 L800 455 C520 485 250 445 0 475Z" fill="#8FA65B"/>',
         acacia(230, 420, 330, "#4C6E45"), acacia(640, 400, 260, "#557A46"),
         '<rect x="330" y="400" width="130" height="12" rx="4" fill="#8A5A3B"/><rect x="340" y="412" width="8" height="40" fill="#6B4430"/><rect x="442" y="412" width="8" height="40" fill="#6B4430"/>',
         '<rect x="320" y="428" width="150" height="8" rx="3" fill="#8A5A3B"/>',
         papyrus(720, 540, 120, rnd, 6)]
    for x in (60, 110, 520, 570):
        b.append(agapanthus(x, 470, 60, rnd))
    return svg(W, H, "".join(b), "Illustration of the picnic terrace under acacia trees, stepping down to the river", defs)

def forest_trail():
    W, H = 800, 600; rnd = random.Random(41)
    defs = grad("f", "#C5CDB2", "#6E8B5E")
    b = [f'<rect width="{W}" height="{H}" fill="url(#f)"/>']
    for x, w, o in [(130, 34, .4), (300, 30, .4), (560, 36, .4), (30, 70, 1), (690, 80, 1)]:
        b.append(f'<rect x="{x}" y="0" width="{w}" height="600" fill="#3B2A1E" opacity="{o}"/><rect x="{x}" y="0" width="{w*.35:.0f}" height="600" fill="#4E3828" opacity="{o}"/>')
    b += ['<path d="M300 600 C360 470 430 430 420 330 L470 330 C480 430 560 480 620 600Z" fill="#E9DFCB"/>',
          '<ellipse cx="160" cy="70" rx="240" ry="120" fill="#2F4A3A"/><ellipse cx="680" cy="60" rx="250" ry="130" fill="#253D2F"/>',
          '<path d="M90 230 C220 210 300 240 380 220" stroke="#3B2A1E" stroke-width="10" fill="none" stroke-linecap="round"/>',
          '<g transform="translate(250 170)"><ellipse cx="30" cy="30" rx="26" ry="18" fill="#1E6B5A"/><path d="M30 20 C40 30 40 42 20 46 Z" fill="#B4552F"/><circle cx="54" cy="20" r="12" fill="#1E6B5A"/><path d="M64 20 C82 26 92 36 96 44" stroke="#2B2B2B" stroke-width="3" fill="none"/><circle cx="57" cy="17" r="2.5" fill="#fff"/><path d="M6 32 L-30 52 L4 40Z" fill="#14493D"/></g>',
          '<path d="M0 520 C150 480 240 540 320 600 L0 600Z" fill="#2F4A3A"/><path d="M800 500 C660 480 600 550 590 600 L800 600Z" fill="#2F4A3A"/>']
    return svg(W, H, "".join(b), "Illustration of a forest trail at the edge of the resort with a sunbird on a branch", defs)

# ---------------- Estate map (inline) ----------------
def deca_pts(cx, cy, r, rot=0):
    return " ".join(f"{cx + r*math.cos(math.radians(rot + 36*i)):.1f},{cy + r*math.sin(math.radians(rot + 36*i)):.1f}" for i in range(10))

def deca_roof(cx, cy, r, fill=TERRA):
    out = [f'<polygon points="{deca_pts(cx, cy, r)}" fill="{fill}"/>']
    for i in range(10):
        if i % 2:
            a1, a2 = math.radians(36*i), math.radians(36*(i+1))
            out.append(f'<path d="M{cx} {cy} L{cx+r*math.cos(a1):.1f} {cy+r*math.sin(a1):.1f} L{cx+r*math.cos(a2):.1f} {cy+r*math.sin(a2):.1f}Z" fill="#000" opacity=".14"/>')
    return "".join(out)

PINS = [
    (1, 62, 340, "Gate and parking", "Secure parking inside the gate"),
    (2, 226, 308, "Reception", "Check-in from 2:00 pm"),
    (3, 452, 236, "The Mill Bar", "Ten-sided bar at the heart of the garden"),
    (4, 305, 226, "Restaurant and outdoor dining", "Meals cooked to order"),
    (5, 682, 126, "Decagon cottages", "Bush stone with full-height windows"),
    (6, 412, 432, "Pond cottage", "A cottage on its own pond"),
    (7, 636, 438, "Picnic terrace", "Acacia shade above the river"),
    (8, 800, 410, "Bandas", "Six bush-stone bandas for events and private dining"),
    (9, 562, 308, "Conference hall", "Two-storey decagon, up to 200 guests"),
    (10, 372, 134, "Standard rooms", "Twin and double rooms, seminar block"),
    (11, 524, 54, "Forest trails", "Into the indigenous forest"),
]

def estate_map():
    rnd = random.Random(99)
    b = ['<rect width="900" height="600" fill="#DCE3C4"/>']
    # forest
    for i in range(40):
        x = i * 24 + rnd.uniform(-8, 8); y = rnd.uniform(10, 70)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(26,40):.0f}" fill="{rnd.choice(["#3E6243","#335239","#47704A"])}"/>')
    # river
    b.append('<path d="M-10 560 C150 530 300 585 470 555 C640 525 760 575 910 540" stroke="#8DAAA5" stroke-width="28" fill="none"/>')
    b.append('<path d="M-10 560 C150 530 300 585 470 555 C640 525 760 575 910 540" stroke="#B4CBC6" stroke-width="6" fill="none" stroke-dasharray="20 18"/>')
    # road
    b.append('<path d="M20 0 L20 600" stroke="#C9BEA8" stroke-width="26"/>')
    # paths
    P = "#F4EEE2"
    for d in ["M30 380 C120 380 160 350 226 350 C300 350 380 300 452 300", "M452 300 C520 300 580 240 640 220 C690 205 720 190 760 200",
              "M452 300 C480 330 520 350 562 360 C640 380 720 400 800 405", "M452 300 C420 340 380 380 330 410",
              "M452 300 C500 360 560 420 630 470", "M452 300 C460 230 480 170 500 110 L520 60", "M226 350 C230 300 240 240 250 205"]:
        b.append(f'<path d="{d}" stroke="{P}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    # parking
    for i in range(4):
        b.append(f'<rect x="{44 + i*30}" y="410" width="24" height="44" rx="3" fill="#C9BEA8"/>')
    # standard rooms blocks
    b.append('<rect x="150" y="118" width="200" height="30" rx="3" fill="#B8AD9B"/><rect x="150" y="162" width="200" height="30" rx="3" fill="#B8AD9B"/>')
    for i in range(8):
        b.append(f'<line x1="{150 + i*25}" y1="118" x2="{150 + i*25}" y2="148" stroke="#8F8574"/><line x1="{150 + i*25}" y1="162" x2="{150 + i*25}" y2="192" stroke="#8F8574"/>')
    # reception, restaurant
    b.append('<rect x="190" y="330" width="72" height="40" rx="3" fill="#A44E2C"/>')
    b.append('<rect x="258" y="246" width="96" height="44" rx="3" fill="#A44E2C"/>')
    for x, y in [(272, 302), (300, 306), (328, 302)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#8A5A3B"/>')
    # mill bar
    b.append(deca_roof(452, 300, 42, "#7E3B22"))
    # cottages
    for x, y in [(560, 170), (640, 222), (722, 172), (792, 248)]:
        b.append(deca_roof(x, y, 22))
    # conference hall
    b.append(f'<polygon points="{deca_pts(562, 360, 38)}" fill="#B8AD9B"/>' + deca_roof(562, 360, 30, "#8C4024"))
    # pond
    b.append('<path d="M210 430 C220 380 300 370 360 385 C410 398 400 470 350 482 C290 496 205 480 210 430Z" fill="#9FBDB8"/>')
    for _ in range(26):
        b.append(f'<circle cx="{rnd.uniform(215,250):.0f}" cy="{rnd.uniform(400,470):.0f}" r="3" fill="#6E8F4E"/>')
    b.append(deca_roof(310, 432, 20))
    # acacias
    for x, y, r in [(590, 470, 30), (680, 500, 30), (520, 495, 22)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#557A46" opacity=".9"/><circle cx="{x-6}" cy="{y-6}" r="{r*.55:.0f}" fill="#6E8F4E"/>')
    # bandas U
    for x, y in [(760, 372), (758, 408), (772, 442), (828, 442), (842, 408), (840, 372)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#C9A45E"/><circle cx="{x}" cy="{y}" r="4" fill="#A9853F"/>')
    # north
    b.append('<g transform="translate(860 120)"><path d="M0 -22 L8 6 L0 0 L-8 6Z" fill="#1F3A2C"/><text x="0" y="22" text-anchor="middle" font-size="14" font-family="Instrument Sans,system-ui,sans-serif" fill="#1F3A2C" font-weight="600">N</text></g>')
    # pins
    for n, x, y, _, _ in PINS:
        b.append(f'<g class="pin" data-pin="{n}"><circle cx="{x}" cy="{y}" r="15" fill="#FBF8F1" stroke="#1F3A2C" stroke-width="2"/>'
                 f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="14" font-weight="700" font-family="Instrument Sans,system-ui,sans-serif" fill="#1F3A2C">{n}</text></g>')
    return f'<svg viewBox="0 0 900 600" role="img" aria-labelledby="map-t" class="estate"><title id="map-t">Illustrated map of the resort grounds, numbered to match the list</title>{"".join(b)}</svg>'

def write_all(out):
    files = {
        "hero.svg": hero(),
        "banner.svg": banner(),
        "cottage.svg": cottage_scene("dusk", "cottage", label="Illustration of a ten-sided bush-stone cottage at dusk, its full-height windows glowing"),
        "pond-cottage.svg": cottage_scene("day", "pond", pond=True, label="Illustration of the cottage built on a pond, ringed by papyrus"),
        "cabin.svg": cottage_scene("night", "cabin", label="Illustration of a secluded deluxe cabin among trees at night"),
        "villa.svg": cottage_scene("day", "villa", two=True, label="Illustration of a villa of two linked ten-sided cottages"),
        "room.svg": interior("standard"),
        "dorm.svg": interior("dorm"),
        "dining.svg": dining(),
        "millbar.svg": millbar(),
        "bandas.svg": bandas(),
        "garden.svg": garden(),
        "forest.svg": forest_trail(),
        "favicon.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1F3A2C"/>' + deca_roof(32, 32, 22, "#B4552F") + '</svg>\n',
    }
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
