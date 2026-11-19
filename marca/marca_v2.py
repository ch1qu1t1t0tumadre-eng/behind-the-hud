"""Marca v2 de Behind the HUD: logo cromado synthwave + banner como pantalla HUD de un juego."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import anim  # registra fuentes
from hud import *  # noqa

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = (0.03, 0.01, 0.10)


def sky(ctx, w, h, hz):
    g = cairo.LinearGradient(0, 0, 0, hz)
    g.add_color_stop_rgb(0, 0.02, 0.01, 0.08); g.add_color_stop_rgb(0.6, 0.16, 0.03, 0.30); g.add_color_stop_rgb(1, 0.55, 0.08, 0.45)
    ctx.set_source(g); ctx.rectangle(0, 0, w, hz); ctx.fill()
    rng = np.random.default_rng(7)
    for _ in range(int(w * h / 9000)):
        x, y = rng.uniform(0, w), rng.uniform(0, hz * 0.8)
        r = rng.uniform(0.8, 2.6)
        circle(ctx, x, y, r); fill(ctx, WHITE, rng.uniform(0.3, 0.9) * (1 - y / hz))


def sun(ctx, cx, cy, r, bg_y_top, bg_y_bot):
    glow(ctx, cx, cy, r * 2.2, (1, 0.35, 0.55), 0.35)
    g = cairo.LinearGradient(0, cy - r, 0, cy + r)
    g.add_color_stop_rgb(0, 1, 0.93, 0.35); g.add_color_stop_rgb(0.5, 1, 0.45, 0.35); g.add_color_stop_rgb(1, 0.95, 0.10, 0.55)
    ctx.save(); circle(ctx, cx, cy, r); ctx.clip()
    ctx.set_source(g); ctx.paint()
    # franjas recortadas (clásicas del synthwave)
    n = 7
    for k in range(n):
        p = k / n
        y = cy + r * (0.05 + 0.95 * p)
        hgt = r * (0.02 + 0.07 * p)
        ctx.rectangle(cx - r, y, 2 * r, hgt); ctx.set_operator(cairo.OPERATOR_CLEAR); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.restore()


def mountains(ctx, w, hz, scale, seed=2):
    rng = np.random.default_rng(seed)
    pts = [(-50, hz)]
    x = -50
    while x < w + 50:
        x += rng.uniform(80, 200) * scale
        pts.append((x, hz - rng.uniform(40, 170) * scale))
        x += rng.uniform(60, 160) * scale
        pts.append((x, hz - rng.uniform(5, 60) * scale))
    pts.append((w + 50, hz))
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source_rgb(0.05, 0.01, 0.12); ctx.fill_preserve()
    ctx.set_source_rgba(*MAGENTA, 0.9); ctx.set_line_width(3 * scale); ctx.stroke()


def floor(ctx, w, h, hz, scale):
    g = cairo.LinearGradient(0, hz, 0, h)
    g.add_color_stop_rgb(0, 0.10, 0.01, 0.18); g.add_color_stop_rgb(1, 0.01, 0.0, 0.04)
    ctx.set_source(g); ctx.rectangle(0, hz, w, h - hz); ctx.fill()
    for i in range(-40, 41):
        ctx.move_to(w / 2 + i * 40 * scale, hz); ctx.line_to(w / 2 + i * 300 * scale, h + 200)
    ctx.set_source_rgba(*CYAN, 0.55); ctx.set_line_width(2.2 * scale); ctx.stroke()
    for k in range(1, 14):
        y = hz + (h - hz) * (k / 14) ** 2.2
        ctx.move_to(0, y); ctx.line_to(w, y)
        ctx.set_source_rgba(*CYAN, 0.25 + 0.04 * k); ctx.set_line_width((1.5 + k * 0.35) * scale); ctx.stroke()
    glow(ctx, w / 2, hz, w * 0.5, MAGENTA, 0.22)
    ctx.move_to(0, hz); ctx.line_to(w, hz); ctx.set_source_rgba(1, 0.6, 0.9, 0.9); ctx.set_line_width(3 * scale); ctx.stroke()


def chrome_text(ctx, s, cx, base, size, font="Anton", extrude=None, skew=-0.12, maxw=None):
    """Texto cromado synthwave con extrusión 3D, contorno y brillo."""
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(size)
    adv = ctx.text_extents(s)[4]
    if maxw and adv > maxw:
        size *= maxw / adv; ctx.set_font_size(size); adv = ctx.text_extents(s)[4]
    ex = extrude if extrude is not None else size * 0.09
    ctx.save()
    ctx.translate(cx, base)
    ctx.transform(cairo.Matrix(1, 0, skew, 1, 0, 0))
    x0 = -adv / 2
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    # halo
    for lw, a in ((size * 0.28, 0.10), (size * 0.16, 0.18)):
        ctx.new_path(); ctx.move_to(x0, 0); ctx.text_path(s); ctx.set_source_rgba(*MAGENTA, a); ctx.set_line_width(lw); ctx.stroke()
    # extrusión
    steps = int(ex)
    for k in range(steps, 0, -1):
        t = k / steps
        ctx.new_path(); ctx.move_to(x0 + k * 0.5, k); ctx.text_path(s)
        ctx.set_source_rgb(lerp(0.55, 0.20, t), lerp(0.05, 0.02, t), lerp(0.45, 0.25, t)); ctx.fill()
    ctx.new_path(); ctx.move_to(x0, 0); ctx.text_path(s)
    ctx.set_source_rgb(0.02, 0.0, 0.06); ctx.set_line_width(size * 0.05); ctx.stroke()
    # relleno cromado: cielo arriba, línea de horizonte, reflejo cálido abajo
    g = cairo.LinearGradient(0, -size * 0.74, 0, 0)
    g.add_color_stop_rgb(0.00, 0.85, 0.97, 1.00)
    g.add_color_stop_rgb(0.40, 0.30, 0.55, 0.95)
    g.add_color_stop_rgb(0.52, 0.98, 0.98, 1.00)
    g.add_color_stop_rgb(0.54, 0.25, 0.05, 0.35)
    g.add_color_stop_rgb(0.75, 0.95, 0.35, 0.65)
    g.add_color_stop_rgb(1.00, 1.00, 0.85, 0.55)
    ctx.new_path(); ctx.move_to(x0, 0); ctx.text_path(s); ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.move_to(x0, 0); ctx.text_path(s); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(size * 0.012); ctx.stroke()
    ctx.restore()
    return adv


def pixel_text(ctx, s, x, y, size, rgb, align="left", shadow=MAGENTA):
    ctx.select_font_face("Press Start 2P"); ctx.set_font_size(size)
    adv = ctx.text_extents(s)[4]
    if align == "center":
        x -= adv / 2
    elif align == "right":
        x -= adv
    if shadow:
        ctx.move_to(x + size * 0.15, y + size * 0.15); ctx.set_source_rgb(*shadow); ctx.show_text(s)
    ctx.move_to(x, y); ctx.set_source_rgb(*rgb); ctx.show_text(s)
    return adv


def bar(ctx, x, y, w, h, val, rgb, label):
    pixel_text(ctx, label, x, y - h * 0.45, h * 0.7, WHITE, shadow=None)
    rrect(ctx, x, y, w, h, h * 0.25); fill_keep(ctx, (0, 0, 0), 0.65); stroke(ctx, WHITE, 3, 0.8)
    segs = 12
    for k in range(int(segs * val)):
        rrect(ctx, x + 6 + k * (w - 12) / segs, y + 6, (w - 12) / segs - 5, h - 12, 3)
        fill(ctx, rgb)


def avatar(path, S=800):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); ctx = cairo.Context(surf)
    hz = S * 0.66
    sky(ctx, S, S, hz)
    sun(ctx, S / 2, hz - S * 0.02, S * 0.33, 0, hz)
    mountains(ctx, S, hz, S / 1400, seed=5)
    floor(ctx, S, S, hz, S / 1400)
    chrome_text(ctx, "HUD", S / 2 + 10, hz + S * 0.03, S * 0.40, maxw=S * 0.74)
    # mira pequeña de HUD
    ctx.set_line_width(S * 0.012)
    for (x, y, sx, sy) in ((S * 0.24, S * 0.24, 1, 1), (S * 0.76, S * 0.24, -1, 1)):
        ctx.move_to(x, y + sy * S * 0.06); ctx.line_to(x, y); ctx.line_to(x + sx * S * 0.06, y)
        ctx.set_source_rgba(*CYAN, 0.95); ctx.stroke()
    surf.write_to_png(path)


def banner(path, Wb=2560, Hb=1440):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Wb, Hb); ctx = cairo.Context(surf)
    hz = Hb * 0.60
    sky(ctx, Wb, Hb, hz)
    sun(ctx, Wb / 2, hz - 30, 330, 0, hz)
    mountains(ctx, Wb, hz, 1.25, seed=3)
    floor(ctx, Wb, Hb, hz, 1.25)
    # logo (dentro de la zona segura 1546x423 centrada: y 508–931)
    chrome_text(ctx, "BEHIND THE HUD", Wb / 2 + 12, 770, 210, maxw=1400)
    rrect(ctx, Wb / 2 - 640, 872, 1280, 54, 12); fill_keep(ctx, (0.02, 0.0, 0.06), 0.85); stroke(ctx, CYAN, 3, 0.7)
    pixel_text(ctx, "THE HIDDEN REASONS BEHIND VIDEO GAMES", Wb / 2, 913, 28, CYAN, align="center", shadow=(0.2, 0.0, 0.3))
    # elementos de HUD a los lados (visibles en PC y TV; franja central 508–931)
    bar(ctx, 140, 540, 420, 44, 0.9, (0.25, 1, 0.45), "HP")
    bar(ctx, 140, 640, 420, 30, 0.55, CYAN, "XP  LVL 01")
    rrect(ctx, 120, 712, 470, 140, 14); fill_keep(ctx, (0.02, 0.0, 0.06), 0.85); stroke(ctx, YELLOW, 3, 0.8)
    pixel_text(ctx, "QUEST", 145, 755, 26, YELLOW, shadow=(0.4, 0.2, 0))
    pixel_text(ctx, "FIND THE SECRET", 145, 800, 20, WHITE, shadow=None)
    pixel_text(ctx, "BEHIND EVERY GAME", 145, 834, 20, WHITE, shadow=None)
    # minimapa
    mx, my, mr = 2300, 700, 150
    circle(ctx, mx, my, mr); fill_keep(ctx, (0.02, 0.05, 0.10), 0.85); stroke(ctx, CYAN, 6)
    for k in range(1, 3):
        circle(ctx, mx, my, mr * k / 3); stroke(ctx, CYAN, 2, 0.35)
    ctx.move_to(mx - mr, my); ctx.line_to(mx + mr, my); ctx.move_to(mx, my - mr); ctx.line_to(mx, my + mr); stroke(ctx, CYAN, 2, 0.35)
    for (dx, dy, c) in ((50, -60, YELLOW), (-70, 30, MAGENTA), (20, 80, LIME)):
        circle(ctx, mx + dx, my + dy, 12); fill(ctx, c)
    ctx.move_to(mx, my - 22); ctx.line_to(mx + 16, my + 16); ctx.line_to(mx - 16, my + 16); ctx.close_path(); fill(ctx, WHITE)
    rrect(ctx, 2140, 872, 320, 84, 12); fill_keep(ctx, (0.02, 0.0, 0.06), 0.85); stroke(ctx, YELLOW, 3, 0.8)
    pixel_text(ctx, "NEW SHORT", 2300, 906, 22, YELLOW, align="center", shadow=(0.4, 0.2, 0))
    pixel_text(ctx, "EVERY DAY", 2300, 940, 22, YELLOW, align="center", shadow=(0.4, 0.2, 0))
    # esquinas de HUD alrededor del logo
    for (x, y, sx, sy) in ((580, 520, 1, 1), (1980, 520, -1, 1), (580, 950, 1, -1), (1980, 950, -1, -1)):
        ctx.move_to(x, y + sy * 60); ctx.line_to(x, y); ctx.line_to(x + sx * 60, y)
        ctx.set_source_rgba(*CYAN, 0.9); ctx.set_line_width(8); ctx.stroke()
    # líneas de barrido
    for y in range(0, Hb, 5):
        ctx.rectangle(0, y, Wb, 1.5)
    ctx.set_source_rgba(0, 0, 0, 0.10); ctx.fill()
    surf.write_to_png(path)


if __name__ == "__main__":
    avatar(os.path.join(OUT, "foto_perfil_v2.png"))
    banner(os.path.join(OUT, "banner_v2.png"))
    print("ok")
