"""Behind the HUD · 023-L (EN) — 3 Mario Facts You Didn't Know. Formato lista.
Sin sprites ni personajes de Nintendo: cara de píxeles genérica, nube/arbusto genéricos, emojis (buey, tortuga, gorra).
Datos: (1) el bigote de Mario porque con tan pocos píxeles no se podía dibujar la boca, y la gorra porque el pelo era
difícil de animar (Miyamoto; Iwata Asks New Super Mario Bros. Wii, Nintendo UK; GameSpot); (2) en Super Mario Bros. (1985)
las nubes y los arbustos son el mismo gráfico con otra paleta (Kotaku «Mario's great and terrible secret»,
TodayIFoundOut, Creative Bloq); (3) Miyamoto dibujó primero a Bowser como un buey, inspirado en el Rey Buey de la película
china Princess Iron Fan, y Takashi Tezuka dijo que parecía una tortuga (Iwata Asks vía GameZone «The Birth of Bowser»,
Wikipedia «Bowser», Super Mario Wiki)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 023-L"
SUBTITULO = subtitulo_hud
MRED = (0.95, 0.20, 0.18)
SKY = (0.36, 0.58, 1.0)
BUSH = (0.30, 0.78, 0.25)

FACE = ["..XXXXX...",
        ".XXXXXXXX.",
        ".SSSSESS..",
        "SSSSSESSS.",
        "SSSSSSSSSS",
        ".MMMMMMM..",
        "..SSSSSS..",
        "...SSSS..."]


def pixel_face(ctx, x, y, px, mouth=False, a=1.0):
    """Cara de píxeles genérica (diseño propio): gorra, ojo, bigote."""
    cols = {"X": (0.35, 0.40, 0.55), "S": (0.98, 0.78, 0.60), "E": (0.1, 0.1, 0.15), "M": (0.30, 0.18, 0.10)}
    w = len(FACE[0]) * px
    for r, row in enumerate(FACE):
        for c, ch in enumerate(row):
            if ch in cols:
                ctx.rectangle(x - w / 2 + c * px, y + r * px, px - 2, px - 2); fill(ctx, cols[ch], a)
    if mouth:
        ctx.rectangle(x - w / 2 + 3 * px, y + 6 * px, 3 * px - 2, px - 2); fill(ctx, (0.85, 0.2, 0.25), a)


def cloud(ctx, x, y, s, col, a=1.0):
    """Nube/arbusto genérico: 3 bultos redondos con base plana."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for (dx, dy, r) in ((-110, 10, 80), (0, -30, 110), (110, 10, 80)):
        circle(ctx, dx, dy, r); fill(ctx, col, a)
    ctx.rectangle(-190, 10, 380, 80); fill(ctx, col, a)
    for (dx, dy, r) in ((-110, 10, 80), (0, -30, 110), (110, 10, 80)):
        ctx.arc(dx, dy, r, math.pi * 1.1, math.pi * 1.9); stroke(ctx, (0, 0, 0), 8, 0.35 * a)
    ctx.restore()


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): buey gigante + ficha de Bowser."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.05, 0.02), floor=False)
    rays(ctx, W / 2, 560, T, ORANGE, 0.07)
    icon(ctx, "🐂", W / 2, 540, 400, 1.0)
    ficha(ctx, "BOWSER", "SUPER MARIO · 1985", W / 2, 840, 1.0, emoji="🐢", accent=ORANGE, w=720)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "MARIO · 3 FACTS", W / 2, 1400, 1.0, size=52, rgb=ORANGE)


def e_hook(ctx, lt, dur, T):  # «Bowser was supposed to be an»
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e_ox(ctx, lt, dur, T):  # «OX.»  (primer corte ~1,7 s)
    camera(ctx, keyframes(lt, [(0, 1.25), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.06, 0.02), floor=False)
    rays(ctx, W / 2, 620, T, ORANGE, 0.1)
    icon(ctx, "🐂", W / 2, 640, 580, 1.0, rot=0.04 * math.sin(T * 6))
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "AN OX?!", W / 2, 1400, clamp((lt - 0.1) / 0.25), ORANGE, size=90, rot=-0.06)


