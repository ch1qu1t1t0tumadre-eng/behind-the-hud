"""Behind the HUD · 004 (EN) — Nintendo started with hand-painted cards in 1889 (formato bucle).
Cartas de flores genéricas dibujadas por el canal; sin logos ni personajes de Nintendo ni de Disney."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 004"
SUBTITULO = subtitulo_hud
CREAM = (0.97, 0.93, 0.84)
CARD_RED = (0.85, 0.15, 0.18)
PALETTE = [CARD_RED, (0.20, 0.55, 0.30), (0.95, 0.70, 0.15), (0.30, 0.35, 0.80), MAGENTA, ORANGE]


def flower_card(ctx, x, y, s, k=0, rot=0.0, a=1.0, back=False):
    """Carta de flores genérica (diseño propio): marco rojo, flor/luna sencilla."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -70 + 6, -110 + 8, 140, 220, 14); fill(ctx, (0, 0, 0), 0.35 * a)
    if back:
        rrect(ctx, -70, -110, 140, 220, 14); fill(ctx, (0.12, 0.10, 0.12), a)
        rrect(ctx, -58, -98, 116, 196, 10); stroke(ctx, CARD_RED, 6, a)
        ctx.restore(); return
    rrect(ctx, -70, -110, 140, 220, 14); fill(ctx, CREAM, a)
    rrect(ctx, -60, -100, 120, 200, 10); stroke(ctx, CARD_RED, 6, a)
    col = PALETTE[k % len(PALETTE)]
    kind = k % 3
    if kind == 0:  # flor de 5 pétalos
        for p in range(5):
            ang = p * math.tau / 5
            circle(ctx, 26 * math.cos(ang), -20 + 26 * math.sin(ang), 20); fill(ctx, col, a)
        circle(ctx, 0, -20, 13); fill(ctx, (0.98, 0.85, 0.2), a)
    elif kind == 1:  # sol rojo sobre hierba
        circle(ctx, 0, -40, 40); fill(ctx, CARD_RED, a)
        for j in range(9):
            xx = -52 + j * 13
            ctx.move_to(xx, 60); ctx.line_to(xx + 6 * math.sin(j), 10 + (j % 3) * 8); stroke(ctx, (0.2, 0.45, 0.25), 5, a)
    else:  # rama con hojas
        ctx.move_to(-40, 70); ctx.curve_to(-10, 20, 10, -20, 30, -70); stroke(ctx, (0.35, 0.22, 0.12), 6, a)
        for j in range(4):
            yy = 50 - j * 36
            ellipse(ctx, -14 + j * 14 + 16, yy, 16, 9); fill(ctx, col, a)
    for j in range(3):
        rrect(ctx, -46 + j * 34, 66, 24, 10, 3); fill(ctx, (0.15, 0.15, 0.15), 0.6 * a)
    ctx.restore()


def fan(ctx, x, y, s, T, n=5, spread=0.22, appear=1.0):
    for i in range(n):
        r = (i - (n - 1) / 2) * spread * appear + 0.02 * math.sin(T * 2 + i)
        ctx.save(); ctx.translate(x, y); ctx.rotate(r)
        flower_card(ctx, 0, -120 * s, s, k=i)
        ctx.restore()


