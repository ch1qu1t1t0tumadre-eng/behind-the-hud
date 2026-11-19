"""Behind the HUD · v03 (EN) — Tetris made its creator $0 for 12 years (formato bucle).
Bloques genéricos con paleta propia (sin logo ni estética oficial de Tetris)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 003"
SUBTITULO = subtitulo_hud
PIECES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(1, 0), (2, 0), (0, 1), (1, 1)],
]
COLS = [CYAN, MAGENTA, LIME, ORANGE, VIOLET, YELLOW]


def block(ctx, x, y, s, rgb, a=1.0):
    rrect(ctx, x + 3, y + 3, s - 6, s - 6, s * 0.14)
    fill(ctx, tuple(c * 0.35 for c in rgb), a)
    rrect(ctx, x + 3, y + 3, s - 6, s - 6, s * 0.14)
    stroke(ctx, rgb, max(3, s * 0.08), a)
    rrect(ctx, x + s * 0.22, y + s * 0.22, s * 0.56, s * 0.56, s * 0.08)
    fill(ctx, rgb, 0.55 * a)


def piece(ctx, k, x, y, s, rot=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    cells = PIECES[k % len(PIECES)]
    cx = (max(c[0] for c in cells) + 1) * s / 2
    cy = (max(c[1] for c in cells) + 1) * s / 2
    for (i, j) in cells:
        block(ctx, i * s - cx, j * s - cy, s, COLS[k % len(COLS)], a)
    ctx.restore()


def rain(ctx, T, n=10, s=70, speed=260, seed=3, a=1.0, x0=-200, x1=W + 200):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x = rng.uniform(x0, x1)
        ph = rng.uniform(0, 2400)
        y = -300 + ((T * speed * rng.uniform(0.7, 1.3) + ph) % 2400)
        piece(ctx, k, x, y, s, rng.choice([0, math.pi / 2, math.pi]), a)


def stack(ctx, x, y, s, rows, T, crumble=0.0):
    """Montón de bloques apilados (base en y). crumble 0..1 los hace caer."""
    rng = np.random.default_rng(7)
    for r in range(rows):
        for c in range(10):
            if rng.random() < 0.12:
                continue
            bx = x + (c - 5) * s
            by = y - (r + 1) * s
            if crumble > 0:
                d = rng.uniform(0.3, 1.0)
                by += 1400 * (crumble * d) ** 2
                bx += rng.uniform(-200, 200) * crumble
            block(ctx, bx, by, s, COLS[(r + c * 3) % len(COLS)])


def stamp(ctx, txt, x, y, appear, rgb=RED, rot=-0.18, size=74):
    if appear <= 0.01:
        return
    s = lerp(2.2, 1.0, ease(clamp(appear)))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.select_font_face("Anton"); ctx.set_font_size(size)
    w = ctx.text_extents(txt)[4]
    rrect(ctx, -w / 2 - 34, -size * 0.75, w + 68, size * 1.5, 16)
    fill_keep(ctx, (0.06, 0.02, 0.04), 0.88 * min(1, appear * 1.5))
    stroke(ctx, rgb, 10, min(1, appear * 1.5))
    text(ctx, txt, 0, 0, size, rgb, a=min(1, appear * 1.5), font="Anton", shadow=False)
    ctx.restore()


def handheld(ctx, x, y, s, T):
    """Consola portátil genérica horizontal, diseño propio (no imita ninguna marca)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -420, -220, 840, 440, 200); fill(ctx, (0.16, 0.10, 0.30))
    rrect(ctx, -420, -220, 840, 440, 200); stroke(ctx, MAGENTA, 8, 0.8)
    rrect(ctx, -230, -170, 460, 300, 20); fill(ctx, (0.02, 0.03, 0.08))
    for k in range(4):
        piece(ctx, k, -150 + k * 100, -130 + ((T * 110 + k * 60) % 240), 34)
    rrect(ctx, -350, -20, 90, 30, 8); fill(ctx, CYAN)
    rrect(ctx, -320, -50, 30, 90, 8); fill(ctx, CYAN)
    for (bx, by) in ((320, -50), (360, -10), (280, -10), (320, 30)):
        circle(ctx, bx, by, 18); fill(ctx, YELLOW)
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): lluvia de bloques y un $0 gigante."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    rain(ctx, T, 12, 80, 300)
    hud(ctx, T, TAG, CYAN)
    big_number(ctx, "$0", W / 2, 520, 330, LIME, 1.0)
    pill(ctx, "12 YEARS · 0 ROYALTIES", W / 2, 1420, 1.0, size=48, rgb=LIME)


