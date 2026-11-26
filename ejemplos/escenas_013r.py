"""Behind the HUD · 013 (EN) — Silent Hill's fog only exists because the PlayStation couldn't keep up (formato bucle).
Pueblo, niebla, linterna, radio y monstruo-sombra genéricos dibujados por el canal; consola = caja genérica sin forma ni logo reales;
sin personajes, logos, carátulas ni capturas de Konami/Sony."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 013"
SUBTITULO = subtitulo_hud
FOG = (0.82, 0.84, 0.86)
ASH = (0.55, 0.57, 0.60)
BLOOD = (0.75, 0.10, 0.10)


# ---------- piezas propias ----------
def sky_fog(ctx, dark=0.0):
    g = vgrad(ctx, 0, 0, 0, H, [(0, (lerp(0.62, 0.08, dark), lerp(0.64, 0.08, dark), lerp(0.66, 0.10, dark))),
                               (0.55, (lerp(0.75, 0.12, dark), lerp(0.76, 0.12, dark), lerp(0.78, 0.14, dark))),
                               (1, (lerp(0.30, 0.03, dark), lerp(0.30, 0.03, dark), lerp(0.32, 0.04, dark)))])
    ctx.rectangle(-600, -600, W + 1200, H + 1200); ctx.set_source(g); ctx.fill()


def building(ctx, x, base, w, h, col, a=1.0, lit=0.0, seed=0):
    ctx.rectangle(x - w / 2, base - h, w, h); fill(ctx, col, a)
    ctx.rectangle(x - w / 2 - 8, base - h - 14, w + 16, 16); fill(ctx, tuple(c * 0.8 for c in col), a)
    rng = np.random.default_rng(seed)
    for r in range(int(h // 70)):
        for q in range(max(1, int(w // 60))):
            on = rng.random() < lit
            ctx.rectangle(x - w / 2 + 16 + q * 60, base - h + 26 + r * 70, 30, 36)
            fill(ctx, (1.0, 0.85, 0.45) if on else tuple(c * 0.6 for c in col), a)


def street(ctx, T, layers=4, fogk=1.0, popped=None, dark=0.0):
    """Calle genérica en perspectiva; las capas lejanas desaparecen en la niebla."""
    hor = 780
    ctx.move_to(-300, H); ctx.line_to(W / 2 - 40, hor); ctx.line_to(W / 2 + 40, hor); ctx.line_to(W + 300, H)
    ctx.close_path(); fill(ctx, (lerp(0.30, 0.06, dark),) * 3)
    for k in range(layers - 1, -1, -1):
        d = k / max(1, layers - 1)          # 0 = cerca, 1 = lejos
        s = lerp(1.0, 0.28, d)
        base = lerp(1000, hor + 10, d)
        col = tuple(lerp(c, f, fogk * d * 0.9) for c, f in zip((lerp(0.30, 0.10, dark), lerp(0.28, 0.10, dark), lerp(0.30, 0.12, dark)), FOG if dark < 0.5 else (0.05, 0.05, 0.07)))
        a = 1.0 if popped is None else (1.0 if k < popped else 0.0)
        for side in (-1, 1):
            x = W / 2 + side * lerp(380, 130, d)
            building(ctx, x, base, 220 * s, (380 + 90 * ((k + (side > 0)) % 2)) * s, col, a, seed=k * 2 + (side > 0))


def fog_layer(ctx, T, amount=1.0, y0=300, y1=950, rgb=FOG):
    if amount <= 0:
        return
    for k in range(9):
        y = lerp(y0, y1, k / 8)
        x = (T * (25 + 7 * k) + k * 260) % (W + 900) - 450
        ellipse(ctx, x, y, 520, 120); fill(ctx, rgb, 0.16 * amount)
        ellipse(ctx, x - W - 300, y + 30, 520, 120); fill(ctx, rgb, 0.16 * amount)
    ctx.rectangle(-600, y0 - 200, W + 1200, y1 - y0 + 400)
    g = vgrad(ctx, 0, y0 - 200, 0, y1 + 200, [(0, rgb, 0), (0.5, rgb, 0.35 * amount), (1, rgb, 0)])
    ctx.set_source(g); ctx.fill()


def console_box(ctx, x, y, s, T, strain=0.0):
    """Consola genérica de los 90: caja gris con ranura y botones (sin forma ni logo reales)."""
    ctx.save(); ctx.translate(x + (math.sin(T * 50) * 5 * strain if strain > 0.5 else 0), y); ctx.scale(s, s)
    soft_shadow(ctx, 0, 170, 360, 40, 0.35)
    rrect(ctx, -330, -150, 660, 300, 30); fill(ctx, (0.62, 0.63, 0.66))
    rrect(ctx, -330, -150, 660, 300, 30); stroke(ctx, (0.35, 0.36, 0.40), 6)
    rrect(ctx, -270, -100, 540, 60, 12); fill(ctx, (0.25, 0.26, 0.30))
    for k, c in enumerate((CYAN, LIME, ORANGE)):
        circle(ctx, 140 + k * 60, 60, 20); fill(ctx, c)
    rrect(ctx, -270, 40, 200, 40, 10); fill(ctx, (0.30, 0.31, 0.35))
    circle(ctx, 280, -110, 10); fill(ctx, RED if strain > 0.3 else (0.3, 0.3, 0.3))
    if strain > 0:
        glow(ctx, 0, 0, 380, ORANGE, 0.35 * strain)
        for k in range(3):
            yy = -200 - ((T * 120 + k * 60) % 160)
            ctx.move_to(-80 + k * 80, yy); ctx.curve_to(-60 + k * 80, yy - 30, -100 + k * 80, yy - 50, -80 + k * 80, yy - 80)
            stroke(ctx, (0.7, 0.7, 0.75), 10, 0.5 * strain)
    ctx.restore()


def monster(ctx, x, y, s, T, a=1.0):
    """Sombra genérica sin forma definida con ojos rojos (diseño del canal)."""
    ctx.save(); ctx.translate(x, y + 8 * math.sin(T * 2)); ctx.scale(s, s)
    ctx.move_to(-120, 260); ctx.curve_to(-160, 40, -110, -200, 0, -220)
    ctx.curve_to(110, -200, 160, 40, 120, 260); ctx.close_path(); fill(ctx, (0.06, 0.05, 0.07), 0.9 * a)
    for sx in (-40, 40):
        glow(ctx, sx, -120, 50, RED, 0.6 * a)
        ellipse(ctx, sx, -120, 16, 9); fill(ctx, (1, 0.2, 0.15), a)
    ctx.restore()


def flashlight(ctx, x, y, s, T, beam=1.0, reach=420):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if beam > 0:
        ctx.move_to(60, -25); ctx.line_to(60 + reach * beam, -150); ctx.line_to(60 + reach * beam, 150); ctx.line_to(60, 25)
        ctx.close_path()
        g = cairo.LinearGradient(60, 0, 60 + reach, 0)
        g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.7); g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0.0)
        ctx.set_source(g); ctx.fill()
    rrect(ctx, -110, -26, 150, 52, 14); fill(ctx, (0.18, 0.18, 0.22))
    rrect(ctx, 30, -38, 40, 76, 10); fill(ctx, (0.30, 0.30, 0.36))
    ellipse(ctx, 70, 0, 8, 32); fill(ctx, (1, 0.95, 0.7))
    ctx.restore()


def radio(ctx, x, y, s, T, noise=1.0):
    ctx.save(); ctx.translate(x + (math.sin(T * 70) * 4 * noise), y); ctx.scale(s, s)
    rrect(ctx, -170, -120, 340, 240, 26); fill(ctx, (0.35, 0.22, 0.14))
    rrect(ctx, -170, -120, 340, 240, 26); stroke(ctx, (0.20, 0.12, 0.08), 6)
    ctx.move_to(110, -120); ctx.line_to(170, -260); stroke(ctx, STEEL, 8)
    rrect(ctx, -140, -90, 170, 180, 14); fill(ctx, (0.12, 0.10, 0.10))
    rng = np.random.default_rng(int(T * 30))
    for r in range(8):
        for q in range(7):
            circle(ctx, -122 + q * 22, -70 + r * 21, 6); fill(ctx, (0.25, 0.22, 0.20))
    circle(ctx, 100, -30, 34); fill(ctx, (0.75, 0.72, 0.65))
    circle(ctx, 100, 60, 22); fill(ctx, (0.75, 0.72, 0.65))
    for k in range(int(10 * noise)):
        xx = rng.uniform(-260, 260); yy = rng.uniform(-260, -150)
        ctx.move_to(xx, yy); ctx.line_to(xx + rng.uniform(-30, 30), yy + rng.uniform(-30, 30))
        stroke(ctx, WHITE, 5, 0.7 * noise)
    ctx.restore()


def review_card(ctx, x, y, s, appear, stars=5, rot=0.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * appear, s * appear)
    rrect(ctx, -200, -130, 400, 260, 20); fill(ctx, (0.95, 0.94, 0.90))
    rrect(ctx, -200, -130, 400, 60, 20); fill(ctx, (0.15, 0.15, 0.20))
    text(ctx, "REVIEW", 0, -98, 34, WHITE, font="Anton", shadow=False)
    for k in range(5):
        text(ctx, "★", -120 + k * 60, -10, 56, YELLOW if k < stars else (0.7, 0.7, 0.7), font="DejaVu Sans", shadow=False)
    for k in range(3):
        rrect(ctx, -160, 50 + k * 26, 320 - 60 * k, 12, 6); fill(ctx, (0.6, 0.6, 0.65))
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): calle genérica que se pierde en la niebla."""
    camera(ctx, zoom, W / 2, 960)
    sky_fog(ctx, 0.15)
    street(ctx, T, layers=5, fogk=1.0)
    fog_layer(ctx, T, 1.0, 380, 900)
    hud(ctx, T, TAG, FOG)
    pill(ctx, "WHY IS THIS TOWN SO FOGGY?", W / 2, 1420, 1.0, size=48, rgb=ASH)


