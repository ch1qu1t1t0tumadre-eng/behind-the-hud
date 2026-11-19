"""Foto de perfil (800x800) y banner (2560x1440) de Behind the HUD, con la estética del canal."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import anim  # registra las fuentes
from hud import *  # noqa
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ejemplos"))
from escenas_v03 import piece  # bloques genéricos

OUT = os.path.dirname(os.path.abspath(__file__))


def synth_bg(ctx, w, h, hz):
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgb(0, 0.02, 0.01, 0.07); g.add_color_stop_rgb(0.55, 0.10, 0.03, 0.20); g.add_color_stop_rgb(1, 0.03, 0.01, 0.08)
    ctx.set_source(g); ctx.paint()
    glow(ctx, w / 2, hz, w * 0.55, MAGENTA, 0.30)
    for i in range(-30, 31):
        ctx.move_to(w / 2 + i * w * 0.035, hz); ctx.line_to(w / 2 + i * w * 0.30, h + 400)
    stroke(ctx, MAGENTA, max(2, w / 600), 0.45)
    for k in range(10):
        y = hz + (h - hz) * (k / 10) ** 2.0
        ctx.move_to(0, y); ctx.line_to(w, y)
        stroke(ctx, MAGENTA, max(2, w / 700) * (1 + k / 5), 0.15 + 0.06 * k)
    rng = np.random.default_rng(3)
    for _ in range(int(w / 12)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, hz), rng.uniform(2, 5)
        ctx.rectangle(x, y, r, r); fill(ctx, rng.choice([0, 1]) and CYAN or WHITE, rng.uniform(0.2, 0.7))


def brackets(ctx, x0, y0, x1, y1, L, lw, rgb):
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        ctx.move_to(x, y + sy * L); ctx.line_to(x, y); ctx.line_to(x + sx * L, y)
        stroke(ctx, rgb, lw, 0.95)


def neon_word(ctx, s, x, y, size, rgb, font="Anton", align="center"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(size)
    adv = ctx.text_extents(s)[4]
    x0 = x - adv / 2 if align == "center" else x
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, a in ((size * 0.30, 0.10), (size * 0.18, 0.22), (size * 0.10, 0.45)):
        ctx.new_path(); ctx.move_to(x0, y); ctx.text_path(s); ctx.set_source_rgba(*rgb, a); ctx.set_line_width(lw); ctx.stroke()
    ctx.new_path(); ctx.move_to(x0, y); ctx.text_path(s); ctx.set_source_rgb(0.02, 0.02, 0.05); ctx.set_line_width(size * 0.06); ctx.stroke()
    ctx.new_path(); ctx.move_to(x0, y); ctx.text_path(s); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    return adv


def avatar(path, S=800):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); ctx = cairo.Context(surf)
    synth_bg(ctx, S, S, S * 0.74)
    # retícula de HUD
    cx, cy, r = S / 2, S / 2, S * 0.30
    glow(ctx, cx, cy, r * 1.5, CYAN, 0.25)
    ctx.arc(cx, cy, r, 0, math.tau); stroke(ctx, CYAN, S * 0.018, 0.95)
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        ctx.move_to(cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78)
        ctx.line_to(cx + math.cos(a) * r * 1.22, cy + math.sin(a) * r * 1.22)
    stroke(ctx, CYAN, S * 0.018)
    sprite(ctx, JELLY[0], cx, cy, S * 0.032, LIME)
    brackets(ctx, S * 0.20, S * 0.20, S * 0.80, S * 0.80, S * 0.07, S * 0.018, MAGENTA)
    surf.write_to_png(path)


def banner(path, Wb=2560, Hb=1440):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Wb, Hb); ctx = cairo.Context(surf)
    synth_bg(ctx, Wb, Hb, Hb * 0.62)
    # zona segura de YouTube: 1546x423 centrada
    sx0, sy0, sx1, sy1 = (Wb - 1546) / 2, (Hb - 423) / 2, (Wb + 1546) / 2, (Hb + 423) / 2
    # decoración a los lados (fuera del texto)
    for k, (x, y) in enumerate(((250, 380), (420, 1060), (2330, 420), (2150, 1080), (120, 780), (2450, 760))):
        alien(ctx, x, y, 14, 0.2 * k, k)
    for k, (x, y, rot) in enumerate(((620, 300, 0.3), (1960, 280, -0.2), (700, 1150, 0), (1880, 1160, 1.57))):
        piece(ctx, k, x, y, 46, rot, 0.9)
    cartridge(ctx, 2250, 640, 0.42, 0.18, label="PLAY")
    tank(ctx, 560, 760, 12)
    brackets(ctx, sx0 - 20, sy0 - 10, sx1 + 20, sy1 + 10, 70, 10, CYAN)
    neon_word(ctx, "BEHIND THE HUD", Wb / 2, Hb / 2 + 40, 190, MAGENTA)
    ctx.select_font_face("Press Start 2P"); ctx.set_font_size(30)
    t = "THE HIDDEN REASONS BEHIND VIDEO GAMES"
    adv = ctx.text_extents(t)[4]
    ctx.move_to(Wb / 2 - adv / 2, Hb / 2 + 130); ctx.set_source_rgb(*CYAN); ctx.show_text(t)
    ctx.select_font_face("Press Start 2P"); ctx.set_font_size(24)
    t2 = "NEW SHORT EVERY DAY"
    adv2 = ctx.text_extents(t2)[4]
    ctx.move_to(Wb / 2 - adv2 / 2, Hb / 2 - 150); ctx.set_source_rgb(*YELLOW); ctx.show_text(t2)
    circle(ctx, Wb / 2 - adv2 / 2 - 34, Hb / 2 - 160, 10); fill(ctx, RED)
    surf.write_to_png(path)


if __name__ == "__main__":
    avatar(os.path.join(OUT, "foto_perfil.png"))
    banner(os.path.join(OUT, "banner.png"))
    print("ok")