def shop(ctx, x, y, s, T, lit=1.0):
    """Tienda tradicional genérica (madera + tejado + farol)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-300, -120); ctx.line_to(0, -260); ctx.line_to(300, -120); ctx.close_path()
    fill(ctx, (0.22, 0.20, 0.26))
    ctx.move_to(-300, -120); ctx.line_to(0, -260); ctx.line_to(300, -120); stroke(ctx, (0.1, 0.1, 0.12), 10)
    ctx.rectangle(-250, -120, 500, 300); fill(ctx, (0.45, 0.28, 0.16))
    for k in range(-2, 3):
        ctx.rectangle(k * 100 - 4, -120, 8, 300); fill(ctx, (0.30, 0.18, 0.10))
    ctx.rectangle(-150, -40, 300, 220); fill(ctx, (0.98, 0.85, 0.55), 0.35 + 0.4 * lit)
    for i in range(3):
        flower_card(ctx, -80 + i * 80, 60, 0.42, k=i)
    rrect(ctx, -230, -110, 160, 60, 8); fill(ctx, CREAM)
    text(ctx, "CARDS", -150, -78, 34, CARD_RED, font="Anton", shadow=False)
    ctx.move_to(200, -120); ctx.line_to(200, -70); stroke(ctx, (0.1, 0.1, 0.1), 3)
    ellipse(ctx, 200, -30, 30, 42); fill(ctx, CARD_RED)
    glow(ctx, 200, -30, 90, ORANGE, 0.25 * (0.8 + 0.2 * math.sin(T * 6)))
    ctx.restore()


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


def rice_bowl(ctx, x, y, s, a=1.0):
    """Cuenco de arroz dibujado a mano."""
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(7):
        circle(ctx, -90 + k * 30, -20 - 25 * math.sin(k / 6 * math.pi), 38); fill(ctx, (0.98, 0.98, 0.95), a)
    ctx.move_to(-140, -10); ctx.curve_to(-130, 120, 130, 120, 140, -10); ctx.close_path()
    fill(ctx, (0.80, 0.20, 0.20), a)
    ctx.move_to(-140, -10); ctx.line_to(140, -10); stroke(ctx, (0.5, 0.1, 0.1), 8, a)
    ctx.rectangle(-60, 30, 120, 14); fill(ctx, WHITE, 0.5 * a)
    for dx in (-20, 20):
        ctx.move_to(60 + dx, -170); ctx.line_to(-10 + dx, -40); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        stroke(ctx, (0.55, 0.35, 0.18), 10, a)
    ctx.restore()


def taxi(ctx, x, y, s):
    """Taxi genérico de los 60 dibujado a mano."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -200, -40, 400, 110, 30); fill(ctx, (0.98, 0.78, 0.15))
    ctx.move_to(-120, -40); ctx.line_to(-80, -120); ctx.line_to(90, -120); ctx.line_to(130, -40); ctx.close_path()
    fill(ctx, (0.98, 0.78, 0.15))
    for (a0, a1) in ((-105, -10), (10, 112)):
        ctx.move_to(a0, -45); ctx.line_to(a0 + 25, -105); ctx.line_to(a1 - 20, -105); ctx.line_to(a1, -45); ctx.close_path()
        fill(ctx, (0.55, 0.80, 0.95))
    rrect(ctx, -40, -160, 80, 40, 8); fill(ctx, (0.1, 0.1, 0.1))
    text(ctx, "TAXI", 0, -138, 26, YELLOW, font="Anton", shadow=False)
    ctx.rectangle(-200, 10, 400, 14); fill(ctx, (0.1, 0.1, 0.1))
    for wx in (-120, 120):
        circle(ctx, wx, 70, 46); fill(ctx, (0.08, 0.08, 0.08))
        circle(ctx, wx, 70, 20); fill(ctx, STEEL)
    ctx.restore()


