"""Behind the HUD · v02 (EN) — Atari buried E.T. in the New Mexico desert (formato bucle).
No se dibuja al personaje de la película: solo un cartucho genérico con el título."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 002"


def mound(ctx, x, y, w, col=SAND):
    ctx.move_to(x - w, y + 200)
    ctx.curve_to(x - w * 0.6, y - 30, x + w * 0.6, y - 30, x + w, y + 200)
    ctx.close_path()
    fill(ctx, col)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): cartucho medio enterrado en el desierto, de noche, brillando."""
    camera(ctx, zoom, W / 2, 960)
    bg_desert(ctx, T, night=1.0)
    glow(ctx, W / 2, 700, 520, ORANGE, 0.35 + 0.08 * math.sin(T * 3))
    cartridge(ctx, W / 2, 640, 1.05, -0.18, dirt=0.4)
    mound(ctx, W / 2, 800, 520, (0.42, 0.30, 0.22))
    rng = np.random.default_rng(9)
    for k in range(18):  # arena que cae
        y = 400 + ((T * 160 + k * 47) % 420)
        circle(ctx, W / 2 + rng.uniform(-260, 260), y, 5)
        fill(ctx, SAND, 0.6)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "ATARI · 1983", W / 2, 1420, 1.0, size=54, rgb=ORANGE)


# 0.00 "Atari buried E.T. in the desert, and it's still down there."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 3.41 "And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.45), (0.3, 1.2), (dur, 1.25)]), W / 2, 900)
    bg_desert(ctx, T, night=1.0)
    cartridge(ctx, W / 2, 640, 1.05, -0.18, dirt=0.4)
    mound(ctx, W / 2, 800, 520, (0.42, 0.30, 0.22))
    hud(ctx, T, TAG, ORANGE)
    badge(ctx, "REAL", W / 2, 1400, pop(lt, 0.05), size=80)


# 4.49 "E.T. was the video game of Spielberg's hit movie."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.05, 0.16))
    glow(ctx, 380, 600, 380, ORANGE, 0.25)
    cartridge(ctx, 380, 600, 0.95, -0.08 + 0.04 * math.sin(T * 2))
    icon(ctx, "🎞️", 790, 500, 260, pop(lt, 0.4), T * 0.8)
    icon(ctx, "🍿", 800, 760, 170, pop(lt, 0.7))
    hud(ctx, T, TAG, ORANGE)
    ficha(ctx, "STEVEN SPIELBERG", "FILM DIRECTOR · E.T. (1982)", W / 2, 1420, pop(lt, 1.1), "🎬", YELLOW)


# 7.09 "Atari rushed it out for Christmas 1982."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.06), floor=False)
    icon(ctx, "🎁", 330, 620, 340, pop(lt, 0.0), 0.1 * math.sin(T * 5))
    ctx.save(); ctx.translate(760, 620)
    circle(ctx, 0, 0, 190); fill_keep(ctx, WHITE); stroke(ctx, RED, 14)
    for k in range(12):
        a = k * math.tau / 12
        ctx.move_to(150 * math.cos(a), 150 * math.sin(a)); ctx.line_to(175 * math.cos(a), 175 * math.sin(a))
    stroke(ctx, (0.2, 0.2, 0.2), 8)
    for sp, L, w in ((14, 140, 10), (1.2, 100, 16)):
        a = T * sp
        ctx.move_to(0, 0); ctx.line_to(L * math.sin(a), -L * math.cos(a)); stroke(ctx, (0.1, 0.1, 0.1), w)
    ctx.restore()
    hud(ctx, T, TAG, RED)
    big_number(ctx, counter(lt, 1975, 1982, 0.9), W / 2, 1390, 150, YELLOW, pop(lt, 0.2))


# 9.46 "Players hated it."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_dark(ctx, T)
    cartridge(ctx, W / 2, 600, 0.8, 0.05)
    rng = np.random.default_rng(1)
    for k in range(9):
        x = rng.uniform(140, 940)
        y = -100 + ((lt * 700 + rng.uniform(0, 600)) % 900)
        icon(ctx, "👎", x, y, 130, 1.0, rng.uniform(-0.4, 0.4))
    hud(ctx, T, TAG, RED)
    pill(ctx, "PLAYERS HATED IT", W / 2, 1400, pop(lt, 0.3), size=54, rgb=RED)


