"""Behind the HUD · 009 (EN) — GTA 5 vs GTA 6: launch money (formato bucle).
Solo cifras, gráficos y escenario genérico (palmeras, atardecer) dibujados por el canal; sin logos, personajes ni arte de Rockstar.
Cifras: GTA V $800M día 1 y $1B en 3 días (Take-Two, 2013), 230M+ copias (Take-Two). GTA VI ≈$1.84B y ≈19M copias
a la mañana del lanzamiento, reservas incluidas (estimación de Sensor Tower, 19/11/2026; Take-Two no ha dado cifras)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 009-L"
SUBTITULO = subtitulo_hud
PINK = (1.0, 0.35, 0.65)
TEAL = (0.20, 0.85, 0.80)


def palm(ctx, x, y, s, T, col=(0.06, 0.03, 0.10)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.curve_to(10, -120, 30, -240, 20, -360); stroke(ctx, col, 22)
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.55 + 0.04 * math.sin(T * 1.5 + k)
        ctx.move_to(20, -360)
        ctx.curve_to(20 + 90 * math.cos(a - 0.3), -360 + 90 * math.sin(a - 0.3),
                     20 + 170 * math.cos(a), -360 + 170 * math.sin(a) + 40,
                     20 + 200 * math.cos(a), -360 + 200 * math.sin(a) + 90)
        stroke(ctx, col, 18)
    ctx.restore()


def sunset(ctx, T):
    g = vgrad(ctx, 0, 0, 0, H, [(0, (0.10, 0.04, 0.22)), (0.40, (0.85, 0.25, 0.50)), (0.48, (1.0, 0.60, 0.30)),
                                (0.5, (0.10, 0.04, 0.22)), (1, (0.06, 0.03, 0.10))])
    ctx.rectangle(-600, -600, W + 1200, H + 1200); ctx.set_source(g); ctx.fill()
    circle(ctx, W / 2, 900, 260); fill(ctx, (1.0, 0.82, 0.40), 0.9)
    for k in range(6):
        ctx.rectangle(W / 2 - 300, 860 + k * 26, 600, 8 + k * 2); fill(ctx, (0.85, 0.25, 0.50))
    palm(ctx, 120, 940, 1.1, T); palm(ctx, 960, 960, 1.25, T)
    ctx.rectangle(-500, 930, W + 1000, 1400); fill(ctx, (0.06, 0.03, 0.10))


def bars(ctx, T, items, base=880, top=330, appear=1.0, vmax=2.0):
    """Barras comparativas: items = [(etiqueta, valor_en_miles_de_millones, texto, color, retraso)]."""
    n = len(items)
    bw = 300
    gap = 120
    x0 = W / 2 - (n * bw + (n - 1) * gap) / 2
    for i, (lab, v, txt, col, dl) in enumerate(items):
        p = ease(clamp((appear - dl) / 0.8))
        h = (base - top) * (v / vmax) * p
        x = x0 + i * (bw + gap)
        rrect(ctx, x, base - h, bw, h, 18); fill(ctx, col, 0.9)
        glow(ctx, x + bw / 2, base - h, 200, col, 0.15 * p)
        if p > 0.6:
            text(ctx, txt, x + bw / 2, base - h - 50, 64, WHITE, font="Anton")
        pill(ctx, lab, x + bw / 2, base + 60, 1.0, size=40, rgb=col)


def money_rain(ctx, T, n=18, seed=2, a=1.0):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x = rng.uniform(60, 1020); ph = rng.uniform(0, 1200)
        y = -120 + ((T * 380 * rng.uniform(0.7, 1.3) + ph) % 1150)
        icon(ctx, "💵", x, y, 90, a, 0.6 * math.sin(T * 2 + k))


def calendar(ctx, x, y, s, top, big, small, col=RED, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * appear, s * appear)
    rrect(ctx, -160, -170, 320, 340, 24); fill(ctx, WHITE)
    rrect(ctx, -160, -170, 320, 90, 24); fill(ctx, col)
    ctx.rectangle(-160, -110, 320, 30); fill(ctx, col)
    text(ctx, top, 0, -125, 46, WHITE, font="Anton", shadow=False)
    text(ctx, big, 0, 20, 150, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    text(ctx, small, 0, 130, 36, (0.4, 0.4, 0.45), font="Anton", shadow=False)
    ctx.restore()


def price_tag(ctx, x, y, s, price, sub, col, rot=0.0, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * appear, s * appear)
    ctx.move_to(-170, -90); ctx.line_to(130, -90); ctx.line_to(200, 0); ctx.line_to(130, 90); ctx.line_to(-170, 90)
    ctx.close_path(); fill_keep(ctx, col); stroke(ctx, WHITE, 6)
    circle(ctx, 120, 0, 16); fill(ctx, (0.1, 0.05, 0.15))
    text(ctx, price, -30, -10, 110, WHITE, font="Anton")
    text(ctx, sub, -30, 60, 30, WHITE, font="Anton", shadow=False)
    ctx.restore()


HERO_BARS = [("GTA V · DAY 1", 0.8, "$800M", TEAL, 0.0), ("GTA VI · LAUNCH", 1.84, "$1.84B*", PINK, 0.25)]


def hero(ctx, T, zoom, grow=1.5):
    """Gancho (inicio y final del bucle): GTA V en 3 días vs GTA VI antes de salir."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    rays(ctx, W / 2, 600, T, PINK, 0.05)
    bars(ctx, T, HERO_BARS, base=860, top=470, appear=grow)
    hud(ctx, T, TAG, PINK)
    pill(ctx, "*ESTIMATE, PRE-ORDERS INCLUDED", W / 2, 1420, 1.0, size=40, rgb=YELLOW)


