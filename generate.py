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
    rows = [("NAME", "Ignacio"), ("CLASS", "Fullstack Dev"), ("TITLE", "Univ. Technician"),
            ("GUILD", "NETIZAR S.A."), ("QUEST", "ERP System"), ("LANG", "ES / EN B2"), ("HOME", "Argentina")]
    for i, (k, v) in enumerate(rows):
        b.append(t(x0, 104 + i * 24, k, 12, "#9fb4ff"))
        b.append(t(x0 + 100, 104 + i * 24, v, 12, "#ffd75e" if k == "TITLE" else "#ffffff"))
    # bars
    bars = [("HP", "#4ade80", 1.0, "999/999"), ("MP", "#60a5fa", .85, "COFFEE"), ("EXP", "#ffd75e", .72, "LV UP SOON")]
    for i, (k, col, pct, lbl) in enumerate(bars):
        y = 280 + i * 32
        b.append(t(x0, y + 12, k, 12, "#9fb4ff"))
        b.append(f'<rect class="crisp" x="{x0+55}" y="{y}" width="260" height="16" fill="#0a0820" stroke="#f4f0ff" stroke-width="2"/>')
        b.append(f'<rect class="crisp fill" x="{x0+58}" y="{y+3}" width="{int(254*pct)}" height="10" fill="{col}" '
                 f'style="animation-delay:{i*.3}s"/>')
        b.append(t(x0 + 325, y + 12, lbl, 9, "#ffffff"))
    # attributes
    x1 = 660
    b.append(t(x1, 100, "ATTRIBUTES", 12, "#ffd75e"))
    attrs = [("STR", "React", 9), ("INT", "Node.js", 9), ("DEX", "TypeScript", 8),
             ("VIT", "MySQL", 8), ("AGI", "Tailwind", 8), ("WIS", "C# / .NET", 7), ("MAG", "Claude AI", 10), ("LUK", "Debugging", 10)]
    for i, (k, v, n) in enumerate(attrs):
        y = 124 + i * 31
        b.append(t(x1, y, k, 11, "#ffd75e" if k == "MAG" else "#9fb4ff"))
        b.append(t(x1 + 50, y, v, 10, "#ffb070" if k == "MAG" else "#ffffff"))
        for j in range(10):
            col = ("#ff9a3c" if k == "MAG" else "#c084fc") if j < n else "#2a2160"
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
    W, H = 1000, 334
    b = [WIN_GRAD, window(8, 8, W - 16, H - 16)]
    b.append(t(40, 52, "QUEST LOG", 16, "#ffd75e"))
    b.append(f'<rect class="crisp" x="40" y="64" width="{W-80}" height="3" fill="#7a6cff" opacity=".7"/>')
    qs = [("Graduate: Univ. Technician in Programming", "CLEAR!", "#4ade80"),
          ("Reach English level B2", "CLEAR!", "#4ade80"),
          ("Join a guild as Software Developer", "CLEAR!", "#4ade80"),
          ("Build & maintain the NETIZAR ERP", "ACTIVE", "#ffd75e"),
          ("Keep leveling up as a Fullstack Dev", "ENDLESS", "#c084fc")]
    for i, (q, st, col) in enumerate(qs):
        y = 110 + i * 44
        mark = "[X]" if st == "CLEAR!" else "[ ]"
        b.append(t(80, y, mark, 13, col))
        b.append(t(140, y, q, 13))
        b.append(t(W - 50, y, st, 11, col, "end", 'class="blink"' if st == "ACTIVE" else ""))
    b.append('<g class="cursor"><polygon class="crisp" points="48,98 62,105 48,112" fill="#ffffff"/></g>')
    css = """
@keyframes cur { 0%,19% {transform:translateY(0)} 20%,39% {transform:translateY(44px)} 40%,59% {transform:translateY(88px)} 60%,79% {transform:translateY(132px)} 80%,100% {transform:translateY(176px)} }
.cursor { animation: cur 5s steps(1) infinite; }
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


# ---------- 6. ACHIEVEMENTS ----------
CAP = [".....KK.....", "...KKCCKK...", ".KKCCCCCCKK.", "KCCCCLLCCCCK", ".KKCCCCCCKKY",
       "...KKKKKK.KY", "...KCCCCK.KY", "...KCCCCK.YY", "...KKKKKK..."]
ORB = ["...KKKK...", ".KKMMWWKK.", ".KMMMMWMK.", "KMMMMMMMMK", "KMmMMMMMMK",
       "KmmMMMMMmK", ".KmmmmmmK.", "..KKKKKK..", ".KYYYYYYK.", "KKKKKKKKKK"]
BUBBLE = [".KKKKKKKK.", "KWWWWWWWWK", "KWWWWWWWWK", "KWWWWWWWWK", "KWWWWWWWWK",
          ".KKWKKKKK.", "..KWK.....", "..KK......"]
CASE = ["...KKKK...", "...K..K...", "KKKKKKKKKK", "KBBBBBBBBK", "KBBBBBBBBK",
        "KbbbYYbbbK", "KBBBBBBBBK", "KKKKKKKKKK"]
TROPHY = ["KKKKKKKKKK", "KYYYYYYWYK", "KYYYYYYWYK", ".KYYYYWYK.", "..KYYYYK..",
          "...KYYK...", "....KK....", "...KOOK...", "..KOOOOK..", "..KKKKKK.."]
ICON_PAL = {"K": "#0a0820", "C": "#3a3a5a", "L": "#7a7aa0", "Y": "#ffd75e", "W": "#ffffff",
            "B": "#b0743a", "b": "#7a4a20", "O": "#c08a20", "M": "#ff9a3c", "m": "#c2410c"}


def achievements():
    W, H = 1000, 330
    b = [WIN_GRAD, window(8, 8, W - 16, H - 16)]
    b.append(t(40, 52, "ACHIEVEMENTS UNLOCKED  5/5", 16, "#ffd75e"))
    b.append(f'<rect class="crisp" x="40" y="64" width="{W-80}" height="3" fill="#7a6cff" opacity=".7"/>')
    cards = [(CAP, "GRADUATED!", "Univ. Technician", "in Programming"),
             (BUBBLE, "ENGLISH B2", "Language skill", "unlocked"),
             (CASE, "PRO DEV", "Software Dev", "@ NETIZAR S.A."),
             (ORB, "CLAUDE EXPERT", "AI-powered", "developer"),
             (TROPHY, "SINCE 2022", "Writing code", "and counting")]
    for i, (icon, ttl, s1, s2) in enumerate(cards):
        x, y, w, h = 32 + i * 188, 86, 176, 210
        cx = x + w // 2
        b.append(f'<g class="card" style="animation-delay:{i*0.35:.2f}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#0a0820" fill-opacity=".55" stroke="#ffd75e" stroke-width="3"/>')
        b.append(f'<circle cx="{cx}" cy="{y+62}" r="44" fill="#ffd75e" opacity=".12" class="glow" style="animation-delay:{i*0.4:.1f}s"/>')
        b.append(sprite(icon, ICON_PAL, cx - len(icon[0]) * 3, y + 62 - len(icon) * 3, 6))
        if icon is BUBBLE:
            b.append(f'<text x="{cx}" y="{y+55}" font-size="14" fill="#0a0820" text-anchor="middle">B2</text>')
        b.append(t(cx, y + 138, ttl, 12, "#ff9a3c" if icon is ORB else "#ffd75e", "middle"))
        b.append(t(cx, y + 164, s1, 10, "#ffffff", "middle"))
        b.append(t(cx, y + 182, s2, 10, "#c9bfff", "middle"))
        for sx, sy, d in [(x + 22, y + 24, 0), (x + w - 28, y + 40, .5), (x + w - 36, y + 100, 1)]:
            b.append(f'<g class="spark" style="animation-delay:{d+i*0.2:.1f}s"><rect class="crisp" x="{sx}" y="{sy-6}" width="3" height="15" fill="#fff"/>'
                     f'<rect class="crisp" x="{sx-6}" y="{sy}" width="15" height="3" fill="#fff"/></g>')
        b.append("</g>")
    css = """
