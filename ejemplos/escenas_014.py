"""Behind the HUD · 014 (EN) — 3 GTA 6 Facts You Didn't Know (Part 2). Formato lista.
Todo dibujado por el canal (tele genérica, servidores, calendario); sin logos, personajes ni arte de Rockstar.
Datos: hackeo de 2022 con un Fire Stick en la tele de un hotel y 90 clips filtrados (BBC vía Kotaku, NME, GamesRadar);
tráiler 1 filtrado un día antes y publicado al momento, 90 M de vistas en 24 h, récord Guinness (Push Square, PC Gamer, TechCrunch);
retrasos: otoño 2025 -> 26/05/2026 -> 19/11/2026 (Take-Two / Rockstar; PC Gamer, VGC, TechRadar)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 014-L"
SUBTITULO = subtitulo_hud
PINK = (1.0, 0.35, 0.65)
TEAL = (0.20, 0.85, 0.80)
LIME = (0.72, 1.0, 0.0)


# ---------- piezas ----------
def stick(ctx, x, y, s=1.0, glow_a=0.0):
    """Stick de streaming genérico (sin marca) enchufado de lado."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, 0, -22, 120, 44, 12); fill(ctx, (0.08, 0.08, 0.10))
    rrect(ctx, -26, -12, 30, 24, 4); fill(ctx, (0.55, 0.55, 0.60))
    circle(ctx, 96, 0, 6); fill(ctx, LIME, 0.5 + 0.5 * glow_a)
    ctx.restore()


def hotel_tv(ctx, x, y, s, T, screen="GTA 6", hacked=1.0, stick_in=1.0, dresser=True, stick_s=1.0):
    """Tele de habitación de hotel en una cómoda, con el stick enchufado."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # cómoda
    if dresser:
        rrect(ctx, -330, 250, 660, 120, 14); fill(ctx, (0.30, 0.18, 0.12))
        ctx.rectangle(-330, 290, 660, 6); fill(ctx, (0.20, 0.11, 0.07))
    rrect(ctx, -40, 205, 80, 50, 6); fill(ctx, (0.12, 0.12, 0.14))
    # tele
    rrect(ctx, -300, -200, 600, 400, 22); fill(ctx, (0.06, 0.06, 0.08))
    rrect(ctx, -280, -182, 560, 348, 10); fill(ctx, (0.05, 0.10, 0.12))
    g = 0.5 + 0.5 * math.sin(T * 9)
    ctx.save(); rrect(ctx, -280, -182, 560, 348, 10); ctx.clip()
    for k in range(14):
        yy = -182 + ((k * 31 + T * 220) % 348)
        ctx.rectangle(-280, yy, 560, 4); fill(ctx, (0.3, 1.0, 0.8), 0.06)
    text(ctx, screen, 0, -40, 120, WHITE, font="Anton")
    if hacked > 0:
        off = 8 * math.sin(T * 37)
        text(ctx, "HACKED", off, 90, 92, RED, a=hacked * (0.75 + 0.25 * g), font="Anton")
        text(ctx, "HACKED", -off, 92, 92, TEAL, a=hacked * 0.35, font="Anton", shadow=False)
    ctx.restore()
    circle(ctx, 250, 180, 6); fill(ctx, RED)
    # stick enchufado en el lateral derecho
    if stick_s > 1.0:
        circle(ctx, 300 + 60 * stick_s, 60, 70 * stick_s); stroke(ctx, LIME, 6, 0.4 + 0.4 * g)
    stick(ctx, 300 + 40 * stick_s * (1 - stick_in), 60, stick_s, g)
    ctx.restore()


def hoodie(ctx, x, y, s, T, a=1.0):
    """Silueta genérica de hacker con capucha (no es nadie real)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-170, 260); ctx.curve_to(-170, 60, -120, -10, -90, -30)
    ctx.curve_to(-120, -120, -80, -230, 0, -235); ctx.curve_to(80, -230, 120, -120, 90, -30)
    ctx.curve_to(120, -10, 170, 60, 170, 260); ctx.close_path(); fill(ctx, (0.05, 0.05, 0.08), a)
    ellipse(ctx, 0, -110, 62, 78); fill(ctx, (0.0, 0.0, 0.0), a)
    for dx in (-24, 24):
        circle(ctx, dx, -112, 9); fill(ctx, LIME, a * (0.7 + 0.3 * math.sin(T * 5)))
    ctx.restore()


