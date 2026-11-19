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
