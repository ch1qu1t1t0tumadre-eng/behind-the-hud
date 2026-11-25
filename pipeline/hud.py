"""Piezas visuales del canal "Behind the HUD" (estética arcade/neón + marco de HUD).
Se importan desde work/vNN/escenas.py con `from hud import *` (después de `from anim import *`)."""
import math
from anim import *  # noqa

CYAN = (0.10, 0.90, 1.00)
MAGENTA = (1.00, 0.22, 0.65)
LIME = (0.55, 1.00, 0.35)
ORANGE = (1.00, 0.55, 0.15)
VIOLET = (0.55, 0.35, 1.00)
SAND = (0.86, 0.66, 0.42)
SAND_D = (0.62, 0.43, 0.25)
STEEL = (0.55, 0.58, 0.66)
STEEL_D = (0.30, 0.32, 0.40)


def screen(ctx):
    """Vuelve a coordenadas de pantalla (sin cámara) dentro de una escena."""
    ctx.restore()
    ctx.save()


def glow(ctx, x, y, r, rgb, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *rgb, a)
    g.add_color_stop_rgba(1, *rgb, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


# ---------------- fondos ----------------
def bg_arcade(ctx, T, hue=(0.06, 0.03, 0.16), floor=True, speed=0.6):
    ctx.set_source(vgrad(ctx, 0, -800, 0, H + 800, [(0, (0.02, 0.01, 0.06)), (0.5, hue), (1, (0.03, 0.01, 0.08))]))
    ctx.paint()
    rng = np.random.default_rng(11)
    for _ in range(60):
        x, y, r = rng.uniform(-500, W + 500), rng.uniform(-700, H + 300), rng.uniform(2, 5)
        tw = 0.5 + 0.5 * math.sin(T * rng.uniform(1, 3) + x)
        ctx.rectangle(x, y, r, r)
        fill(ctx, rng.choice([0, 1]) and CYAN or MAGENTA, 0.15 + 0.35 * tw)
    if floor:
        hz = 1250
        for i in range(-16, 17):
            ctx.move_to(W / 2 + i * 70, hz)
            ctx.line_to(W / 2 + i * 480, H + 900)
        stroke(ctx, MAGENTA, 3, 0.35)
        for k in range(12):
            p = (k + (T * speed) % 1) / 12
            y = hz + (H + 900 - hz) * p ** 2.1
            ctx.move_to(-900, y)
            ctx.line_to(W + 900, y)
            stroke(ctx, MAGENTA, 2 + 3 * p, 0.15 + 0.4 * p)
        glow(ctx, W / 2, hz, 700, MAGENTA, 0.18)


def bg_desert(ctx, T, night=0.0):
    top = (lerp(0.98, 0.05, night), lerp(0.60, 0.05, night), lerp(0.35, 0.18, night))
    mid = (lerp(1.0, 0.25, night), lerp(0.78, 0.12, night), lerp(0.45, 0.30, night))
    ctx.set_source(vgrad(ctx, 0, -800, 0, 1200, [(0, top), (1, mid)]))
    ctx.paint()
    if night > 0.4:
        rng = np.random.default_rng(5)
        for _ in range(50):
            circle(ctx, rng.uniform(-400, W + 400), rng.uniform(-600, 800), rng.uniform(1.5, 3.5))
            fill(ctx, WHITE, 0.3 + 0.4 * math.sin(T * 2 + _))
    # dunas
    for k, (yb, col) in enumerate(((1050, SAND_D), (1180, SAND), (1350, (0.78, 0.56, 0.33)))):
        ctx.move_to(-900, H + 900)
        ctx.line_to(-900, yb)
        for x in range(-900, W + 950, 60):
            ctx.line_to(x, yb + 40 * math.sin(x / 260 + k * 1.7))
        ctx.line_to(W + 900, H + 900)
        ctx.close_path()
        fill(ctx, tuple(c * lerp(1, 0.35, night) for c in col))
    for cx, s in ((90, 1.0), (960, 0.8), (-200, 1.3)):
        cactus(ctx, cx, 1110, s, (0.10, 0.20, 0.12) if night < 0.5 else (0.04, 0.06, 0.08))


def cactus(ctx, x, y, s, col):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -22, -230, 44, 240, 22)
    rrect(ctx, -80, -150, 30, 80, 15)
    rrect(ctx, -80, -100, 70, 26, 13)
    rrect(ctx, 50, -190, 30, 100, 15)
    rrect(ctx, 10, -120, 70, 26, 13)
    fill(ctx, col)
    ctx.restore()


