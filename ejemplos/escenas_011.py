"""Behind the HUD · 011 (EN) — The Game Boy that survived a Gulf War bombing (formato bucle).
Consola portátil genérica horizontal de diseño propio (no la carcasa real); bloques que caen genéricos; sin logos."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 011"
SUBTITULO = subtitulo_hud
LCD = (0.55, 0.68, 0.35)
LCD_D = (0.20, 0.30, 0.15)


def falling_blocks(c, x0, y0, w, h, T, on=1.0):
    if on <= 0.01:
        return
    cell = w / 8
    rng = np.random.default_rng(7)
    for k in range(10):
        col = int(rng.integers(0, 8)); row = int(rng.integers(5, 10))
        c.rectangle(x0 + col * cell + 2, y0 + h - (10 - row) * cell + 2, cell - 4, cell - 4); fill(c, LCD_D, on)
    fy = ((T * 1.2) % 1) * (h - 3 * cell)
    for dx, dy in ((0, 0), (1, 0), (2, 0), (1, 1)):
        c.rectangle(x0 + (3 + dx) * cell + 2, y0 + fy + dy * cell + 2, cell - 4, cell - 4); fill(c, LCD_D, on)


def handheld(ctx, x, y, s, T, burnt=0.0, on=1.0, rot=0.0):
    """Portátil genérica horizontal. burnt 0..1 = chamuscada; on 0..1 = pantalla encendida."""
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    body = (lerp(0.18, 0.22, burnt), lerp(0.48, 0.18, burnt), lerp(0.58, 0.15, burnt))
    rrect(ctx, -330, -190, 660, 380, 70); fill(ctx, body)
    if burnt > 0:
        rng = np.random.default_rng(3)
        for k in range(14):
            circle(ctx, rng.uniform(-300, 300), rng.uniform(-170, 170), rng.uniform(25, 70))
            fill(ctx, (0.05, 0.04, 0.03), 0.55 * burnt)
    rrect(ctx, -170, -150, 340, 260, 18); fill(ctx, (0.25, 0.25, 0.30))
    scr = (lerp(0.12, LCD[0], on), lerp(0.14, LCD[1], on), lerp(0.10, LCD[2], on))
    ctx.rectangle(-130, -120, 260, 200); fill(ctx, scr)
    falling_blocks(ctx, -130, -120, 260, 200, T, on)
    if on > 0.3:
        glow(ctx, 0, -20, 220, LCD, 0.25 * on)
    circle(ctx, -150, 140, 9); fill(ctx, RED if on > 0.5 else (0.3, 0.1, 0.1))
    dcol = (0.08, 0.08, 0.1)
    ctx.rectangle(-275, -25, 90, 30); fill(ctx, dcol)
    ctx.rectangle(-245, -55, 30, 90); fill(ctx, dcol)
    for bx, by in ((235, -40), (275, 10)):
        circle(ctx, bx, by, 30); fill(ctx, ORANGE if burnt < 0.5 else (0.10, 0.08, 0.08))
    ctx.restore()


def blast(ctx, x, y, r, T, a=1.0):
    for k in range(14):
        ang = k * math.tau / 14
        rr = r * (0.8 + 0.3 * math.sin(T * 30 + k))
        ctx.move_to(x, y); ctx.line_to(x + rr * math.cos(ang), y + rr * math.sin(ang))
        stroke(ctx, ORANGE if k % 2 else YELLOW, 18, a)
    circle(ctx, x, y, r * 0.45); fill(ctx, (1, 0.95, 0.7), a)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): la portátil quemada… encendida."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.06, 0.02))
    rays(ctx, W / 2, 600, T, ORANGE, 0.05)
    handheld(ctx, W / 2, 640, 1.05, T, burnt=1.0, on=1.0, rot=-0.05)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "BOMBED · STILL WORKS", W / 2, 1420, 1.0, size=54, rgb=ORANGE)


# 0.03 "A Game Boy survived a bombing,"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


# 1.97 "and it still turned on."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 960)
    bg_dark(ctx, T)
    handheld(ctx, W / 2, 640, 1.05, T, burnt=1.0, on=clamp((lt - 0.3) / 0.5))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "POWER: ON", W / 2, 1400, pop(lt, 0.6), size=60, rgb=LIME)


# 3.38 "And it's real. In 1991,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 420, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 1.0, 1981, 1991, 0.6) if lt > 1.0 else "", W / 2, 700, 230, YELLOW, pop(lt, 1.0))


# 5.77 "during the Gulf War,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_desert(ctx, T)
    cactus(ctx, 220, 860, 1.0, (0.25, 0.45, 0.25))
    hud(ctx, T, TAG, SAND)
    pill(ctx, "GULF WAR · 1991", W / 2, 1400, pop(lt, 0.1), size=58, rgb=SAND)


# 6.85 "Army medic Stephan Scoggins brought his Game Boy to relax between shifts."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.08, 0.04), floor=False)
    handheld(ctx, W / 2, 660, 0.95 * max(pop(lt, 0.4), 0.01), T, on=1.0, rot=0.05 * math.sin(T * 2))
    icon(ctx, "🩺", 220, 400, 120, pop(lt, 0.2))
    hud(ctx, T, TAG, LIME)
    ficha(ctx, "STEPHAN SCOGGINS", "U.S. ARMY MEDIC", W / 2, 1420, pop(lt, 0.1), "🩺", LIME)


# 10.79 "Then his barracks were hit in a bombing."
def e6(ctx, lt, dur, T):
    shake = 0.015 * math.sin(T * 60) * (lt > 0.5)
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + shake, W / 2, 960)
    bg_desert(ctx, T, night=0.8)
    for k in range(3):
        x = 220 + k * 320
        ctx.move_to(x - 130, 860); ctx.line_to(x - 110, 700); ctx.line_to(x + 110, 700); ctx.line_to(x + 130, 860)
        ctx.close_path(); fill(ctx, (0.40, 0.38, 0.28))
    if lt > 0.5:
        blast(ctx, 540, 680, 300 * ease(clamp((lt - 0.5) / 0.3)), T, clamp(1.4 - (lt - 0.5)))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "BOMBED", W / 2, 1400, clamp((lt - 0.6) / 0.2), RED, size=80)


# 12.87 "The Game Boy's front was scorched and melted, and its buttons were fused."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 960)
    bg_dark(ctx, T)
    handheld(ctx, W / 2, 640, 1.05, T, burnt=clamp(lt / 1.2), on=0.0)
    for k in range(6):
        circle(ctx, 300 + k * 90, 380 - ((T * 120 + k * 60) % 200), 30 + k * 4); fill(ctx, (0.4, 0.4, 0.4), 0.25)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "SCORCHED · MELTED · FUSED", W / 2, 1400, pop(lt, 0.4), size=50, rgb=ORANGE)


# 16.67 "Scoggins sent the wreck to Nintendo."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.05, 0.14), floor=False)
    p = ease(clamp(lt / 1.4))
    icon(ctx, "📦", lerp(220, 860, p), 600 - 220 * math.sin(p * math.pi), 230, 1.0, 0.3 * math.sin(T * 4))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "SHIPPED TO NINTENDO", W / 2, 1400, pop(lt, 0.2), size=54, rgb=CYAN)


# 18.45 "But here's the twist."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 560, T, MAGENTA, 0.05)
    character(ctx, W / 2, 600, 0.8, T, mood="duda", look=(0.3, -0.2))
    icon(ctx, "⚠️", 820, 380, 160, pop(lt, 0.1))
    hud(ctx, T, TAG, MAGENTA)


# 19.48 "When Nintendo tested the Game Boy, it still powered on."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_blueprint(ctx, T)
    handheld(ctx, W / 2, 640, 1.05, T, burnt=1.0, on=clamp((lt - 1.5) / 0.4))
    if lt > 1.5:
        icon(ctx, "⚡", W / 2 + 330, 420, 120, pop(lt, 1.5))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "STILL POWERED ON", W / 2, 1400, pop(lt, 1.6), size=58, rgb=LIME)


# 22.57 "In other words, a handheld toy took a bomb blast and kept playing Tetris."  (2.º gancho)
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, ORANGE, 0.08)
    blast(ctx, W / 2, 600, 420, T, 0.25)
    handheld(ctx, W / 2, 640, 1.055, T, burnt=1.0, on=1.0, rot=0.04 * math.sin(T * 3))
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "BOMB-PROOF?!", W / 2, 1400, clamp((lt - 1.0) / 0.25), YELLOW, size=72, rot=-0.06)


# 26.97 "Nintendo sent Scoggins a brand new Game Boy as a Desert Storm courtesy."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 600, T, LIME, 0.05)
    handheld(ctx, W / 2, 660, 1.0 * max(pop(lt, 0.5), 0.01), T, burnt=0.0, on=1.0)
    icon(ctx, "🎁", 200, 420, 140, pop(lt, 0.1), 0.2 * math.sin(T * 3))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "A FREE REPLACEMENT", W / 2, 1400, pop(lt, 0.3), size=56, rgb=LIME)


# 30.57 "The burned one went on display at Nintendo's New York store, running Tetris for decades."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    ctx.move_to(W / 2 - 80, 260); ctx.line_to(W / 2 - 360, 900); ctx.line_to(W / 2 + 360, 900); ctx.line_to(W / 2 + 80, 260)
    ctx.close_path(); fill(ctx, (1, 0.95, 0.75), 0.10)
    rrect(ctx, W / 2 - 340, 430, 680, 400, 20); stroke(ctx, (0.7, 0.85, 1.0), 6, 0.6)
    handheld(ctx, W / 2, 640, 0.9, T, burnt=1.0, on=1.0)
    icon(ctx, "🗽", 160, 420, 130, pop(lt, 0.2))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "ON DISPLAY · NEW YORK", W / 2, 1400, pop(lt, 0.3), size=54, rgb=CYAN,
         sub="FOR DECADES" if lt > 2.6 else None)


# 34.92 "In 2023, it was finally retired to Nintendo's offices."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.14))
    big_number(ctx, "2023", W / 2, 450, 200, YELLOW, pop(lt, 0.0))
    icon(ctx, "📦", 330, 760, 180, pop(lt, 0.6))
    arrow(ctx, 450, 760, 620, 760, clamp((lt - 1.0) / 0.4), WHITE, 12)
    icon(ctx, "🏢", 760, 760, 200, pop(lt, 1.3))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "RETIRED", W / 2, 1400, pop(lt, 0.4), size=60, rgb=YELLOW)


# 38.46 "Which is why people still say" -> vuelve a e1 (bucle)
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.97, e2), (3.38, e3), (5.77, e4), (6.85, e5), (10.79, e6), (12.87, e7), (16.67, e8),
           (18.45, e9), (19.48, e10), (22.57, e11), (26.97, e12), (30.57, e13), (34.92, e14), (38.46, e15)]
SFX = [(3.40, "pop"), (11.3, "pop"), (21.0, "ding"), (22.58, "ding"), (34.94, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.12, 0.06, 0.02))
    rays(ctx, W / 2, 1200, 1.0, ORANGE, 0.06)
    blast(ctx, W / 2, 1250, 600, 0.0, 0.3)
    handheld(ctx, W / 2, 1250, 1.6, 0.3, burnt=1.0, on=1.0, rot=-0.06)
    thumb_circle(ctx, W / 2, 1210, 330, 260)
    thumb_arrow(ctx, 120, 1900, 380, 1420)
    thumb_vignette(ctx)
    thumb_text(ctx, [("IT SURVIVED", WHITE), "A BOMBING"], y=330)