@keyframes cardin { 0% {opacity:0} 100% {opacity:1} }
.card { animation: cardin .3s steps(3) both; }
@keyframes spark { 0%,70%,100% {opacity:0} 80%,90% {opacity:1} }
.spark { animation: spark 2s steps(1) infinite; }
@keyframes glow { 0%,100% {opacity:.08} 50% {opacity:.3} }
.glow { animation: glow 2s steps(4) infinite; }
"""
    save("achievements.svg", svg(W, H, "".join(b), css))


# ---------- 7. BOSS BATTLE ----------
BUG = [
    "..K..........K..", "...K........K...", "....KKKKKKKK....", "...KRRRRRRRRK...",
    "..KRRYYRRYYRRK..", "..KRRYKRRYKRRK..", ".KRRRRRRRRRRRRK.", ".KRrRRWRRWRRrRK.",
    "KLKRrRRRRRRrRKLK", "K.KRRrrrrrrRRK.K", "KLKRRRRRRRRRRKLK", "...KRrRRRRrRK...",
    "..KLK.KKKK.KLK..", ".KK..........KK.",
]
BUG_PAL = {"K": "#1a1020", "R": "#e0485e", "r": "#8a2030", "Y": "#ffe680", "W": "#ffffff", "L": "#3a1020"}


def battle():
    W, H = 1000, 420
    b = ['<defs><linearGradient id="arena" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#1a0b2e"/><stop offset=".6" stop-color="#3b1450"/><stop offset="1" stop-color="#5a1a4a"/></linearGradient>'
         '<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2a9a"/><stop offset="1" stop-color="#120b3a"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="12" fill="url(#arena)"/>']
    # floor tiles
    for r in range(5):
        y = 220 + r * 14
        for c in range(0, W, 40):
            col = "#2a1040" if (c // 40 + r) % 2 else "#341650"
            b.append(f'<rect class="crisp" x="{c}" y="{y}" width="40" height="14" fill="{col}"/>')
    # background code-rain columns
    for i in range(18):
        x = 30 + i * 55
        b.append(f'<text x="{x}" y="0" font-size="10" fill="#7a3fbf" opacity=".35" class="rain" '
                 f'style="animation-delay:-{random.uniform(0,6):.1f}s;animation-duration:{random.uniform(5,9):.1f}s">'
                 f'{random.choice(["0", "1", "{", "}", ";", "=>", "()"])}</text>')
    # nameplates
    def plate(x, y, name, hp_cls):
        return (f'<rect x="{x}" y="{y}" width="300" height="56" rx="6" fill="#0a0820" fill-opacity=".8" stroke="#f4f0ff" stroke-width="3"/>'
                + t(x + 14, y + 22, name, 12, "#ffd75e")
                + t(x + 14, y + 44, "HP", 10, "#9fb4ff")
                + f'<rect class="crisp" x="{x+50}" y="{y+34}" width="234" height="12" fill="#2a2160"/>'
                + f'<rect class="crisp {hp_cls}" x="{x+50}" y="{y+34}" width="234" height="12" fill="#4ade80"/>')
    b.append(plate(30, 24, "IGNACIO  LV 04", "hphero"))
    b.append(plate(W - 330, 24, "PROD BUG  LV 99", "hpboss"))
    # fighters
    b.append(f'<g class="dash">{sprite(HERO, HERO_PAL, 170, 110, 6, "bob")}</g>')
    b.append(f'<g class="boss"><g class="shake">{sprite(BUG, BUG_PAL, 690, 100, 9, "bob")}</g></g>')
    # slash + flash + damage
    b.append('<g class="slash">'
             + "".join(f'<rect class="crisp" x="{700+k*14}" y="{210-k*14}" width="16" height="16" fill="#ffffff"/>' for k in range(8))
             + "".join(f'<rect class="crisp" x="{700+k*14}" y="{230-k*14}" width="10" height="10" fill="#c084fc"/>' for k in range(8))
             + '</g>')
    b.append(f'<rect width="{W}" height="{H}" rx="12" fill="#ffffff" class="flash"/>')
    b.append(f'<g class="dmg">{t(760, 190, "-9999", 28, "#ffd75e", "middle")}</g>')
    b.append(f'<g class="victory">{t(W//2, 170, "VICTORY!", 40, "#ffd75e", "middle")}{t(W//2, 205, "+500 EXP  *  +1 CLEAN DEPLOY", 12, "#ffffff", "middle")}</g>')
    # battle text window
    b.append('<rect x="20" y="304" width="960" height="100" rx="10" fill="url(#win)" stroke="#0a0820" stroke-width="8"/>'
             '<rect x="20" y="304" width="960" height="100" rx="10" fill="none" stroke="#f4f0ff" stroke-width="4"/>')
    msgs = ["A wild PROD BUG appeared!", "Ignacio summoned CLAUDE CODE!", "CRITICAL HIT! The bug was squashed!"]
    for i, m in enumerate(msgs):
        b.append(f'<g class="msg msg{i}">{t(50, 362, m, 16)}</g>')
    b.append('<polygon class="blink crisp" points="940,380 960,380 950,392" fill="#ffffff"/>')
    css = """
