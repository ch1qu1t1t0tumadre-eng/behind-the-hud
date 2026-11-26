"""Behind the HUD · 016 (EN) — Minecraft's Creeper Was Supposed To Be A Pig. Formato historia.
Sin dibujar el Creeper ni ningún mob ni textura de Minecraft: solo cajas de plano genéricas, emojis genéricos (cerdo, bomba) y texto.
Datos: en agosto de 2009 Markus «Notch» Persson, programando el cerdo en la pre-alpha, cambió por error la longitud y la altura
del modelo: salió una cosa alta con cuatro patitas. La guardó por «creepy», le puso una textura verde basada en las hojas
y un amigo le dijo que molaría que explotara (Wikipedia «Creeper (Minecraft)»; Minecraft.net «Meet the Creeper», cita de Jens Bergensten;
GameZone, Notch: «I accidentally made them tall instead of long»)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 016"
SUBTITULO = subtitulo_hud
PINK = (1.0, 0.45, 0.62)
LEAF = (0.30, 0.70, 0.25)
LEAF_D = (0.18, 0.48, 0.16)


# ---------- piezas ----------
def body_box(ctx, x, y, s, rot=0.0, col=(0.85, 0.90, 1.0), a=1.0, labels=True, fill_col=None, feet_col=None):
    """Caja de plano genérica: cuerpo 'largo' de 360x150 con 4 patas. rot=pi/2 -> se pone de pie."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(rot)
    if fill_col:
        ctx.rectangle(-180, -75, 360, 150); fill(ctx, fill_col, a)
    ctx.rectangle(-180, -75, 360, 150); stroke(ctx, col, 8, a)
    ctx.restore()
    # patas siempre hacia abajo (en pantalla)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    c, si = math.cos(rot), math.sin(rot)
    hw = abs(180 * c) + abs(75 * si)
    hh = abs(180 * si) + abs(75 * c)
    lw = min(40, 2 * hw / 6)
    gap = (2 * hw - 4 * lw) / 5
    for k in range(4):
        lx = -hw + gap + k * (lw + gap)
        if fill_col:
            ctx.rectangle(lx, hh, lw, 46); fill(ctx, fill_col, a)
        ctx.rectangle(lx, hh, lw, 46); stroke(ctx, feet_col or col, 6, a)
    if labels:
        text(ctx, "LENGTH", 0, -hh - 40, 40, YELLOW, a=a, font="Anton")
        text(ctx, "HEIGHT", hw + 100, 0, 40, CYAN, a=a, font="Anton")
    ctx.restore()


def code_panel(ctx, x, y, w, h, lines, a=1.0, hl=None):
    rrect(ctx, x - w / 2, y - h / 2, w, h, 20); fill(ctx, (0.04, 0.05, 0.10), 0.95 * a)
    rrect(ctx, x - w / 2, y - h / 2, w, h, 20); stroke(ctx, LIME, 5, a)
    for i, (s, col) in enumerate(lines):
        yy = y - h / 2 + 70 + i * 70
        if hl is not None and i in hl:
            rrect(ctx, x - w / 2 + 20, yy - 32, w - 40, 64, 10); fill(ctx, RED, 0.25 * a)
        text(ctx, s, x - w / 2 + 50, yy, 44, col, a=a, font="DejaVu Sans Mono", align="left", shadow=False)


def tree(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-22, -120, 44, 120); fill(ctx, (0.40, 0.26, 0.14), a)
    for (dx, dy, r) in ((-60, -170, 70), (60, -170, 70), (0, -230, 80), (0, -150, 70)):
        rrect(ctx, dx - r, dy - r, 2 * r, 2 * r, 18); fill(ctx, LEAF if dy < -160 else LEAF_D, a)
    ctx.restore()


