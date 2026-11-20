"""Behind the HUD · 012 (EN) — The Legend of Zelda started with a scared kid and a cave (formato bucle).
Paisaje, cueva, farol y mapa genéricos dibujados por el canal; niño = personaje propio del canal; sin personajes, mapas ni logos de Nintendo."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 012"
SUBTITULO = subtitulo_hud
FOREST = (0.12, 0.30, 0.18)
ROCK = (0.30, 0.28, 0.32)
LAMP = (1.0, 0.80, 0.35)


def sky(ctx, T, dusk=0.0):
    g = vgrad(ctx, 0, 0, 0, H, [(0, (lerp(0.45, 0.10, dusk), lerp(0.70, 0.12, dusk), lerp(0.90, 0.25, dusk))),
                               (0.5, (lerp(0.80, 0.35, dusk), lerp(0.90, 0.25, dusk), lerp(0.85, 0.35, dusk))),
                               (1, (0.10, 0.16, 0.12))])
    ctx.rectangle(-600, -600, W + 1200, H + 1200); ctx.set_source(g); ctx.fill()


def hills(ctx, T):
    for k, (col, y0) in enumerate(((0.20, 760), (0.14, 820), (0.09, 880))):
        ctx.move_to(-200, H)
        ctx.line_to(-200, y0)
        for x in range(-200, W + 260, 60):
            ctx.line_to(x, y0 - 90 * math.sin(x / (230 + 60 * k) + k) - 30)
        ctx.line_to(W + 200, H); ctx.close_path(); fill(ctx, (col, col + 0.18, col + 0.06))


def tree(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-10, -40, 20, 60); fill(ctx, (0.35, 0.22, 0.12))
    for k in range(3):
        ctx.move_to(-70 + k * 12, -30 - k * 50); ctx.line_to(0, -120 - k * 50); ctx.line_to(70 - k * 12, -30 - k * 50)
        ctx.close_path(); fill(ctx, (0.10, 0.38 - k * 0.04, 0.20))
    ctx.restore()


def cave(ctx, x, y, s, T, inner=0.0, bars=0.0):
    """Boca de cueva genérica; inner = luz de farol dentro; bars = tablones de bloqueo."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-420, 200); ctx.curve_to(-400, -250, 400, -250, 420, 200); ctx.close_path(); fill(ctx, ROCK)
    for k in range(6):
        circle(ctx, -330 + k * 130, -40 - 60 * math.sin(k), 50 + 10 * (k % 3)); fill(ctx, (0.36, 0.34, 0.38), 0.7)
    ctx.move_to(-200, 200); ctx.curve_to(-190, -110, 190, -110, 200, 200); ctx.close_path(); fill(ctx, (0.02, 0.02, 0.03))
    if inner > 0:
        glow(ctx, 0, 90, 220, LAMP, 0.45 * inner)
    for k in range(2):
        circle(ctx, -40 + k * 80, 40, 10); fill(ctx, YELLOW, 0.0)
    if bars > 0:
        for k in range(3):
            ctx.save(); ctx.translate(0, -10 + k * 70); ctx.rotate(0.12 * (1 if k % 2 else -1))
            rrect(ctx, -230 * bars, -22, 460 * bars, 44, 8); fill(ctx, (0.55, 0.36, 0.18))
            ctx.restore()
    ctx.restore()