# ---------------- HUD ----------------
def hud(ctx, T, label="", accent=CYAN):
    """Marco de HUD en coordenadas de pantalla: esquinas, etiqueta del canal y líneas de barrido."""
    screen(ctx)
    m, L = 60, 90
    for (x, y, sx, sy) in ((m, 230, 1, 1), (W - m, 230, -1, 1), (m, 1640, 1, -1), (W - m, 1640, -1, -1)):
        ctx.move_to(x, y + sy * L)
        ctx.line_to(x, y)
        ctx.line_to(x + sx * L, y)
        stroke(ctx, accent, 6, 0.85)
    if label:
        text(ctx, label, m + 4, 196, 30, accent, font="DejaVu Sans Mono", align="left", shadow=False)
    blink = 0.5 + 0.5 * math.sin(T * 6)
    circle(ctx, W - m - 12, 196, 10)
    fill(ctx, (1, 0.2, 0.2), 0.4 + 0.6 * blink)
    text(ctx, "REC", W - m - 32, 196, 28, WHITE, font="DejaVu Sans Mono", align="right", shadow=False)
    for y in range(0, H, 6):
        ctx.rectangle(0, y, W, 2)
    fill(ctx, (0, 0, 0), 0.10)


# ---------------- sprites pixel (diseño propio, no son los de Taito) ----------------
JELLY = [
    ["...XXXXX...",
     ".XXXXXXXXX.",
     "XX..X.X..XX",
     "XXXXXXXXXXX",
     "XXXXXXXXXXX",
     ".X..X.X..X.",
     "X..X...X..X"],
    ["...XXXXX...",
     ".XXXXXXXXX.",
     "XX..X.X..XX",
     "XXXXXXXXXXX",
     "XXXXXXXXXXX",
     "..X.X.X.X..",
     ".X.X...X.X."],
]
BLOB = [
    ["..X.....X..",
     "...XXXXX...",
     "..XXXXXXX..",
     ".XX.XXX.XX.",
     "XXXXXXXXXXX",
     "X.XX...XX.X",
     "...X...X..."],
    ["..X.....X..",
     "X..XXXXX..X",
     "X.XXXXXXX.X",
     "XXX.XXX.XXX",
     ".XXXXXXXXX.",
     "..XX...XX..",
     ".X.......X."],
]
TANK = ["....X....",
        "...XXX...",
        ".XXXXXXX.",
        "XXXXXXXXX",
        "XXXXXXXXX"]


def sprite(ctx, rows, x, y, px, rgb, a=1.0, halo=True):
    """Dibuja un sprite de texto ('X' = píxel) centrado en (x, y)."""
    h, w = len(rows), len(rows[0])
    x0, y0 = x - w * px / 2, y - h * px / 2
    if halo:
        glow(ctx, x, y, w * px * 0.9, rgb, 0.18 * a)
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c == "X":
                ctx.rectangle(x0 + i * px, y0 + j * px, px * 0.92, px * 0.92)
    fill(ctx, rgb, a)


def alien(ctx, x, y, px, T, kind=0, rgb=None, a=1.0, rate=2.0):
    frames = JELLY if kind % 2 == 0 else BLOB
    col = rgb or (LIME if kind % 2 == 0 else CYAN)
    sprite(ctx, frames[int(T * rate) % 2], x, y, px, col, a)


def alien_grid(ctx, cx, cy, T, rows=5, cols=11, px=9, gap=118, alive=None, shift=0.0, rate=2.0):
    """Formación de alienígenas. alive(r, c) -> bool."""
    for r in range(rows):
        for c in range(cols):
            if alive and not alive(r, c):
                continue
            x = cx + (c - (cols - 1) / 2) * gap * 0.82 + shift
            y = cy + (r - (rows - 1) / 2) * gap * 0.75
            alien(ctx, x, y, px, T + r * 0.1, r // 2, rate=rate)


def tank(ctx, x, y, px=12, rgb=LIME):
    sprite(ctx, TANK, x, y, px, rgb)


def crt(ctx, x, y, w, h, T, inner=None, frame=STEEL_D):
    """Pantalla CRT con marco. inner(ctx) dibuja dentro (recortado)."""
    rrect(ctx, x - w / 2 - 30, y - h / 2 - 30, w + 60, h + 60, 40)
    fill(ctx, frame)
    rrect(ctx, x - w / 2, y - h / 2, w, h, 30)
    fill_keep(ctx, (0.01, 0.02, 0.04))
    ctx.save()
    ctx.clip()
    if inner:
        inner(ctx)
    for yy in range(int(y - h / 2), int(y + h / 2), 6):
        ctx.rectangle(x - w / 2, yy, w, 2)
    fill(ctx, (0, 0, 0), 0.25)
    ctx.restore()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 30)
    stroke(ctx, CYAN, 4, 0.4)


