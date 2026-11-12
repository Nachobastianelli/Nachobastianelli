"""Generates the pixel-RPG SVG scenes for the GitHub profile README.
Usage: python generate.py font/PressStart2P.woff2  (Press Start 2P, SIL Open Font License)
Outputs into ./assets/
"""
import base64, os, random, sys

random.seed(7)
FONT = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

BASE_CSS = f"""
@font-face {{ font-family: 'Px'; src: url(data:font/woff2;base64,{FONT}) format('woff2'); }}
text {{ font-family: 'Px', monospace; }}
.crisp {{ shape-rendering: crispEdges; }}
@keyframes blink {{ 0%,49% {{opacity:1}} 50%,100% {{opacity:0}} }}
@keyframes bob {{ 0%,49% {{transform:translateY(0)}} 50%,100% {{transform:translateY(-6px)}} }}
@keyframes twinkle {{ 0%,100% {{opacity:.15}} 50% {{opacity:1}} }}
.blink {{ animation: blink 1s steps(1) infinite; }}
.bob > g {{ animation: bob 1s steps(1) infinite; }}
"""


def svg(w, h, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"<style>{BASE_CSS}{css}</style>{body}</svg>")


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content) // 1024, "KB")


# ---------- sprites ----------
HERO = [
    "......KKKK......",
    "....KKHHHHKK....",
    "...KHHhhHHHHK...",
    "...KHhHHHHHHK...",
    "...KHHSSSSHHK...",
    "...KHSSSSSSHK...",
    "...KSSESSESSK...",
    "...KSSSSSSSSK...",
    "....KSSsSSSK....",
    ".....KKSSKK.....",
    "....KPPLPPPK....",
    "...KPPLLPPPPK...",
    "..KPPPLPPPPPPK..",
    "..KSKPPPPPPKSK..",
    "..KSKpPPPPpKSK..",
    "...K.KppppK.K...",
    ".....KBBBBK.....",
    ".....KBKKBK.....",
    "....KWWK.KWWK...",
    "....KKKK.KKKK...",
]
HERO_PAL = {"K": "#1a1020", "H": "#5a3418", "h": "#9a6030", "S": "#f2c49a", "s": "#c88a60",
            "E": "#1a1020", "P": "#7F3FBF", "p": "#4e2380", "L": "#b98af0", "B": "#2a3a6a", "W": "#eeeeee"}

SLIME = [
    "....KKKK....",
    "..KKllmmKK..",
    ".KmlmmmmmmK.",
    ".KmmmmmmmmK.",
    "KmmKmmmmKmmK",
    "KmmKmmmmKmmK",
    "KmmmmmmmmmmK",
    "KddmmmmmmddK",
    ".KKKKKKKKKK.",
]
SLIME_PAL = {"K": "#1a1020", "m": "#5fd068", "l": "#c8ffcf", "d": "#2f8a3a"}


def sprite(rows, pal, x, y, px, cls=""):
    out = [f'<g class="crisp {cls}" transform="translate({x},{y})"><g>']
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in pal:
                out.append(f'<rect x="{c*px}" y="{r*px}" width="{px}" height="{px}" fill="{pal[ch]}"/>')
    out.append("</g></g>")
    return "".join(out)