# 0.03 "GTA 6 reportedly made more money before launch"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.08)]), grow=1.5)


# 3.00 "than GTA 5 made in its first three days."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12), floor=False)
    for i in range(3):
        calendar(ctx, 220 + i * 320, 540, 0.75, "SEPT 2013", str(i + 1), "DAY · GTA V", TEAL, pop(lt, i * 0.25))
    big_number(ctx, "$1B", W / 2, 820, 150, TEAL, pop(lt, 1.0))
    hud(ctx, T, TAG, TEAL)


# 5.87 "And it's real. In 2013,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 420, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.6, 2003, 2013, 0.4) if lt > 0.6 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.6))


# 7.57 "GTA 5 made eight hundred million dollars in a single day."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12))
    money_rain(ctx, T, 12, 3, 0.7)
    v = int(counter(lt, 0, 800000000, 1.6))
    big_number(ctx, f"${v:,}", W / 2, 560, 140, TEAL, pop(lt, 0.0))
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "GTA V · DAY ONE · 2013", W / 2, 1400, pop(lt, 0.2), size=50, rgb=TEAL)


# 10.73 "Three days later, it passed one billion."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12), floor=False)
    rays(ctx, W / 2, 560, T, TEAL, 0.06)
    calendar(ctx, W / 2, 500, 0.85, "SEPT 2013", "3", "DAY · GTA V", TEAL, pop(lt, 0.0))
    big_number(ctx, "$1,000,000,000", W / 2, 820, 120, YELLOW, pop(lt, 0.8))
    hud(ctx, T, TAG, YELLOW)


# 12.77 "No movie or game had ever reached a billion that fast."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02))
    icon(ctx, "🎬", 250, 600, 200, pop(lt, 0.0))
    icon(ctx, "🎮", 830, 600, 200, pop(lt, 0.2))
    icon(ctx, "🏆", W / 2, 470, 300, pop(lt, 0.6))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "FASTEST TO $1B", W / 2, 1400, clamp((lt - 1.0) / 0.25), YELLOW, size=66, rot=-0.06)


# 15.51 "Since then, GTA 5 has sold more than two hundred thirty million copies."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.08, 0.14))
    for c in range(7):
        hgt = int(clamp((lt - c * 0.12) / 1.2) * 9)
        for r in range(hgt):
            rrect(ctx, 150 + c * 120, 870 - r * 48, 100, 38, 6); fill(ctx, TEAL if (r + c) % 2 else CYAN, 0.9)
    v = int(counter(lt, 0, 230000000, 1.8))
    big_number(ctx, f"{v:,}+", W / 2, 390, 120, WHITE, pop(lt, 0.0))
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "GTA V COPIES SOLD", W / 2, 1400, pop(lt, 0.3), size=54, rgb=TEAL)


# 19.45 "But here's the twist."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 560, T, PINK, 0.05)
    character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
    icon(ctx, "⚠️", 820, 330, 170, pop(lt, 0.1))
    hud(ctx, T, TAG, PINK)