def bubble(ctx, x, y, w, h, txt, a=1.0, size=56):
    rrect(ctx, x - w / 2, y - h / 2, w, h, 40); fill(ctx, WHITE, a)
    ctx.move_to(x - 120, y + h / 2 - 2); ctx.line_to(x - 170, y + h / 2 + 70); ctx.line_to(x - 40, y + h / 2 - 2); ctx.close_path()
    fill(ctx, WHITE, a)
    for i, ln in enumerate(txt):
        text(ctx, ln, x, y - (len(txt) - 1) * size * 0.55 + i * size * 1.1, size, (0.1, 0.1, 0.14), a=a, font="Anton", shadow=False)


# ---------- escenas ----------
def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): el cerdo + ficha del Creeper."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.05), floor=False)
    rays(ctx, W / 2, 560, T, LIME, 0.06)
    icon(ctx, "🐷", W / 2, 530, 380, 1.0)
    ficha(ctx, "THE CREEPER", "MINECRAFT · 2009", W / 2, 800, 1.0, emoji="💥", accent=LIME, w=760)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "MINECRAFT · REAL STORY", W / 2, 1400, 1.0, size=52, rgb=LIME)


# 0.00 "Minecraft's Creeper"
def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


# 1.43 "was supposed to be a PIG."  (primer corte ~1,4 s)
def e_hook2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (0.25, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.04, 0.10), floor=False)
    rays(ctx, W / 2, 600, T, PINK, 0.09)
    icon(ctx, "🐷", W / 2, 620, 560, 1.0, rot=0.05 * math.sin(T * 6))
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "IT WAS A PIG", W / 2, 1400, clamp((lt - 0.6) / 0.25), PINK, size=80, rot=-0.06)


# 3.05 "In two thousand nine, Notch was building Minecraft alone,"
def e_notch(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_blueprint(ctx, T)
    old_pc(ctx, 760, 560, 0.9, T)
    rrect(ctx, 130, 400, 300, 320, 24); fill(ctx, WHITE)
    rrect(ctx, 130, 400, 300, 90, 24); fill(ctx, RED); ctx.rectangle(130, 460, 300, 30); fill(ctx, RED)
    text(ctx, "AUG", 280, 445, 46, WHITE, font="Anton", shadow=False)
    text(ctx, "2009", 280, 590, 110, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    ficha(ctx, "NOTCH", "MARKUS PERSSON · SOLO DEV", W / 2, 1380, pop(lt, 0.9), emoji="💻", accent=CYAN, w=800)
    hud(ctx, T, TAG, CYAN)


# 6.25 "and he wanted a farm animal. So he coded a pig."
def e_farm(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.08, 0.14), floor=False)
    code_panel(ctx, W / 2, 470, 820, 260, [("new Animal(\"pig\")", LIME), ("length = 16", WHITE), ("height = 8", WHITE)], pop(lt, 0.0))
    icon(ctx, "🐷", W / 2 + 230, 790, 230, pop(lt, 1.4))
    icon(ctx, "🐄", W / 2 - 230, 800, 170, pop(lt, 0.3) * (1 - clamp((lt - 1.3) / 0.3)))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "A FARM ANIMAL", W / 2, 1400, pop(lt, 0.2), size=60, rgb=LIME)


# 8.88 "But he mixed up two NUMBERS."
def e_numbers(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (0.25, 1.0), (dur, 1.06)]) + 0.01 * math.sin(T * 45) * (lt > 0.7), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.05), floor=False)
    sw = lt > 0.9
    code_panel(ctx, W / 2, 560, 820, 260, [("new Animal(\"pig\")", LIME), ("length = " + ("8" if sw else "16"), RED if sw else WHITE),
                                          ("height = " + ("16" if sw else "8"), RED if sw else WHITE)], 1.0, hl=(1, 2) if sw else None)
    hud(ctx, T, TAG, RED)
    stamp(ctx, "OOPS", W / 2 + 300, 380, clamp((lt - 1.0) / 0.2), RED, size=90, rot=0.12)


