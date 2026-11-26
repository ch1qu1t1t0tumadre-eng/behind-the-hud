"""Behind the HUD · 015-L (EN) — 3 GTA 6 Facts You Didn't Know (Part 3). Formato lista.
Todo dibujado por el canal (casita, palmeras, ovni, consola y tele genéricas); sin logos, personajes ni arte de Rockstar.
Datos: (1) 62 especies de aves y diario de fauna con prismáticos (Rockstar vía Insider Gaming; PC Gamer, Dexerto);
(2) la consola JoySystem de casa de Jason tiene juegos completos jugables, p. ej. el shooter de zombis Street Trash III,
hecho por un equipo pequeño dentro de Rockstar (Kotaku, Game8, IGN);
(3) la foto de una casita con palmeras y un ovni escondida en 2021 en una cafetería de San Andreas (Definitive Edition)
es una casa real de GTA 6 (Belville, Leonard County) con una pizarra «IT'S A SIMULATION» (Kotaku, VGC, Dexerto)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 015-L"
SUBTITULO = subtitulo_hud
PINK = (1.0, 0.35, 0.65)
TEAL = (0.20, 0.85, 0.80)
LIME2 = (0.72, 1.0, 0.0)
UFO_BLUE = (0.45, 0.85, 1.0)


# ---------- piezas ----------
def palm(ctx, x, y, s, T, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    sway = 0.05 * math.sin(T * 1.6 + x)
    ctx.move_to(-8, 0); ctx.curve_to(-6, -120, 10 + 30 * sway, -220, 20, -300)
    ctx.line_to(36, -300); ctx.curve_to(26 + 30 * sway, -220, 12, -120, 10, 0); ctx.close_path()
    fill(ctx, (0.45, 0.28, 0.16), a)
    for k in range(6):
        ang = -math.pi / 2 + (k - 2.5) * 0.55 + sway
        ctx.save(); ctx.translate(28, -300); ctx.rotate(ang)
        ctx.move_to(0, 0); ctx.curve_to(60, -30, 120, -10, 150, 40); ctx.curve_to(110, 10, 60, 0, 0, 0)
        fill(ctx, (0.18, 0.62, 0.32), a)
        ctx.restore()
    ctx.restore()


def small_house(ctx, x, y, s, lit=1.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-140, -120, 280, 120); fill(ctx, (0.93, 0.86, 0.74), a)
    ctx.move_to(-165, -118); ctx.line_to(0, -210); ctx.line_to(165, -118); ctx.close_path(); fill(ctx, (0.80, 0.38, 0.30), a)
    rrect(ctx, -30, -75, 60, 75, 6); fill(ctx, (0.30, 0.20, 0.16), a)
    for wx in (-95, 65):
        ctx.rectangle(wx, -90, 46, 40); fill(ctx, (1.0, 0.85, 0.40) if lit > 0.5 else (0.25, 0.35, 0.45), a)
    ctx.restore()


def ufo(ctx, x, y, s, T, beam=1.0, a=1.0):
    ctx.save(); ctx.translate(x, y + 6 * math.sin(T * 3)); ctx.scale(s, s)
    if beam > 0:
        ctx.move_to(-40, 20); ctx.line_to(40, 20); ctx.line_to(130, 300); ctx.line_to(-130, 300); ctx.close_path()
        fill(ctx, UFO_BLUE, 0.22 * beam * a)
    ellipse(ctx, 0, -18, 60, 44); fill(ctx, (0.75, 0.95, 1.0), 0.85 * a)
    ellipse(ctx, 0, 6, 150, 36); fill(ctx, (0.62, 0.64, 0.72), a)
    for k in range(5):
        circle(ctx, -100 + k * 50, 10, 9); fill(ctx, (1.0, 0.9, 0.3) if (int(T * 6) + k) % 2 else UFO_BLUE, a)
    ctx.restore()


def photo_inner(ctx, T, cx, cy, w, h, house=1.0, palms=1.0, ufo_p=1.0, night=1.0):
    """Contenido de la foto: cielo de noche, casita, 2 palmeras y un ovni (todo genérico)."""
    ctx.save(); rrect(ctx, cx - w / 2, cy - h / 2, w, h, 10); ctx.clip()
    g = vgrad(ctx, 0, cy - h / 2, 0, cy + h / 2, [(0, (0.06, 0.06, 0.22)), (0.7, (0.28, 0.14, 0.38)), (1, (0.12, 0.20, 0.12))])
    ctx.rectangle(cx - w / 2, cy - h / 2, w, h); ctx.set_source(g); ctx.fill()
    for k in range(18):
        circle(ctx, cx - w / 2 + (k * 97) % w, cy - h / 2 + (k * 53) % int(h * 0.5), 2.5); fill(ctx, WHITE, 0.6)
    ctx.rectangle(cx - w / 2, cy + h * 0.30, w, h * 0.2); fill(ctx, (0.10, 0.22, 0.12))
    sc = w / 640
    if house > 0:
        small_house(ctx, cx, cy + h * 0.31, 0.95 * sc * house)
    if palms > 0:
        palm(ctx, cx - 210 * sc, cy + h * 0.33, 0.8 * sc * palms, T)
        palm(ctx, cx + 200 * sc, cy + h * 0.33, 0.7 * sc * palms, T + 1)
    if ufo_p > 0:
        ufo(ctx, cx + 40 * sc, cy - h * 0.22, 0.75 * sc * ufo_p, T, beam=ufo_p)
    ctx.restore()


def framed_photo(ctx, x, y, w, h, T, rot=-0.03, **kw):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    rrect(ctx, -w / 2 - 34, -h / 2 - 34 + 12, w + 68, h + 68, 12); fill(ctx, (0, 0, 0), 0.35)
    rrect(ctx, -w / 2 - 34, -h / 2 - 34, w + 68, h + 68, 12); fill(ctx, (0.36, 0.22, 0.12))
    rrect(ctx, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 6); fill(ctx, (0.95, 0.93, 0.88))
    photo_inner(ctx, T, 0, 0, w, h, **kw)
    ctx.restore()


def cafe_wall(ctx, T):
    g = vgrad(ctx, 0, 0, 0, H, [(0, (0.28, 0.18, 0.14)), (1, (0.14, 0.08, 0.06))])
    ctx.rectangle(-500, -500, W + 1000, H + 1000); ctx.set_source(g); ctx.fill()
    for k in range(-4, 20):
        ctx.rectangle(k * 90, -500, 4, H + 1000); fill(ctx, (0, 0, 0), 0.12)


def binoculars(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for dx in (-70, 70):
        rrect(ctx, dx - 55, -90, 110, 180, 40); fill(ctx, (0.12, 0.12, 0.16), a)
        circle(ctx, dx, 60, 46); fill(ctx, (0.35, 0.65, 0.95), a)
        circle(ctx, dx - 12, 48, 12); fill(ctx, WHITE, 0.7 * a)
    rrect(ctx, -30, -50, 60, 60, 10); fill(ctx, (0.25, 0.25, 0.30), a)
    ctx.restore()


def logbook(ctx, x, y, s, T, checked=3, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.04)
    rrect(ctx, -230, -280, 460, 560, 22); fill(ctx, (0.20, 0.45, 0.30), a)
    rrect(ctx, -205, -260, 420, 520, 14); fill(ctx, (0.96, 0.93, 0.84), a)
    text(ctx, "WILDLIFE LOG", 0, -205, 48, (0.15, 0.12, 0.10), a=a, font="Anton", shadow=False)
    birds = ["🐦", "🦜", "🦩", "🦉", "🦅", "🦆"]
    for i, b in enumerate(birds):
        r, c = divmod(i, 2)
        bx, by = -100 + c * 200, -90 + r * 130
        icon(ctx, b, bx - 30, by, 90, a)
        rrect(ctx, bx + 30, by - 24, 48, 48, 8); stroke(ctx, (0.15, 0.12, 0.10), 5, a)
        if i < checked:
            ctx.move_to(bx + 38, by); ctx.line_to(bx + 52, by + 16); ctx.line_to(bx + 74, by - 18); stroke(ctx, (0.1, 0.6, 0.2), 8, a)
    ctx.restore()


def retro_console(ctx, x, y, s, T, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -220, -60, 440, 120, 20); fill(ctx, (0.85, 0.84, 0.80), a)
    rrect(ctx, -200, -40, 260, 30, 6); fill(ctx, (0.25, 0.25, 0.30), a)
    circle(ctx, 140, 0, 22); fill(ctx, RED, a)
    circle(ctx, 190, 0, 10); fill(ctx, LIME2, a * (0.5 + 0.5 * math.sin(T * 6)))
    text(ctx, "JOYSYSTEM", -70, 30, 26, (0.3, 0.3, 0.35), a=a, font="Anton", shadow=False)
    ctx.restore()


def zombie_game(ctx, T, cx, cy, w, h):
    """Mini juego de zombis visto desde arriba (sprites propios)."""
    ctx.rectangle(cx - w / 2, cy - h / 2, w, h); fill(ctx, (0.10, 0.16, 0.10))
    for k in range(10):
        ctx.rectangle(cx - w / 2 + (k * 131) % w, cy - h / 2 + (k * 71) % h, 60, 60); fill(ctx, (0.14, 0.22, 0.13))
    px, py = cx + 30 * math.sin(T * 2), cy + 20 * math.cos(T * 2)
    for k in range(7):
        ang = k * 0.9 + T * 0.6
        rr = 0.42 * min(w, h) - 20 * math.sin(T * 3 + k)
        zx, zy = px + rr * math.cos(ang), py + rr * math.sin(ang) * 0.8
        ctx.rectangle(zx - 18, zy - 18, 36, 36); fill(ctx, (0.45, 0.85, 0.35))
        ctx.rectangle(zx - 10, zy - 8, 6, 6); fill(ctx, RED)
        ctx.rectangle(zx + 4, zy - 8, 6, 6); fill(ctx, RED)
    ctx.rectangle(px - 18, py - 18, 36, 36); fill(ctx, YELLOW)
    if int(T * 8) % 2:
        ctx.move_to(px, py); ctx.line_to(px + 120 * math.cos(T * 3), py + 120 * math.sin(T * 3)); stroke(ctx, WHITE, 4)


def pixel_game(ctx, T, cx, cy, w, h):
    ctx.rectangle(cx - w / 2, cy - h / 2, w, h); fill(ctx, (0.05, 0.05, 0.12))
    for k in range(8):
        xx = cx - w / 2 + ((k * 120 - T * 160) % (w + 120)) - 60
        ctx.rectangle(xx, cy + h * 0.25, 70, 30); fill(ctx, VIOLET)
    jx = cx - 120
    jy = cy + h * 0.25 - 40 - 90 * abs(math.sin(T * 3))
    ctx.rectangle(jx - 20, jy - 20, 40, 40); fill(ctx, YELLOW)
    text(ctx, "SCORE 0420", cx, cy - h / 2 + 40, 34, LIME2, font="Anton", shadow=False)


def calendar(ctx, x, y, s, top, big, small, col=RED, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * appear, s * appear)
    rrect(ctx, -160, -170, 320, 340, 24); fill(ctx, WHITE)
    rrect(ctx, -160, -170, 320, 90, 24); fill(ctx, col)
    ctx.rectangle(-160, -110, 320, 30); fill(ctx, col)
    text(ctx, top, 0, -125, 46, WHITE, font="Anton", shadow=False)
    text(ctx, big, 0, 20, 120, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    text(ctx, small, 0, 130, 32, (0.4, 0.4, 0.45), font="Anton", shadow=False)
    ctx.restore()


# ---------- escenas ----------
def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): la foto escondida de 2021 en la pared."""
    camera(ctx, zoom, W / 2, 960)
    cafe_wall(ctx, T)
    rays(ctx, W / 2, 640, T, UFO_BLUE, 0.05)
    framed_photo(ctx, W / 2, 640, 640, 470, T)
    hud(ctx, T, TAG, UFO_BLUE)
    pill(ctx, "GTA 6 · HIDDEN IN 2021", W / 2, 1400, 1.0, size=50, rgb=RED)