def window(x, y, w, h):
    """Classic JRPG menu window: blue gradient + double border."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#win)" stroke="#0a0820" stroke-width="10"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="#f4f0ff" stroke-width="4"/>'
            f'<rect x="{x+7}" y="{y+7}" width="{w-14}" height="{h-14}" rx="7" fill="none" stroke="#7a6cff" stroke-width="2" opacity=".6"/>')


WIN_GRAD = ('<defs><linearGradient id="win" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#3a2a9a"/><stop offset="1" stop-color="#120b3a"/></linearGradient></defs>')


def t(x, y, s, size=14, fill="#ffffff", anchor="start", extra=""):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x+2}" y="{y+2}" font-size="{size}" fill="#0a0820" text-anchor="{anchor}" {extra}>{s}</text>'
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


# ---------- 1. HERO BANNER ----------
def hero():
    W, H = 1000, 340
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#07061f"/><stop offset=".55" stop-color="#2d1557"/>'
         '<stop offset=".85" stop-color="#8a2f7a"/><stop offset="1" stop-color="#e86a8a"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # stars
    for i in range(70):
        x, y, s = random.randint(0, W), random.randint(0, 190), random.choice([2, 2, 3, 4])
        b.append(f'<rect class="crisp" x="{x}" y="{y}" width="{s}" height="{s}" fill="#fff" '
                 f'style="animation:twinkle {random.uniform(1.5,4):.1f}s steps(4) {random.uniform(0,3):.1f}s infinite"/>')
    # pixel moon
    cx, cy, r, p = 935, 62, 4, 8
    for gy in range(-r, r + 1):
        for gx in range(-r, r + 1):
            if gx * gx + gy * gy <= r * r + 2:
                col = "#fff6d8" if (gx - 1) ** 2 + (gy + 1) ** 2 > 4 else "#f0e2b0"
                b.append(f'<rect class="crisp" x="{cx+gx*p}" y="{cy+gy*p}" width="{p}" height="{p}" fill="{col}"/>')
    # mountains (stepped, pixel style)
    def ridge(base, amp, step, color, seed):
        rnd = random.Random(seed)
        pts, hgt = [f"0,{H}"], base
        for x in range(0, W + step, step):
            hgt = max(base - amp, min(base, hgt + rnd.choice([-step, 0, step])))
            pts += [f"{x},{hgt}", f"{x+step},{hgt}"]
        pts.append(f"{W},{H}")
        return f'<polygon class="crisp" points="{" ".join(pts)}" fill="{color}"/>'
    b.append(ridge(250, 90, 20, "#3a1f63", 1))
    b.append(ridge(275, 50, 16, "#24123f", 2))
    # pine trees
    for x in [40, 90, 300, 340, 640, 690, 930, 965]:
        for i, wdt in enumerate([8, 16, 24, 32]):
            b.append(f'<rect class="crisp" x="{x-wdt//2}" y="{230+i*12}" width="{wdt}" height="12" fill="#150a28"/>')
        b.append(f'<rect class="crisp" x="{x-4}" y="278" width="8" height="10" fill="#150a28"/>')
    # ground
    b.append(f'<rect class="crisp" y="288" width="{W}" height="52" fill="#120822"/>')
    b.append(f'<rect class="crisp" y="288" width="{W}" height="6" fill="#4b2a7a"/>')
    for x in range(0, W, 24):
        b.append(f'<rect class="crisp" x="{x+random.randint(0,12)}" y="282" width="4" height="6" fill="#4b2a7a"/>')
    # fireflies
    for i in range(14):
        x = random.randint(120, 900)
        d = random.uniform(4, 8)
        b.append(f'<rect class="crisp" x="{x}" y="285" width="4" height="4" fill="#ffe680" '
                 f'style="animation:fly{i%3} {d:.1f}s linear {random.uniform(0,5):.1f}s infinite;opacity:0"/>')
    # characters
    b.append(sprite(HERO, HERO_PAL, 150, 168, 6, "bob"))
    b.append(sprite(SLIME, SLIME_PAL, 790, 234, 5, "hop"))
    b.append(t(814, 222, "!", 16, "#ffe680", "middle", 'class="blink"'))
    # title
    b.append(t(W // 2, 112, "IGNACIO BASTIANELLI", 34, "#ffffff", "middle"))
    b.append(t(W // 2, 150, "- FULLSTACK DEVELOPER -", 14, "#ffd75e", "middle"))
    b.append(t(W // 2, 178, "ARGENTINA  *  EST. 2022", 10, "#d9c8ff", "middle"))
    b.append(t(W // 2, 322, "> PRESS START <", 14, "#ffffff", "middle", 'class="blink"'))
    css = """