def cabinet(ctx, x, y, s, T, marquee="ARCADE", screen_fn=None, col=VIOLET):
    """Máquina recreativa genérica (sin logos). (x, y) = centro de la pantalla."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-260, -420); ctx.line_to(260, -420); ctx.line_to(260, 760); ctx.line_to(-260, 760); ctx.close_path()
    fill(ctx, tuple(c * 0.55 for c in col))
    rrect(ctx, -240, -400, 480, 130, 16)
    fill(ctx, (0.05, 0.05, 0.10))
    text(ctx, marquee, 0, -335, 64, MAGENTA, font="Anton", shadow=False)
    glow(ctx, 0, -335, 260, MAGENTA, 0.15)
    crt(ctx, 0, 0, 400, 320, T, screen_fn)
    ctx.move_to(-260, 230); ctx.line_to(260, 230); ctx.line_to(300, 360); ctx.line_to(-300, 360); ctx.close_path()
    fill(ctx, tuple(c * 0.75 for c in col))
    circle(ctx, -120, 290, 26); fill(ctx, (0.1, 0.1, 0.1))
    rrect(ctx, -128, 220, 16, 70, 8); fill(ctx, (0.1, 0.1, 0.1))
    circle(ctx, -120, 220, 22); fill(ctx, RED)
    for bx in (60, 140):
        circle(ctx, bx, 295, 24); fill(ctx, YELLOW if bx == 60 else CYAN)
    rrect(ctx, -60, 520, 120, 90, 10); fill(ctx, (0.05, 0.05, 0.08))
    rrect(ctx, -20, 545, 40, 40, 6); fill(ctx, ORANGE)
    ctx.restore()


def chip(ctx, x, y, s, T, heat=0.0, label="CPU", tired=0.0):
    """Procesador con patas. heat 0..1 lo pone rojo y brillante; tired añade gotas de sudor."""
    ctx.save()
    ctx.translate(x + (math.sin(T * 60) * 4 * heat if heat > 0.7 else 0), y)
    ctx.scale(s, s)
    if heat > 0:
        glow(ctx, 0, 0, 420, ORANGE, 0.45 * heat)
    for k in range(8):
        for sgn in (-1, 1):
            rrect(ctx, -175 + k * 50 - 9, sgn * 180 - 24, 18, 48, 4)
            rrect(ctx, sgn * 180 - 24, -175 + k * 50 - 9, 48, 18, 4)
    fill(ctx, (0.85, 0.80, 0.60))
    body = tuple(lerp(a, b, heat) for a, b in zip((0.12, 0.13, 0.18), (0.75, 0.15, 0.10)))
    rrect(ctx, -170, -170, 340, 340, 26)
    fill_keep(ctx, body)
    stroke(ctx, (0.35, 0.37, 0.45), 6)
    rrect(ctx, -110, -110, 220, 220, 14)
    stroke(ctx, (0.45, 0.47, 0.55), 4, 0.8)
    text(ctx, label, 0, 0, 70, WHITE, font="DejaVu Sans Mono", shadow=False)
    if tired > 0:
        for k in range(3):
            yy = -150 + ((T * 140 + k * 70) % 220)
            ctx.move_to(200 + k * 30, yy - 30)
            ctx.curve_to(225 + k * 30, yy, 225 + k * 30, yy + 15, 200 + k * 30, yy + 15)
            ctx.curve_to(175 + k * 30, yy + 15, 175 + k * 30, yy, 200 + k * 30, yy - 30)
            fill(ctx, CYAN, 0.8 * tired)
    ctx.restore()


def meter(ctx, x, y, w, val, label, rgb=ORANGE, appear=1.0):
    """Barra de carga horizontal con porcentaje."""
    if appear <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    text(ctx, label, -w / 2, -58, 38, WHITE, font="DejaVu Sans Mono", align="left", shadow=False)
    text(ctx, f"{val * 100:.0f}%", w / 2, -58, 38, rgb, font="DejaVu Sans Mono", align="right", shadow=False)
    rrect(ctx, -w / 2, -24, w, 48, 12)
    fill_keep(ctx, (0.05, 0.05, 0.10))
    stroke(ctx, WHITE, 4, 0.6)
    segs = 20
    for k in range(int(segs * clamp(val))):
        rrect(ctx, -w / 2 + 8 + k * (w - 16) / segs, -16, (w - 16) / segs - 6, 32, 4)
        fill(ctx, rgb if k < segs * 0.75 else RED)
    ctx.restore()


def speedometer(ctx, x, y, r, val, label="SPEED", appear=1.0):
    if appear <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    ctx.arc(0, 0, r, math.pi * 0.8, math.pi * 2.2)
    stroke(ctx, (0.2, 0.2, 0.3), 34)
    ctx.arc(0, 0, r, math.pi * 0.8, math.pi * (0.8 + 1.4 * clamp(val)))
    stroke(ctx, RED if val > 0.75 else ORANGE, 34)
    ang = math.pi * (0.8 + 1.4 * clamp(val))
    ctx.move_to(0, 0)
    ctx.line_to(math.cos(ang) * r * 0.85, math.sin(ang) * r * 0.85)
    stroke(ctx, WHITE, 12)
    circle(ctx, 0, 0, 22); fill(ctx, WHITE)
    text(ctx, label, 0, r * 0.55, 40, WHITE, font="DejaVu Sans Mono", shadow=False)
    ctx.restore()


def big_number(ctx, s, x, y, size=220, rgb=YELLOW, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    glow(ctx, 0, 0, size * 1.6, rgb, 0.18)
    ctx.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    adv = ctx.text_extents(s)[4]
    if adv > 900:
        size *= 900 / adv
        ctx.set_font_size(size)
        adv = ctx.text_extents(s)[4]
    ctx.move_to(-adv / 2, size * 0.36)
    ctx.text_path(s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(16); ctx.stroke_preserve()
    ctx.set_source_rgb(*rgb); ctx.fill()
    ctx.restore()


def rays(ctx, x, y, T, rgb, a=0.06, n=16):
    for k in range(n):
        ctx.save(); ctx.translate(x, y); ctx.rotate(k * math.tau / n + T * 0.25)
        ctx.move_to(0, 0); ctx.line_to(1600, -110); ctx.line_to(1600, 110); ctx.close_path()
        fill(ctx, rgb, a); ctx.restore()


def old_pc(ctx, x, y, s, T, bad=0.0):
    """Ordenador antiguo beige con una barra de carga que no avanza."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -300, -260, 600, 440, 30); fill(ctx, (0.85, 0.80, 0.68))
    rrect(ctx, -250, -215, 500, 330, 18); fill(ctx, (0.05, 0.12, 0.08))
    text(ctx, "LOADING...", 0, -90, 46, LIME, font="DejaVu Sans Mono", shadow=False)
    rrect(ctx, -200, -20, 400, 50, 8); stroke(ctx, LIME, 4)
    p = 0.12 + 0.03 * math.sin(T * 2)
    rrect(ctx, -192, -12, 384 * p, 34, 6); fill(ctx, LIME)
    rrect(ctx, -120, 180, 240, 60, 10); fill(ctx, (0.75, 0.70, 0.58))
    rrect(ctx, -360, 240, 720, 120, 20); fill(ctx, (0.80, 0.75, 0.63))
    for k in range(10):
        rrect(ctx, -320 + k * 66, 268, 52, 30, 6); fill(ctx, (0.62, 0.58, 0.48))
    ctx.restore()
    if bad > 0:
        ctx.save(); ctx.translate(x, y - 40 * s); ctx.scale(bad * s, bad * s)
        for sg in (-1, 1):
            ctx.move_to(-200, -200 * sg); ctx.line_to(200, 200 * sg)
        stroke(ctx, RED, 40); ctx.restore()