# 0.00 "Rockstar hid GTA 6"
def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


# 1.42 "...inside a game from twenty twenty-one."  (primer corte ~1,4 s)
def e_hook2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.12), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.14), floor=False)
    rays(ctx, W / 2, 620, T, YELLOW, 0.06)
    crt(ctx, W / 2 + 120, 640, 560, 420, T, inner=lambda c: photo_inner(c, T, W / 2 + 120, 640, 560, 420))
    calendar(ctx, 230, 520, 0.75, "GAME FROM", "2021", "SAN ANDREAS", RED, pop(lt, 0.2))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "A GAME FROM 2021", W / 2, 1400, pop(lt, 0.3), size=60, rgb=YELLOW)


# 3.85 "Three GTA 6 facts you didn't know."
def l_intro(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    rays(ctx, W / 2, 620, T, PINK, 0.05)
    for i in range(3):
        big_number(ctx, str(i + 1), 250 + i * 290, 640, 230, (PINK, YELLOW, TEAL)[i], pop(lt, 0.1 + i * 0.2))
    badge(ctx, "PART 3", W / 2, 400, pop(lt, 0.0), size=70, bg=PINK)
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


# 6.35 "GTA 6 has sixty-two kinds of BIRDS,"
def e_birds(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.12), floor=False)
    v = int(counter(lt, 0, 62, 1.3))
    big_number(ctx, str(v), W / 2, 520, 300, TEAL, 1.0)
    birds = ["🐦", "🦜", "🦩", "🦉", "🦅", "🦆", "🦢"]
    for i, b in enumerate(birds):
        ang = i / len(birds) * 2 * math.pi + T * 0.5
        icon(ctx, b, W / 2 + 380 * math.cos(ang), 560 + 260 * math.sin(ang) * 0.9, 120, pop(lt, 0.1 + i * 0.12))
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "62 BIRD SPECIES", W / 2, 1400, pop(lt, 0.4), size=60, rgb=TEAL)