# ---------- escenas ----------
# 0.00 "Silent Hill's famous fog only exists"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.44 "because the PlayStation couldn't keep up."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.04))
    console_box(ctx, W / 2, 620, 1.1, T, strain=clamp(lt / 1.2))
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "COULDN'T KEEP UP", W / 2, 1400, pop(lt, 0.3), size=58, rgb=ORANGE)


# 4.40 "And it's real. In 1999,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    if lt < 1.0:
        badge(ctx, "REAL", W / 2, 600, pop(lt, 0.05), size=110)
    else:
        big_number(ctx, counter(lt - 1.0, 1989, 1999, 0.6), W / 2, 600, 260, YELLOW, pop(lt, 1.0))


# 6.57 "Konami's Team Silent built a 3D town for the PlayStation."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_blueprint(ctx, T)
    p = ease(clamp(lt / 2.0))
    for k, (x, w, h) in enumerate(((250, 160, 300), (430, 140, 420), (620, 180, 260), (820, 150, 360))):
        hh = h * p
        ctx.rectangle(x - w / 2, 860 - hh, w, hh); stroke(ctx, CYAN, 5, 0.9)
        ctx.move_to(x - w / 2, 860 - hh); ctx.line_to(x - w / 2 + 40, 830 - hh); ctx.line_to(x + w / 2 + 40, 830 - hh)
        ctx.line_to(x + w / 2 + 40, 830); ctx.line_to(x + w / 2, 860); stroke(ctx, CYAN, 4, 0.6)
        ctx.move_to(x + w / 2, 860 - hh); ctx.line_to(x + w / 2 + 40, 830 - hh); stroke(ctx, CYAN, 4, 0.6)
    text(ctx, "3D", W / 2, 400, 120, WHITE, font="Anton", a=pop(lt, 0.4))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "SILENT HILL", "1999 · PLAYSTATION · TEAM SILENT (KONAMI)", W / 2, 1400, pop(lt, 0.1), "🌫️", CYAN)