def circuit(ctx, x, y, w, h, T, progress=1.0):
    """Placa de circuito que se va 'trazando' (progress 0..1)."""
    rrect(ctx, x - w / 2, y - h / 2, w, h, 20)
    fill_keep(ctx, (0.04, 0.30, 0.18))
    stroke(ctx, (0.6, 0.9, 0.6), 5, 0.6)
    rng = np.random.default_rng(8)
    n = 26
    for k in range(int(n * clamp(progress))):
        x0, y0 = rng.uniform(x - w / 2 + 40, x + w / 2 - 40), rng.uniform(y - h / 2 + 40, y + h / 2 - 40)
        x1 = x0 + rng.choice([-1, 1]) * rng.uniform(60, 220)
        y1 = y0 + rng.choice([-1, 1]) * rng.uniform(40, 160)
        x1 = clamp(x1, x - w / 2 + 30, x + w / 2 - 30)
        y1 = clamp(y1, y - h / 2 + 30, y + h / 2 - 30)
        ctx.move_to(x0, y0); ctx.line_to(x1, y0); ctx.line_to(x1, y1)
        stroke(ctx, (0.95, 0.80, 0.35), 6)
        circle(ctx, x1, y1, 12); fill(ctx, (0.95, 0.80, 0.35))
    for k in range(int(4 * clamp(progress * 1.3))):
        rrect(ctx, x - w / 2 + 80 + k * (w - 160) / 4, y - 40, 120, 80, 8)
        fill(ctx, (0.08, 0.08, 0.10))