def lantern(ctx, x, y, s, T, a=1.0):
    ctx.save(); ctx.translate(x, y + 6 * math.sin(T * 3)); ctx.scale(s, s)
    glow(ctx, 0, 0, 220, LAMP, 0.35 * a)
    ctx.move_to(-25, -80); ctx.curve_to(-25, -120, 25, -120, 25, -80); stroke(ctx, (0.25, 0.25, 0.28), 8, a)
    rrect(ctx, -45, -80, 90, 20, 6); fill(ctx, (0.25, 0.25, 0.28), a)
    rrect(ctx, -38, -62, 76, 110, 14); fill(ctx, (1.0, 0.90, 0.55), a)
    ellipse(ctx, 0, -5, 14, 26 + 4 * math.sin(T * 12)); fill(ctx, ORANGE, a)
    rrect(ctx, -45, 48, 90, 20, 6); fill(ctx, (0.25, 0.25, 0.28), a)
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): niño con farol ante la cueva."""
    camera(ctx, zoom, W / 2, 960)
    sky(ctx, T, 0.8)
    hills(ctx, T)
    cave(ctx, W / 2, 640, 1.05, T, inner=0.3)
    character(ctx, 270, 780, 0.55, T, mood="duda", look=(0.4, -0.1))
    lantern(ctx, 400, 700, 0.6, T)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "THE CAVE THAT STARTED IT", W / 2, 1420, 1.0, size=50, rgb=YELLOW)


# 0.03 "The Legend of Zelda started with a kid who was afraid of a cave."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 3.75 "And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 600, pop(lt, 0.05), size=110)


# 4.63 "Shigeru Miyamoto grew up in Sonobe, a small town near Kyoto,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    sky(ctx, T, 0.0)
    hills(ctx, T)
    for k in range(4):
        x = 330 + k * 120
        ctx.rectangle(x - 45, 690, 90, 70); fill(ctx, (0.85, 0.80, 0.70))
        ctx.move_to(x - 60, 690); ctx.line_to(x, 640); ctx.line_to(x + 60, 690); ctx.close_path(); fill(ctx, (0.25, 0.25, 0.30))
    icon(ctx, "📍", W / 2, 520, 150, pop(lt, 0.3), 0.0)
    hud(ctx, T, TAG, LIME)
    ficha(ctx, "SHIGERU MIYAMOTO", "GAME DESIGNER · NINTENDO", W / 2, 1420, pop(lt, 0.1), "🗺️", LIME)


# 8.24 "in the nineteen fifties."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02))
    big_number(ctx, "1950s", W / 2, 580, 260, YELLOW, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "SONOBE · NEAR KYOTO", W / 2, 1400, pop(lt, 0.2), size=54, rgb=YELLOW)


# 10.11 "As a boy, Miyamoto explored the hills, forests and lakes around his home."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2 + 20 * lt, 960)
    sky(ctx, T, 0.1)
    hills(ctx, T)
    ellipse(ctx, 760, 860, 220, 50); fill(ctx, (0.35, 0.60, 0.85))
    for k, x in enumerate((120, 220, 330, 920, 1010)):
        tree(ctx, x, 880 + (k % 2) * 20, 1.1)
    character(ctx, 460, 820, 0.5, T, mood="normal", look=(0.3, 0))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "HILLS · FORESTS · LAKES", W / 2, 1400, pop(lt, 0.3), size=52, rgb=LIME)


# 13.77 "One day he found a dark cave."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, 960)
    sky(ctx, T, 0.5)
    hills(ctx, T)
    cave(ctx, W / 2, 620, 1.0, T)
    tree(ctx, 120, 880, 1.3); tree(ctx, 980, 900, 1.2)
    hud(ctx, T, TAG, ROCK)
    pill(ctx, "A DARK CAVE", W / 2, 1400, pop(lt, 0.3), size=58, rgb=YELLOW)


# 15.85 "For days, he was too nervous to go in."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    sky(ctx, T, 0.7)
    hills(ctx, T)
    cave(ctx, 780, 700, 0.7, T)
    character(ctx, 300, 780, 0.6, T, mood="duda", look=(0.5, 0))
    day = 1 + min(2, int(lt / 0.7))
    rrect(ctx, 170, 330, 260, 240, 20); fill(ctx, WHITE)
    rrect(ctx, 170, 330, 260, 70, 20); fill(ctx, RED)
    text(ctx, "DAY", 300, 368, 40, WHITE, font="Anton", shadow=False)
    text(ctx, str(day), 300, 490, 120, (0.15, 0.15, 0.2), font="Anton", shadow=False)
    hud(ctx, T, TAG, RED)
    pill(ctx, "TOO SCARED TO GO IN", W / 2, 1400, pop(lt, 0.3), size=54, rgb=RED)


# 18.10 "Then he came back with a lantern and stepped inside."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.3)]), W / 2, 960)
    sky(ctx, T, 0.8)
    hills(ctx, T)
    cave(ctx, W / 2, 620, 1.0, T, inner=clamp(lt / 1.2))
    p = ease(clamp(lt / 2.0))
    lantern(ctx, lerp(250, W / 2, p), lerp(800, 700, p), lerp(0.7, 0.45, p), T)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "WITH A LANTERN", W / 2, 1400, pop(lt, 0.3), size=58, rgb=YELLOW)


# 20.82 "In other words, gaming's greatest adventure series began with one scared kid and a lamp."  (2.º gancho)
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.10, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, YELLOW, 0.08)
    character(ctx, 360, 660, 0.75, T, mood="duda", look=(0.4, 0))
    lantern(ctx, 720, 600, 1.0, T)
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "1 SCARED KID + 1 LAMP", W / 2, 1400, clamp((lt - 1.0) / 0.25), YELLOW, size=56, rot=-0.05)


# 25.68 "Miyamoto wanted players to feel that same mix of fear and wonder."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "😨", 300, 560, 260, pop(lt, 0.2))
    text(ctx, "+", W / 2, 570, 120, WHITE, font="Anton", a=pop(lt, 0.6))
    icon(ctx, "✨", 780, 560, 260, pop(lt, 0.9), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, "FEAR + WONDER", W / 2, 1400, pop(lt, 0.4), size=58, rgb=MAGENTA)


# 29.36 "So in 1986,"
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    big_number(ctx, counter(lt, 1976, 1986, 0.8), W / 2, 580, 260, LIME, pop(lt, 0.0))
    hud(ctx, T, TAG, LIME)


# 30.93 "The Legend of Zelda dropped you into an open world full of caves and secrets."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    def inner(c):
        cell = 96
        x0, y0 = W / 2 - 3 * cell, 640 - 2 * cell
        rng = np.random.default_rng(11)
        for r in range(4):
            for q in range(6):
                k = rng.integers(0, 4)
                colr = [(0.20, 0.50, 0.25), (0.45, 0.40, 0.30), (0.25, 0.45, 0.70), (0.15, 0.35, 0.18)][k]
                c.rectangle(x0 + q * cell, y0 + r * cell, cell - 4, cell - 4); fill(c, colr)
        reveal = int(clamp(lt / 3.0) * 6)
        for j, (q, r) in enumerate(((1, 0), (4, 1), (2, 3), (5, 3), (0, 2), (3, 1))):
            if j <= reveal:
                cx, cy = x0 + q * cell + cell / 2 - 2, y0 + r * cell + cell / 2 - 2
                c.move_to(cx - 28, cy + 30); c.curve_to(cx - 26, cy - 30, cx + 26, cy - 30, cx + 28, cy + 30)
                c.close_path(); fill(c, (0.02, 0.02, 0.03))
                text(c, "?", cx, cy + 4, 40, YELLOW, font="Press Start 2P", shadow=False)
    crt(ctx, W / 2, 640, 700, 480, T, inner)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "OPEN WORLD · CAVES · SECRETS", W / 2, 1400, pop(lt, 0.3), size=46, rgb=LIME)


# 35.41 "Today, that real cave is reportedly blocked off."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    sky(ctx, T, 0.4)
    hills(ctx, T)
    cave(ctx, W / 2, 620, 1.0, T, bars=ease(clamp(lt / 0.8)))
    icon(ctx, "🚧", 900, 820, 120, pop(lt, 0.6))
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "REPORTEDLY BLOCKED OFF", W / 2, 1400, pop(lt, 0.3), size=52, rgb=ORANGE)


# 38.00 "But its story lives on,"
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, YELLOW, 0.06)
    lantern(ctx, W / 2, 620, 1.4, T)
    hud(ctx, T, TAG, YELLOW)


# 39.81 "because" -> vuelve a e1 (bucle)
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.12), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.75, e2), (4.63, e3), (8.24, e4), (10.11, e5), (13.77, e6), (15.85, e7), (18.10, e8),
           (20.82, e9), (25.68, e10), (29.36, e11), (30.93, e12), (35.41, e13), (38.00, e14), (39.81, e15)]
SFX = [(3.77, "pop"), (13.79, "pop"), (20.83, "ding"), (29.38, "ding")]


def MINIATURA(ctx):
    sky(ctx, 1.0, 0.85)
    hills(ctx, 1.0)
    ctx.save(); ctx.translate(0, 450)
    cave(ctx, W / 2, 760, 1.25, 1.0, inner=0.5)
    character(ctx, 260, 900, 0.7, 1.0, mood="duda", look=(0.5, -0.1))
    lantern(ctx, 420, 800, 0.8, 1.0)
    ctx.restore()
    thumb_circle(ctx, W / 2, 1240, 300, 240)
    thumb_arrow(ctx, 960, 1900, W / 2 + 200, 1380)
    thumb_vignette(ctx)
    thumb_text(ctx, [("ZELDA BEGAN", WHITE), "WITH A CAVE"], y=330)