# 10.80 "Stores sent it back."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    icon(ctx, "🏬", 860, 560, 300, pop(lt, 0.0))
    for k in range(3):
        p = clamp((lt - k * 0.15) / 0.8)
        icon(ctx, "📦", lerp(700, 220, ease(p)), 520 + k * 110, 150, 1.0, -0.2 * p)
    arrow(ctx, 700, 860, 200, 860, clamp(lt / 0.7), RED, 14)
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "RETURNED", W / 2, 1400, pop(lt, 0.4), size=70)


# 11.76 "By 1983,"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16))
    big_number(ctx, counter(lt, 1982, 1983, 0.5), W / 2, 620, 300, ORANGE, pop(lt, 0.0))
    hud(ctx, T, TAG, ORANGE)


# 12.86 "an Atari warehouse in Texas was full of games nobody wanted."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.1)]), W / 2, 960)
    bg_desert(ctx, T, night=0.0)
    warehouse(ctx, W / 2, 640, 1.0, clamp(lt / 2.5), T)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "EL PASO, TEXAS", W / 2, 1400, pop(lt, 0.4), size=56, rgb=ORANGE)


# 16.13 "So that September, up to twenty trucks"
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_desert(ctx, T, night=0.0)
    n = int(clamp(lt / 1.6) * 20)
    for k in range(6):
        x = ((lt * 380 + k * 220) % 1500) - 300
        icon(ctx, "🚚", x, 860 - (k % 2) * 90, 260)
    hud(ctx, T, TAG, ORANGE)
    big_number(ctx, f"{max(n, 1)} TRUCKS", W / 2, 520, 150, YELLOW, pop(lt, 0.0))
    pill(ctx, "SEPTEMBER 1983", W / 2, 1400, pop(lt, 0.2), size=54, rgb=ORANGE)


# 18.55 "drove to a landfill in Alamogordo, New Mexico."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    ctx.move_to(260, 280); ctx.line_to(860, 280); ctx.line_to(860, 900); ctx.line_to(320, 900)
    ctx.line_to(320, 860); ctx.line_to(250, 860); ctx.close_path()
    fill_keep(ctx, (0.85, 0.55, 0.30)); stroke(ctx, WHITE, 8, 0.8)
    text(ctx, "NEW MEXICO", 560, 360, 52, WHITE, font="Anton", shadow=False)
    yy = 800 - 200 * (1 - ease_back(clamp(lt / 0.4)))
    ctx.new_path()
    ctx.save(); ctx.translate(0, yy - 800)
    ctx.move_to(560, 800); ctx.curve_to(480, 700, 480, 610, 560, 610); ctx.curve_to(640, 610, 640, 700, 560, 800)
    fill(ctx, RED); circle(ctx, 560, 680, 30); fill(ctx, WHITE)
    ctx.restore()
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "ALAMOGORDO LANDFILL", W / 2, 1400, pop(lt, 0.3), size=50, rgb=ORANGE)


# 20.36 "The cartridges were crushed and buried."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_desert(ctx, T, night=0.3)
    pit(ctx, W / 2, 820, 700, 500, T, carts=int(clamp(lt / 1.5) * 10))
    for k in range(4):
        p = ((lt * 1.4 + k * 0.25) % 1)
        cartridge(ctx, W / 2 + (k - 1.5) * 140, lerp(200, 900, p ** 2), 0.3, T * 3 + k)
    press = abs(math.sin(lt * 4))
    rrect(ctx, W / 2 - 360, 250 + 200 * press, 720, 60, 10); fill(ctx, STEEL_D)
    hud(ctx, T, TAG, ORANGE)


# 22.42 "In other words, Atari held a funeral for its own games."  (2.º gancho)
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_desert(ctx, T, night=1.0)
    rays(ctx, W / 2, 600, T, ORANGE, 0.05)
    tombstone(ctx, W / 2, 620, 1.0, ["R.I.P.", "ATARI GAMES", "1983"], T, pop(lt, 0.0))
    candle(ctx, 250, 900, T)
    candle(ctx, 830, 900, T)
    character(ctx, 200, 1430, 0.5, T, mood="sorpresa")
    hud(ctx, T, TAG, ORANGE)
    badge(ctx, "FUNERAL", 700, 1420, pop(lt, 1.2), size=70)


# 25.80 "For decades, it was just a legend."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_desert(ctx, T, night=0.8)
    for k in range(5):  # niebla
        ellipse(ctx, ((T * 60 + k * 300) % 1600) - 300, 700 + k * 60, 360, 70)
        fill(ctx, WHITE, 0.08)
    icon(ctx, "❓", W / 2, 560, 320, pop(lt, 0.0), 0.1 * math.sin(T * 2))
    hud(ctx, T, TAG, VIOLET)
    big_number(ctx, counter(lt, 1983, 2013, 1.8), W / 2, 1390, 140, VIOLET, 1.0)
    badge(ctx, "LEGEND", W / 2, 300, pop(lt, 0.6), size=60, bg=VIOLET)