def l_intro(ctx, lt, dur, T):  # «Here are three Mario facts you didn't know.»
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.03, 0.08))
    for i, (e, c) in enumerate([("🥸", MRED), ("☁️", SKY), ("🐢", BUSH)]):
        card(ctx, 250 + i * 290, 680, 0.72, e, ["#1", "#2", "#3"][i], c, T, appear=pop(lt, 0.1 + i * 0.18), rot=(i - 1) * 0.08)
    badge(ctx, "MARIO FACTS", W / 2, 400, pop(lt, 0.0), size=66, bg=MRED)
    hud(ctx, T, TAG, MRED)
    pill(ctx, "YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=56, rgb=MRED)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 440, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 690, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


def e_mustache(ctx, lt, dur, T):  # «Mario has a mustache because the old pixels couldn't draw a MOUTH.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_blueprint(ctx, T)
    mouth = lt > 1.4 and lt < 2.4 and int(T * 6) % 2 == 0
    pixel_face(ctx, W / 2, 330, 70, mouth=mouth)
    if lt > 2.4:
        x_mark(ctx, W / 2 - 70, 330 + 6 * 70 + 30, 110, clamp((lt - 2.4) / 0.25))
    hud(ctx, T, TAG, MRED)
    stamp(ctx, "NO ROOM FOR A MOUTH", W / 2, 1400, clamp((lt - 2.2) / 0.25), MRED, size=62, rot=-0.06)


def e_cap(ctx, lt, dur, T):  # «And the cap? His hair was too hard to animate.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.04), floor=False)
    icon(ctx, "🧢", W / 2, 470, 300, 1.0, rot=0.06 * math.sin(T * 4))
    icon(ctx, "💇", W / 2 - 180, 800, 170, pop(lt, 0.9))
    icon(ctx, "🎞️", W / 2 + 180, 800, 170, pop(lt, 1.2))
    x_mark(ctx, W / 2 - 180, 800, 100, clamp((lt - 1.7) / 0.25))
    hud(ctx, T, TAG, MRED)
    pill(ctx, "HAIR = TOO HARD TO ANIMATE", W / 2, 1400, pop(lt, 0.6), size=48, rgb=MRED)


def e_same(ctx, lt, dur, T):  # «in Super Mario Bros, the clouds and the bushes are the SAME picture.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    ctx.rectangle(-200, -200, W + 400, H + 400); fill(ctx, SKY)
    ctx.rectangle(-200, 820, W + 400, 800); fill(ctx, (0.75, 0.42, 0.20))
    cloud(ctx, W / 2, 400, 0.95, WHITE, pop(lt, 0.0))
    cloud(ctx, W / 2, 730, 0.95, BUSH, pop(lt, 0.8))
    text(ctx, "=", W / 2 + 330, 570, 160, YELLOW, a=clamp((lt - 1.8) / 0.3), font="Anton")
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "SUPER MARIO BROS · 1985", W / 2, 1400, pop(lt, 0.1), size=52, rgb=BUSH)


def e_owords(ctx, lt, dur, T):  # «In other words, every bush is just a green cloud.» (2.º gancho)
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    ctx.rectangle(-200, -200, W + 400, H + 400); fill(ctx, (0.25, 0.42, 0.85))
    rays(ctx, W / 2, 600, T, WHITE, 0.10)
    p = ease(clamp((lt - 1.0) / 1.2))
    col = tuple(WHITE[i] * (1 - p) + BUSH[i] * p for i in range(3))
    cloud(ctx, W / 2, 480 + 260 * p, 1.35, col)
    ctx.rectangle(-200, 900, W + 400, 800); fill(ctx, (0.75, 0.42, 0.20))
    hud(ctx, T, TAG, BUSH)
    stamp(ctx, "BUSH = GREEN CLOUD", W / 2, 1400, clamp((lt - 1.6) / 0.25), YELLOW, size=68, rot=-0.06)


def e_memory(ctx, lt, dur, T):  # «Nintendo reused one drawing to save memory.» (sin pill: aquí va el aviso SUBSCRIBE)
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.06), floor=False)
    chip(ctx, W / 2, 470, 1.1, T, heat=0.2, label="40 KB")
    cloud(ctx, W / 2 - 230, 800, 0.5, WHITE, pop(lt, 0.4))
    text(ctx, "+", W / 2, 810, 90, YELLOW, a=clamp((lt - 0.7) / 0.3), font="Anton")
    cloud(ctx, W / 2 + 230, 800, 0.5, BUSH, pop(lt, 0.9))
    text(ctx, "1 DRAWING", W / 2, 930, 70, YELLOW, a=clamp((lt - 1.3) / 0.3), font="Anton")
    hud(ctx, T, TAG, LIME)