def tongs(ctx, x, y, s, ext, T):
    """Brazo extensible de tijera (juguete genérico). ext 0..1."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    n = 5
    seg = lerp(40, 110, ext)
    hgt = lerp(90, 40, ext)
    pts_top, pts_bot = [], []
    for i in range(n + 1):
        xx = -340 + i * seg
        pts_top.append((xx, -hgt if i % 2 == 0 else hgt))
        pts_bot.append((xx, hgt if i % 2 == 0 else -hgt))
    for pts, col in ((pts_top, ORANGE), (pts_bot, CYAN)):
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); stroke(ctx, col, 22)
    for i in range(n + 1):
        circle(ctx, -340 + i * seg, 0, 12); fill(ctx, WHITE)
    # mango
    rrect(ctx, -440, -40, 110, 80, 20); fill(ctx, VIOLET)
    # pinza
    ex = -340 + n * seg
    ctx.move_to(ex, 0); ctx.line_to(ex + 70, -50); stroke(ctx, LIME, 18)
    ctx.move_to(ex, 0); ctx.line_to(ex + 70, 50); stroke(ctx, LIME, 18)
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): abanico de cartas y un 137 gigante."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.06))
    rays(ctx, W / 2, 620, T, CARD_RED, 0.05)
    fan(ctx, W / 2, 900, 1.25, T)
    hud(ctx, T, TAG, CARD_RED)
    big_number(ctx, "137", W / 2, 360, 250, YELLOW, 1.0)
    pill(ctx, "YEARS OLD · BEFORE GAMES", W / 2, 1420, 1.0, size=46, rgb=CARD_RED)


# 0.03 "Nintendo is one hundred thirty-seven years old,"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.68 "and it didn't start with games."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "🎮", W / 2, 560, 400, pop(lt, 0.0))
    x_mark(ctx, W / 2, 560, 230, clamp((lt - 0.35) / 0.5))
    hud(ctx, T, TAG, RED)
    pill(ctx, "NOT GAMES", W / 2, 1400, pop(lt, 0.4), size=56, rgb=RED)


# 4.13 "And it's real. In 1889,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 400, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.75, 1800, 1889, 0.6) if lt > 0.75 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.75))


# 5.95 "Fusajiro Yamauchi opened a tiny shop in Kyoto."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_sky(ctx, T, warm=0.7)
    ground(ctx, 830, (0.22, 0.18, 0.16))
    shop(ctx, W / 2, 650, 1.05 * max(pop(lt, 0.0), 0.01), T)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "KYOTO · 1889", W / 2, 230, pop(lt, 0.4), size=48, rgb=ORANGE)
    ficha(ctx, "FUSAJIRO YAMAUCHI", "FOUNDER · CARD MAKER", W / 2, 1420, pop(lt, 0.1), "🌸", ORANGE)


# 8.70 "He sold hanafuda, Japanese playing cards, painted by hand."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.04), floor=False)
    for i in range(3):
        p = pop(lt, 0.1 + i * 0.25)
        if p > 0.01:
            flower_card(ctx, 260 + i * 280, 560 + 20 * math.sin(T * 2 + i), 1.6 * p, k=i, rot=(i - 1) * 0.12)
    # pincel pintando la última carta
    if lt > 2.0:
        bx = 820 + 30 * math.sin(T * 9); by = 500 + 25 * math.cos(T * 7)
        ctx.move_to(bx, by); ctx.line_to(bx + 140, by - 200); stroke(ctx, (0.45, 0.28, 0.16), 16)
        circle(ctx, bx, by, 14); fill(ctx, CARD_RED)
    hud(ctx, T, TAG, CARD_RED)
    pill(ctx, "HANAFUDA · FLOWER CARDS", W / 2, 1400, pop(lt, 0.2), size=48, rgb=CARD_RED,
         sub="PAINTED BY HAND" if lt > 2.1 else None)


# 11.64 "Nintendo's cards became a hit."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.98)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.06))
    rays(ctx, W / 2, 560, T, YELLOW, 0.05)
    rng = np.random.default_rng(4)
    for k in range(14):
        p = clamp((lt - k * 0.07) / 0.3)
        if p > 0:
            flower_card(ctx, rng.uniform(140, 940), rng.uniform(280, 860), 0.9 * p, k=k, rot=rng.uniform(-0.5, 0.5))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "A HIT IN JAPAN", W / 2, 1400, pop(lt, 0.3), size=56, rgb=YELLOW)


# 13.34 "Decades later, his grandson Hiroshi Yamauchi"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    big_number(ctx, counter(lt, 1889, 1949, 0.9), W / 2, 520, 260, CYAN, pop(lt, 0.0))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "HIROSHI YAMAUCHI", "GRANDSON · PRESIDENT FROM 1949", W / 2, 1420, pop(lt, 0.6), "🌸", CYAN)


# 16.30 "made a deal with Disney to print its characters on cards."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.16), floor=False)
    icon(ctx, "🤝", W / 2, 420, 300, pop(lt, 0.0))
    for i in range(4):
        p = pop(lt, 0.6 + i * 0.15)
        if p > 0.01:
            flower_card(ctx, 240 + i * 200, 760, 1.0 * p, k=i, rot=(i - 1.5) * 0.08, back=True)
            text(ctx, "★", 240 + i * 200, 762, 70, YELLOW, a=p, shadow=False)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "DISNEY CHARACTER CARDS", W / 2, 1400, pop(lt, 0.4), size=50, rgb=YELLOW)


# 18.53 "But here's the weird part. When the card business slowed down,"
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    if lt < 1.05:
        character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
        icon(ctx, "⚠️", 820, 330, 180, pop(lt, 0.1))
    else:
        line_chart(ctx, 150, 330, 780, 520, [0.85, 0.9, 0.95, 0.85, 0.65, 0.45, 0.3, 0.18], progress=clamp((lt - 1.1) / 1.2),
                   title="CARD SALES", color=RED)
    hud(ctx, T, TAG, RED)
    pill(ctx, "CARD MARKET SLOWS DOWN", W / 2, 1400, pop(lt, 1.1), size=48, rgb=RED)


# 21.27 "Nintendo tried everything. A taxi company."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_sky(ctx, T, warm=0.3)
    ground(ctx, 800, (0.25, 0.25, 0.30))
    for k in range(8):
        ctx.rectangle(((k * 180 - T * 600) % 1600) - 200, 860, 100, 14); fill(ctx, WHITE, 0.7)
    p = ease(clamp((lt - 0.9) / 0.9))
    taxi(ctx, lerp(-300, W / 2, p), 680 + 4 * math.sin(T * 30), 1.25)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "TRIED EVERYTHING", W / 2, 260, pop(lt, 0.0), size=52, rgb=MAGENTA)
    pill(ctx, "DAIYA TAXI · 1960s", W / 2, 1400, pop(lt, 1.1), size=50, rgb=YELLOW)


def checklist(ctx, lt, T, items, t0):
    for i, (emo, lab, ti) in enumerate(items):
        p = pop(lt, ti - t0)
        if p > 0.01:
            y = 320 + i * 210
            rrect(ctx, 130, y - 80, 820, 160, 30); fill_keep(ctx, (0.06, 0.07, 0.14), 0.92 * p)
            stroke(ctx, ORANGE, 6, p)
            if emo == "🍚":
                rice_bowl(ctx, 230, y + 15, 0.38 * p, p)
            else:
                icon(ctx, emo, 230, y, 120, p)
            text(ctx, lab, 320, y + 4, 64, WHITE, a=p, font="Anton", align="left")


ITEMS = [("🚕", "TAXI COMPANY", 22.41), ("🍚", "INSTANT RICE", 23.41), ("🧹", "VACUUM CLEANERS", 24.25)]


# 23.41 "Instant rice. Even vacuum cleaners."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.06, 0.02), floor=False)
    ITEMS0 = [(e, l, t if t > 23.0 else 23.41) for (e, l, t) in ITEMS]
    checklist(ctx, lt, T, ITEMS0, 23.41)
    hud(ctx, T, TAG, ORANGE)


# 25.41 "In other words, Nintendo almost became a rice and taxi company."  (2.º gancho)
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, ORANGE, 0.08)
    rice_bowl(ctx, 320, 600, 1.15 * pop(lt, 0.3))
    taxi(ctx, 760, 620, 0.9 * max(pop(lt, 0.5), 0.01))
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "RICE & TAXI CO.?", W / 2, 1400, clamp((lt - 1.0) / 0.25), size=64, rot=-0.06, rgb=ORANGE)


# 28.93 "Most of it failed."
def e13(ctx, lt, dur, T):
    camera(ctx, 1.05 + 0.012 * math.sin(T * 50) * (lt > 0.2), W / 2, 960)
    bg_dark(ctx, T)
    for i, (emo, _, _) in enumerate(ITEMS):
        if emo == "🍚":
            rice_bowl(ctx, 250 + i * 290, 600, 0.7)
        else:
            icon(ctx, emo, 250 + i * 290, 580, 220, 1.0)
        x_mark(ctx, 250 + i * 290, 580, 110, clamp((lt - 0.1 - i * 0.12) / 0.3), w=18)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "FAILED", W / 2, 1400, clamp((lt - 0.3) / 0.2), size=80)


# 29.82 "Then an engineer named Gunpei Yokoi built a toy arm just for fun."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_blueprint(ctx, T)
    ext = 0.5 + 0.5 * math.sin(clamp((lt - 1.0) / 2.2) * math.pi * 2 - math.pi / 2)
    tongs(ctx, W / 2 + 60, 580, 1.1, ext, T)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "EXTENDING TOY ARM", W / 2, 260, pop(lt, 1.5), size=48, rgb=LIME)
    ficha(ctx, "GUNPEI YOKOI", "ENGINEER · MAINTENANCE", W / 2, 1420, pop(lt, 0.1), "🔧", LIME)


# 33.32 "Yamauchi turned it into a hit. Toys led to video games."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 560, T, LIME, 0.05)
    if lt < 1.5:
        tongs(ctx, W / 2 + 60, 440, 0.8, 0.5 + 0.5 * math.sin(T * 5), T)
        meter(ctx, W / 2, 760, 700, clamp(lt / 1.0) * 0.95, "SALES", LIME, pop(lt, 0.0))
    else:
        icon(ctx, "🧸", 260, 560, 240, 1.0)
        arrow(ctx, 420, 560, 660, 560, clamp((lt - 1.6) / 0.4), YELLOW, 16)
        icon(ctx, "🎮", 820, 560, 280, pop(lt, 1.9))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "TOYS → VIDEO GAMES" if lt > 1.5 else "A TOY HIT", W / 2, 1400, 1.0, size=52, rgb=LIME)


# 36.31 "And that card shop became the company behind your favorite games."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 0.95)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16))
    shop(ctx, W / 2, 560, 0.75, T)
    for i, (x, y) in enumerate(((170, 330), (910, 330), (170, 800), (910, 800))):
        p = pop(lt, 0.4 + i * 0.15)
        if p > 0.01:
            ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
            crt(ctx, 0, 0, 220, 160, T, lambda c, k=i: icon(c, ["👾", "🏎️", "🗡️", "🕹️"][k], 0, 0, 110))
            ctx.restore()
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "CARD SHOP → GAME GIANT", W / 2, 1400, pop(lt, 0.2), size=50, rgb=YELLOW)


# 38.40 "Because" -> vuelve a e1 (bucle)
def e17(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.12), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.68, e2), (4.13, e3), (5.95, e4), (8.70, e5), (11.64, e6), (13.34, e7), (16.30, e8),
           (18.53, e9), (21.27, e10), (23.41, e11), (25.41, e12), (28.93, e13), (29.82, e14), (33.32, e15),
           (36.31, e16), (38.40, e17)]
SFX = [(4.15, "pop"), (11.66, "ding"), (25.42, "ding"), (28.95, "pop"), (33.34, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.10, 0.03, 0.06))
    rays(ctx, W / 2, 1150, 1.0, CARD_RED, 0.06)
    fan(ctx, W / 2, 1500, 2.0, 1.0)
    thumb_circle(ctx, W / 2, 1120, 380, 300)
    thumb_arrow(ctx, 900, 1800, W / 2 + 260, 1420)
    thumb_vignette(ctx)
    thumb_text(ctx, [("NINTENDO'S", WHITE), "FIRST PRODUCT?"], y=330)