# 8.85 "and a logbook to spot them all with binoculars."
def e_logbook(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06), floor=False)
    logbook(ctx, 380, 620, 0.95, T, checked=int(clamp(lt / 1.6) * 6))
    binoculars(ctx, 830, 600 + 10 * math.sin(T * 2), 1.0, pop(lt, 0.3))
    hud(ctx, T, TAG, LIME2)
    pill(ctx, "SPOT THEM ALL", W / 2, 1400, pop(lt, 0.2), size=60, rgb=LIME2)


# 11.33 "Two: the console in Jason's house"
def e_console(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.05, 0.12), floor=False)
    crt(ctx, W / 2, 560, 600, 400, T, inner=lambda c: (c.rectangle(0, 0, W, H), fill(c, (0.02, 0.02, 0.05)),
                                                     text(c, "PRESS START", W / 2, 560, 70, WHITE, a=0.5 + 0.5 * math.sin(T * 5), font="Anton")))
    retro_console(ctx, W / 2, 860, 1.1, T, pop(lt, 0.0))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "JASON'S HOUSE", W / 2, 1400, pop(lt, 0.2), size=60, rgb=PINK)


# 13.42 "really WORKS, and its games are fully playable."
def e_works(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.14), floor=False)
    rays(ctx, W / 2, 600, T, LIME2, 0.06)
    crt(ctx, W / 2, 580, 680, 460, T, inner=lambda c: pixel_game(c, T, W / 2, 580, 680, 460))
    gamepad(ctx, W / 2, 900, 0.55, T, press="A" if int(T * 4) % 2 else "right")
    hud(ctx, T, TAG, LIME2)
    stamp(ctx, "FULLY PLAYABLE", W / 2, 1400, clamp((lt - 0.4) / 0.25), LIME2, size=74, rot=-0.06)