# 0.00 "Tetris made its creator zero dollars for twelve years."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 3.64 "And it's real. In 1984,"
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    rain(ctx, T, 8, 60, 200, a=0.5)
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 420, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.5, 1970, 1984, 0.7) if lt > 0.5 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.5))


# 5.62 "Alexey Pajitnov built Tetris in a Soviet computer lab in Moscow."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    crt(ctx, W / 2, 560, 620, 460, T, lambda c: [piece(c, k, W / 2 - 180 + k * 120,
                                                        360 + ((T * 160 + k * 90) % 400), 50) for k in range(4)])
    rrect(ctx, W / 2 - 360, 840, 720, 70, 12); fill(ctx, (0.55, 0.55, 0.50))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "MOSCOW · 1984", W / 2, 260, pop(lt, 0.3), size=48, rgb=RED)
    ficha(ctx, "ALEXEY PAJITNOV", "COMPUTER ENGINEER · SOVIET ACADEMY", W / 2, 1420, pop(lt, 0.1), "🧩", CYAN)


# 9.03 "Even Pajitnov couldn't stop playing it at work."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    rain(ctx, T, 9, 70, 340, seed=5)
    ctx.save(); ctx.translate(W / 2, 600)
    circle(ctx, 0, 0, 220); fill_keep(ctx, WHITE); stroke(ctx, CYAN, 14)
    for sp, L, w in ((12, 170, 10), (1.0, 110, 18)):
        a = T * sp
        ctx.move_to(0, 0); ctx.line_to(L * math.sin(a), -L * math.cos(a)); stroke(ctx, (0.1, 0.1, 0.1), w)
    ctx.restore()
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "ONE MORE GAME...", W / 2, 1400, pop(lt, 0.3), size=54, rgb=CYAN)


# 11.11 "A sixteen-year-old intern helped bring it to the PC."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, floor=False)
    big_number(ctx, "16", 300, 560, 300, ORANGE, pop(lt, 0.0))
    text(ctx, "YEARS OLD", 300, 760, 54, WHITE, font="Anton", a=pop(lt, 0.2))
    crt(ctx, 760, 560, 380, 300, T, lambda c: [piece(c, k, 700 + k * 60, 470 + ((T * 140 + k * 60) % 180), 36)
                                                for k in range(3)])
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "INTERN PORTS IT TO PC", W / 2, 1400, pop(lt, 0.5), size=48, rgb=ORANGE)


# 13.54 "But here's the catch."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 560, T, MAGENTA, 0.05)
    character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
    icon(ctx, "⚠️", 820, 330, 180, pop(lt, 0.15))
    hud(ctx, T, TAG, MAGENTA)


# 14.49 "He worked for the state."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_blueprint(ctx, T)
    icon(ctx, "🏛️", W / 2, 560, 420, pop(lt, 0.0))
    hud(ctx, T, TAG, RED)
    pill(ctx, "EMPLOYER: THE STATE", W / 2, 1400, pop(lt, 0.4), size=52, rgb=RED)


# 16.96 "So under Soviet law, Tetris belonged to the Soviet Union."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    stack(ctx, W / 2 + 35, 900, 80, 6, T)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "STATE PROPERTY", W / 2, 560, clamp((lt - 0.9) / 0.25))


# 18.72 "A state agency called Elorg sold the rights around the world."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, floor=False)
    icon(ctx, "🌍", W / 2, 600, 440, pop(lt, 0.0), T * 0.3)
    for k in range(6):
        a = k * math.tau / 6 + T * 0.6
        p = clamp((lt - 0.4 - k * 0.12) / 0.4)
        if p > 0:
            arrow(ctx, W / 2 + 250 * math.cos(a), 600 + 250 * math.sin(a),
                  W / 2 + 420 * math.cos(a), 600 + 420 * math.sin(a), p, YELLOW, 10)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "ELORG · STATE AGENCY", W / 2, 1400, pop(lt, 0.3), size=50, rgb=YELLOW)


# 21.65 "Nintendo got the handheld rights."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.08, 0.16))
    handheld(ctx, W / 2, 600, 1.05 * max(pop(lt, 0.0), 0.01), T)
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, "HANDHELD RIGHTS → NINTENDO", W / 2, 1400, pop(lt, 0.3), size=44, rgb=MAGENTA)