# 10.68 "He swapped the length and the height."
def e_swap(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_blueprint(ctx, T)
    p = ease(clamp((lt - 0.4) / 1.1))
    body_box(ctx, W / 2 - 60, 620 - 60 * p, 1.0, rot=p * math.pi / 2)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "LENGTH ↔ HEIGHT", W / 2, 1400, pop(lt, 0.1), size=60, rgb=CYAN)


# 12.69 "Instead of a long pig,"
def e_long(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_blueprint(ctx, T)
    body_box(ctx, W / 2, 620, 1.0, labels=False, fill_col=(1.0, 0.70, 0.78))
    icon(ctx, "🐷", W / 2, 620, 130, 1.0)
    x_mark(ctx, W / 2, 620, 200, clamp((lt - 0.8) / 0.3))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "A LONG PIG", W / 2, 1400, pop(lt, 0.0), size=60, rgb=PINK)


# 14.41 "he got a tall, skinny thing on four tiny feet."
def e_tall(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    body_box(ctx, W / 2 - 40, 560, 1.0, rot=math.pi / 2, labels=True, feet_col=YELLOW if lt > 1.2 and int(T * 6) % 2 else None)
    hud(ctx, T, TAG, CYAN)
    pill(ctx, "4 TINY FEET", W / 2, 1400, pop(lt, 1.2), size=60, rgb=YELLOW)


# 16.98 "In other words, the Creeper is a pig that stood UP."  (2.º gancho: plano más fuerte)
def e_owords(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.03, 0.10), floor=False)
    rays(ctx, W / 2, 600, T, PINK, 0.11)
    r = -math.pi / 2 * ease(clamp((lt - 1.6) / 0.5))
    icon(ctx, "🐷", W / 2, 620, 480, 1.0, rot=r)
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "A PIG THAT STOOD UP", W / 2, 1400, clamp((lt - 0.6) / 0.25), YELLOW, size=64, rot=-0.06)


# 20.40 "Notch didn't delete it. He thought it looked creepy."
def e_keep(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_dark(ctx, T)
    rrect(ctx, W / 2 - 330, 380, 660, 300, 30); fill(ctx, (0.10, 0.11, 0.18))
    text(ctx, "DELETE MODEL?", W / 2, 450, 56, WHITE, font="Anton")
    rrect(ctx, W / 2 - 280, 540, 240, 90, 20); fill(ctx, RED, 0.35)
    text(ctx, "DELETE", W / 2 - 160, 585, 46, WHITE, a=0.5, font="Anton")
    rrect(ctx, W / 2 + 40, 540, 240, 90, 20); fill(ctx, LIME)
    text(ctx, "KEEP", W / 2 + 160, 585, 50, (0.05, 0.1, 0.05), font="Anton", shadow=False)
    x_mark(ctx, W / 2 - 160, 585, 70, clamp((lt - 0.5) / 0.25))
    icon(ctx, "👀", W / 2, 820, 170, pop(lt, 1.3))
    hud(ctx, T, TAG, LIME)


# 22.68 "He painted it with the green of Minecraft's LEAVES,"
def e_green(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.05), floor=False)
    tree(ctx, 280, 840, 1.25)
    p = ease(clamp((lt - 0.6) / 1.0))
    rrect(ctx, 620, 380, 300, 400, 26); fill(ctx, (0.15, 0.15, 0.18))
    ctx.save(); rrect(ctx, 620, 380, 300, 400, 26); ctx.clip()
    ctx.rectangle(620, 780 - 400 * p, 300, 400 * p); fill(ctx, LEAF); ctx.restore()
    text(ctx, "LEAF GREEN", 770, 830, 48, LIME, font="Anton")
    icon(ctx, "🖌️", 900, 380 + 360 * (1 - p), 130, 1.0)
    hud(ctx, T, TAG, LIME)
    pill(ctx, "SAME GREEN AS LEAVES", W / 2, 1400, pop(lt, 0.4), size=56, rgb=LIME)