# 9.73 "But the console couldn't draw that much at once."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    chip(ctx, W / 2, 520, 0.95, T, heat=clamp(lt / 1.4), label="GPU", tired=clamp(lt / 1.4))
    meter(ctx, W / 2, 870, 760, lerp(1.0, 0.35, ease(clamp(lt / 1.6))), "DRAW DISTANCE", ORANGE, pop(lt, 0.1))
    hud(ctx, T, TAG, RED)
    pill(ctx, "TOO MUCH AT ONCE", W / 2, 1400, pop(lt, 0.3), size=58, rgb=RED)


# 11.89 "Distant buildings just popped into view."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_dark(ctx, T)
    def inner(c):
        sky_fog(c, 0.6)
        street(c, T, layers=5, fogk=0.0, popped=2 + int(lt / 0.5))
    crt(ctx, W / 2, 600, 860, 600, T, inner)
    hud(ctx, T, TAG, MAGENTA)
    if int(lt / 0.5) != int((lt - 1 / 60) / 0.5):
        pass
    stamp(ctx, "POP-IN!", 800, 380, clamp((lt - 0.5) / 0.2), MAGENTA, size=70, rot=0.12)
    pill(ctx, "BUILDINGS POPPING IN", W / 2, 1400, pop(lt, 0.3), size=54, rgb=MAGENTA)


