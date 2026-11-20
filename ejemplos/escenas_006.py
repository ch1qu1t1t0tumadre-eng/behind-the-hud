"""Behind the HUD · 006 (EN) — The Konami Code exists because its creator couldn't beat Gradius (formato bucle).
Nave, mando y consola genéricos dibujados por el canal; sin sprites ni logos de Konami."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 006"
SUBTITULO = subtitulo_hud
CODE = ["up", "up", "down", "down", "left", "right", "left", "right", "B", "A"]
CODE_T = [18.84, 19.07, 19.32, 19.62, 20.19, 20.50, 20.84, 21.14, 21.35, 21.65]
COLS = [CYAN, CYAN, MAGENTA, MAGENTA, LIME, ORANGE, LIME, ORANGE, RED, YELLOW]


def dir_tile(ctx, d, x, y, size, appear=1.0, rgb=CYAN):
    """Ficha con flecha dibujada (o letra B/A)."""
    if d in ("A", "B"):
        tile(ctx, d, x, y, size, appear, rgb)
        return
    tile(ctx, "", x, y, size, appear, rgb)
    if appear <= 0.01:
        return
    ang = {"up": -math.pi / 2, "down": math.pi / 2, "left": math.pi, "right": 0}[d]
    ctx.save(); ctx.translate(x, y); ctx.scale(appear, appear); ctx.rotate(ang)
    s = size * 0.3
    ctx.move_to(s, 0); ctx.line_to(-s * 0.4, -s * 0.85); ctx.line_to(-s * 0.4, -s * 0.3); ctx.line_to(-s, -s * 0.3)
    ctx.line_to(-s, s * 0.3); ctx.line_to(-s * 0.4, s * 0.3); ctx.line_to(-s * 0.4, s * 0.85); ctx.close_path()
    fill(ctx, rgb)
    ctx.restore()


def code_rows(ctx, T, size=150, y0=420, appear_fn=None):
    for i, d in enumerate(CODE):
        r, c = divmod(i, 5)
        x = W / 2 + (c - 2) * size * 1.12
        y = y0 + r * size * 1.15 + 6 * math.sin(T * 3 + i)
        a = appear_fn(i) if appear_fn else 1.0
        dir_tile(ctx, d, x, y, size, a, COLS[i])


def ship(ctx, x, y, s, T, shield=0.0, col=CYAN):
    """Nave genérica de diseño propio (flecha con motor)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(3):
        ctx.move_to(-70, -12 + k * 12); ctx.line_to(-70 - 50 - 30 * math.sin(T * 30 + k), -6 + k * 6)
        stroke(ctx, ORANGE, 8, 0.8)
    ctx.move_to(90, 0); ctx.line_to(-60, -50); ctx.line_to(-30, 0); ctx.line_to(-60, 50); ctx.close_path()
    fill_keep(ctx, (0.85, 0.88, 0.95)); stroke(ctx, col, 6)
    circle(ctx, 10, 0, 16); fill(ctx, col)
    if shield > 0:
        for k in range(2):
            circle(ctx, 70 + k * 30, 0, 22); fill(ctx, ORANGE, shield)
        circle(ctx, 0, 0, 120); stroke(ctx, CYAN, 6, 0.6 * shield)
        glow(ctx, 0, 0, 160, CYAN, 0.2 * shield)
    ctx.restore()


def bullets(ctx, T, n=26, x0=140, x1=940, y0=300, y1=820, seed=3, a=1.0):
    rng = np.random.default_rng(seed)
    for k in range(n):
        sp = rng.uniform(250, 520)
        x = x1 - ((T * sp + rng.uniform(0, 900)) % (x1 - x0))
        y = rng.uniform(y0, y1)
        circle(ctx, x, y, rng.uniform(8, 16)); fill(ctx, (ORANGE, MAGENTA, RED)[k % 3], a)