.dash, .boss, .shake, .slash, .flash, .dmg, .victory, .msg, .hpboss { animation-duration: 6s; animation-iteration-count: infinite; animation-timing-function: steps(1); }
@keyframes dash { 0%,30% {transform:translateX(0)} 33% {transform:translateX(200px)} 36%,44% {transform:translateX(420px)} 47% {transform:translateX(200px)} 50%,100% {transform:translateX(0)} }
.dash { animation-name: dash; }
@keyframes slash { 0%,37% {opacity:0} 38%,44% {opacity:1} 45%,100% {opacity:0} }
.slash { animation-name: slash; }
@keyframes flash { 0%,38% {opacity:0} 39% {opacity:.7} 41% {opacity:0} 42% {opacity:.4} 43%,100% {opacity:0} }
.flash { animation-name: flash; opacity:0; }
@keyframes shake { 0%,39% {transform:translateX(0)} 40% {transform:translateX(-10px)} 42% {transform:translateX(10px)} 44% {transform:translateX(-8px)} 46% {transform:translateX(8px)} 48%,100% {transform:translateX(0)} }
.shake { animation-name: shake; }
@keyframes boss { 0%,58% {opacity:1} 60% {opacity:0} 62% {opacity:1} 64% {opacity:0} 66% {opacity:.5} 68%,96% {opacity:0} 98%,100% {opacity:1} }
.boss { animation-name: boss; }
@keyframes dmg { 0%,39% {opacity:0;transform:translateY(0)} 40% {opacity:1;transform:translateY(0)} 46% {opacity:1;transform:translateY(-30px)} 56%,100% {opacity:0;transform:translateY(-40px)} }
.dmg { animation-name: dmg; animation-timing-function: steps(4); }
@keyframes hpboss { 0%,40% {transform:scaleX(1)} 52%,100% {transform:scaleX(0)} }
.hpboss { transform-box: fill-box; transform-origin: left; animation-name: hpboss; animation-timing-function: steps(12); }
@keyframes victory { 0%,69% {opacity:0} 70%,96% {opacity:1} 97%,100% {opacity:0} }
.victory { animation-name: victory; }
@keyframes msg0 { 0%,32% {opacity:1} 33%,100% {opacity:0} }
@keyframes msg1 { 0%,32% {opacity:0} 33%,54% {opacity:1} 55%,100% {opacity:0} }
@keyframes msg2 { 0%,54% {opacity:0} 55%,100% {opacity:1} }
.msg0 { animation-name: msg0; } .msg1 { animation-name: msg1; } .msg2 { animation-name: msg2; }
@keyframes rain { 0% {transform:translateY(-20px)} 100% {transform:translateY(320px)} }
.rain { animation: rain 7s linear infinite; }
.bob > g { animation: bob 1s steps(1) infinite; }
"""
    save("battle.svg", svg(W, H, "".join(b), css))


# ---------- 8. SKILL TREE ----------
def skilltree():
    W = 1000
    work = {"React", "TypeScript", "JavaScript", "Node.js", "Express", "MySQL"}
    tree = [("FRONTEND", "#c084fc", ["React", "TypeScript", "JavaScript", "Tailwind CSS", "HTML + CSS"]),
            ("BACKEND", "#60a5fa", ["Node.js", "Express", "C# / .NET"]),
            ("DATA VAULT", "#4ade80", ["MySQL", "MongoDB"]),
            ("AI MAGIC", "#ff9a3c", ["Claude", "Claude Code", "Prompt Engineering", "AI-assisted Dev"]),
            ("TOOLS", "#9fb4ff", ["Git", "GitHub", "Figma", "VS Code"])]
    H = 100 + len(tree) * 54 + 50
    b = [WIN_GRAD, window(8, 8, W - 16, H - 16)]
    b.append(t(40, 52, "SKILL TREE", 16, "#ffd75e"))
    b.append(f'<rect class="crisp" x="40" y="64" width="{W-80}" height="3" fill="#7a6cff" opacity=".7"/>')
    k = 0
    for r, (cat, col, chips) in enumerate(tree):
        y = 96 + r * 54
        b.append(t(40, y + 22, cat, 11, col))
        b.append(f'<rect class="crisp" x="40" y="{y+30}" width="{len(cat)*11}" height="2" fill="{col}" opacity=".6"/>')
        x = 200
        for c in chips:
            star = c in work
            label = ("* " if star else "") + c
            w = len(label) * 11 + 28
            glow = ' class="aiglow"' if cat == "AI MAGIC" else ""
            b.append(f'<g class="chip" style="animation-delay:{k*0.06:.2f}s">')
            b.append(f'<rect{glow} x="{x}" y="{y}" width="{w}" height="34" rx="4" fill="#0a0820" fill-opacity=".6" '
                     f'stroke="{"#ffd75e" if star else col}" stroke-width="3"/>')
            b.append(t(x + 14, y + 23, label, 11, "#ffd75e" if star else "#ffffff"))
            b.append("</g>")
            x += w + 12
            k += 1
    b.append(t(W - 40, H - 36, "* = equipped at work", 10, "#ffd75e", "end"))
    css = """
