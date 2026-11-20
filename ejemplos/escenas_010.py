"""Behind the HUD · 010 (EN) — Fighting game combos started as a Street Fighter II bug (formato bucle).
Luchadores genéricos de diseño propio (figuras geométricas); sin personajes, sprites ni logos de Capcom."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 010"
SUBTITULO = subtitulo_hud


def fighter(ctx, x, y, s, T, col=CYAN, facing=1, punch=0.0, hit=0.0):
    """Luchador geométrico genérico. punch 0..1 extiende el brazo; hit 0..1 lo echa hacia atrás."""
    ctx.save(); ctx.translate(x - facing * 40 * hit, y); ctx.scale(s * facing, s)
    ctx.rotate(-0.25 * hit)
    bob = 6 * math.sin(T * 6)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx in (-30, 30):
        ctx.move_to(dx * 0.5, 40 + bob); ctx.line_to(dx * 1.6, 170); stroke(ctx, col, 26)
    rrect(ctx, -45, -90 + bob, 90, 140, 30); fill(ctx, col)
    circle(ctx, 0, -135 + bob, 42); fill(ctx, (0.95, 0.80, 0.65))
    ctx.rectangle(-44, -160 + bob, 88, 16); fill(ctx, RED)
    ext = lerp(40, 190, ease(clamp(punch)))
    ctx.move_to(20, -60 + bob); ctx.line_to(20 + ext, -70 + bob); stroke(ctx, col, 24)
    circle(ctx, 24 + ext, -70 + bob, 26); fill(ctx, WHITE)
    ctx.move_to(-20, -60 + bob); ctx.line_to(30, -20 + bob); stroke(ctx, col, 24)
    circle(ctx, 34, -18 + bob, 22); fill(ctx, WHITE)
    ctx.restore()


def hits_counter(ctx, n, x, y, appear=1.0, size=180):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(appear, appear); ctx.rotate(-0.06)
    text(ctx, str(n), -80, 0, size, YELLOW, font="Bangers")
    text(ctx, "HITS", 120, 20, size * 0.45, WHITE, font="Bangers")
    ctx.restore()


def impact(ctx, x, y, r, T, a=1.0):
    for k in range(10):
        ang = k * math.tau / 10 + 0.2
        ctx.move_to(x + r * 0.4 * math.cos(ang), y + r * 0.4 * math.sin(ang))
        ctx.line_to(x + r * math.cos(ang), y + r * math.sin(ang))
        stroke(ctx, YELLOW, 10, a)
    circle(ctx, x, y, r * 0.35); fill(ctx, WHITE, 0.8 * a)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): dos golpes encadenados + contador."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.06))
    rays(ctx, W / 2, 600, T, ORANGE, 0.05)
    ph = (T * 1.5) % 1
    fighter(ctx, 330, 720, 1.15, T, CYAN, 1, punch=1 if ph < 0.5 else 0.2)
    fighter(ctx, 760, 720, 1.15, T, MAGENTA, -1, hit=0.6 if ph < 0.5 else 0.2)
    if ph < 0.5:
        impact(ctx, 600, 630, 90, T)
    hits_counter(ctx, 2, W / 2, 390, 1.0, 160)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "IT WAS A BUG", W / 2, 1420, 1.0, size=56, rgb=ORANGE)


# 0.03 "Combos in fighting games started as a bug"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.08)]))


# 2.20 "nobody was supposed to find."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "🐛", W / 2 - 40, 560, 300, pop(lt, 0.0))
    icon(ctx, "🔍", W / 2 + 160, 470, 220, pop(lt, 0.4), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "NOBODY WAS SUPPOSED TO FIND IT", W / 2, 1400, pop(lt, 0.3), size=42, rgb=LIME)


# 4.18 "And it's real. In 1991,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 420, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.8, 1981, 1991, 0.6) if lt > 0.8 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.8))


# 6.38 "Capcom was finishing Street Fighter II for arcades."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16))
    cabinet(ctx, W / 2, 700, 0.68, T, "STREET FIGHTER II",
            lambda c: (fighter(c, -90, 60, 0.5, T, CYAN, 1, punch=0.5 + 0.5 * math.sin(T * 5)),
                       fighter(c, 90, 60, 0.5, T, MAGENTA, -1)), ORANGE)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "CAPCOM · ARCADES · 1991", W / 2, 1400, pop(lt, 0.3), size=50, rgb=ORANGE)


# 9.35 "Producer Noritaka Funamizu was bug testing the car bonus stage"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    icon(ctx, "🚗", W / 2 - 150, 620, 260, pop(lt, 0.2), 0.05 * math.sin(T * 8))
    icon(ctx, "🔨", W / 2 + 180, 540, 190, pop(lt, 0.5), 0.5 * math.sin(T * 9))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "NORITAKA FUNAMIZU", "PRODUCER · CAPCOM", W / 2, 1420, pop(lt, 0.1), "🕹️", CYAN)


# 12.20 "when he noticed something strange."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + 0.006 * math.sin(T * 40), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, W / 2, 580, 680, 480, T, lambda c: (
        fighter(c, W / 2 - 120, 640, 0.75, T, CYAN, 1, punch=0.6),
        fighter(c, W / 2 + 140, 640, 0.75, T, MAGENTA, -1),
        text(c, "?!", W / 2, 420, 110, YELLOW, a=0.6 + 0.4 * math.sin(T * 10), font="Bangers")))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "SOMETHING STRANGE", W / 2, 1400, pop(lt, 0.2), size=54, rgb=YELLOW)


# 14.68 "If he started a punch and quickly launched a special move,"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16), floor=False)
    p = clamp(lt / 0.6)
    fighter(ctx, 360, 680, 1.25, T, CYAN, 1, punch=p)
    if lt > 1.3:
        for k in range(3):
            circle(ctx, 640 + k * 90 + ((T * 400) % 90), 600, 40 - k * 8); fill(ctx, CYAN, 0.7 - k * 0.2)
        glow(ctx, 700, 600, 200, CYAN, 0.3)
    tile(ctx, "", 260, 380, 150, pop(lt, 0.2), YELLOW); icon(ctx, "👊", 260, 380, 100, pop(lt, 0.2))
    text(ctx, "+", W / 2, 385, 100, WHITE, font="Anton", a=pop(lt, 0.9))
    tile(ctx, "", 820, 380, 150, pop(lt, 1.3), CYAN); icon(ctx, "⚡", 820, 380, 100, pop(lt, 1.3))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "PUNCH → SPECIAL MOVE", W / 2, 1400, pop(lt, 0.4), size=52, rgb=CYAN)


# 17.61 "the game skipped the rest of the animation."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_dark(ctx, T)
    for i in range(6):
        x = 140 + i * 160
        rrect(ctx, x - 65, 460, 130, 200, 10); fill(ctx, (0.15, 0.15, 0.22))
        rrect(ctx, x - 65, 460, 130, 200, 10); stroke(ctx, STEEL, 4)
        fighter(ctx, x - 10, 590, 0.32, T * 0, CYAN, 1, punch=i / 5)
        text(ctx, f"F{i + 1}", x, 690, 28, STEEL, font="Press Start 2P", shadow=False)
        if i >= 2:
            x_mark(ctx, x, 560, 55, clamp((lt - 0.4 - (i - 2) * 0.12) / 0.25), w=12)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "FRAMES SKIPPED", W / 2, 1400, clamp((lt - 0.6) / 0.25), RED, size=64, rot=-0.05)


# 19.70 "Two hits landed before the opponent could react."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]) + 0.01 * math.sin(T * 50) * (lt < 1.2), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.06))
    rays(ctx, W / 2, 600, T, YELLOW, 0.06)
    ph = (lt * 2.5) % 1
    fighter(ctx, 330, 680, 1.15, T, CYAN, 1, punch=1 if ph < 0.5 else 0.3)
    fighter(ctx, 760, 680, 1.15, T, MAGENTA, -1, hit=0.7)
    impact(ctx, 600, 590, 100, T, 1.0 if ph < 0.5 else 0.4)
    hits_counter(ctx, 1 if lt < 0.5 else 2, W / 2, 390, pop(lt, 0.0), 190)
    hud(ctx, T, TAG, YELLOW)


# 22.24 "In other words, Street Fighter II let you hit faster than the game was built for."  (2.º gancho)
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.06, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, ORANGE, 0.08)
    speedometer(ctx, W / 2, 620, 300, min(1.0, lt / 1.2), "HIT SPEED", pop(lt, 0.0))
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "FASTER THAN THE GAME", W / 2, 1400, clamp((lt - 0.9) / 0.25), ORANGE, size=58, rot=-0.06)


# 26.42 "The team kept it, thinking the timing was too hard for most players."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_blueprint(ctx, T)
    x0, x1, y = 160, 920, 600
    rrect(ctx, x0, y - 40, x1 - x0, 80, 40); fill(ctx, (0.12, 0.14, 0.24))
    rrect(ctx, 610, y - 40, 34, 80, 8); fill(ctx, LIME)
    cur = x0 + (x1 - x0) * (0.5 + 0.5 * math.sin(T * 5))
    ctx.rectangle(cur - 5, y - 70, 10, 140); fill(ctx, WHITE)
    text(ctx, "TIMING WINDOW", W / 2, 470, 50, WHITE, font="Anton")
    icon(ctx, "✅", W / 2, 800, 140, pop(lt, 0.0))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "KEPT: \"TOO HARD TO FIND\"", W / 2, 1400, pop(lt, 0.4), size=48, rgb=LIME)


# 29.59 "They were wrong."
def e12(ctx, lt, dur, T):
    camera(ctx, 1.05 + 0.012 * math.sin(T * 50), W / 2, 960)
    bg_dark(ctx, T)
    stamp(ctx, "WRONG", W / 2, 680, clamp(lt / 0.2), RED, size=150, rot=-0.1)
    hud(ctx, T, TAG, RED)


# 30.39 "Arcade players found it fast and started chaining hits together."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 0.97)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16))
    for i, x in enumerate((200, 540, 880)):
        cabinet(ctx, x, 760, 0.42, T, "COMBO!", lambda c, i=i: text(c, str(2 + int(lt * 3) + i), 0, 0, 120,
                                                                  YELLOW, font="Bangers"), (VIOLET, MAGENTA, CYAN)[i])
    hits_counter(ctx, min(9, 2 + int(lt * 2.5)), W / 2, 390, pop(lt, 0.0), 150)
    hud(ctx, T, TAG, MAGENTA)


# 33.62 "Later versions of Street Fighter II even counted your combo on screen."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, W / 2, 630, 700, 480, T, lambda c: (
        fighter(c, W / 2 - 140, 730, 0.7, T, CYAN, 1, punch=0.5 + 0.5 * math.sin(T * 8)),
        fighter(c, W / 2 + 150, 730, 0.7, T, MAGENTA, -1, hit=0.5),
        hits_counter(c, 3 + int(lt * 1.5), W / 2 - 160, 480, 1.0, 90)))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "ON-SCREEN COMBO COUNTER", W / 2, 1400, pop(lt, 0.3), size=50, rgb=YELLOW)


# 37.18 "Now almost every fighting game has combos,"
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.97)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    for r in range(2):
        for c in range(3):
            k = r * 3 + c
            p = clamp((lt - k * 0.07) / 0.3)
            if p > 0:
                x, y = 220 + c * 320, 480 + r * 300
                ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
                crt(ctx, 0, 0, 240, 190, T, lambda cc, k=k: hits_counter(cc, 3 + k * 2, -20, 0, 1.0, 70))
                ctx.restore()
    hud(ctx, T, TAG, CYAN)


# 39.44 "all because" -> vuelve a e1 (bucle)
def e16(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.08), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.20, e2), (4.18, e3), (6.38, e4), (9.35, e5), (12.20, e6), (14.68, e7), (17.61, e8),
           (19.70, e9), (22.24, e10), (26.42, e11), (29.59, e12), (30.39, e13), (33.62, e14), (37.18, e15),
           (39.44, e16)]
SFX = [(4.20, "pop"), (19.72, "ding"), (22.25, "ding"), (29.60, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.14, 0.03, 0.06))
    rays(ctx, W / 2, 1200, 1.0, ORANGE, 0.06)
    fighter(ctx, 330, 1350, 2.0, 0.0, CYAN, 1, punch=1)
    fighter(ctx, 790, 1350, 2.0, 0.0, MAGENTA, -1, hit=0.6)
    impact(ctx, 600, 1180, 150, 0.0)
    thumb_circle(ctx, 600, 1180, 220, 180)
    thumb_arrow(ctx, 120, 1900, 450, 1300)
    thumb_vignette(ctx)
    thumb_text(ctx, [("THIS MOVE", WHITE), "WAS A BUG"], y=330)