def home_console(ctx, x, y, s, T, label="HOME CONSOLE"):
    """Consola de sobremesa genérica (caja + ranura de cartucho)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -90, 520, 180, 26); fill(ctx, (0.80, 0.80, 0.82))
    rrect(ctx, -260, 30, 520, 60, 20); fill(ctx, (0.30, 0.30, 0.34))
    rrect(ctx, -150, -70, 300, 50, 10); fill(ctx, (0.15, 0.15, 0.18))
    for bx in (-200, -150):
        rrect(ctx, bx, 45, 36, 22, 6); fill(ctx, RED if bx == -200 else STEEL)
    text(ctx, label, 120, 60, 26, WHITE, font="Anton", shadow=False)
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): el código completo en fichas."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.04, 0.16))
    rays(ctx, W / 2, 560, T, VIOLET, 0.05)
    code_rows(ctx, T, 150, 520)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "THE MOST FAMOUS CHEAT", W / 2, 1420, 1.0, size=52, rgb=YELLOW)


# 0.03 "The most famous cheat code in gaming exists"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 2.90 "because its creator was bad at his own game."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, 760, 400, 380, 260, T, lambda c: text(c, "GAME OVER", 760, 400, 30, RED,
                                                   a=1.0 if int(T * 3) % 2 == 0 else 0.3,
                                                   font="Press Start 2P", shadow=False))
    character(ctx, 330, 600, 0.75, T, mood="duda", look=(0.4, -0.3))
    hud(ctx, T, TAG, RED)
    pill(ctx, "CREATOR: CAN'T WIN", W / 2, 1400, pop(lt, 0.3), size=52, rgb=RED)


# 5.01 "And it's real. In 1986,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.10))
    hud(ctx, T, TAG, CYAN)
    badge(ctx, "REAL", W / 2, 400, pop(lt, 0.05), size=80)
    big_number(ctx, counter(lt - 0.8, 1976, 1986, 0.5) if lt > 0.8 else "", W / 2, 700, 230, YELLOW, pop(lt, 0.8))


# 7.04 "Kazuhisa Hashimoto was porting the arcade shooter Gradius"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16))
    cabinet(ctx, W / 2, 560, 0.62, T, "GRADIUS",
            lambda c: (bullets(c, T, 8, -170, 170, -120, 120, seed=5), ship(c, -80, 0, 0.5, T)), VIOLET)
    hud(ctx, T, TAG, CYAN)
    ficha(ctx, "KAZUHISA HASHIMOTO", "PROGRAMMER · KONAMI", W / 2, 1420, pop(lt, 0.1), "🕹️", CYAN)


# 9.30 "to Nintendo's home console."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.16), floor=False)
    icon(ctx, "🕹️", 250, 540, 230, 1.0)
    arrow(ctx, 400, 540, 600, 540, clamp(lt / 0.5), YELLOW, 16)
    home_console(ctx, 800, 560, 0.75 * max(pop(lt, 0.4), 0.01), T)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "ARCADE → HOME CONSOLE", W / 2, 1400, pop(lt, 0.2), size=50, rgb=YELLOW)


# 11.57 "But there was a problem. Gradius was brutally hard,"
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]) + 0.006 * math.sin(T * 40), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, W / 2, 560, 760, 520, T, lambda c: (bullets(c, T, 30, 190, 890, 330, 790, seed=7),
                                                ship(c, 300, 560, 0.7, T)))
    hud(ctx, T, TAG, RED)
    meter(ctx, W / 2, 1400, 760, clamp(lt / 1.6) * 1.0, "DIFFICULTY", RED, pop(lt, 0.2))


# 14.44 "and Hashimoto couldn't beat it while testing."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    crt(ctx, W / 2, 520, 700, 460, T, lambda c: (
        text(c, "GAME OVER", W / 2, 470, 70, RED, a=1.0 if int(T * 3) % 2 == 0 else 0.35,
             font="Press Start 2P", shadow=False),
        text(c, "TEST RUN #" + str(40 + int(lt * 9)), W / 2, 600, 34, CYAN, font="Press Start 2P", shadow=False)))
    hud(ctx, T, TAG, RED)
    ficha(ctx, "KAZUHISA HASHIMOTO", "STUCK IN TESTING", W / 2, 1420, pop(lt, 0.2), "🕹️", RED)


# 16.54 "So he hid a secret button combo."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_blueprint(ctx, T)
    gamepad(ctx, W / 2, 560, 1.2 * max(pop(lt, 0.0), 0.01), T)
    icon(ctx, "🔒", W / 2, 320, 150, pop(lt, 0.6), 0.1 * math.sin(T * 4))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "SECRET COMBO", W / 2, 1400, pop(lt, 0.3), size=56, rgb=LIME)


# 18.84 "Up, up, down, down, left, right, left, right, B, A."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.04, 0.16), floor=False)
    t = lt + 18.84
    cur = max([i for i, ct in enumerate(CODE_T) if t >= ct] or [0])
    code_rows(ctx, T, 130, 380, lambda i: pop(t, CODE_T[i], 0.18))
    gamepad(ctx, W / 2, 800, 0.9, T, press=CODE[cur] if t - CODE_T[cur] < 0.22 else None)
    hud(ctx, T, TAG, CYAN)


# 21.94 "Enter the Konami Code, and your ship got every power-up."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.06))
    rays(ctx, W / 2, 520, T, LIME, 0.06)
    ship(ctx, W / 2 - 40, 520, 1.6, T, shield=clamp((lt - 0.8) / 0.5))
    hud(ctx, T, TAG, LIME)
    meter(ctx, W / 2, 1300, 760, clamp((lt - 0.8) / 0.8), "POWER", LIME, pop(lt, 0.6))
    pill(ctx, "KONAMI CODE: FULL POWER-UP", W / 2, 1440, pop(lt, 0.2), size=44, rgb=LIME)


# 24.97 "In other words, the developer cheated at his own game."  (2.º gancho)
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 560, T, MAGENTA, 0.08)
    character(ctx, W / 2, 560, 0.8, T, mood="normal", look=(0.2, 0.1))
    icon(ctx, "😈", W / 2 + 230, 330, 150, pop(lt, 0.6))
    hud(ctx, T, TAG, MAGENTA)
    stamp(ctx, "THE DEV CHEATED", W / 2, 1400, clamp((lt - 0.9) / 0.25), MAGENTA, size=64, rot=-0.06)


# 27.93 "He meant to delete the Konami Code before release."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 960)
    bg_dark(ctx, T)
    code_rows(ctx, T, 110, 330, lambda i: 1.0 - clamp((lt - 1.2 - i * 0.05) / 0.3))
    icon(ctx, "🗑️", W / 2, 760, 200, pop(lt, 0.8))
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "TO-DO: DELETE BEFORE RELEASE", W / 2, 1400, pop(lt, 0.2), size=44, rgb=ORANGE)


# 30.38 "It shipped anyway. Players found it, and two years later,"
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.04, 0.16))
    cartridge(ctx, W / 2, 520, 1.3 * max(pop(lt, 0.0), 0.01), 0.05 * math.sin(T * 2), label="GRADIUS",
              col=(0.22, 0.22, 0.26))
    stamp(ctx, "SHIPPED", W / 2 + 160, 360, clamp((lt - 0.4) / 0.2), LIME, rot=0.12, size=54)
    icon(ctx, "👀", W / 2 - 280, 330, 140, pop(lt, 1.0))
    hud(ctx, T, TAG, LIME)
    big_number(ctx, counter(lt - 1.7, 1986, 1988, 0.5) if lt > 1.7 else "1986", W / 2, 1400, 140, YELLOW, 1.0)


# 32.99 "Contra used the Konami Code to give you thirty lives."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.04, 0.04))
    rays(ctx, W / 2, 520, T, RED, 0.05)
    big_number(ctx, counter(lt - 0.5, 3, 30, 1.2) if lt > 0.5 else "3", W / 2, 470, 300, RED, pop(lt, 0.0))
    text(ctx, "LIVES", W / 2, 700, 80, WHITE, font="Anton", a=pop(lt, 0.2))
    for k in range(min(30, int(clamp((lt - 0.5) / 1.2) * 30) + 3)):
        icon(ctx, "❤️", 150 + (k % 10) * 87, 800 + (k // 10) * 70, 60, 1.0)
    hud(ctx, T, TAG, RED)
    pill(ctx, "CONTRA · 1988", W / 2, 1400, pop(lt, 0.3), size=54, rgb=RED)


# 35.92 "Today, the Konami Code is hidden in games and even websites."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 0.97)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.05, 0.16), floor=False)
    rrect(ctx, 120, 260, 840, 600, 30); fill(ctx, (0.92, 0.93, 0.96))
    rrect(ctx, 120, 260, 840, 80, 30); fill(ctx, (0.30, 0.32, 0.40))
    for k, c in enumerate((RED, YELLOW, LIME)):
        circle(ctx, 170 + k * 45, 300, 14); fill(ctx, c)
    rrect(ctx, 320, 282, 560, 38, 19); fill(ctx, WHITE)
    text(ctx, "www.", 360, 302, 24, STEEL, align="left", shadow=False)
    for i, d in enumerate(CODE):
        r, c = divmod(i, 5)
        dir_tile(ctx, d, 290 + c * 125, 470 + r * 150, 100, pop(lt, 0.2 + i * 0.06), COLS[i])
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "HIDDEN IN GAMES & WEBSITES", W / 2, 1400, pop(lt, 0.4), size=46, rgb=CYAN)


# 39.18 "Which is why" -> vuelve a e1 (bucle)
def e16(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.1), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.90, e2), (5.01, e3), (7.04, e4), (9.30, e5), (11.57, e6), (14.44, e7), (16.54, e8),
           (18.84, e9), (21.94, e10), (24.97, e11), (27.93, e12), (30.38, e13), (32.99, e14), (35.92, e15),
           (39.18, e16)]
SFX = [(5.03, "pop"), (18.86, "pop"), (21.67, "ding"), (24.98, "ding"), (30.40, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.05, 0.04, 0.16))
    rays(ctx, W / 2, 1150, 1.0, VIOLET, 0.06)
    code_rows(ctx, 1.0, 170, 1040)
    thumb_circle(ctx, W / 2, 1130, 520, 260)
    thumb_arrow(ctx, 900, 1850, W / 2 + 300, 1420)
    thumb_vignette(ctx)
    thumb_text(ctx, [("HE COULDN'T", WHITE), "BEAT HIS GAME"], y=330)
