"""Behind the HUD · 007 (EN) — Adventure's secret room: the first famous easter egg (formato bucle).
Consola, cartucho y habitaciones genéricas dibujadas por el canal; sin sprites ni arte original de Atari."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 007"
SUBTITULO = subtitulo_hud
RAINBOW = [RED, ORANGE, YELLOW, LIME, CYAN, VIOLET, MAGENTA]


def egg(ctx, x, y, s, T, a=1.0, glow_on=True):
    """Huevo decorado (diseño propio)."""
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow_on:
        glow(ctx, 0, 0, 260, YELLOW, 0.25 * a)
    ctx.save(); ctx.scale(1.0, 1.3); circle(ctx, 0, 0, 120); ctx.restore()
    fill_keep(ctx, (0.98, 0.95, 0.88), a); stroke(ctx, (0.1, 0.1, 0.1), 6, a)
    ctx.save(); ctx.scale(1.0, 1.3); circle(ctx, 0, 0, 120); ctx.restore(); ctx.clip()
    for k, c in enumerate((MAGENTA, CYAN, LIME)):
        yy = -70 + k * 70
        ctx.move_to(-140, yy)
        for j in range(8):
            ctx.line_to(-140 + j * 40 + 20, yy + (18 if j % 2 == 0 else -18))
        stroke(ctx, c, 16, a)
    ctx.restore()


def wood_console(ctx, x, y, s):
    """Consola genérica de los 70 (caja negra con franja de madera)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-300, 80); ctx.line_to(-260, -40); ctx.line_to(260, -40); ctx.line_to(300, 80); ctx.close_path()
    fill(ctx, (0.10, 0.10, 0.12))
    ctx.rectangle(-300, 80, 600, 60); fill(ctx, (0.55, 0.33, 0.16))
    for k in range(6):
        ctx.move_to(-300, 90 + k * 9); ctx.curve_to(-100, 84 + k * 9, 100, 96 + k * 9, 300, 90 + k * 9)
        stroke(ctx, (0.42, 0.24, 0.10), 2)
    rrect(ctx, -110, -60, 220, 40, 6); fill(ctx, (0.05, 0.05, 0.06))
    for k in range(4):
        rrect(ctx, -250 + k * 40, -10, 24, 40, 4); fill(ctx, STEEL)
    ctx.restore()