# 15.34 "In other words, GTA 6 has whole video games inside it."  (2.º gancho: plano más fuerte)
def e_owords(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.12)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 620, T, PINK, 0.10)

    def nest(c, k):
        if k > 2:
            return
        w, h = 760 * 0.62 ** k, 520 * 0.62 ** k
        rrect(c, W / 2 - w / 2, 620 - h / 2, w, h, 18); fill(c, (0.06, 0.06, 0.10))
        rrect(c, W / 2 - w / 2, 620 - h / 2, w, h, 18); stroke(c, (PINK, YELLOW, TEAL, LIME2)[k], 8)
        text(c, "GAME" if k else "GTA 6", W / 2, 620 - h / 2 + 52 * 0.62 ** k, 72 * 0.62 ** k, WHITE, font="Anton")
        nest(c, k + 1)
    nest(ctx, 0)
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "GAMES INSIDE THE GAME", W / 2, 1400, clamp((lt - 0.5) / 0.25), YELLOW, size=62, rot=-0.06)


# 18.67 "One zombie shooter takes hours to beat."
def e_zombie(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.05), floor=False)
    crt(ctx, W / 2, 560, 700, 460, T, inner=lambda c: zombie_game(c, T, W / 2, 560, 700, 460))
    digital_clock(ctx, f"{int(counter(lt, 0, 4, 1.4))}:00:00", W / 2, 880, 1.0, pop(lt, 0.3), YELLOW)
    icon(ctx, "🧟", 150, 860, 140, pop(lt, 0.1))
    hud(ctx, T, TAG, GREEN)