# 13.86 "So the developers filled Silent Hill with thick fog"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 960)
    sky_fog(ctx, 0.15)
    street(ctx, T, layers=5, fogk=ease(clamp(lt / 2.0)))
    fog_layer(ctx, T, ease(clamp(lt / 1.5)) * 1.3, 350, 920)
    hud(ctx, T, TAG, FOG)
    pill(ctx, "THICK FOG", W / 2, 1400, pop(lt, 0.3), size=60, rgb=ASH)


# 16.56 "and darkness to hide the gaps."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    d = ease(clamp(lt / 1.0))
    sky_fog(ctx, d)
    street(ctx, T, layers=5, fogk=1.0, dark=d)
    fog_layer(ctx, T, 1.0 - 0.6 * d, 350, 920, (lerp(0.82, 0.10, d),) * 3)
    hud(ctx, T, TAG, VIOLET)
    pill(ctx, "DARKNESS HIDES THE GAPS", W / 2, 1400, pop(lt, 0.3), size=52, rgb=VIOLET)


# 18.17 "In other words, the scariest town in gaming is foggy"  (2.º gancho)
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 960)
    sky_fog(ctx, 0.5)
    rays(ctx, W / 2, 600, T, RED, 0.07)
    street(ctx, T, layers=5, fogk=1.0, dark=0.5)
    fog_layer(ctx, T, 1.2, 380, 900)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "FOG = NOT ENOUGH POWER", W / 2, 1400, clamp((lt - 0.8) / 0.25), RED, size=56, rot=-0.05)


# 21.32 "because the hardware ran out of power."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.03))
    console_box(ctx, W / 2, 590, 0.9, T, strain=1.0)
    meter(ctx, W / 2, 880, 760, lerp(0.6, 0.0, ease(clamp(lt / 1.4))), "POWER", RED, pop(lt, 0.1))
    hud(ctx, T, TAG, RED)
    pill(ctx, "OUT OF POWER", W / 2, 1400, pop(lt, 0.3), size=58, rgb=RED)


# 23.23 "Then something unexpected happened."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.12), floor=False)
    for k in range(3):
        text(ctx, "?!", W / 2 + (k - 1) * 8 * math.sin(T * 30), 620, 320, (CYAN, MAGENTA, WHITE)[k], font="Anton",
             a=(0.5 if k < 2 else 1.0) * pop(lt, 0.1), shadow=k == 2)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "PLOT TWIST", W / 2, 1400, pop(lt, 0.3), size=58, rgb=CYAN)


# 24.91 "In Silent Hill, players couldn't see what was coming,"
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    sky_fog(ctx, 0.3)
    street(ctx, T, layers=4, fogk=1.0, dark=0.3)
    monster(ctx, 700, 620, 0.9, T, a=clamp(lt / 2.0) * 0.6)
    fog_layer(ctx, T, 1.4, 380, 920)
    character(ctx, 300, 800, 0.6, T, mood="duda", look=(0.5, -0.1))
    hud(ctx, T, TAG, FOG)
    pill(ctx, "WHAT'S IN THE FOG?", W / 2, 1400, pop(lt, 0.3), size=56, rgb=ASH)


# 27.35 "and it was terrifying."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.2, 1.05), (dur, 1.12)]) + 0.008 * math.sin(T * 50), W / 2, 960)
    bg_dark(ctx, T)
    character(ctx, W / 2, 760, 0.85, T, mood="miedo" if False else "duda", look=(0, 0.1))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "TERRIFYING", W / 2, 1400, clamp((lt - 0.2) / 0.2), RED, size=70, rot=-0.06)


