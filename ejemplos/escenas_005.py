"""Behind the HUD · 005 (EN) — Pac-Man was first called Puck-Man (formato bucle).
Recreativas genéricas con el nombre en texto liso; sin el personaje, fantasmas, laberinto ni arte original."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 005"
SUBTITULO = subtitulo_hud


def insert_coin(c, x, y, T, txt="INSERT COIN"):
    if int(T * 2) % 2 == 0:
        text(c, txt, x, y, 30, LIME, font="Press Start 2P", shadow=False)
    text(c, "1980", x, y - 70, 40, CYAN, font="Press Start 2P", shadow=False)


def machine(ctx, x, y, s, T, marquee, col=VIOLET):
    cabinet(ctx, x, y, s, T, marquee, lambda c: insert_coin(c, 0, 40, T), col)


def tile(ctx, ch, x, y, size, appear=1.0, rgb=YELLOW, rot=0.0, bg=(0.06, 0.07, 0.14)):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(appear, appear)
    rrect(ctx, -size / 2 + 8, -size / 2 + 12, size, size, size * 0.14); fill(ctx, (0, 0, 0), 0.4)
    rrect(ctx, -size / 2, -size / 2, size, size, size * 0.14); fill_keep(ctx, bg); stroke(ctx, rgb, size * 0.05)
    glow(ctx, 0, 0, size * 0.8, rgb, 0.12)
    text(ctx, ch, 0, size * 0.05, size * 0.72, rgb, font="Anton", shadow=False)
    ctx.restore()


def word_tiles(ctx, word, cy, size, T, rgb=YELLOW, appear=1.0, override=None):
    n = len(word)
    gap = size * 1.08
    x0 = W / 2 - gap * (n - 1) / 2
    for i, ch in enumerate(word):
        a = appear if override is None else override(i)
        tile(ctx, ch, x0 + i * gap, cy + 6 * math.sin(T * 3 + i), size, a, rgb)


def x_mark(ctx, x, y, r, p, rgb=RED, w=26):
    if p <= 0:
        return
    for sgn in (1, -1):
        q = clamp(p * 2 - (0 if sgn == 1 else 1))
        if q > 0:
            ctx.move_to(x - r, y - sgn * r); ctx.line_to(x - r + 2 * r * q, y - sgn * r + sgn * 2 * r * q)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); stroke(ctx, rgb, w)


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


def jaws(ctx, x, y, s, T, speed=8):
    """Mandíbulas genéricas que mastican (concepto 'paku'), dibujo propio."""
    o = 0.5 + 0.5 * math.sin(T * speed)
    gap = lerp(10, 120, o)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sgn in (-1, 1):
        yy = sgn * gap / 2
        rrect(ctx, -260, yy - (150 if sgn < 0 else 0), 520, 150, 60); fill(ctx, (0.85, 0.25, 0.35))
        for k in range(7):
            tx = -210 + k * 70
            if sgn < 0:
                ctx.move_to(tx - 28, yy); ctx.line_to(tx + 28, yy); ctx.line_to(tx, yy + 45)
            else:
                ctx.move_to(tx - 28, yy); ctx.line_to(tx + 28, yy); ctx.line_to(tx, yy - 45)
            ctx.close_path(); fill(ctx, WHITE)
    ctx.restore()


def key(ctx, x, y, s, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    circle(ctx, -110, 0, 60); fill_keep(ctx, (0.85, 0.75, 0.35)); stroke(ctx, (0.4, 0.3, 0.1), 8)
    circle(ctx, -110, 0, 22); fill(ctx, (0.05, 0.05, 0.1))
    ctx.rectangle(-55, -16, 200, 32); fill(ctx, (0.85, 0.75, 0.35))
    for k in (90, 125):
        ctx.rectangle(k, 16, 18, 30); fill(ctx, (0.85, 0.75, 0.35))
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): recreativa genérica con el nombre tachado."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.14))
    rays(ctx, W / 2, 500, T, MAGENTA, 0.05)
    machine(ctx, W / 2, 640, 0.75, T, "PAC-MAN")
    x_mark(ctx, W / 2, 640 - 0.75 * 335, 90, 1.0 if int(T * 3) % 2 == 0 else 0.0, w=20)
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, "NOT ITS FIRST NAME", W / 2, 1420, 1.0, size=50, rgb=MAGENTA)


# 0.03 "Pac-Man wasn't called Pac-Man,"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 1.91 "and the reason is one letter."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    tile(ctx, "?", W / 2, 560, 420, pop(lt, 0.0), YELLOW, 0.08 * math.sin(T * 3))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "ONE LETTER", W / 2, 1400, pop(lt, 0.3), size=56, rgb=YELLOW)


# 3.61 "And it's real. In 1980,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 400, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.8, 1970, 1980, 0.6) if lt > 0.8 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.8))


# 5.38 "Toru Iwatani created a game at Namco in Japan."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    crt(ctx, W / 2, 560, 620, 440, T, lambda c: (
        text(c, "NEW GAME", W / 2, 470, 44, LIME, font="Press Start 2P", shadow=False),
        text(c, "LOADING" + "." * (int(T * 3) % 4), W / 2, 600, 34, CYAN, font="Press Start 2P", shadow=False)))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "NAMCO · JAPAN", W / 2, 230, pop(lt, 0.5), size=48, rgb=RED)
    ficha(ctx, "TORU IWATANI", "GAME DESIGNER · NAMCO", W / 2, 1420, pop(lt, 0.1), "🕹️", CYAN)


# 8.18 "He wanted a game everyone would enjoy, not just war games."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.05, 0.16), floor=False)
    icon(ctx, "👥", W / 2, 450, 300, pop(lt, 0.0))
    icon(ctx, "❤️", W / 2 + 180, 330, 110, pop(lt, 0.4))
    if lt > 1.7:
        p = pop(lt, 1.7)
        for i, emo in enumerate(("🚀", "💥", "🎯")):
            icon(ctx, emo, 300 + i * 240, 790, 150, p)
        x_mark(ctx, W / 2, 790, 300, clamp((lt - 2.1) / 0.5), w=20)
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, "NOT JUST WAR GAMES" if lt > 1.7 else "A GAME FOR EVERYONE", W / 2, 1400, 1.0, size=50, rgb=MAGENTA)


# 11.02 "He called it Puck-Man."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.05, 0.02))
    rays(ctx, W / 2, 560, T, YELLOW, 0.06)
    word_tiles(ctx, "PUCK", 470, 200, T, YELLOW, override=lambda i: pop(lt, i * 0.08))
    word_tiles(ctx, "MAN", 720, 200, T, YELLOW, override=lambda i: pop(lt, 0.35 + i * 0.08))
    hud(ctx, T, TAG, YELLOW)


# 12.06 "The name came from paku, the Japanese word for chomping."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    big_number(ctx, "PAKU", W / 2, 390, 170, YELLOW, pop(lt, 0.0))
    jaws(ctx, W / 2, 680, 0.95 * max(pop(lt, 1.0), 0.01), T, 10)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "PAKU = CHOMP", W / 2, 1400, pop(lt, 0.4), size=58, rgb=YELLOW)


# 14.79 "In May 1980, Puck-Man hit Tokyo arcades."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 0.95)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16))
    for i, x in enumerate((200, 540, 880)):
        p = pop(lt, 0.9 + i * 0.15)
        if p > 0.01:
            machine(ctx, x, 600, 0.58 * p, T, "PUCK-MAN", (VIOLET, MAGENTA, CYAN)[i])
    big_number(ctx, "MAY 1980", W / 2, 300, 150, YELLOW, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "TOKYO ARCADES", W / 2, 1400, pop(lt, 1.0), size=54, rgb=CYAN)


# 17.85 "But here's the problem."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 560, T, MAGENTA, 0.05)
    character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
    icon(ctx, "⚠️", 820, 330, 180, pop(lt, 0.15))
    hud(ctx, T, TAG, MAGENTA)


# 18.80 "An American company, Midway, wanted to bring it to the U.S."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.20), floor=False)
    p = ease(clamp((lt - 0.8) / 1.6))
    ctx.move_to(880, 760); ctx.curve_to(700, 300, 400, 300, 200, 600)
    stroke(ctx, WHITE, 6, 0.4)
    icon(ctx, "🇯🇵", 880, 760, 170, pop(lt, 0.0))
    icon(ctx, "🇺🇸", 200, 600, 190, pop(lt, 1.6))
    icon(ctx, "✈️", lerp(880, 200, p), 760 - 380 * math.sin(p * math.pi) * 0.9 - 160 * p, 150, 1.0,
         lerp(0.6, -0.6, p) + math.pi)
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "MIDWAY", "U.S. ARCADE COMPANY", W / 2, 1420, pop(lt, 0.4), "🇺🇸", CYAN)


# 21.79 "They warned Namco about the name."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_dark(ctx, T)
    machine(ctx, W / 2, 660, 0.75, T, "PUCK-MAN")
    blink = 1.0 if int(T * 4) % 2 == 0 else 0.4
    rrect(ctx, W / 2 - 0.75 * 250, 660 - 0.75 * 410, 0.75 * 500, 0.75 * 150, 16); stroke(ctx, RED, 12, blink * pop(lt, 0.4))
    icon(ctx, "⚠️", 870, 300, 150, pop(lt, 0.3))
    hud(ctx, T, TAG, RED)
    pill(ctx, "WARNING: THE NAME", W / 2, 1400, pop(lt, 0.5), size=52, rgb=RED)


# 23.54 "Kids could scratch the P and turn it into an F."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.04), floor=False)
    tile(ctx, "P", 330, 560, 330, pop(lt, 0.0), YELLOW)
    if 0.5 < lt < 1.8:
        kx = 330 + 70 * math.sin(T * 14); ky = 520 + 60 * math.cos(T * 11)
        key(ctx, kx + 120, ky - 40, 0.9, -0.6)
        for k in range(4):
            ctx.move_to(260 + k * 25, 600 - k * 10); ctx.line_to(330 + k * 25, 640 - k * 10)
            stroke(ctx, WHITE, 4, 0.7)
    arrow(ctx, 540, 560, 700, 560, clamp((lt - 1.6) / 0.3), RED, 14)
    tile(ctx, "F", 850, 560, 260, pop(lt, 1.8), RED, 0.1)
    hud(ctx, T, TAG, RED)
    pill(ctx, "P → F", W / 2, 1400, pop(lt, 1.6), size=64, rgb=RED)


# 26.11 "In other words, one bored kid with a key"  (2.º gancho)
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.06), floor=False)
    rays(ctx, W / 2, 600, T, RED, 0.08)
    key(ctx, W / 2 + 60, 560, 2.2 * max(pop(lt, 0.2), 0.01), -0.35 + 0.1 * math.sin(T * 6))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "ONE KID · ONE KEY", W / 2, 1400, clamp((lt - 0.7) / 0.25), size=60, rot=-0.06)


# 28.20 "could ruin every machine."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 0.95)]) + 0.01 * math.sin(T * 50) * (lt > 0.4), W / 2, 960)
    bg_dark(ctx, T)
    for i, x in enumerate((200, 540, 880)):
        machine(ctx, x, 600, 0.58, T, "PUCK-MAN", (VIOLET, MAGENTA, CYAN)[i])
        x_mark(ctx, x, 600 - 0.58 * 335, 70, clamp((lt - 0.3 - i * 0.15) / 0.3), w=14)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "EVERY MACHINE", W / 2, 1400, clamp((lt - 0.5) / 0.2), size=66)


# 29.83 "So Puck-Man became Pac-Man."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 560, T, LIME, 0.05)
    if lt < 0.9:
        word_tiles(ctx, "PUCK", 460, 190, T, YELLOW)
        x_mark(ctx, W / 2 + 108, 460, 110, clamp((lt - 0.3) / 0.4), w=16)
    else:
        word_tiles(ctx, "PAC", 460, 210, T, LIME, override=lambda i: pop(lt, 0.9 + i * 0.08))
    word_tiles(ctx, "MAN", 720, 190, T, LIME if lt >= 0.9 else YELLOW)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "NEW NAME FOR AMERICA", W / 2, 1400, pop(lt, 0.9), size=50, rgb=LIME)


# 31.70 "It launched in America that October and exploded."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 0.95)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    big_number(ctx, "OCT 1980", W / 2, 300, 150, YELLOW, pop(lt, 0.0))
    for c in range(4):
        p = clamp((lt - 0.6 - c * 0.1) / 0.3)
        if p > 0:
            machine(ctx, 165 + c * 250, 600, 0.42 * p, T, "PAC-MAN", (VIOLET, MAGENTA, CYAN, ORANGE)[c])
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "U.S. LAUNCH · A SMASH HIT", W / 2, 1400, pop(lt, 0.4), size=50, rgb=YELLOW)


# 34.33 "Guinness later named Pac-Man the most successful coin-operated game ever."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 560, T, YELLOW, 0.07)
    rng = np.random.default_rng(2)
    for k in range(16):
        x = rng.uniform(80, 1000); ph = rng.uniform(0, 1200)
        y = -100 + ((T * 420 * rng.uniform(0.7, 1.3) + ph) % 1100)
        icon(ctx, "🪙", x, y, 80, 0.9)
    icon(ctx, "🏆", W / 2, 560, 380, pop(lt, 0.2))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "MOST SUCCESSFUL COIN-OP GAME", W / 2, 1400, pop(lt, 0.8), size=46, rgb=YELLOW,
         sub="GUINNESS WORLD RECORDS")


# 37.70 "And remember, back in Japan," -> vuelve a e1 (bucle)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.1), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.91, e2), (3.61, e3), (5.38, e4), (8.18, e5), (11.02, e6), (12.06, e7), (14.79, e8),
           (17.85, e9), (18.80, e10), (21.79, e11), (23.54, e12), (26.11, e13), (28.20, e14), (29.83, e15),
           (31.70, e16), (34.33, e17), (37.70, e18)]
SFX = [(3.63, "pop"), (11.04, "ding"), (25.15, "pop"), (26.12, "ding"), (30.75, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.10, 0.04, 0.14))
    rays(ctx, W / 2, 1150, 1.0, MAGENTA, 0.06)
    machine(ctx, W / 2, 1250, 1.25, 1.0, "PAC-MAN")
    thumb_circle(ctx, W / 2, 1250 - 1.25 * 335, 360, 150)
    thumb_arrow(ctx, 920, 1900, W / 2 + 230, 860)
    thumb_vignette(ctx)
    thumb_text(ctx, [("ONE LETTER", WHITE), "CHANGED IT"], y=330)