# 20.68 "And three:"  -> l_num(3)
# 21.14 "in twenty twenty-one, the San Andreas remaster"
def e_2021(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    calendar(ctx, 300, 540, 0.95, "NOV", "2021", "REMASTER", ORANGE, pop(lt, 0.0))
    ficha(ctx, "SAN ANDREAS", "REMASTER · 2021", 690, 790, pop(lt, 0.5), emoji="🎮", accent=ORANGE, w=620)
    icon(ctx, "🕹️", 780, 500, 200, pop(lt, 0.2))
    hud(ctx, T, TAG, ORANGE)


# 23.48 "hid a PHOTO on a coffee shop wall."
def e_wall(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    cafe_wall(ctx, T)
    framed_photo(ctx, W / 2 + 120, 560, 420, 310, T, rot=0.03, house=0.0, palms=0.0, ufo_p=0.0)
    icon(ctx, "☕", 230, 820, 200, pop(lt, 0.2))
    text(ctx, "?", W / 2 + 120, 560, 160, WHITE, a=0.8, font="Anton")
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "A COFFEE SHOP WALL", W / 2, 1400, pop(lt, 0.3), size=56, rgb=ORANGE)


# 25.13 "A small house, palm trees, a UFO."
def e_photo(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    cafe_wall(ctx, T)
    framed_photo(ctx, W / 2, 620, 760, 560, T, rot=0.0,
                 house=pop(lt, 0.0), palms=pop(lt, 0.9), ufo_p=pop(lt, 1.85))
    hud(ctx, T, TAG, UFO_BLUE)


# 27.80 "Players just found that exact house in GTA 6."
def e_found(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.05, 0.18), floor=False)
    rays(ctx, W / 2, 620, T, PINK, 0.06)
    framed_photo(ctx, 300, 520, 360, 260, T, rot=-0.06)
    text(ctx, "2021", 300, 700, 56, ORANGE, font="Anton")
    arrow(ctx, 500, 560, 600, 600, pop(lt, 0.3), YELLOW, 12)
    crt(ctx, 790, 640, 420, 320, T, inner=lambda c: photo_inner(c, T, 790, 640, 420, 320, ufo_p=0.0))
    text(ctx, "GTA 6", 790, 860, 56, PINK, font="Anton")
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "SAME HOUSE", W / 2, 1400, clamp((lt - 0.8) / 0.25), PINK, size=76, rot=-0.06)


# 30.51 "Inside, a board says IT'S A SIMULATION."
def e_board(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + 0.006 * math.sin(T * 40) * (lt > 1.4), W / 2, 960)
    bg_dark(ctx, T)
    rrect(ctx, 120, 400, 840, 500, 18); fill(ctx, (0.30, 0.22, 0.14))
    rrect(ctx, 150, 430, 780, 440, 10); fill(ctx, (0.92, 0.90, 0.84))
    icon(ctx, "🛸", 860, 480, 100, 1.0)
    if lt > 1.3:
        text(ctx, "IT'S A", W / 2, 580, 120, RED, a=pop(lt, 1.3), font="Anton", shadow=False)
    if lt > 1.75:
        text(ctx, "SIMULATION", W / 2, 730, 150, RED, a=pop(lt, 1.75), font="Anton", shadow=False)
    hud(ctx, T, TAG, RED)


# 32.99 "So the truth is," -> vuelve al gancho (bucle)
def e_end(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.42, e_hook2), (3.85, l_intro), (5.86, l_num(1, PINK)), (6.35, e_birds),
           (8.85, e_logbook), (11.33, l_num(2, YELLOW)), (11.78, e_console), (13.42, e_works), (15.34, e_owords),
           (18.67, e_zombie), (20.68, l_num(3, TEAL)), (21.14, e_2021), (23.48, e_wall), (25.13, e_photo),
           (27.80, e_found), (30.51, e_board), (32.99, e_end)]
HOOK = "GTA 6 WAS HIDDEN IN 2021"
LISTA = [(5.86, "1/3"), (11.33, "2/3"), (20.68, "3/3")]
COLA = 0.02
SFX = [(5.88, "ding"), (11.35, "ding"), (13.7, "pop"), (20.70, "ding"), (27.2, "pop"), (32.3, "pop")]
CTA = 18.75  # aviso SUBSCRIBE · LIKE · SHARE justo después del «in other words», sobre el plano de los zombis (sin pill abajo)


def MINIATURA(ctx):
    cafe_wall(ctx, 1.0)
    rays(ctx, W / 2, 1050, 1.0, UFO_BLUE, 0.06)
    framed_photo(ctx, W / 2, 1060, 820, 600, 1.0, rot=-0.03)
    thumb_circle(ctx, W / 2 + 40, 900, 170, 110)
    thumb_arrow(ctx, 130, 1760, W / 2 - 60, 1000)
    thumb_vignette(ctx)
    thumb_text(ctx, [("GTA 6 WAS", WHITE), "HIDDEN HERE?"], y=330)