# 20.36 "GTA 6 launched on November 19, 2026."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    sunset(ctx, T)
    calendar(ctx, W / 2, 570, 0.95, "NOV 2026", "19", "GTA VI LAUNCH", PINK, pop(lt, 0.0))
    hud(ctx, T, TAG, PINK)


# 23.53 "By launch morning, Sensor Tower estimated about nineteen million copies sold,"
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    icon(ctx, "📊", W / 2, 410, 180, pop(lt, 0.0))
    v = int(counter(lt - 0.8, 0, 19000000, 1.6)) if lt > 0.8 else 0
    big_number(ctx, f"~{v:,}", W / 2, 720, 150, PINK, pop(lt, 0.8))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "COPIES · SENSOR TOWER ESTIMATE", W / 2, 1400, pop(lt, 0.3), size=42, rgb=PINK)


# 27.26 "worth around one point eight four billion dollars."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    money_rain(ctx, T, 20, 5, 0.85)
    big_number(ctx, "~$1.84B", W / 2, 580, 260, YELLOW, pop(lt, 0.2))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "BY LAUNCH MORNING · ESTIMATE", W / 2, 1400, pop(lt, 0.4), size=44, rgb=YELLOW)


# 29.68 "In other words, GTA 6 more than doubled GTA 5's record day"  (2.º gancho)
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.06)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 600, T, PINK, 0.08)
    bars(ctx, T, [("GTA V · DAY 1", 0.816, "$816M", TEAL, 0.0), ("GTA VI · LAUNCH", 1.84, "$1.84B", PINK, 0.3)],
         base=800, top=330, appear=lt / 0.8 + 0.3)
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "MORE THAN 2X", W / 2, 1420, clamp((lt - 1.4) / 0.25), YELLOW, size=70, rot=-0.06)


# 32.50 "before most players even pressed start."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    gamepad(ctx, W / 2, 560, 1.25, T, col=(0.20, 0.12, 0.26), accent=PINK)
    ctx.save(); ctx.translate(W / 2, 560); ctx.scale(1.25, 1.25)
    rrect(ctx, 30 - 10, 50, 80, 38, 12); stroke(ctx, YELLOW, 5, 0.6 + 0.4 * math.sin(T * 6))
    ctx.restore()
    text(ctx, "START", W / 2 + 85, 690, 34, YELLOW, font="Anton")
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "NOT EVEN PLAYED YET", W / 2, 1400, clamp((lt - 0.6) / 0.25), PINK, size=60, rot=-0.06)


# 35.22 "Part of that is the price. Eighty dollars, instead of sixty."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.06, 0.12), floor=False)
    price_tag(ctx, 330, 520, 1.0, "$60", "GTA V · 2013", TEAL, -0.08, pop(lt, 1.8))
    price_tag(ctx, 720, 750, 1.1, "$80", "GTA VI · 2026", PINK, 0.06, pop(lt, 1.1))
    if lt < 1.1:
        icon(ctx, "🏷️", W / 2, 560, 300, pop(lt, 0.0))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "STANDARD EDITION PRICE", W / 2, 1400, pop(lt, 0.2), size=48, rgb=PINK)


# 37.90 "Rockstar hasn't confirmed any numbers yet."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.12)]), W / 2, 960)
    bg_blueprint(ctx, T)
    rrect(ctx, W / 2 - 260, 340, 520, 540, 20); fill(ctx, (0.95, 0.93, 0.86))
    text(ctx, "OFFICIAL SALES", W / 2, 410, 50, (0.15, 0.15, 0.2), font="Anton", shadow=False)
    for k in range(4):
        text(ctx, "$ ???", W / 2, 510 + k * 90, 60, (0.5, 0.5, 0.55), font="Anton", shadow=False)
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "NOT CONFIRMED YET", W / 2, 620, clamp((lt - 0.4) / 0.25), ORANGE, size=66)


# 39.70 "But if that estimate holds, then" -> vuelve a e1 (bucle)
def e16(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.08), (dur, 1.0)]), grow=1.5)




# ---------- formato lista (rehecho 25/11/2026) ----------
def _punch(fn, z=1.22):
    def f(ctx, lt, dur, T):
        ctx.translate(W / 2, 960); ctx.scale(z, z); ctx.translate(-W / 2, -960)
        fn(ctx, lt + 1.4, dur, T)
    return f