# ---------------- piezas del vídeo de Atari ----------------
def cartridge(ctx, x, y, s, rot=0.0, label="E.T.", wrap=0.0, dirt=0.0, col=(0.20, 0.20, 0.22)):
    """Cartucho genérico de consola de los 80 (sin logos ni personajes). (x, y) = centro."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -170, -230, 340, 460, 22); fill(ctx, (0, 0, 0), 0.35)
    rrect(ctx, -180, -240, 360, 460, 22); fill(ctx, col)
    for k in range(6):
        rrect(ctx, -150 + k * 52, -225, 36, 70, 6); fill(ctx, tuple(c * 0.7 for c in col))
    rrect(ctx, -140, -120, 280, 260, 14)
    ctx.set_source(vgrad(ctx, 0, -120, 0, 140, [(0, (0.95, 0.55, 0.15)), (1, (0.85, 0.20, 0.15))]))
    ctx.fill()
    glow(ctx, 60, -40, 90, (1, 0.95, 0.7), 0.55)
    circle(ctx, 60, -40, 34); fill(ctx, (1, 0.97, 0.85))
    ctx.move_to(-140, 60); ctx.curve_to(-60, 20, 40, 90, 140, 40); ctx.line_to(140, 140); ctx.line_to(-140, 140)
    ctx.close_path(); fill(ctx, (0.25, 0.08, 0.18))
    rrect(ctx, -140, 150, 280, 56, 8); fill(ctx, (0.08, 0.08, 0.10))
    text(ctx, label, 0, 178, 44, WHITE, font="Anton", shadow=False)
    if dirt > 0:
        rng = np.random.default_rng(2)
        for _ in range(40):
            circle(ctx, rng.uniform(-170, 170), rng.uniform(-230, 210), rng.uniform(6, 22))
            fill(ctx, SAND_D, 0.55 * dirt)
    if wrap > 0:
        rrect(ctx, -190, -250, 380, 480, 26)
        fill_keep(ctx, (0.9, 0.95, 1.0), 0.10 * wrap)
        stroke(ctx, WHITE, 5, 0.6 * wrap)
        ctx.move_to(-150, -230); ctx.line_to(-60, -230); ctx.line_to(-170, 30); ctx.line_to(-180, -100)
        ctx.close_path(); fill(ctx, WHITE, 0.25 * wrap)
    ctx.restore()


def warehouse(ctx, x, y, s, fill_lvl=1.0, T=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-460, -260); ctx.line_to(0, -420); ctx.line_to(460, -260); ctx.close_path()
    fill(ctx, (0.35, 0.36, 0.44))
    ctx.rectangle(-440, -262, 880, 560); fill(ctx, (0.25, 0.26, 0.34))
    ctx.rectangle(-360, -150, 720, 448); fill(ctx, (0.08, 0.08, 0.12))
    n = int(48 * clamp(fill_lvl))
    for k in range(n):
        c, r = k % 8, k // 8
        rrect(ctx, -350 + c * 88, 230 - r * 72, 82, 66, 6)
        fill(ctx, (0.78, 0.58, 0.36) if (c + r) % 3 else (0.70, 0.50, 0.30))
        text(ctx, "E.T.", -309 + c * 88, 263 - r * 72, 22, (0.35, 0.22, 0.12), font="Anton", shadow=False)
    ctx.restore()


def pit(ctx, x, y, w, depth, T, carts=0, dug=1.0):
    """Corte de terreno: un hoyo con capas y cartuchos al fondo."""
    ctx.rectangle(-900, y, W + 1800, H + 900)
    fill(ctx, SAND)
    for k, col in enumerate(((0.70, 0.50, 0.30), (0.58, 0.40, 0.24), (0.45, 0.30, 0.18), (0.34, 0.22, 0.14))):
        ctx.rectangle(-900, y + 80 + k * 170, W + 1800, 170)
        fill(ctx, col)
    d = depth * dug
    ctx.move_to(x - w / 2, y); ctx.line_to(x - w / 2 + 60, y + d); ctx.line_to(x + w / 2 - 60, y + d)
    ctx.line_to(x + w / 2, y); ctx.close_path()
    fill(ctx, (0.10, 0.07, 0.06))
    rng = np.random.default_rng(4)
    for k in range(carts):
        cartridge(ctx, x + rng.uniform(-w / 2 + 120, w / 2 - 120), y + depth - 80 - rng.uniform(0, 140),
                  0.32, rng.uniform(-0.8, 0.8), dirt=0.6)


def tombstone(ctx, x, y, s, lines, T, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * appear, s * appear)
    ctx.move_to(-230, 300); ctx.line_to(-230, -150); ctx.curve_to(-230, -390, 230, -390, 230, -150)
    ctx.line_to(230, 300); ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -380, 0, 300, [(0, (0.62, 0.64, 0.70)), (1, (0.38, 0.40, 0.46))]))
    ctx.fill()
    ctx.move_to(-230, 300); ctx.line_to(-230, -150); ctx.curve_to(-230, -390, 230, -390, 230, -150)
    ctx.line_to(230, 300)
    stroke(ctx, (0.25, 0.26, 0.30), 8)
    for k, ln in enumerate(lines):
        text(ctx, ln, 0, -170 + k * 110, 88 if k == 0 else 54, (0.20, 0.20, 0.24), font="Anton", shadow=False)
    ctx.restore()


def candle(ctx, x, y, T):
    rrect(ctx, x - 18, y - 90, 36, 110, 8); fill(ctx, (0.95, 0.92, 0.85))
    fl = 1 + 0.15 * math.sin(T * 18 + x)
    glow(ctx, x, y - 120, 90 * fl, ORANGE, 0.5)
    ellipse(ctx, x, y - 118, 14 * fl, 28 * fl); fill(ctx, (1, 0.85, 0.3))


# ======================================================================
# SUBTÍTULOS "Behind the HUD": 5 estilos gamer que cambian en cada frase.
# Uso en escenas.py:  SUBTITULO = subtitulo_hud
# Los números, años y cantidades ($) usan siempre el estilo COMBO.
# ======================================================================
CAP_Y = 1060
CAP_MAXW = 900
_CAP_ACCENTS = [CYAN, MAGENTA, LIME, ORANGE, VIOLET]


def _cap_word(chunk):
    return " ".join(x["text"] for x in chunk["words"]).upper().strip().rstrip(",")


def _fit(ctx, font, w, size, maxw=CAP_MAXW, weight=cairo.FONT_WEIGHT_NORMAL):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, weight)
    ctx.set_font_size(size)
    adv = ctx.text_extents(w)[4]
    if adv > maxw:
        size *= maxw / adv
        ctx.set_font_size(size)
        adv = ctx.text_extents(w)[4]
    return size, adv


def _path(ctx, w, x, y):
    ctx.new_path(); ctx.move_to(x, y); ctx.text_path(w)


def cap_neon(ctx, w, lt, acc):
    """Letras blancas con halo de neón del color de la frase."""
    size, adv = _fit(ctx, "Anton", w, 170)
    k = ease_back(clamp(lt / 0.08))
    ctx.save(); ctx.translate(W / 2, CAP_Y); ctx.scale(0.8 + 0.2 * k, 0.8 + 0.2 * k)
    x0, y0 = -adv / 2, size * 0.36
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    flick = 0.85 + 0.15 * math.sin(lt * 40) if lt < 0.12 else 1.0
    for lw, a in ((46, 0.12), (30, 0.22), (18, 0.45)):
        _path(ctx, w, x0, y0); ctx.set_source_rgba(*acc, a * flick); ctx.set_line_width(lw); ctx.stroke()
    _path(ctx, w, x0, y0); ctx.set_source_rgb(0.02, 0.02, 0.05); ctx.set_line_width(10); ctx.stroke()
    _path(ctx, w, x0, y0); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.restore()


def cap_arcade(ctx, w, lt, acc):
    """Letra pixelada de recreativa (escritura casi instantánea, 0,06 s); en 2 líneas si es larga."""
    words = w.split()
    if len(w) > 10 and len(words) > 1:
        best = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
    else:
        lines = [w]
    size = 92
    ctx.select_font_face("Press Start 2P", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    for ln in lines:
        ctx.set_font_size(size)
        adv = ctx.text_extents(ln)[4]
        if adv > CAP_MAXW:
            size *= CAP_MAXW / adv
    ctx.set_font_size(size)
    total = sum(len(x) for x in lines)
    n = max(1, int(math.ceil(total * clamp(lt / 0.06))))
    lh = size * 1.35
    y_first = CAP_Y + size * 0.5 - (len(lines) - 1) * lh / 2
    ctx.set_line_join(cairo.LINE_JOIN_MITER)
    for k, ln in enumerate(lines):
        shown = ln[:max(0, n)]
        n -= len(ln)
        if not shown:
            continue
        adv = ctx.text_extents(ln)[4]
        x0, y0 = W / 2 - adv / 2, y_first + k * lh
        _path(ctx, shown, x0 + 8, y0 + 8); ctx.set_source_rgb(*acc); ctx.fill()
        _path(ctx, shown, x0, y0); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(12); ctx.stroke()
        _path(ctx, shown, x0, y0); ctx.set_source_rgb(1, 1, 1); ctx.fill()


def cap_glitch(ctx, w, lt, acc):
    """La palabra entra 'rota' (canales rojo/cian desplazados) y se estabiliza."""
    size, adv = _fit(ctx, "Anton", w, 175)
    x0, y0 = W / 2 - adv / 2, CAP_Y + size * 0.36
    amt = 22 * (1 - clamp(lt / 0.10)) + 4
    rng = np.random.default_rng(int(lt * 30) + len(w))
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    _path(ctx, w, x0, y0); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(20); ctx.stroke()
    for dx, col in ((-amt, (1, 0.15, 0.3)), (amt, (0.1, 0.9, 1))):
        _path(ctx, w, x0 + dx, y0); ctx.set_source_rgba(*col, 0.85); ctx.fill()
    _path(ctx, w, x0, y0); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    if lt < 0.10:  # cortes horizontales
        for _ in range(4):
            yy = CAP_Y + rng.uniform(-size * 0.6, size * 0.3)
            ctx.rectangle(W / 2 - adv / 2 - 30, yy, adv + 60, rng.uniform(6, 16))
            ctx.set_source_rgba(*acc, 0.8); ctx.fill()


def cap_combo(ctx, w, lt, acc):
    """Dorado/naranja con rebote fuerte, como un 'COMBO x2'. Para números y años."""
    size, adv = _fit(ctx, "Bangers", w, 185)
    k = ease_back(clamp(lt / 0.09))
    s = 0.7 + 0.3 * k + (0.06 * math.sin(lt * 18) * math.exp(-lt * 4))
    ctx.save(); ctx.translate(W / 2, CAP_Y); ctx.rotate(-0.06); ctx.scale(s, s)
    x0, y0 = -adv / 2, size * 0.36
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    _path(ctx, w, x0 + 10, y0 + 12); ctx.set_source_rgb(0.45, 0.05, 0.02); ctx.set_line_width(28); ctx.stroke_preserve(); ctx.fill()
    _path(ctx, w, x0, y0); ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(22); ctx.stroke()
    g = cairo.LinearGradient(0, -size * 0.5, 0, size * 0.4)
    g.add_color_stop_rgb(0, 1, 0.97, 0.45); g.add_color_stop_rgb(0.55, 1, 0.80, 0.10); g.add_color_stop_rgb(1, 1, 0.45, 0.05)
    _path(ctx, w, x0, y0); ctx.set_source(g); ctx.fill()
    if lt < 0.35:  # destellos
        for k2 in range(6):
            a = k2 * math.tau / 6 + 0.3
            r = adv / 2 + 40 + 120 * (lt / 0.35)
            ctx.save(); ctx.translate(r * math.cos(a) * 0.9, r * math.sin(a) * 0.45)
            ctx.move_to(0, -18); ctx.line_to(6, 0); ctx.line_to(0, 18); ctx.line_to(-6, 0); ctx.close_path()
            ctx.set_source_rgba(1, 0.95, 0.5, 1 - lt / 0.35); ctx.fill(); ctx.restore()
    ctx.restore()


def cap_panel(ctx, w, lt, acc):
    """Panel de notificación de juego que entra deslizándose, con la palabra dentro."""
    size, adv = _fit(ctx, "Montserrat", w, 112, maxw=820, weight=cairo.FONT_WEIGHT_BOLD)
    p = ease(clamp(lt / 0.08))
    dx = (1 - p) * -160
    pw, ph = adv + 90, size * 1.45
    x, y = W / 2 - pw / 2 + dx, CAP_Y - ph / 2
    rrect(ctx, x + 8, y + 10, pw, ph, 18); fill(ctx, (0, 0, 0), 0.55 * p)
    rrect(ctx, x, y, pw, ph, 18); fill_keep(ctx, (0.04, 0.03, 0.10), 0.92 * p); stroke(ctx, acc, 7, p)
    ctx.rectangle(x, y + 14, 12, ph - 28); fill(ctx, acc, p)
    ctx.select_font_face("Montserrat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    _path(ctx, w, x + 45, CAP_Y + size * 0.36)
    ctx.set_source_rgba(1, 1, 1, p); ctx.fill()


CAP_STYLES = [cap_neon, cap_arcade, cap_glitch, cap_panel, cap_neon, cap_glitch, cap_arcade, cap_panel]


def subtitulo_hud(ctx, chunk, T):
    """Subtítulo del canal: el estilo cambia en cada frase; los números van en COMBO."""
    w = _cap_word(chunk)
    if not w:
        return
    lt = T - chunk["start"]
    sent = chunk.get("sent", 0)
    acc = _CAP_ACCENTS[sent % len(_CAP_ACCENTS)]
    if any(c.isdigit() for c in w) or "$" in w:
        cap_combo(ctx, w, lt, acc)
    else:
        CAP_STYLES[sent % len(CAP_STYLES)](ctx, w, lt, acc)


# ---------- piezas comunes añadidas en 006 ----------
def stamp(ctx, txt, x, y, appear, rgb=RED, rot=-0.18, size=74):
    """Sello que cae con golpe (texto en caja con borde)."""
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


def x_mark(ctx, x, y, r, p, rgb=RED, w=26):
    """Aspa roja que se dibuja (p 0..1)."""
    if p <= 0:
        return
    for sgn in (1, -1):
        q = clamp(p * 2 - (0 if sgn == 1 else 1))
        if q > 0:
            ctx.move_to(x - r, y - sgn * r); ctx.line_to(x - r + 2 * r * q, y - sgn * r + sgn * 2 * r * q)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); stroke(ctx, rgb, w)


def tile(ctx, ch, x, y, size, appear=1.0, rgb=YELLOW, rot=0.0, bg=(0.06, 0.07, 0.14)):
    """Ficha cuadrada con una letra/símbolo (botón, tecla)."""
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(appear, appear)
    rrect(ctx, -size / 2 + 8, -size / 2 + 12, size, size, size * 0.14); fill(ctx, (0, 0, 0), 0.4)
    rrect(ctx, -size / 2, -size / 2, size, size, size * 0.14); fill_keep(ctx, bg); stroke(ctx, rgb, size * 0.05)
    glow(ctx, 0, 0, size * 0.8, rgb, 0.12)
    text(ctx, ch, 0, size * 0.05, size * 0.72, rgb, font="Anton", shadow=False)
    ctx.restore()


def gamepad(ctx, x, y, s, T, press=None, col=(0.22, 0.22, 0.30), accent=CYAN):
    """Mando genérico rectangular (diseño propio). press: 'up','down','left','right','B','A' resalta."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -330, -140, 660, 280, 70); fill(ctx, col)
    rrect(ctx, -330, -140, 660, 280, 70); stroke(ctx, accent, 6, 0.7)
    dirs = {"up": (0, -55), "down": (0, 55), "left": (-55, 0), "right": (55, 0)}
    ctx.rectangle(-230 - 25, -80, 50, 160); fill(ctx, (0.08, 0.08, 0.1))
    ctx.rectangle(-230 - 80, -25, 160, 50); fill(ctx, (0.08, 0.08, 0.1))
    if press in dirs:
        dx, dy = dirs[press]
        rrect(ctx, -230 + dx - 25, dy - 25, 50, 50, 8); fill(ctx, YELLOW)
        glow(ctx, -230 + dx, dy, 80, YELLOW, 0.4)
    for lab, bx in (("B", 150), ("A", 250)):
        on = press == lab
        circle(ctx, bx, 20, 44); fill(ctx, YELLOW if on else RED)
        if on:
            glow(ctx, bx, 20, 100, YELLOW, 0.4)
        text(ctx, lab, bx, 100, 36, WHITE, font="Anton", shadow=False)
    for k in (-50, 30):
        rrect(ctx, k, 60, 60, 18, 9); fill(ctx, (0.08, 0.08, 0.1))
    ctx.restore()