@keyframes hop { 0%,60%,100% {transform:translateY(0)} 70% {transform:translateY(-18px)} 80% {transform:translateY(-24px)} 90% {transform:translateY(-10px)} }
.hop > g { animation: hop 1.6s steps(1) infinite; }
.bob > g { animation: bob 1s steps(1) infinite; }
@keyframes fly0 { 0% {opacity:0;transform:translate(0,0)} 20% {opacity:1} 100% {opacity:0;transform:translate(30px,-140px)} }
@keyframes fly1 { 0% {opacity:0;transform:translate(0,0)} 20% {opacity:1} 100% {opacity:0;transform:translate(-40px,-120px)} }
@keyframes fly2 { 0% {opacity:0;transform:translate(0,0)} 20% {opacity:1} 100% {opacity:0;transform:translate(10px,-180px)} }
"""
    save("hero.svg", svg(W, H, "".join(b), css))


# ---------- 2. STATUS SCREEN ----------
def status():
    W, H = 1000, 400
    b = [WIN_GRAD, window(8, 8, W - 16, H - 16)]
    b.append(t(40, 52, "STATUS", 16, "#ffd75e"))
    b.append(f'<rect class="crisp" x="40" y="64" width="{W-80}" height="3" fill="#7a6cff" opacity=".7"/>')
    # portrait
    b.append('<rect x="40" y="90" width="170" height="200" rx="6" fill="#0a0820" stroke="#f4f0ff" stroke-width="3"/>')
    b.append(sprite(HERO, HERO_PAL, 69, 118, 7, "bob"))
    b.append(t(125, 324, "LV 04", 16, "#ffd75e", "middle"))
    b.append(t(125, 350, "since 2022", 10, "#c9bfff", "middle"))
    # info
    x0 = 250
    rows = [("NAME", "Ignacio"), ("CLASS", "Fullstack Dev"), ("GUILD", "NETIZAR S.A."),
            ("QUEST", "ERP System"), ("HOME", "Argentina")]
    for i, (k, v) in enumerate(rows):
        b.append(t(x0, 110 + i * 30, k, 12, "#9fb4ff"))
        b.append(t(x0 + 100, 110 + i * 30, v, 12))
    # bars
    bars = [("HP", "#4ade80", 1.0, "999/999"), ("MP", "#60a5fa", .85, "COFFEE"), ("EXP", "#ffd75e", .72, "NEXT: ENG")]
    for i, (k, col, pct, lbl) in enumerate(bars):
        y = 275 + i * 34
        b.append(t(x0, y + 12, k, 12, "#9fb4ff"))
        b.append(f'<rect class="crisp" x="{x0+55}" y="{y}" width="260" height="16" fill="#0a0820" stroke="#f4f0ff" stroke-width="2"/>')
        b.append(f'<rect class="crisp fill" x="{x0+58}" y="{y+3}" width="{int(254*pct)}" height="10" fill="{col}" '
                 f'style="animation-delay:{i*.3}s"/>')
        b.append(t(x0 + 325, y + 12, lbl, 9, "#ffffff"))
    # attributes
    x1 = 660
    b.append(t(x1, 100, "ATTRIBUTES", 12, "#ffd75e"))
    attrs = [("STR", "React", 9), ("INT", "Node.js", 9), ("DEX", "TypeScript", 8),
             ("VIT", "MySQL", 8), ("AGI", "Tailwind", 8), ("WIS", "C# / .NET", 7), ("LUK", "Debugging", 10)]
    for i, (k, v, n) in enumerate(attrs):
        y = 130 + i * 34
        b.append(t(x1, y, k, 11, "#9fb4ff"))
        b.append(t(x1 + 50, y, v, 10))
        for j in range(10):
            col = "#c084fc" if j < n else "#2a2160"
            b.append(f'<rect class="crisp pip" x="{x1+50+j*13}" y="{y+6}" width="10" height="8" fill="{col}" '
                     f'style="animation-delay:{(i*10+j)*0.03:.2f}s"/>')
    css = """