def laptop(ctx, x, y, s, T, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -170, -230, 340, 220, 14); fill(ctx, (0.15, 0.16, 0.22), a)
    rrect(ctx, -152, -214, 304, 188, 8); fill(ctx, (0.02, 0.06, 0.04), a)
    for k in range(6):
        w = 60 + (k * 53 + int(T * 8) * 17) % 200
        ctx.rectangle(-136, -198 + k * 28, w, 12); fill(ctx, LIME, a * 0.8)
    ctx.move_to(-210, 0); ctx.line_to(210, 0); ctx.line_to(180, -10); ctx.line_to(-180, -10); ctx.close_path()
    fill(ctx, (0.25, 0.26, 0.32), a)
    ctx.restore()


def server(ctx, x, y, s, T, broken=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, -260, 300, 520, 18); fill(ctx, (0.10, 0.11, 0.16))
    for r in range(7):
        rrect(ctx, -126, -236 + r * 70, 252, 54, 8); fill(ctx, (0.17, 0.18, 0.25))
        for c in range(4):
            on = (math.sin(T * 7 + r * 1.7 + c * 2.3) > 0)
            col = RED if broken > 0.5 else GREEN
            circle(ctx, -96 + c * 26, -209 + r * 70, 7); fill(ctx, col, 0.9 if on else 0.25)
        ctx.rectangle(20, -214 + r * 70, 90, 10); fill(ctx, (0.30, 0.32, 0.40))
    ctx.restore()


def padlock(ctx, x, y, s, open_p=0.0, rgb=YELLOW):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.translate(55, -20); ctx.rotate(-0.9 * open_p); ctx.translate(-55, 20)
    ctx.arc(0, -40, 55, math.pi, 0); stroke(ctx, (0.75, 0.76, 0.80), 22)
    ctx.move_to(-55, -40); ctx.line_to(-55, -10); stroke(ctx, (0.75, 0.76, 0.80), 22)
    ctx.restore()
    ctx.move_to(55, -40); ctx.line_to(55, -10); stroke(ctx, (0.75, 0.76, 0.80), 22)
    rrect(ctx, -90, -20, 180, 150, 18); fill(ctx, rgb)
    circle(ctx, 0, 40, 18); fill(ctx, (0.1, 0.1, 0.1))
    ctx.restore()


def clip_tile(ctx, x, y, w, h, a=1.0, col=PINK):
    rrect(ctx, x, y, w, h, 6); fill(ctx, (0.12, 0.10, 0.18), a)
    ctx.move_to(x + w * 0.40, y + h * 0.28); ctx.line_to(x + w * 0.66, y + h * 0.5); ctx.line_to(x + w * 0.40, y + h * 0.72)
    ctx.close_path(); fill(ctx, col, a)