def l_intro(ctx, lt, dur, T):
    """Here are three GTA 6 facts you didn't know."""
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    sunset(ctx, T)
    for i in range(3):
        big_number(ctx, str(i + 1), 250 + i * 290, 620, 230, (PINK, YELLOW, TEAL)[i], pop(lt, 0.15 + i * 0.25))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "GTA 6 FACTS YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=50, rgb=PINK)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 420, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 680, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


def l_lucia(ctx, lt, dur, T):
    """Lucia is the first female lead in a modern GTA."""
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.12))
    sunset(ctx, T)
    palm(ctx, 170, 900, 1.0, T); palm(ctx, 910, 900, 0.9, T)
    pill(ctx, "LUCIA", W / 2, 470, pop(lt, 0.0), size=110, rgb=PINK)
    icon(ctx, "⭐", W / 2, 700, 170, pop(lt, 0.3))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "FIRST FEMALE LEAD · MODERN GTA", W / 2, 1400, pop(lt, 0.4), size=46, rgb=YELLOW)


def l_1997(ctx, lt, dur, T):
    """The original 1997 game only had female avatars with no story."""
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.06, 0.12))
    big_number(ctx, "1997", W / 2 - 80, 470, 190, YELLOW, pop(lt, 0.0))
    for i in range(4):
        x = 230 + i * 210
        rrect(ctx, x - 80, 600, 160, 200, 14); fill(ctx, (0.15, 0.16, 0.26), pop(lt, 0.3 + i * 0.12))
        icon(ctx, "👤", x, 690, 110, pop(lt, 0.3 + i * 0.12))
    stamp(ctx, "NO STORY", W / 2, 880, clamp((lt - 1.4) / 0.25), RED, size=70, rot=-0.08)
    hud(ctx, T, TAG, YELLOW)


def l_years(ctx, lt, dur, T):
    """In other words, it took GTA almost thirty years..."""
    camera(ctx, keyframes(lt, [(0, 1.4), (0.3, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 560, T, PINK, 0.10)
    big_number(ctx, str(int(counter(lt, 1997, 2026, 1.6))), W / 2, 620, 230, PINK, pop(lt, 0.0))
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "~30 YEARS", W / 2, 860, clamp((lt - 1.7) / 0.25), YELLOW, size=80, rot=-0.06)


def l_work(ctx, lt, dur, T):
    """Experts estimated one and a half million people would skip work."""
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12))
    v = int(counter(lt, 0, 1500000, 1.4))
    big_number(ctx, f"{v:,}", W / 2 - 60, 520, 140, TEAL, pop(lt, 0.0))
    icon(ctx, "🏢", 330, 760, 190, pop(lt, 0.3))
    icon(ctx, "❌", 330, 760, 120, pop(lt, 0.9))
    icon(ctx, "🎮", 750, 760, 190, pop(lt, 0.6))
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "SKIPPING WORK FOR GTA 6 (EST.)", W / 2, 1400, pop(lt, 0.4), size=46, rgb=TEAL)


ESCENAS = [(0.0, e1), (1.45, _punch(e1)), (5.17, l_intro), (7.78, l_num(1, PINK)), (8.27, e9), (11.60, e11), (13.70, e4), (16.47, l_num(2, YELLOW)), (17.07, l_lucia), (19.94, l_1997), (23.93, l_years), (28.05, l_num(3, TEAL)), (28.72, l_work), (33.19, e16), (31.00, _punch(l_work)), (26.0, _punch(l_years))]
HOOK = 'GTA 6 BEAT GTA 5 BEFORE LAUNCH'
LISTA = [(7.78, '1/3'), (16.47, '2/3'), (28.05, '3/3')]
COLA = 0.02

SFX = [(7.80, "ding"), (16.49, "ding"), (24.0, "pop"), (28.07, "ding")]


def MINIATURA(ctx):
    sunset(ctx, 1.0)
    ctx.save(); ctx.translate(0, 300)
    bars(ctx, 1.0, [("GTA V", 0.816, "$816M", TEAL, 0.0), ("GTA VI", 1.84, "$1.84B", PINK, 0.0)],
         base=1250, top=480, appear=2.0)
    ctx.restore()
    thumb_circle(ctx, W / 2 + 210, 900, 230, 170)
    thumb_arrow(ctx, 160, 1850, W / 2 - 60, 1300)
    thumb_vignette(ctx)
    thumb_text(ctx, [("3 GTA 6 FACTS", WHITE), "YOU MISSED"], y=330)
