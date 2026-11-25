"""Behind the HUD · 008 (EN) — The PlayStation began as a Nintendo add-on (formato bucle).
Consolas y prototipo genéricos dibujados por el canal; nombres de empresa solo en texto liso, sin logos."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 008"
SUBTITULO = subtitulo_hud
GREY = (0.78, 0.78, 0.80)


def disc(ctx, x, y, r, T, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(T * 2)
    circle(ctx, 0, 0, r); fill(ctx, (0.85, 0.87, 0.92), a)
    for k, c in enumerate((CYAN, MAGENTA, YELLOW)):
        ctx.arc(0, 0, r * (0.55 + k * 0.12), 0.3 + k, 1.4 + k); stroke(ctx, c, r * 0.08, 0.6 * a)
    circle(ctx, 0, 0, r * 0.2); fill(ctx, (0.1, 0.1, 0.12), a)
    ctx.restore()


def prototype(ctx, x, y, s, T, label="PLAY STATION", lid=0.0):
    """Prototipo genérico: consola gris con tapa de CD y ranura de cartucho."""
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -300, -110, 600, 220, 34); fill(ctx, GREY)
    rrect(ctx, -300, 40, 600, 70, 26); fill(ctx, (0.45, 0.45, 0.50))
    ctx.save(); ctx.translate(-80, -60); ctx.rotate(-lid * 0.5)
    circle(ctx, 0, 0, 120); fill(ctx, (0.62, 0.62, 0.66))
    circle(ctx, 0, 0, 120); stroke(ctx, (0.4, 0.4, 0.45), 6)
    ctx.restore()
    if lid > 0.2:
        disc(ctx, -80, -60, 100 * lid, T)
    rrect(ctx, 90, -90, 180, 34, 8); fill(ctx, (0.15, 0.15, 0.18))
    text(ctx, label, 160, 76, 30, WHITE, font="Anton", shadow=False)
    circle(ctx, -240, 75, 12); fill(ctx, RED)
    ctx.restore()


def new_console(ctx, x, y, s, T):
    """Consola genérica de los 90 (diseño propio, sin logo)."""
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -280, -100, 560, 200, 18); fill(ctx, (0.72, 0.72, 0.74))
    circle(ctx, -60, -10, 120); fill(ctx, (0.62, 0.62, 0.66))
    circle(ctx, -60, -10, 120); stroke(ctx, (0.45, 0.45, 0.5), 5)
    for k in range(2):
        rrect(ctx, 120, -60 + k * 50, 120, 30, 6); fill(ctx, (0.5, 0.5, 0.55))
    rrect(ctx, -250, 60, 70, 24, 6); fill(ctx, CYAN)
    ctx.restore()


def company(ctx, name, x, y, appear=1.0, rgb=CYAN, crack=0.0):
    pill(ctx, name, x, y, appear, size=60, rgb=rgb)
    if crack > 0 and appear > 0.5:
        ctx.move_to(x - 10, y - 50); ctx.line_to(x + 15, y - 10); ctx.line_to(x - 12, y + 15); ctx.line_to(x + 8, y + 50)
        stroke(ctx, RED, 8, crack)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): SONY + NINTENDO = ?"""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.18))
    rays(ctx, W / 2, 560, T, CYAN, 0.05)
    company(ctx, "SONY", 280, 400, 1.0, CYAN)
    text(ctx, "+", W / 2, 400, 90, WHITE, font="Anton")
    company(ctx, "NINTENDO", 770, 400, 1.0, RED)
    prototype(ctx, W / 2, 720, 1.15, T, "???", lid=0.5 + 0.5 * math.sin(T * 1.5))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "THE CONSOLE THAT ALMOST WAS", W / 2, 1420, 1.0, size=46, rgb=YELLOW)


# 0.03 "The PlayStation was supposed to be a Nintendo."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 2.61 "And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 560, pop(lt, 0.05), size=110)


# 3.56 "Sony engineer Ken Kutaragi built the sound chip inside the Super Nintendo."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    circuit(ctx, W / 2, 620, 700, 420, T, clamp(lt / 1.5))
    chip(ctx, W / 2, 620, 1.0 * max(pop(lt, 0.2), 0.01), T, label="SOUND")
    for k in range(3):
        r = 200 + ((T * 160 + k * 80) % 240)
        circle(ctx, W / 2, 620, r); stroke(ctx, CYAN, 5, 0.5 * (1 - (r - 200) / 240))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "KEN KUTARAGI", "SONY ENGINEER", W / 2, 1420, pop(lt, 0.1), "🔊", CYAN)