def game_box(ctx, x, y, s, T, title="ADVENTURE", credits_crossed=0.0):
    """Caja de juego genérica con hueco de créditos vacío."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -300, 460, 600, 18); fill(ctx, (0.85, 0.20, 0.18))
    rrect(ctx, -200, -270, 400, 360, 12); fill(ctx, (0.10, 0.12, 0.25))
    for k in range(3):
        ctx.move_to(-200, 30 - k * 60); ctx.line_to(-60 + k * 90, -120 - k * 40); ctx.line_to(200, 60 - k * 50)
        ctx.line_to(200, 90); ctx.line_to(-200, 90); ctx.close_path(); fill(ctx, (0.20 + k * 0.08, 0.25, 0.45))
    text(ctx, title, 0, 150, 70, WHITE, font="Anton")
    rrect(ctx, -160, 205, 320, 60, 10); stroke(ctx, WHITE, 4, 0.8)
    text(ctx, "PROGRAMMER: ???", 0, 237, 30, WHITE, font="Anton", shadow=False, a=0.8)
    ctx.restore()
    x_mark(ctx, x, y + 237 * s, 60 * s, credits_crossed, w=14)


def rooms(ctx, cx, cy, w, h, T, lit=0.0, dot=None, text_on=0.0):
    """Mapa de habitaciones genérico (bloques) para la sala secreta."""
    col = (0.35, 0.65, 0.95)
    th = 22
    ctx.rectangle(cx - w / 2, cy - h / 2, w, th); fill(ctx, col)
    ctx.rectangle(cx - w / 2, cy + h / 2 - th, w, th); fill(ctx, col)
    ctx.rectangle(cx - w / 2, cy - h / 2, th, h); fill(ctx, col)
    ctx.rectangle(cx + w / 2 - th, cy - h / 2, th, h * 0.35); fill(ctx, col)
    ctx.rectangle(cx + w / 2 - th, cy + h * 0.15, th, h * 0.35); fill(ctx, col)
    if lit > 0:
        ctx.rectangle(cx + w / 2 - th, cy - h * 0.15, th, h * 0.3); fill(ctx, col, 1 - lit)
    if dot:
        dx, dy = dot
        circle(ctx, dx, dy, 6); fill(ctx, (0.75, 0.75, 0.78))
        circle(ctx, dx, dy, 34); stroke(ctx, YELLOW, 4, 0.6 + 0.4 * math.sin(T * 8))
    if text_on > 0:
        for i, ch in enumerate("CREATED BY"):
            text(ctx, ch, cx - 60, cy - h / 2 + 50 + i * 30, 28,
                 RAINBOW[(i + int(T * 12)) % 7], a=text_on, font="Press Start 2P", shadow=False)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): el huevo en la sala secreta."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16))
    rays(ctx, W / 2, 560, T, YELLOW, 0.06)
    egg(ctx, W / 2, 560, 1.4 + 0.03 * math.sin(T * 3), T)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "THE FIRST FAMOUS EASTER EGG", W / 2, 1420, 1.0, size=46, rgb=YELLOW)


# 0.03 "The first famous video game easter egg"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 2.90 "was a programmer's secret revenge."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    character(ctx, W / 2, 560, 0.8, T, mood="normal", look=(-0.3, 0.1))
    icon(ctx, "🤫", W / 2 + 240, 330, 150, pop(lt, 0.2))
    hud(ctx, T, TAG, MAGENTA)
    stamp(ctx, "SECRET REVENGE", W / 2, 1400, clamp((lt - 0.4) / 0.25), MAGENTA, size=62, rot=-0.06)


# 4.54 "And it's real. In 1980,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 400, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.8, 1970, 1980, 0.5) if lt > 0.8 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.8))


# 6.35 "Warren Robinett made Adventure for the Atari 2600."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16), floor=False)
    wood_console(ctx, W / 2, 740, 1.15 * max(pop(lt, 0.0), 0.01))
    cartridge(ctx, W / 2, 500, 0.8 * max(pop(lt, 0.5), 0.01), 0.04 * math.sin(T * 2), label="ADVENTURE",
              col=(0.12, 0.12, 0.14))
    hud(ctx, T, TAG, ORANGE)
    ficha(ctx, "WARREN ROBINETT", "PROGRAMMER · ATARI", W / 2, 1420, pop(lt, 0.2), "🧙", ORANGE)


# 9.40 "It sold about a million copies."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 560, T, LIME, 0.05)
    v = int(counter(lt, 0, 1000000, 1.0))
    big_number(ctx, f"{v:,}", W / 2, 520, 190, LIME, pop(lt, 0.0))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "COPIES SOLD (ABOUT)", W / 2, 1400, pop(lt, 0.3), size=52, rgb=LIME)


# 10.98 "But Atari had a rule. Programmers got no credit."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    rrect(ctx, W / 2 - 280, 300, 560, 580, 20); fill(ctx, (0.95, 0.93, 0.86))
    text(ctx, "COMPANY RULES", W / 2, 365, 54, (0.15, 0.15, 0.2), font="Anton", shadow=False)
    for k in range(5):
        ctx.rectangle(W / 2 - 220, 430 + k * 70, 440 - (k % 2) * 120, 16); fill(ctx, (0.6, 0.6, 0.6))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "NO CREDIT", W / 2, 640, clamp((lt - 1.2) / 0.25), RED, size=90)


# 13.82 "No names on the box. Nowhere."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.12)]), W / 2, 960)
    bg_dark(ctx, T)
    game_box(ctx, W / 2, 610, 0.8 * max(pop(lt, 0.0), 0.01), T, credits_crossed=clamp((lt - 0.5) / 0.4))
    hud(ctx, T, TAG, RED)
    pill(ctx, "NO NAMES. NOWHERE.", W / 2, 1400, pop(lt, 1.1), size=54, rgb=RED)


# 15.49 "Atari didn't want star programmers asking for more money."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02), floor=False)
    icon(ctx, "⭐", 330, 520, 260, pop(lt, 0.0), 0.2 * math.sin(T * 2))
    arrow(ctx, 480, 520, 600, 520, clamp((lt - 0.4) / 0.4), YELLOW, 14)
    icon(ctx, "💰", 760, 520, 280, pop(lt, 0.7))
    x_mark(ctx, 760, 520, 150, clamp((lt - 1.4) / 0.4))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "NO STARS = NO RAISES", W / 2, 1400, pop(lt, 0.4), size=52, rgb=YELLOW)


# 18.16 "So Robinett hid his name inside the game."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, W / 2, 590, 700, 480, T, lambda c: (rooms(c, W / 2, 590, 560, 360, T),
                                                text(c, "?", W / 2, 590, 120, YELLOW, a=0.5 + 0.5 * math.sin(T * 5),
                                                     font="Press Start 2P", shadow=False)))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "WARREN ROBINETT", "HIDES HIS NAME", W / 2, 1420, pop(lt, 0.2), "🧙", CYAN)


# 20.73 "A one-pixel dot, carried into a secret room, revealed one line."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 960)
    bg_dark(ctx, T)
    p = ease(clamp((lt - 0.8) / 1.6))
    dx = lerp(W / 2 - 180, W / 2 + 250, p)
    crt(ctx, W / 2, 590, 700, 480, T, lambda c: rooms(c, W / 2, 590, 560, 360, T, lit=clamp((lt - 1.0) / 0.6),
                                                      dot=(dx, 590)))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "1 PIXEL → SECRET ROOM", W / 2, 1400, pop(lt, 0.3), size=52, rgb=YELLOW)


# 24.17 "Created by Warren Robinett."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    def inner(c):
        for i, line in enumerate(("CREATED", "BY", "WARREN", "ROBINETT")):
            text(c, line, W / 2, 440 + i * 100, 50, RAINBOW[(i + int(T * 10)) % 7],
                 a=pop(lt, i * 0.25), font="Press Start 2P", shadow=False)
    crt(ctx, W / 2, 590, 700, 480, T, inner)
    hud(ctx, T, TAG, LIME)


# 25.85 "In other words, he smuggled his signature past his own bosses."  (2.º gancho)
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 560, T, MAGENTA, 0.08)
    p = clamp((lt - 0.3) / 1.4)
    ctx.save(); ctx.translate(W / 2 - 300, 560)
    n = int(60 * p)
    for k in range(n):
        x0 = k * 10; x1 = (k + 1) * 10
        ctx.move_to(x0, 60 * math.sin(k * 0.55) * (1 if k % 7 else -0.4))
        ctx.line_to(x1, 60 * math.sin((k + 1) * 0.55) * (1 if (k + 1) % 7 else -0.4))
        stroke(ctx, WHITE, 10)
    ctx.restore()
    icon(ctx, "✍️", W / 2 - 300 + 600 * p, 520, 140, 1.0)
    hud(ctx, T, TAG, MAGENTA)
    stamp(ctx, "SMUGGLED PAST THE BOSSES", W / 2, 1400, clamp((lt - 1.2) / 0.25), MAGENTA, size=54, rot=-0.05)


# 29.32 "By the time a fifteen-year-old player found it and wrote to Atari,"
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.16))
    big_number(ctx, "15", 300, 520, 300, CYAN, pop(lt, 0.0))
    text(ctx, "YEARS OLD", 300, 730, 54, WHITE, font="Anton", a=pop(lt, 0.2))
    p = ease(clamp((lt - 1.0) / 1.2))
    icon(ctx, "✉️", lerp(560, 860, p), 520 - 120 * math.sin(p * math.pi), 200, pop(lt, 0.8), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "A LETTER TO ATARI", W / 2, 1400, pop(lt, 0.9), size=52, rgb=CYAN)


# 32.26 "Robinett had already quit."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "🚪", W / 2, 520, 360, pop(lt, 0.0))
    hud(ctx, T, TAG, ORANGE)
    ficha(ctx, "WARREN ROBINETT", "ALREADY GONE FROM ATARI", W / 2, 1420, pop(lt, 0.1), "🧙", ORANGE)


# 33.53 "At Atari, they called it an easter egg, and the name stuck."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16))
    rays(ctx, W / 2, 560, T, YELLOW, 0.05)
    egg(ctx, W / 2, 540, 1.2 * max(pop(lt, 0.2), 0.01), T)
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "EASTER EGG", W / 2, 1400, clamp((lt - 0.9) / 0.25), YELLOW, size=72, rot=-0.06)


# 36.64 "Today, almost every big game hides one."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.97)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    for r in range(2):
        for c in range(3):
            k = r * 3 + c
            p = clamp((lt - k * 0.08) / 0.3)
            if p > 0:
                x, y = 220 + c * 320, 400 + r * 320
                ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
                crt(ctx, 0, 0, 240, 190, T, lambda cc: egg(cc, 0, 0, 0.45, T, glow_on=False))
                ctx.restore()
    hud(ctx, T, TAG, CYAN)


# 38.59 "And they all trace back to" -> vuelve a e1 (bucle)
def e17(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.1), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.90, e2), (4.54, e3), (6.35, e4), (9.40, e5), (10.98, e6), (13.82, e7), (15.49, e8),
           (18.16, e9), (20.73, e10), (24.17, e11), (25.85, e12), (29.32, e13), (32.26, e14), (33.53, e15),
           (36.64, e16), (38.59, e17)]
SFX = [(4.56, "pop"), (12.3, "pop"), (24.19, "ding"), (25.86, "ding"), (34.4, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.08, 0.04, 0.16))
    rays(ctx, W / 2, 1180, 1.0, YELLOW, 0.06)
    egg(ctx, W / 2, 1200, 2.3, 1.0)
    thumb_circle(ctx, W / 2, 1200, 360, 420)
    thumb_arrow(ctx, 920, 1880, W / 2 + 250, 1520)
    thumb_vignette(ctx)
    thumb_text(ctx, [("HE HID THIS", WHITE), "FROM HIS BOSS"], y=330)