def video_card(ctx, x, y, s, T, title="TRAILER 1", progress=None, a=1.0):
    """Reproductor genérico (no es el logo de ninguna web)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -320, -200, 640, 400, 26); fill(ctx, (0.08, 0.08, 0.12), a)
    sunset_mini(ctx, T, a)
    ctx.move_to(-40, -60); ctx.line_to(60, 0); ctx.line_to(-40, 60); ctx.close_path(); fill(ctx, WHITE, 0.92 * a)
    text(ctx, title, 0, -150, 50, WHITE, a=a, font="Anton")
    if progress is not None:
        rrect(ctx, -280, 150, 560, 16, 8); fill(ctx, (0.3, 0.3, 0.35), a)
        rrect(ctx, -280, 150, 560 * clamp(progress), 16, 8); fill(ctx, PINK, a)
    ctx.restore()


def sunset_mini(ctx, T, a=1.0):
    ctx.save(); rrect(ctx, -300, -180, 600, 360, 18); ctx.clip()
    g = vgrad(ctx, 0, -180, 0, 180, [(0, (0.25, 0.06, 0.35)), (0.55, (1.0, 0.45, 0.45)), (0.56, (0.10, 0.04, 0.18)), (1, (0.06, 0.03, 0.10))])
    ctx.rectangle(-300, -180, 600, 360); ctx.set_source(g); ctx.paint_with_alpha(a)
    circle(ctx, 0, 20, 90); fill(ctx, (1.0, 0.82, 0.40), 0.85 * a)
    ctx.restore()


def calendar(ctx, x, y, s, top, big, small, col=RED, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * appear, s * appear)
    rrect(ctx, -160, -170, 320, 340, 24); fill(ctx, WHITE)
    rrect(ctx, -160, -170, 320, 90, 24); fill(ctx, col)
    ctx.rectangle(-160, -110, 320, 30); fill(ctx, col)
    text(ctx, top, 0, -125, 46, WHITE, font="Anton", shadow=False)
    text(ctx, big, 0, 20, 140, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    text(ctx, small, 0, 130, 34, (0.4, 0.4, 0.45), font="Anton", shadow=False)
    ctx.restore()


# ---------- escenas ----------
def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): la tele del hotel hackeada."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.12), floor=False)
    rays(ctx, W / 2, 620, T, RED, 0.05)
    hotel_tv(ctx, W / 2 + 50, 600, 0.95, T)
    hoodie(ctx, 190, 770, 0.68, T)
    hud(ctx, T, TAG, RED)
    pill(ctx, "GTA 6 · REAL HACK · 2022", W / 2, 1400, 1.0, size=48, rgb=RED)


# 0.00 "GTA 6 got hacked by a teenager"
def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


# 1.50 "...using a hotel TV."  (primer corte ~1,5 s)
def e_hook2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.12), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.12), floor=False)
    rays(ctx, W / 2, 620, T, RED, 0.06)
    hotel_tv(ctx, W / 2 - 50, 620, 1.18, T, dresser=False)
    hud(ctx, T, TAG, RED)
    pill(ctx, "A HOTEL TV", W / 2, 1400, pop(lt, 0.4), size=60, rgb=YELLOW)


# 3.59 "Here are three more GTA 6 facts you didn't know."
def l_intro(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    rays(ctx, W / 2, 620, T, PINK, 0.05)
    for i in range(3):
        big_number(ctx, str(i + 1), 250 + i * 290, 620, 230, (PINK, YELLOW, TEAL)[i], pop(lt, 0.1 + i * 0.2))
    badge(ctx, "PART 2", W / 2, 400, pop(lt, 0.0), size=70, bg=PINK)
    hud(ctx, T, TAG, PINK)
    pill(ctx, "GTA 6 FACTS YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=50, rgb=PINK)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 440, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 690, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


# 6.65 "In 2022, a hacker out on bail"
def e_bail(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_dark(ctx, T)
    calendar(ctx, 300, 560, 0.85, "SEPT", "2022", "THE LEAK", RED, pop(lt, 0.0))
    hoodie(ctx, 760, 760, 0.95, T, a=clamp(lt / 0.3 + 0.2))
    laptop(ctx, 760, 890, 0.7, T, a=clamp((lt - 0.4) / 0.3))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "OUT ON BAIL", W / 2, 1400, clamp((lt - 1.4) / 0.25), YELLOW, size=70, rot=-0.06)


# 8.92 "plugged a Fire Stick into his hotel TV,"
def e_plug(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.05, 0.10), floor=False)
    hotel_tv(ctx, W / 2 - 110, 620, 0.95, T, screen="NO SIGNAL", hacked=0.0, dresser=False,
             stick_in=ease(clamp((lt - 0.4) / 0.6)), stick_s=1.7)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "STREAMING STICK + HOTEL TV", W / 2, 1400, pop(lt, 0.2), size=48, rgb=LIME)


# 11.14 "broke into Rockstar,"
def e_break(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]) + 0.012 * math.sin(T * 50) * (0.4 < lt < 0.7), W / 2, 960)
    bg_blueprint(ctx, T)
    server(ctx, 300, 640, 0.85, T, broken=1.0 if lt > 0.5 else 0.0)
    server(ctx, 780, 640, 0.85, T + 1, broken=1.0 if lt > 0.6 else 0.0)
    padlock(ctx, W / 2, 610, 0.9, ease(clamp((lt - 0.3) / 0.4)), RED if lt > 0.5 else YELLOW)
    hud(ctx, T, TAG, RED)
    pill(ctx, "ROCKSTAR'S SYSTEMS", W / 2, 1400, pop(lt, 0.0), size=56, rgb=RED)


# 12.33 "and leaked ninety clips of GTA 6."
def e_clips(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.03)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.12), floor=False)
    n = int(clamp(lt / 1.3) * 90)
    for i in range(90):
        r, c = divmod(i, 10)
        clip_tile(ctx, 115 + c * 87, 455 + r * 54, 76, 44, 1.0 if i < n else 0.08, PINK if i % 3 else YELLOW)
    big_number(ctx, str(n), W / 2, 690, 260, WHITE, 1.0 if lt > 0.05 else 0.0)
    hud(ctx, T, TAG, PINK)
    pill(ctx, "CLIPS LEAKED ONLINE", W / 2, 1400, pop(lt, 0.2), size=56, rgb=PINK)


# 15.04 "The first trailer leaked a day early,"
def e_tleak(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.05, 0.14))
    video_card(ctx, W / 2, 640, 1.0, T, "TRAILER 1 · DEC 2023")
    stamp(ctx, "LEAKED", W / 2, 680, clamp((lt - 0.4) / 0.25), RED, size=110, rot=-0.12)
    hud(ctx, T, TAG, RED)
    pill(ctx, "1 DAY EARLY", W / 2, 1400, pop(lt, 1.0), size=60, rgb=YELLOW)


# 16.97 "so Rockstar just dropped it right away."
def e_drop(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    rays(ctx, W / 2, 560, T, PINK, 0.06)
    video_card(ctx, W / 2, 620, 1.0, T, "TRAILER 1", progress=ease(clamp(lt / 0.9)))
    if lt > 0.9:
        badge(ctx, "OUT NOW", W / 2, 885, pop(lt, 0.9), size=70, bg=PINK)
    hud(ctx, T, TAG, PINK)


# 18.50 "It hit ninety million views in twenty-four hours,"
def e_views(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12))
    v = int(counter(lt, 0, 90000000, 1.8))
    big_number(ctx, f"{v:,}", W / 2, 530, 120, TEAL, 1.0)
    text(ctx, "VIEWS", W / 2, 650, 70, WHITE, font="Anton")
    digital_clock(ctx, "24:00", W / 2, 820, 1.2, pop(lt, 0.8), YELLOW)
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "IN 24 HOURS", W / 2, 1400, pop(lt, 0.9), size=60, rgb=TEAL)


# 21.09 "a world record."
def e_record(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (0.3, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 600, T, YELLOW, 0.08)
    icon(ctx, "🏆", W / 2, 640, 440, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "WORLD RECORD", W / 2, 1400, clamp((lt - 0.3) / 0.25), YELLOW, size=76, rot=-0.06)


# 21.95 "In other words, a leak couldn't stop GTA 6 from breaking YouTube."  (2.º gancho: plano más fuerte)
def e_owords(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 600, T, PINK, 0.10)
    video_card(ctx, W / 2, 640, 1.05, T, "GTA 6 · TRAILER 1")
    cr = ease(clamp((lt - 1.6) / 0.4))
    if cr > 0:
        ctx.save(); ctx.translate(W / 2 + 80, 600)
        for ang, L in ((0.3, 260), (1.9, 220), (3.4, 280), (4.6, 200), (5.6, 240)):
            ctx.move_to(0, 0)
            ctx.line_to(L * 0.5 * cr * math.cos(ang + 0.3), L * 0.5 * cr * math.sin(ang + 0.3))
            ctx.line_to(L * cr * math.cos(ang), L * cr * math.sin(ang))
            stroke(ctx, WHITE, 7, 0.9)
        ctx.restore()
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "LEAK? DIDN'T MATTER", W / 2, 1400, clamp((lt - 0.7) / 0.25), YELLOW, size=62, rot=-0.06)


# 26.32 "GTA 6 got delayed twice,"
def e_delay(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    calendar(ctx, 330, 600, 0.9, "GTA 6", "?", "RELEASE DATE", ORANGE, 1.0)
    calendar(ctx, 750, 600, 0.9, "GTA 6", "?", "RELEASE DATE", ORANGE, 1.0)
    x_mark(ctx, 330, 600, 120, clamp((lt - 0.4) / 0.3))
    x_mark(ctx, 750, 600, 120, clamp((lt - 0.9) / 0.3))
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "DELAYED X2", W / 2, 1400, clamp((lt - 1.0) / 0.25), ORANGE, size=76, rot=-0.06)


# 28.10 "from 2025, to May 2026, to November nineteenth."
def e_timeline(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    steps = [(0.2, "FALL", "2025", RED, True), (1.25, "MAY 26", "2026", RED, True), (2.6, "NOV 19", "2026", LIME, False)]
    for i, (t0, top, yr, col, crossed) in enumerate(steps):
        y = 480 + i * 190
        p = pop(lt, t0)
        if p <= 0:
            continue
        rrect(ctx, W / 2 - 340, y - 72, 680, 144, 22); fill(ctx, (0.06, 0.07, 0.14), 0.92 * p)
        text(ctx, top, W / 2 - 150, y, 78, WHITE, a=p, font="Anton")
        text(ctx, yr, W / 2 + 110, y, 78, col, a=p, font="Anton")
        if crossed:
            x_mark(ctx, W / 2 + 270, y, 42, clamp((lt - t0 - 0.5) / 0.25), RED, 12)
        else:
            icon(ctx, "✅", W / 2 + 270, y, 84, pop(lt, t0 + 0.3))
        if i < 2:
            arrow(ctx, W / 2, y + 76, W / 2, y + 116, p, WHITE, 8)
    hud(ctx, T, TAG, LIME)


# 31.65 "And somehow, years before all that," -> vuelve al gancho (bucle)
def e_end(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.50, e_hook2), (3.59, l_intro), (6.15, l_num(1, PINK)), (6.65, e_bail),
           (8.92, e_plug), (11.14, e_break), (12.33, e_clips), (14.51, l_num(2, YELLOW)), (15.04, e_tleak),
           (16.97, e_drop), (18.50, e_views), (21.09, e_record), (21.95, e_owords), (25.65, l_num(3, TEAL)),
           (26.32, e_delay), (28.10, e_timeline), (31.65, e_end)]
HOOK = "GTA 6 HACKED WITH A HOTEL TV"
LISTA = [(6.15, "1/3"), (14.51, "2/3"), (25.65, "3/3")]
COLA = 0.02
SFX = [(6.17, "ding"), (11.6, "pop"), (14.53, "ding"), (21.1, "pop"), (25.67, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.10, 0.03, 0.12), floor=False)
    rays(ctx, W / 2, 1000, 1.0, RED, 0.06)
    hotel_tv(ctx, W / 2 - 90, 1050, 1.25, 0.3)
    thumb_circle(ctx, W / 2 + 330, 1125, 150, 105)
    thumb_arrow(ctx, 130, 1760, W / 2 + 200, 1235)
    thumb_vignette(ctx)
    thumb_text(ctx, [("HACKED WITH", WHITE), "A HOTEL TV?"], y=330)