@keyframes chipin { 0% {opacity:0} 100% {opacity:1} }
.chip { animation: chipin .2s steps(1) both; }
@keyframes aiglow { 0%,100% {stroke:#ff9a3c} 50% {stroke:#ffe0b0} }
.aiglow { animation: aiglow 1.4s steps(4) infinite; }
"""
    save("skilltree.svg", svg(W, H, "".join(b), css))


# ---------- 9. PIXEL LINK BUTTONS ----------
def button(slug, label, col):
    W, H = 240, 64
    b = [f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="#120b3a" stroke="#0a0820" stroke-width="8"/>',
         f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{col}" stroke-width="4"/>',
         f'<rect class="crisp" x="10" y="{H-14}" width="{W-20}" height="4" fill="{col}" opacity=".35"/>',
         t(30, 40, ">", 14, col, extra='class="blink"'),
         t(W // 2 + 10, 40, label, 14, "#ffffff", "middle")]
    save(f"btn-{slug}.svg", svg(W, H, "".join(b)))


hero(); status(); quests(); dialog(); achievements(); battle(); skilltree()
button("portfolio", "PORTFOLIO", "#ffd75e"); button("linkedin", "LINKEDIN", "#60a5fa")
button("email", "EMAIL", "#f87171")
for slug, txt in [("achievements", "TROPHY ROOM"), ("battle", "BOSS BATTLE"),
                  ("party", "JOIN MY PARTY"), ("quests", "STORY SO FAR")]:
    title(slug, txt)