# 25.40 "so it could hide in the trees."
def e_trees(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.02, 0.07, 0.04), floor=False)
    for i, (x, s) in enumerate(((180, 1.0), (430, 1.25), (690, 1.05), (920, 1.2))):
        tree(ctx, x, 900, s)
    icon(ctx, "👀", 560, 640 + 6 * math.sin(T * 3), 110, pop(lt, 0.6))
    hud(ctx, T, TAG, LIME)
    stamp(ctx, "CAMOUFLAGE", W / 2, 1400, clamp((lt - 0.4) / 0.25), LIME, size=76, rot=-0.06)


# 27.04 "Then a friend said it would be cool if it exploded."
def e_friend(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.05, 0.14), floor=False)
    bubble(ctx, W / 2 + 40, 520, 760, 280, ["WHAT IF", "IT EXPLODED?"], pop(lt, 0.3), size=78)
    icon(ctx, "🧑‍💻", 250, 830, 200, pop(lt, 0.0))
    icon(ctx, "💡", 820, 820, 160, pop(lt, 1.2))
    hud(ctx, T, TAG, ORANGE)


# 29.86 "So the Creeper got a fuse."
def e_fuse(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + 0.014 * math.sin(T * 50) * (lt > 1.1), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.06, 0.02), floor=False)
    rays(ctx, W / 2, 620, T, ORANGE, 0.08)
    if lt < 1.1:
        icon(ctx, "💣", W / 2, 640, 380, 1.0)
        for k in range(6):
            ang = T * 9 + k
            circle(ctx, W / 2 + 120 + 30 * math.cos(ang), 470 + 30 * math.sin(ang), 8); fill(ctx, YELLOW, 0.8)
    else:
        icon(ctx, "💥", W / 2, 640, 560 * (0.8 + 0.2 * ease_back(clamp((lt - 1.1) / 0.3))), 1.0)
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "+ FUSE", W / 2, 1400, clamp((lt - 0.4) / 0.25), ORANGE, size=80, rot=-0.06)


# 31.43 "And every time you hear that hiss,"
def e_hiss(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_dark(ctx, T)
    for k in range(5):
        r = 120 + ((lt * 260 + k * 80) % 400)
        ctx.arc(W / 2, 620, r, 0, 2 * math.pi); stroke(ctx, LIME, 8, clamp(1 - (r - 120) / 400) * 0.8)
    text(ctx, "SSSSS...", W / 2, 620, 120, LIME, font="Anton")
    hud(ctx, T, TAG, LIME)


# 33.20 "remember," -> vuelve al gancho (bucle)
def e_end(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.43, e_hook2), (3.05, e_notch), (6.25, e_farm), (8.88, e_numbers), (10.68, e_swap),
           (12.69, e_long), (14.41, e_tall), (16.98, e_owords), (20.40, e_keep), (22.68, e_green), (25.40, e_trees),
           (27.04, e_friend), (29.86, e_fuse), (31.43, e_hiss), (33.20, e_end)]
HOOK = "THE CREEPER WAS A PIG"
COLA = 0.02
SFX = [(9.8, "pop"), (17.0, "ding"), (20.95, "pop"), (31.0, "pop")]
CTA = 20.5  # aviso SUBSCRIBE · LIKE · SHARE justo después del «in other words», sobre el plano de «DELETE / KEEP» (sin pill abajo)


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.04, 0.10, 0.05), floor=False)
    rays(ctx, W / 2, 1050, 1.0, LIME, 0.07)
    icon(ctx, "🐷", W / 2, 1100, 640, 1.0, rot=-0.15)
    thumb_circle(ctx, W / 2, 1100, 340, 300)
    thumb_arrow(ctx, 120, 1780, W / 2 - 200, 1330)
    thumb_vignette(ctx)
    thumb_text(ctx, [("MINECRAFT'S", WHITE), "BIGGEST MISTAKE?"], y=330)