# 7.47 "Then Sony and Nintendo teamed up on a CD drive for it,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.16), floor=False)
    company(ctx, "SONY", 280, 400, pop(lt, 0.0), CYAN)
    company(ctx, "NINTENDO", 770, 400, pop(lt, 0.15), RED)
    icon(ctx, "🤝", W / 2, 580, 220, pop(lt, 0.5))
    disc(ctx, W / 2, 830, 100 * pop(lt, 1.0), T)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "A CD DRIVE, TOGETHER", W / 2, 1400, pop(lt, 0.6), size=52, rgb=YELLOW)


# 10.55 "called the Play Station."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.06, 0.18))
    rays(ctx, W / 2, 560, T, CYAN, 0.06)
    prototype(ctx, W / 2, 640, 1.3 * max(pop(lt, 0.0), 0.01), T, "PLAY STATION", lid=clamp((lt - 0.3) / 0.6))
    hud(ctx, T, TAG, CYAN)


# 11.79 "In June 1991,"
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.06, 0.02))
    icon(ctx, "📅", W / 2, 420, 260, pop(lt, 0.0))
    big_number(ctx, "JUNE 1991", W / 2, 760, 170, YELLOW, pop(lt, 0.3))
    hud(ctx, T, TAG, YELLOW)


# 13.42 "Sony proudly announced it at a huge tech show in Chicago."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    for k, x in enumerate((260, 820)):
        ctx.move_to(x, 260); ctx.line_to(W / 2 - 260 + k * 520, 860); ctx.line_to(W / 2 + 60 - k * 120, 860)
        ctx.close_path(); fill(ctx, (1, 0.95, 0.7), 0.12)
    ctx.rectangle(80, 820, W - 160, 60); fill(ctx, (0.25, 0.18, 0.12))
    prototype(ctx, W / 2, 700, 0.9, T, "PLAY STATION", lid=0.6)
    for k in range(10):
        if (int(T * 6) + k * 3) % 7 == 0:
            circle(ctx, 140 + k * 90, 330 + (k % 3) * 40, 26); fill(ctx, WHITE, 0.8)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "BIG TECH SHOW · CHICAGO", W / 2, 1400, pop(lt, 0.3), size=50, rgb=CYAN)


# 16.21 "But here's the twist. The very next day,"
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.12))
    rays(ctx, W / 2, 560, T, MAGENTA, 0.05)
    if lt < 1.0:
        character(ctx, W / 2, 560, 0.8, T, mood="duda", look=(0.3, -0.2))
        icon(ctx, "⚠️", 820, 330, 170, pop(lt, 0.1))
    else:
        big_number(ctx, "DAY 2", W / 2, 560, 260, MAGENTA, pop(lt, 1.0))
    hud(ctx, T, TAG, MAGENTA)


# 18.47 "Nintendo announced a deal with Philips instead."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.04), floor=False)
    company(ctx, "NINTENDO", 280, 420, pop(lt, 0.0), RED)
    icon(ctx, "🤝", W / 2, 420, 150, pop(lt, 0.3))
    company(ctx, "PHILIPS", 800, 420, pop(lt, 0.5), ORANGE)
    company(ctx, "SONY", W / 2, 760, pop(lt, 0.8), CYAN, crack=clamp((lt - 1.2) / 0.3))
    hud(ctx, T, TAG, RED)
    pill(ctx, "NEW PARTNER, ANNOUNCED LIVE", W / 2, 1400, pop(lt, 0.4), size=46, rgb=RED)


# 20.53 "Sony had no idea."
def e10(ctx, lt, dur, T):
    camera(ctx, 1.05 + 0.01 * math.sin(T * 50), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "😳", W / 2, 520, 360, pop(lt, 0.0))
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "SONY: ???", W / 2, 1400, pop(lt, 0.2), size=60, rgb=CYAN)


# 21.98 "In other words, Nintendo dumped Sony in front of the whole industry."  (2.º gancho)
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.06), floor=False)
    rays(ctx, W / 2, 560, T, RED, 0.08)
    icon(ctx, "💔", W / 2, 500, 380, pop(lt, 0.2))
    for k in range(9):
        icon(ctx, "👀", 130 + k * 102, 820 + 20 * math.sin(T * 3 + k), 70, pop(lt, 0.6 + k * 0.05))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "DUMPED IN PUBLIC", W / 2, 1400, clamp((lt - 1.0) / 0.25), RED, size=64, rot=-0.06)


