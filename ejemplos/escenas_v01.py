"""Behind the HUD · v01 (EN) — Space Invaders' difficulty was a hardware accident (formato bucle)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 001"
SUBTITULO = subtitulo_hud


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): formación de alienígenas bajando hacia el cañón."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T)
    shift = 140 * math.sin(T * 1.2)
    alien_grid(ctx, W / 2, 560, T, rows=4, cols=8, px=10, gap=130, shift=shift, rate=3)
    tank(ctx, W / 2 + 80 * math.sin(T * 2), 1120 + 160, 13)
    for k in range(3):
        y = 1180 - ((T * 900 + k * 330) % 900)
        ctx.rectangle(W / 2 + 80 * math.sin(T * 2) - 5, y, 10, 40)
        fill(ctx, WHITE, 0.9)
    hud(ctx, T, TAG)
    pill(ctx, "SPACE INVADERS · 1978", W / 2, 1420, 1.0, size=50, rgb=MAGENTA)


# 0.00 "Space Invaders' hardest part was never supposed to exist."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 3.38 "And it's real. In 1978,"
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.14))
    cabinet(ctx, W / 2, 720, 0.82, T, "1978",
            lambda c: alien_grid(c, 0, 0, T, rows=3, cols=5, px=5, gap=70, shift=30 * math.sin(T * 2)))
    hud(ctx, T, TAG)
    badge(ctx, "REAL", 820, 330, pop(lt, 0.05), size=70)
    big_number(ctx, counter(lt - 0.6, 1960, 1978, 0.8) if lt > 0.6 else "", W / 2, 1390, 150, YELLOW, pop(lt, 0.6))


# 5.34 "Tomohiro Nishikado built Space Invaders for Taito."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), keyframes(lt, [(0, 600), (dur, 480)]), 960)
    bg_arcade(ctx, T)
    cabinet(ctx, 540, 720, 0.8, T, "INVADERS?",
            lambda c: alien_grid(c, 0, 0, T, rows=3, cols=5, px=5, gap=70, shift=30 * math.sin(T * 2)))
    icon(ctx, "🛠️", 860, 420, 170, pop(lt, 0.3), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG)
    ficha(ctx, "TOMOHIRO NISHIKADO", "GAME DESIGNER · TAITO", W / 2, 1420, pop(lt, 0.1), "🕹️", CYAN)


# 8.06 "Computers back then were too weak,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.12), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    old_pc(ctx, W / 2, 620, 1.05, T, bad=clamp((lt - 0.8) / 0.3))
    hud(ctx, T, TAG, RED)
    pill(ctx, "TOO WEAK", W / 2, 1400, pop(lt, 0.9), size=60, rgb=RED)


# 9.85 "so he built his own hardware."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_blueprint(ctx, T)
    circuit(ctx, W / 2, 620, 860, 560, T, clamp(lt / 1.2))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "HOMEMADE HARDWARE", W / 2, 1400, pop(lt, 0.5), size=50, rgb=LIME)


# 11.33 "Moving all fifty-five space invaders at once"
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, floor=False)
    n = int(clamp(lt / 1.4) * 55)
    alien_grid(ctx, W / 2, 600, T, rows=5, cols=11, px=7, gap=104,
               alive=lambda r, c: r * 11 + c < n, shift=40 * math.sin(T * 1.5))
    hud(ctx, T, TAG)
    big_number(ctx, str(n), W / 2, 1390, 170, LIME, pop(lt, 0.0))


# 13.86 "pushed the chip to its limit."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.2)]), W / 2, 960)
    bg_dark(ctx, T)
    heat = clamp(lt / 1.0)
    chip(ctx, W / 2, 620, 1.15, T, heat=heat, label="8080")
    hud(ctx, T, TAG, ORANGE)
    meter(ctx, W / 2, 1420, 800, lerp(0.4, 1.0, heat), "CPU LOAD", ORANGE, pop(lt, 0.1))


# 15.19 "But here's the weird part."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 620, T, MAGENTA, 0.05)
    character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
    icon(ctx, "❓", 780, 360, 200, pop(lt, 0.2), 0.15 * math.sin(T * 4))
    hud(ctx, T, TAG, MAGENTA)


# 16.30 "Every alien you shot gave the processor less work."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, floor=False)
    killed = clamp(lt / 2.4) * 40
    order = [(r, c) for r in range(4, -1, -1) for c in range(11)]
    dead = set(order[:int(killed)])
    alien_grid(ctx, W / 2, 500, T, rows=5, cols=11, px=6, gap=96, alive=lambda r, c: (r, c) not in dead)
    if order[:int(killed)]:
        r, c = order[int(killed) - 1]
        x = W / 2 + (c - 5) * 96 * 0.82
        y = 500 + (r - 2) * 96 * 0.75
        glow(ctx, x, y, 90, WHITE, 0.7 * (1 - (killed % 1)))
    hud(ctx, T, TAG)
    meter(ctx, W / 2, 1420, 800, lerp(1.0, 0.25, clamp(lt / 2.4)), "CPU LOAD", LIME, 1.0)


# 19.19 "So the survivors moved faster. And faster."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, 960)
    bg_arcade(ctx, T, speed=0.6 + lt * 1.5)
    sp = lerp(1.5, 9.0, clamp(lt / dur))
    for k in range(3):
        x = W / 2 + 330 * math.sin(T * sp + k * 2.1)
        y = 430 + k * 170
        for g in range(4):  # estela
            alien(ctx, x - 40 * g * math.cos(T * sp + k * 2.1), y, 9, T, k, a=0.18 * (4 - g) if g else 1.0, rate=sp)
    screen(ctx)
    speedometer(ctx, W / 2, 1400, 170, clamp(lt / dur) * 0.95 + 0.05, "SPEED", 1.0)
    hud(ctx, T, TAG, ORANGE)


# 21.92 "In other words, Space Invaders sped up because it was broken."  (2.º gancho)
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.06), floor=False)
    rays(ctx, W / 2, 620, T, RED, 0.07)
    chip(ctx, W / 2, 620, 1.1, T, heat=0.9, label="BUG")
    for k in range(5):  # grietas
        ctx.move_to(W / 2 - 40 + k * 20, 460)
        ctx.line_to(W / 2 - 80 + k * 45, 560)
        ctx.line_to(W / 2 - 20 + k * 25, 680)
    stroke(ctx, (0.05, 0.05, 0.05), 8)
    hud(ctx, T, TAG, RED)
    badge(ctx, "BROKEN", W / 2, 1400, pop(lt, 0.9), size=80)


# 25.02 "Nishikado could have fixed it. He didn't."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    icon(ctx, "🔧", W / 2, 600, 380, pop(lt, 0.0), -0.3 + 0.1 * math.sin(T * 3))
    p = clamp((lt - 1.3) / 0.25)
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 600); ctx.scale(p, p)
        circle(ctx, 0, 0, 240); stroke(ctx, RED, 34)
        ctx.move_to(-170, -170); ctx.line_to(170, 170); stroke(ctx, RED, 34)
        ctx.restore()
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "TOMOHIRO NISHIKADO", "GAME DESIGNER · TAITO", W / 2, 1420, pop(lt, 0.1), "🕹️", CYAN)


# 26.91 "He called the bug a feature."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, floor=False)
    flip = clamp((lt - 0.8) / 0.35)
    ctx.save(); ctx.translate(W / 2, 600); ctx.scale(1, abs(math.cos(flip * math.pi)) + 0.001)
    if flip < 0.5:
        icon(ctx, "🐛", 0, 0, 420)
    else:
        icon(ctx, "⭐", 0, 0, 420)
    ctx.restore()
    hud(ctx, T, TAG, LIME)
    if flip < 0.5:
        badge(ctx, "BUG", W / 2, 1400, pop(lt, 0.1), size=80)
    else:
        badge(ctx, "FEATURE", W / 2, 1400, pop(lt, 0.8), size=80, bg=(0.15, 0.6, 0.3))


# 28.39 "He even made the music speed up with the aliens."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.18), speed=1.5)
    sp = 2 + lt * 3
    for k in range(6):
        x = 160 + k * 150
        y = 600 - 140 * abs(math.sin(T * sp + k))
        icon(ctx, "🎵", x, y, 150)
    for k in range(12):  # ecualizador
        h = 60 + 220 * abs(math.sin(T * sp * 1.3 + k * 0.7))
        rrect(ctx, 120 + k * 72, 900 - h, 52, h, 8)
        fill(ctx, MAGENTA if k % 2 else CYAN, 0.9)
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, counter(lt, 60, 180, dur) + " BPM", W / 2, 1400, pop(lt, 0.1), size=56, rgb=MAGENTA)


# 30.73 "By the end of 1978,"
def e15a(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16))
    rrect(ctx, W / 2 - 300, 300, 600, 560, 40); fill_keep(ctx, WHITE); stroke(ctx, MAGENTA, 10)
    rrect(ctx, W / 2 - 300, 300, 600, 150, 40); fill(ctx, MAGENTA)
    text(ctx, "DECEMBER", W / 2, 375, 70, WHITE, font="Anton", shadow=False)
    text(ctx, counter(lt, 1, 31, 1.2), W / 2, 650, 260, (0.1, 0.1, 0.15), font="Anton", shadow=False)
    hud(ctx, T, TAG, MAGENTA)
    big_number(ctx, "1978", W / 2, 1390, 150, YELLOW, pop(lt, 0.1))


# 32.22 "Japan had about one hundred thousand Space Invaders machines."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.85), (dur, 1.05)]), W / 2, keyframes(lt, [(0, 960), (dur, 900)]))
    bg_arcade(ctx, T)
    rows = int(clamp(lt / 1.8) * 4) + 1
    for r in range(rows):
        for c in range(-3, 4):
            s = 0.28 + r * 0.04
            cabinet(ctx, W / 2 + c * 520 * s * 1.1, 400 + r * 160, s, T + c, "", None,
                    (VIOLET, MAGENTA, (0.2, 0.5, 0.9))[(r + c) % 3])
    icon(ctx, "🇯🇵", 860, 300, 150, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    big_number(ctx, counter(lt, 0, 100000, 1.8, "{:,.0f}"), W / 2, 1390, 150, YELLOW, pop(lt, 0.0))


# 35.51 "All thanks to one tired chip."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    glow(ctx, W / 2, 620, 500, CYAN, 0.12)
    chip(ctx, W / 2, 620, 1.1, T, heat=0.35, label="8080", tired=1.0)
    for k in range(3):  # zzz
        p = ((T * 0.8 + k / 3) % 1)
        text(ctx, "Z", W / 2 + 230 + p * 120, 420 - p * 220, 60 + 40 * p, WHITE, a=1 - p, font="Anton")
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "ONE TIRED CHIP", W / 2, 1400, pop(lt, 0.2), size=54, rgb=CYAN)


# 37.37 "And that's the secret. The hardest part of" -> vuelve a e1 (bucle)
def e17(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.15), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.38, e2), (5.34, e3), (8.06, e4), (9.85, e5), (11.33, e6), (13.86, e7),
           (15.19, e8), (16.30, e9), (19.19, e10), (21.92, e11), (25.02, e12), (26.91, e13),
           (28.39, e14), (30.73, e15a), (32.22, e15), (35.51, e16), (37.37, e17)]
SFX = [(3.40, "pop"), (21.95, "ding"), (27.75, "pop"), (32.2, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.3)
    rays(ctx, W / 2, 900, 0.5, LIME, 0.05)
    alien_grid(ctx, W / 2, 820, 0.2, rows=3, cols=6, px=12, gap=170, alive=lambda r, c: (r, c) != (0, 2))
    alien(ctx, W / 2 - 140, 1340, 22, 0.1, 0)
    for g in range(1, 4):
        alien(ctx, W / 2 - 140 - 90 * g, 1340, 22, 0.1, 0, a=0.25 * (4 - g) / 3)
    thumb_circle(ctx, W / 2 - 140, 1340, 210, 170)
    thumb_arrow(ctx, 820, 1650, W / 2 + 60, 1430)
    thumb_vignette(ctx)
    thumb_text(ctx, [("WHY IS IT", WHITE), "SO FAST?"], y=330)