# 28.53 "Silent Hill gave you a flashlight that lit just a few steps."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    sky_fog(ctx, 0.95)
    fog_layer(ctx, T, 0.4, 400, 900, (0.15, 0.15, 0.18))
    flashlight(ctx, 230, 640, 1.2, T, beam=ease(clamp(lt / 0.5)), reach=380)
    for k in range(4):
        x = 420 + k * 150
        text(ctx, "▮", x, 860, 40, YELLOW if x < 720 else (0.25, 0.25, 0.3), font="DejaVu Sans", shadow=False, a=pop(lt, 0.4 + 0.15 * k))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "LIGHT REACH: A FEW STEPS", W / 2, 1400, pop(lt, 0.3), size=50, rgb=YELLOW)


# 31.56 "A pocket radio buzzed with static whenever a monster got close."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    sky_fog(ctx, 0.85)
    near = ease(clamp((lt - 0.8) / 1.8))
    monster(ctx, lerp(1000, 800, near), 600, lerp(0.5, 0.9, near), T, a=0.3 + 0.7 * near)
    fog_layer(ctx, T, 0.6, 400, 900, (0.30, 0.30, 0.33))
    radio(ctx, 340, 640, 1.0, T, noise=0.3 + 0.7 * near)
    hud(ctx, T, TAG, RED)
    pill(ctx, "STATIC = MONSTER NEARBY", W / 2, 1400, pop(lt, 0.3), size=50, rgb=RED)


# 34.66 "Reviewers said the fog made Silent Hill even creepier."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.06, 0.08))
    review_card(ctx, 300, 560, 1.0, pop(lt, 0.1), 5, -0.08)
    review_card(ctx, 780, 520, 1.0, pop(lt, 0.5), 5, 0.07)
    review_card(ctx, W / 2, 760, 1.05, pop(lt, 0.9), 5, -0.02)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "EVEN CREEPIER", W / 2, 1400, pop(lt, 0.3), size=58, rgb=YELLOW)


# 37.76 "Decades later, fog is still the heart of the series,"
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.12), (dur, 1.0)]), W / 2, 960)
    sky_fog(ctx, 0.3)
    street(ctx, T, layers=5, fogk=1.0, dark=0.2)
    fog_layer(ctx, T, 1.2, 380, 900)
    big_number(ctx, counter(lt, 1999, 2026, 1.2), W / 2, 450, 200, WHITE, pop(lt, 0.0))
    hud(ctx, T, TAG, FOG)
    pill(ctx, "STILL THE HEART OF THE SERIES", W / 2, 1400, pop(lt, 0.3), size=46, rgb=ASH)


# 41.02 "because" -> vuelve a e1 (bucle)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.12), (dur, 1.0)]))




def _punch(fn, z=1.22):
    """Mismo plano con zoom de golpe (primer corte a ~1,5 s)."""
    def f(ctx, lt, dur, T):
        ctx.translate(W / 2, 960); ctx.scale(z, z); ctx.translate(-W / 2, -960)
        fn(ctx, lt + 1.4, dur, T)
    return f

ESCENAS = [(0.0, e1), (1.45, _punch(e1)), (2.37, e4), (4.80, _punch(e4)), (7.30, e5), (9.49, e6), (11.48, e7), (13.40, e8), (15.25, e9), (17.90, e10), (20.25, e11), (21.97, e12), (24.51, e13), (25.64, e16), (29.06, e17), (31.85, e18)]
HOOK = 'THE FOG WAS HIDING SOMETHING'
COLA = 0.02

SFX = [(9.51, "pop"), (15.27, "ding"), (24.53, "pop")]


def MINIATURA(ctx):
    sky_fog(ctx, 0.35)
    ctx.save(); ctx.translate(0, 450)
    street(ctx, 1.0, layers=5, fogk=1.0, dark=0.3)
    monster(ctx, 700, 640, 0.8, 1.0, a=0.55)
    fog_layer(ctx, 1.0, 1.3, 380, 920)
    ctx.restore()
    thumb_circle(ctx, 700, 1080, 220, 300)
    thumb_arrow(ctx, 200, 1800, 520, 1260)
    thumb_vignette(ctx)
    thumb_text(ctx, [("THE FOG WAS", WHITE), "NEVER THE PLAN"], y=330)
CTA = 20.1  # aviso SUBSCRIBE · LIKE · SHARE tras el «in other words»