# 23.22 "Tetris went everywhere."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.95)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    for r in range(3):
        for c in range(3):
            p = clamp((lt - (r * 3 + c) * 0.06) / 0.3)
            if p > 0:
                x, y = 220 + c * 320, 330 + r * 260
                ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
                crt(ctx, 0, 0, 240, 180, T, lambda cc, k=r * 3 + c: piece(cc, k, 0, -60 + ((T * 120 + k * 40) % 120), 26))
                ctx.restore()
    hud(ctx, T, TAG, CYAN)


# 24.47 "Pajitnov? No royalties."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 960)
    bg_dark(ctx, T)
    big_number(ctx, "$0", W / 2, 560, 360, RED, pop(lt, 0.5))
    hud(ctx, T, TAG, RED)
    ficha(ctx, "ALEXEY PAJITNOV", "ROYALTIES: NONE", W / 2, 1420, pop(lt, 0.0), "🧩", RED)


# 26.08 "In other words, the most addictive game on Earth belonged to a government."  (2.º gancho)
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.06), floor=False)
    rays(ctx, W / 2, 600, T, RED, 0.07)
    rain(ctx, T, 10, 70, 420, seed=9, a=0.7)
    icon(ctx, "🏛️", W / 2, 600, 380, pop(lt, 0.2))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "OWNED BY A GOVERNMENT", W / 2, 1400, clamp((lt - 1.2) / 0.25), size=56, rot=-0.06)


# 29.82 "Then the Soviet Union collapsed."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 50) * (lt > 0.4), W / 2, 960)
    bg_dark(ctx, T)
    stack(ctx, W / 2 + 35, 900, 80, 6, T, crumble=clamp((lt - 0.3) / 1.2))
    hud(ctx, T, TAG, ORANGE)
    big_number(ctx, "1991", W / 2, 1390, 150, ORANGE, pop(lt, 0.1))


# 31.40 "Pajitnov moved to America in 1991."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.20))
    p = ease(clamp(lt / 1.6))
    ctx.move_to(200, 760); ctx.curve_to(400, 300, 700, 300, 880, 600)
    stroke(ctx, WHITE, 6, 0.4)
    icon(ctx, "✈️", lerp(200, 880, p), 760 - 420 * math.sin(p * math.pi) * 0.9, 170, 1.0, lerp(-0.6, 0.6, p))
    icon(ctx, "🇺🇸", 880, 680, 200, pop(lt, 1.0))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "ALEXEY PAJITNOV", "MOVES TO THE U.S. · 1991", W / 2, 1420, pop(lt, 0.0), "🧩", CYAN)


# 33.73 "And in 1996, the rights finally came back to him."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.12, 0.08))
    rays(ctx, W / 2, 600, T, LIME, 0.05)
    big_number(ctx, counter(lt, 1991, 1996, 0.8), W / 2, 420, 220, LIME, pop(lt, 0.0))
    icon(ctx, "🔑", W / 2, 720, 300, pop(lt, 1.0), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "RIGHTS RETURNED", W / 2, 1400, pop(lt, 1.2), size=54, rgb=LIME)


# 36.51 "He started The Tetris Company with his friend Henk Rogers."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T)
    icon(ctx, "🤝", W / 2, 560, 380, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    ficha(ctx, "HENK ROGERS", "GAME PUBLISHER · CO-FOUNDER", W / 2, 1420, pop(lt, 1.2), "🎮", YELLOW)


# 39.09 "Which is wild, because for so long," -> vuelve a e1 (bucle)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.15), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.64, e2), (5.62, e3), (9.03, e4), (11.11, e5), (13.54, e6), (14.49, e7), (16.96, e8),
           (18.72, e9), (21.65, e10), (23.22, e11), (24.47, e12), (26.08, e13), (29.82, e14), (31.40, e15),
           (33.73, e16), (36.51, e17), (39.09, e18)]
SFX = [(3.66, "pop"), (17.9, "ding"), (25.2, "pop"), (26.1, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.04, 0.05, 0.16))
    rain(ctx, 1.4, 10, 110, 300, seed=4, a=0.8)
    big_number(ctx, "$0", W / 2, 1150, 520, LIME, 1.0)
    thumb_circle(ctx, W / 2, 1150, 360, 300)
    thumb_arrow(ctx, 880, 1750, W / 2 + 200, 1420)
    thumb_vignette(ctx)
    thumb_text(ctx, [("HE MADE TETRIS", WHITE), "AND GOT..."], y=330)