@keyframes grow { 0% {transform:scaleX(0)} 100% {transform:scaleX(1)} }
.fill { transform-box: fill-box; transform-origin: left; animation: grow 1.6s steps(16) both; }
@keyframes pop { 0% {opacity:0} 100% {opacity:1} }
.pip { animation: pop .2s steps(1) both; }
.bob > g { animation: bob 1s steps(1) infinite; }
"""
    save("status.svg", svg(W, H, "".join(b), css))


# ---------- 3. QUEST LOG ----------
def quests():
    W, H = 1000, 290
    b = [WIN_GRAD, window(8, 8, W - 16, H - 16)]
    b.append(t(40, 52, "QUEST LOG", 16, "#ffd75e"))
    b.append(f'<rect class="crisp" x="40" y="64" width="{W-80}" height="3" fill="#7a6cff" opacity=".7"/>')
    qs = [("Join a guild as Software Developer", "CLEAR!", "#4ade80"),
          ("Level up English to fluent", "IN PROGRESS", "#ffd75e"),
          ("Associate's in Software Development", "IN PROGRESS", "#ffd75e"),
          ("Information Systems Engineering", "LOCKED", "#f87171")]
    for i, (q, st, col) in enumerate(qs):
        y = 110 + i * 44
        mark = "[X]" if st == "CLEAR!" else "[ ]"
        b.append(t(80, y, mark, 13, col))
        b.append(t(140, y, q, 13))
        b.append(t(W - 50, y, st, 11, col, "end"))
    b.append('<g class="cursor"><polygon class="crisp" points="48,98 62,105 48,112" fill="#ffffff"/></g>')
    css = """
@keyframes cur { 0%,24% {transform:translateY(0)} 25%,49% {transform:translateY(44px)} 50%,74% {transform:translateY(88px)} 75%,100% {transform:translateY(132px)} }
.cursor { animation: cur 4s steps(1) infinite; }
"""
    save("quests.svg", svg(W, H, "".join(b), css))


# ---------- 4. DIALOG ----------
def dialog():
    W, H = 1000, 190
    lines = ["Thanks for stopping by, traveler!", "Shall we build something legendary together?"]
    b = [WIN_GRAD, window(8, 30, W - 16, H - 38)]
    b.append('<rect x="30" y="8" width="170" height="40" rx="6" fill="#120b3a" stroke="#f4f0ff" stroke-width="3"/>')
    b.append(t(115, 35, "IGNACIO", 14, "#ffd75e", "middle"))
    cps = 16  # px per char at size 16
    for i, line in enumerate(lines):
        y = 100 + i * 40
        n = len(line)
        b.append(f'<clipPath id="c{i}"><rect class="type{i}" x="50" y="{y-24}" width="{n*cps+10}" height="34"/></clipPath>')
        b.append(f'<g clip-path="url(#c{i})">{t(50, y, line, 16)}</g>')
    b.append(f'<polygon class="blink crisp" points="{W-60},{H-32} {W-40},{H-32} {W-50},{H-20}" fill="#ffffff"/>')
    n0, n1 = len(lines[0]), len(lines[1])
    css = f"""
.type0, .type1 {{ transform-box: fill-box; transform-origin: left; }}
@keyframes ty0 {{ 0% {{transform:scaleX(0)}} 30%,100% {{transform:scaleX(1)}} }}
@keyframes ty1 {{ 0%,30% {{transform:scaleX(0)}} 70%,100% {{transform:scaleX(1)}} }}
.type0 {{ animation: ty0 7s steps({n0}) infinite; }}
.type1 {{ animation: ty1 7s steps({n1 + n1 * 30 // 40}) infinite; }}
"""
    save("dialog.svg", svg(W, H, "".join(b), css))


# ---------- 5. SECTION TITLES ----------
def title(slug, text):
    W, H = 1000, 70
    b = [WIN_GRAD]
    w = len(text) * 20 + 120
    x = (W - w) // 2
    b.append(window(x, 10, w, 50))
    b.append(t(x + 30, 44, "*", 16, "#ffd75e", extra='class="blink"'))
    b.append(t(W // 2, 44, text, 16, "#ffffff", "middle"))
    b.append(t(x + w - 46, 44, "*", 16, "#ffd75e", extra='class="blink"'))
    save(f"title-{slug}.svg", svg(W, H, "".join(b)))


hero(); status(); quests(); dialog()
for slug, txt in [("inventory", "INVENTORY"), ("equipped", "EQUIPPED AT WORK"),
                  ("log", "ADVENTURE LOG"), ("dungeon", "CONTRIBUTION DUNGEON"),
                  ("party", "JOIN MY PARTY"), ("quests", "CURRENT QUESTS")]:
    title(slug, txt)