# 25.37 "Kutaragi didn't give up."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.16))
    icon(ctx, "💪", W / 2, 520, 340, pop(lt, 0.0))
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "KEN KUTARAGI", "DIDN'T GIVE UP", W / 2, 1420, pop(lt, 0.1), "🔊", CYAN)


# 26.67 "He pushed Sony to build its own PlayStation console."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_blueprint(ctx, T)
    p = clamp(lt / 2.0)
    ctx.save()
    ctx.rectangle(0, 0, W * p + 1, H); ctx.clip()
    new_console(ctx, W / 2, 640, 1.3, T)
    ctx.restore()
    for k in range(5):
        ctx.rectangle(W / 2 - 400, 480 + k * 70, 800, 2); fill(ctx, CYAN, 0.25)
    icon(ctx, "🔧", W * p, 450, 120, 1.0, T * 4)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "SONY BUILDS ITS OWN", W / 2, 1400, pop(lt, 0.3), size=54, rgb=CYAN)


# 29.25 "The PlayStation launched in 1994"
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.18))
    rays(ctx, W / 2, 620, T, CYAN, 0.06)
    big_number(ctx, counter(lt, 1991, 1994, 0.8), W / 2, 400, 200, YELLOW, pop(lt, 0.0))
    new_console(ctx, W / 2, 740, 1.2 * max(pop(lt, 0.4), 0.01), T)
    hud(ctx, T, TAG, YELLOW)


# 31.00 "and sold over one hundred million units worldwide."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 560, T, LIME, 0.06)
    v = int(counter(lt, 0, 100000000, 1.6))
    big_number(ctx, f"{v:,}+", W / 2, 520, 150, LIME, pop(lt, 0.0))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "CONSOLES SOLD WORLDWIDE", W / 2, 1400, pop(lt, 0.3), size=50, rgb=LIME)


# 34.00 "Nintendo's biggest rival was born from one public breakup."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 0.97)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.14))
    company(ctx, "NINTENDO", 270, 430, pop(lt, 0.0), RED)
    company(ctx, "SONY", 810, 430, pop(lt, 0.1), CYAN)
    big_number(ctx, "VS", W / 2, 620, 260, YELLOW, pop(lt, 0.5))
    icon(ctx, "💔", W / 2, 430, 120, pop(lt, 0.3))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "BORN FROM A BREAKUP", W / 2, 1400, pop(lt, 0.8), size=54, rgb=YELLOW)


# 37.27 "Which is why, believe it or not," -> vuelve a e1 (bucle)
def e17(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.1), (dur, 1.0)]))




def _punch(fn, z=1.22):
    """Mismo plano con zoom de golpe (primer corte a ~1,5 s)."""
    def f(ctx, lt, dur, T):
        ctx.translate(W / 2, 960); ctx.scale(z, z); ctx.translate(-W / 2, -960)
        fn(ctx, lt + 1.4, dur, T)
    return f

ESCENAS = [(0.0, e1), (1.45, _punch(e1)), (2.63, e3), (6.42, e4), (9.59, e5), (10.85, e6), (12.30, e7), (14.57, e8), (15.72, e9), (18.10, e10), (19.43, e11), (22.82, e13), (25.58, e14), (27.60, e15), (29.84, e16), (32.41, e17), (4.50, _punch(e3))]
HOOK = 'PLAYSTATION WAS A NINTENDO'
COLA = 0.02

SFX = [(9.61, "ding"), (19.45, "ding"), (25.60, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.04, 0.05, 0.18))
    rays(ctx, W / 2, 1250, 1.0, CYAN, 0.06)
    company(ctx, "SONY", 300, 1000, 1.0, CYAN)
    text(ctx, "+", W / 2, 1000, 110, WHITE, font="Anton")
    company(ctx, "NINTENDO", 760, 1000, 1.0, RED)
    prototype(ctx, W / 2, 1400, 1.6, 1.0, "???", lid=0.8)
    thumb_circle(ctx, W / 2, 1400, 520, 260)
    thumb_arrow(ctx, 950, 1900, W / 2 + 330, 1640)
    thumb_vignette(ctx)
    thumb_text(ctx, [("THEY ALMOST", WHITE), "MADE THIS"], y=330)
CTA = 22.9  # aviso SUBSCRIBE · LIKE · SHARE justo después del «in other words»
