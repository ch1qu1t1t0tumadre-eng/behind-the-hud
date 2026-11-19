"""Marca v3 de Behind the HUD: oscuro y minimalista, un acento verde ácido y un símbolo propio (ojo con pupila-píxel)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import anim  # registra fuentes
import cairocffi as cairo
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
ACID = (0.72, 1.0, 0.0)
INK = (0.035, 0.035, 0.04)
WHITE = (0.96, 0.96, 0.94)
GREY = (0.45, 0.45, 0.48)


def base(ctx, w, h):
    ctx.set_source_rgb(*INK); ctx.paint()
    g = cairo.RadialGradient(w / 2, h / 2, 0, w / 2, h / 2, max(w, h) * 0.6)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.045); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(g); ctx.paint()
    rng = np.random.default_rng(1)  # grano fino
    for _ in range(int(w * h / 1400)):
        ctx.rectangle(rng.uniform(0, w), rng.uniform(0, h), 1.2, 1.2)
    ctx.set_source_rgba(1, 1, 1, 0.035); ctx.fill()


def eye_mark(ctx, cx, cy, s, lw=None, pupil_dx=0.0):
    """Símbolo: ojo de dos arcos + pupila cuadrada (píxel) verde + 4 esquinas de HUD."""
    lw = lw or s * 0.055
    ctx.set_line_cap(cairo.LINE_CAP_SQUARE); ctx.set_line_join(cairo.LINE_JOIN_MITER)
    w2, h2 = s * 0.50, s * 0.30
    ctx.move_to(cx - w2, cy); ctx.curve_to(cx - w2 * 0.45, cy - h2 * 1.25, cx + w2 * 0.45, cy - h2 * 1.25, cx + w2, cy)
    ctx.curve_to(cx + w2 * 0.45, cy + h2 * 1.25, cx - w2 * 0.45, cy + h2 * 1.25, cx - w2, cy)
    ctx.close_path()
    ctx.set_source_rgb(*WHITE); ctx.set_line_width(lw); ctx.stroke()
    p = s * 0.20
    ctx.rectangle(cx - p / 2 + pupil_dx * s, cy - p / 2, p, p); ctx.set_source_rgb(*ACID); ctx.fill()
    # esquinas de HUD
    b, L = s * 0.70, s * 0.16
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = cx + sx * b, cy + sy * b * 0.82
            ctx.move_to(x, y - sy * L); ctx.line_to(x, y); ctx.line_to(x - sx * L, y)
    ctx.set_source_rgb(*WHITE); ctx.set_line_width(lw * 0.75); ctx.stroke()


def tracked(ctx, s, x, y, size, rgb, font="Anton", track=0.06, weight=cairo.FONT_WEIGHT_NORMAL, measure=False):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, weight); ctx.set_font_size(size)
    total = sum(ctx.text_extents(c)[4] for c in s) + track * size * (len(s) - 1)
    if measure:
        return total
    cx = x
    for c in s:
        ctx.move_to(cx, y); ctx.set_source_rgb(*rgb); ctx.show_text(c)
        cx += ctx.text_extents(c)[4] + track * size
    return total


def avatar(path, S=800):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); ctx = cairo.Context(surf)
    base(ctx, S, S)
    eye_mark(ctx, S / 2, S / 2, S * 0.50)
    surf.write_to_png(path)


def banner(path, Wb=2560, Hb=1440):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Wb, Hb); ctx = cairo.Context(surf)
    base(ctx, Wb, Hb)
    # trama de puntos muy sutil
    for x in range(40, Wb, 64):
        for y in range(40, Hb, 64):
            ctx.rectangle(x, y, 2, 2)
    ctx.set_source_rgba(1, 1, 1, 0.05); ctx.fill()
    # bloque central (zona segura: 1546x423 centrada, y 508–931)
    size = 168
    w1 = tracked(ctx, "BEHIND THE ", 0, 0, size, WHITE, measure=True)
    w2 = tracked(ctx, "HUD", 0, 0, size, ACID, measure=True)
    mark = 230
    gap = 120
    total = mark + gap + w1 + w2
    x0 = Wb / 2 - total / 2
    eye_mark(ctx, x0 + mark / 2, Hb / 2 - 30, mark, lw=12)
    tx = x0 + mark + gap
    tracked(ctx, "BEHIND THE ", tx, Hb / 2 + 30, size, WHITE)
    tracked(ctx, "HUD", tx + w1, Hb / 2 + 30, size, ACID)
    # línea + lema en monoespaciada gris
    ctx.rectangle(tx, Hb / 2 + 70, 120, 6); ctx.set_source_rgb(*ACID); ctx.fill()
    tracked(ctx, "THE HIDDEN REASONS BEHIND VIDEO GAMES", tx + 150, Hb / 2 + 84, 30, GREY,
            font="DejaVu Sans Mono", track=0.12, weight=cairo.FONT_WEIGHT_BOLD)
    # detalles laterales mínimos (visibles en PC/TV)
    tracked(ctx, "NEW SHORT EVERY DAY", tx, Hb / 2 + 160, 24, WHITE, font="DejaVu Sans Mono", track=0.14, weight=cairo.FONT_WEIGHT_BOLD)
    ctx.rectangle(tx - 34, Hb / 2 + 142, 16, 16); ctx.set_source_rgb(*ACID); ctx.fill()
    surf.write_to_png(path)


if __name__ == "__main__":
    avatar(os.path.join(OUT, "foto_perfil_v3.png"))
    banner(os.path.join(OUT, "banner_v3.png"))
    print("ok")