# 27.86 "Then, in April 2014, a film crew dug it up."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, keyframes(lt, [(0, 960), (dur, 1000)]))
    bg_desert(ctx, T, night=0.0)
    pit(ctx, W / 2, 820, 720, 520, T, carts=4, dug=clamp(lt / 2.4))
    icon(ctx, "🎥", 870, 560, 210, pop(lt, 0.4))
    icon(ctx, "🚜", 230, 700, 240, pop(lt, 0.1))
    hud(ctx, T, TAG, ORANGE)
    big_number(ctx, "APRIL 2014", W / 2, 420, 140, YELLOW, pop(lt, 0.3))


# 30.71 "Thirty feet down, they found E.T. Still in the shrink wrap."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.06, 0.04), floor=False)
    arrow(ctx, 150, 260, 150, 860, clamp(lt / 0.6), YELLOW, 12)
    text(ctx, "30 FT", 150, 920, 60, YELLOW, font="Anton")
    p = ease_back(clamp((lt - 0.7) / 0.5))
    glow(ctx, 600, 580, 460 * p, (1, 0.95, 0.75), 0.5)
    cartridge(ctx, 600, 580, 0.95 * max(p, 0.01), -0.05, wrap=clamp((lt - 1.6) / 0.4), dirt=0.25)
    for k in range(5):
        a = k * 1.3 + T * 2
        icon(ctx, "✨", 600 + 330 * math.cos(a), 580 + 300 * math.sin(a), 90, clamp((lt - 1.8) / 0.3))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "STILL IN THE SHRINK WRAP", W / 2, 1400, pop(lt, 2.0), size=46, rgb=CYAN)


# 33.75 "Atari said about seven hundred thousand cartridges went into that hole."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.9), (dur, 1.05)]), W / 2, 960)
    bg_desert(ctx, T, night=0.5)
    rng = np.random.default_rng(6)
    n = int(clamp(lt / 2.0) * 70)
    for k in range(n):
        cartridge(ctx, W / 2 + rng.normal(0, 210), 860 - rng.uniform(0, 380) * (1 - abs(rng.normal(0, 0.4))),
                  0.22, rng.uniform(-1, 1))
    hud(ctx, T, TAG, ORANGE)
    big_number(ctx, counter(lt, 0, 700000, 2.0, "{:,.0f}"), W / 2, 420, 170, YELLOW, pop(lt, 0.0))


# 37.00 "Only about thirteen hundred came out."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    rrect(ctx, 140, 620, 800 * 0.98, 70, 14); fill(ctx, ORANGE, 0.85)
    rrect(ctx, 140, 780, max(800 * 1300 / 700000 * 40, 10), 70, 14); fill(ctx, LIME)
    text(ctx, "BURIED · 700,000", 140, 580, 44, ORANGE, align="left", shadow=False)
    text(ctx, "DUG UP · ~1,300", 140, 740, 44, LIME, align="left", shadow=False)
    hud(ctx, T, TAG, LIME)
    big_number(ctx, counter(lt, 0, 1300, 0.9, "{:,.0f}"), W / 2, 1390, 160, LIME, pop(lt, 0.0))


# 38.69 "The rest? Still buried. Because in 1983," -> vuelve a e1 (bucle)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.15), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.41, e2), (4.49, e3), (7.09, e4), (9.46, e5), (10.80, e6), (11.76, e7), (12.86, e8),
           (16.13, e9), (18.55, e10), (20.36, e11), (22.42, e12), (25.80, e13), (27.86, e14), (30.71, e15),
           (33.75, e16), (37.00, e17), (38.69, e18)]
SFX = [(3.43, "pop"), (22.45, "ding"), (32.1, "ding"), (37.05, "pop")]


def MINIATURA(ctx):
    bg_desert(ctx, 1.0, night=1.0)
    glow(ctx, W / 2, 1100, 650, ORANGE, 0.45)
    cartridge(ctx, W / 2, 1060, 1.25, -0.18, dirt=0.4)
    mound(ctx, W / 2, 1260, 640, (0.42, 0.30, 0.22))
    thumb_circle(ctx, W / 2, 1060, 330, 380)
    thumb_arrow(ctx, 900, 1700, W / 2 + 180, 1350)
    thumb_vignette(ctx)
    thumb_text(ctx, [("WHAT'S UNDER", WHITE), "THIS DESERT?"], y=330)