def e_miyamoto(ctx, lt, dur, T):  # «Miyamoto first drew Bowser as an ox,»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    rrect(ctx, W / 2 - 300, 300, 600, 480, 20); fill(ctx, WHITE, 0.95)
    icon(ctx, "🐂", W / 2, 540, 300, pop(lt, 0.3))
    icon(ctx, "✏️", W / 2 + 260 + 20 * math.sin(T * 8), 720, 110, 1.0)
    ficha(ctx, "MIYAMOTO", "MARIO'S CREATOR", W / 2, 1380, pop(lt, 0.0), emoji="✏️", accent=ORANGE, w=740)
    hud(ctx, T, TAG, ORANGE)


def e_movie(ctx, lt, dur, T):  # «from an old Chinese movie about an Ox King.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_dark(ctx, T)
    rrect(ctx, 140, 330, 800, 520, 24); fill(ctx, (0.08, 0.08, 0.10))
    for i in range(9):
        rrect(ctx, 160 + i * 88, 345, 50, 30, 6); fill(ctx, WHITE, 0.6)
        rrect(ctx, 160 + i * 88, 805, 50, 30, 6); fill(ctx, WHITE, 0.6)
    icon(ctx, "🐂", W / 2, 620, 260, pop(lt, 0.2))
    icon(ctx, "👑", W / 2, 450, 130, pop(lt, 1.2))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "THE OX KING", W / 2, 1400, pop(lt, 1.0), size=60, rgb=YELLOW, sub="OLD CHINESE MOVIE")


def e_tezuka(ctx, lt, dur, T):  # «But his partner Takashi Tezuka said it looked like a TURTLE.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.10, 0.05), floor=False)
    rrect(ctx, W / 2 - 340, 380, 680, 200, 40); fill(ctx, WHITE, pop(lt, 1.2))
    if lt > 1.3:
        text(ctx, "THAT'S A TURTLE!", W / 2, 480, 76, (0.1, 0.1, 0.14), font="Anton", shadow=False)
    icon(ctx, "🐂", W / 2 - 200, 760, 220, 1.0 - 0.5 * clamp((lt - 2.2) / 0.3))
    icon(ctx, "🐢", W / 2 + 200, 760, 220, pop(lt, 2.4))
    ficha(ctx, "TAKASHI TEZUKA", "MIYAMOTO'S PARTNER", W / 2, 1380, pop(lt, 0.0), emoji="💬", accent=BUSH, w=800)
    hud(ctx, T, TAG, BUSH)


def e_king(ctx, lt, dur, T):  # «So Miyamoto made him a turtle king.»
    camera(ctx, keyframes(lt, [(0, 1.25), (0.25, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.12, 0.04), floor=False)
    rays(ctx, W / 2, 620, T, YELLOW, 0.11)
    card(ctx, W / 2, 660, 1.15, "🐢", "BOWSER", BUSH, T, appear=1.0, crown=pop(lt, 0.4))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "TURTLE KING", W / 2, 1400, clamp((lt - 0.5) / 0.25), YELLOW, size=84, rot=-0.06)


def e_end(ctx, lt, dur, T):  # «Which means, for a while,» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.69, e_ox), (2.58, l_intro), (5.00, l_num(1, MRED)), (5.68, e_mustache), (9.30, e_cap),
           (11.87, l_num(2, BUSH)), (12.43, e_same), (16.09, e_owords), (19.39, e_memory), (22.08, l_num(3, ORANGE)),
           (22.61, e_miyamoto), (25.17, e_movie), (27.43, e_tezuka), (30.52, e_king), (32.55, e_end)]
HOOK = "BOWSER WAS AN OX"
LISTA = [(5.00, "1/3"), (11.87, "2/3"), (22.08, "3/3")]
CTA = 19.45  # justo después del «in other words», sobre el plano de la memoria (sin pill abajo)
COLA = 0.02
SFX = [(5.02, "ding"), (11.89, "ding"), (22.10, "ding"), (30.55, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.16, 0.05, 0.02), floor=False)
    rays(ctx, W / 2, 1050, 1.0, ORANGE, 0.07)
    icon(ctx, "🐂", W / 2, 1100, 620, 1.0, rot=-0.1)
    thumb_circle(ctx, W / 2, 1100, 340, 320)
    thumb_arrow(ctx, 120, 1780, W / 2 - 200, 1330)
    thumb_vignette(ctx)
    thumb_text(ctx, [("BOWSER'S", WHITE), "FIRST DESIGN?"], y=330)
