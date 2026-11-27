"""Behind the HUD · 022 (EN) — Sonic Was Almost A Rabbit. Formato historia.
Sin dibujar a Sonic ni a Eggman: solo emojis genéricos (erizo, conejo, perro, bigote), cartas y nombres en texto.
Datos: para buscar mascota contra Mario (1990), Naoto Ohshima dibujó varios candidatos: un conejo que agarraba cosas con
las orejas, un perro, un armadillo y un hombre gordo con bigote en pijama; se enseñaron a gente en Central Park (Nueva York)
y ganó el erizo; el hombre del bigote se convirtió en el Dr. Robotnik / Eggman (Vice «Sonic the Hedgehog was almost Sonic
the Rabbit», Den of Geek «Sonic Almost Looked Like Eggman Instead», Sonic Retro, Wikipedia)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 022"
SUBTITULO = subtitulo_hud
SBLUE = (0.15, 0.45, 1.0)
PARK = (0.25, 0.75, 0.35)


def hero(ctx, T, zoom):
    """Gancho (inicio y final del bucle): conejo gigante + ficha de Sonic."""
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.06, 0.20), floor=False)
    rays(ctx, W / 2, 560, T, SBLUE, 0.07)
    icon(ctx, "🐰", W / 2, 540, 400, 1.0)
    ficha(ctx, "SONIC", "SEGA · 1991", W / 2, 840, 1.0, emoji="🦔", accent=SBLUE, w=700)
    hud(ctx, T, TAG, SBLUE)
    pill(ctx, "SEGA · REAL STORY", W / 2, 1400, 1.0, size=52, rgb=SBLUE)


def e_hook(ctx, lt, dur, T):  # «Sonic was almost a»
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e_rabbit(ctx, lt, dur, T):  # «RABBIT.»  (primer corte ~1,4 s)
    camera(ctx, keyframes(lt, [(0, 1.25), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.04, 0.12), floor=False)
    rays(ctx, W / 2, 620, T, MAGENTA, 0.09)
    icon(ctx, "🐰", W / 2, 640, 580, 1.0, rot=0.05 * math.sin(T * 6))
    hud(ctx, T, TAG, MAGENTA)
    stamp(ctx, "A RABBIT?!", W / 2, 1400, clamp((lt - 0.15) / 0.25), MAGENTA, size=84, rot=-0.06)


def e_1990(ctx, lt, dur, T):  # «In 1990, Sega needed a hero to beat Mario.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    calendar_page(ctx, W / 2, 470, 0.8, "SEGA", "1990", "NEEDS A HERO", SBLUE, pop(lt, 0.0))
    card(ctx, 290, 790, 0.62, "❓", "SEGA HERO", SBLUE, T, appear=pop(lt, 1.0), rot=-0.06)
    text(ctx, "VS", W / 2, 800, 90, YELLOW, a=clamp((lt - 1.6) / 0.3), font="Anton")
    card(ctx, 790, 790, 0.62, "🍄", "MARIO", RED, T, appear=pop(lt, 2.0), rot=0.06)
    hud(ctx, T, TAG, SBLUE)


def e_ohshima(ctx, lt, dur, T):  # «Artist Naoto Ohshima drew rival mascots.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.06, 0.16), floor=False)
    for i in range(4):
        rrect(ctx, 150 + i * 205, 330 + 25 * (i % 2), 170, 220, 14); fill(ctx, WHITE, 0.92 * pop(lt, 0.6 + i * 0.15))
        text(ctx, "?", 235 + i * 205, 440 + 25 * (i % 2), 110, (0.2, 0.2, 0.3), a=pop(lt, 0.6 + i * 0.15), font="Anton", shadow=False)
    icon(ctx, "✏️", 880 + 30 * math.sin(T * 8), 650, 120, pop(lt, 0.3))
    ficha(ctx, "NAOTO OHSHIMA", "ARTIST · SEGA", W / 2, 1380, pop(lt, 0.0), emoji="✏️", accent=SBLUE, w=800)
    hud(ctx, T, TAG, SBLUE)


def e_ears(ctx, lt, dur, T):  # «A rabbit that grabbed things with its long EARS.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.04, 0.12), floor=False)
    icon(ctx, "🐰", 330, 700, 300, 1.0)
    p = ease(clamp((lt - 0.6) / 0.9))
    ctx.move_to(360, 560); ctx.line_to(360 + 420 * p, 560 - 120 * p); stroke(ctx, (1, 0.85, 0.9), 30)
    ctx.move_to(300, 560); ctx.line_to(300 + 420 * p, 500 - 120 * p); stroke(ctx, (1, 0.85, 0.9), 30)
    icon(ctx, "🍎", 800 - 30 * (1 - p), 430, 140, 1.0)
    hud(ctx, T, TAG, MAGENTA)
    pill(ctx, "GRABS WITH ITS EARS", W / 2, 1400, pop(lt, 0.2), size=56, rgb=MAGENTA)


def e_dog(ctx, lt, dur, T):  # «A dog. An armadillo.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.05, 0.14))
    card(ctx, 330, 650, 0.85, "🐶", "DOG", ORANGE, T, appear=pop(lt, 0.0), rot=-0.07)
    card(ctx, 750, 650, 0.85, "🛡️", "ARMADILLO", LIME, T, appear=pop(lt, 0.55), rot=0.07)
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "MORE CANDIDATES", W / 2, 1400, pop(lt, 0.1), size=56, rgb=ORANGE)


def e_man(ctx, lt, dur, T):  # «And a fat man with a giant mustache, in pajamas.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.06, 0.03), floor=False)
    rays(ctx, W / 2, 620, T, ORANGE, 0.07)
    icon(ctx, "🥸", W / 2, 600, 420, 1.0)
    icon(ctx, "👔", W / 2 - 300, 820, 140, pop(lt, 1.6))
    text(ctx, "PAJAMAS", W / 2 + 260, 830, 70, YELLOW, a=clamp((lt - 1.6) / 0.3), font="Anton")
    hud(ctx, T, TAG, ORANGE)
    stamp(ctx, "GIANT MUSTACHE", W / 2, 1400, clamp((lt - 0.7) / 0.25), ORANGE, size=70, rot=-0.06)


def e_park(ctx, lt, dur, T):  # «Sega took them to Central Park in New York»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.10, 0.06), floor=False)
    for i, x in enumerate((150, 330, 750, 930)):
        icon(ctx, "🌳", x, 760 + 30 * (i % 2), 200, pop(lt, 0.1 * i))
    icon(ctx, "🗽", W / 2, 560, 330, pop(lt, 0.0))
    hud(ctx, T, TAG, PARK)
    pill(ctx, "CENTRAL PARK · NYC", W / 2, 1400, pop(lt, 0.2), size=58, rgb=PARK)


def e_vote(ctx, lt, dur, T):  # «and asked total STRANGERS to vote.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.06))
    for i in range(12):
        icon(ctx, ["🙋", "🙋‍♀️", "🧑", "👩"][i % 4], 150 + (i % 6) * 156, 520 + (i // 6) * 210, 140, pop(lt, 0.05 * i))
    icon(ctx, "🗳️", W / 2, 920, 150, pop(lt, 0.9))
    hud(ctx, T, TAG, PARK)
    stamp(ctx, "STRANGERS VOTED", W / 2, 1400, clamp((lt - 0.4) / 0.25), YELLOW, size=72, rot=-0.06)


def e_won(ctx, lt, dur, T):  # «The spiky hedgehog won.»
    camera(ctx, keyframes(lt, [(0, 1.2), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.06, 0.20), floor=False)
    rays(ctx, W / 2, 620, T, YELLOW, 0.1)
    card(ctx, W / 2, 640, 1.15, "🦔", "HEDGEHOG", SBLUE, T, appear=1.0, crown=pop(lt, 0.5))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "WINNER", W / 2, 1400, clamp((lt - 0.4) / 0.25), YELLOW, size=84, rot=-0.06)


def e_owords(ctx, lt, dur, T):  # «In other words, Sonic was picked by random people in a park.» (2.º gancho)
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.03, 0.08, 0.20), floor=False)
    rays(ctx, W / 2, 600, T, SBLUE, 0.12)
    icon(ctx, "🦔", W / 2, 600, 400, 1.0)
    for i in range(6):
        a = T * 1.2 + i * math.pi / 3
        icon(ctx, "👍", W / 2 + 330 * math.cos(a), 600 + 250 * math.sin(a), 100, pop(lt, 0.8 + i * 0.1))
    hud(ctx, T, TAG, SBLUE)
    stamp(ctx, "PICKED BY STRANGERS", W / 2, 1400, clamp((lt - 1.2) / 0.25), YELLOW, size=64, rot=-0.06)


def e_trash(ctx, lt, dur, T):  # «But Sega didn't throw the losers away.»  (sin pill: aquí va el aviso SUBSCRIBE)
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "🗑️", W / 2, 720, 300, 1.0)
    for i, (e, c) in enumerate([("🐰", MAGENTA), ("🐶", ORANGE), ("🥸", RED)]):
        card(ctx, 260 + i * 280, 420, 0.5, e, "", c, T, appear=1.0, rot=(i - 1) * 0.1)
    x_mark(ctx, W / 2, 720, 190, clamp((lt - 0.6) / 0.25))
    hud(ctx, T, TAG, RED)


def e_villain(ctx, lt, dur, T):  # «That man with the mustache became the VILLAIN.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]) + 0.01 * math.sin(T * 45) * (lt > 1.6), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.03), floor=False)
    rays(ctx, W / 2, 620, T, RED, 0.1 * clamp((lt - 1.2) / 0.3))
    icon(ctx, "🥸", W / 2, 620, 440, 1.0)
    icon(ctx, "😈", W / 2 + 240, 430, 160, pop(lt, 1.4))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "THE VILLAIN", W / 2, 1400, clamp((lt - 1.5) / 0.25), RED, size=84, rot=-0.06)


def e_eggman(ctx, lt, dur, T):  # «Doctor Eggman.»
    camera(ctx, keyframes(lt, [(0, 1.3), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.03, 0.04), floor=False)
    rays(ctx, W / 2, 600, T, RED, 0.12)
    icon(ctx, "🥚", W / 2, 560, 380, 1.0)
    ficha(ctx, "DR. EGGMAN", "SONIC'S ARCH-ENEMY", W / 2, 860, pop(lt, 0.0), emoji="🥸", accent=RED, w=760)
    hud(ctx, T, TAG, RED)


def e_lost(ctx, lt, dur, T):  # «Sonic's worst enemy is the design that lost to him.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16), floor=False)
    card(ctx, 300, 620, 0.85, "🦔", "WON", SBLUE, T, appear=1.0, rot=-0.06, crown=1.0)
    text(ctx, "VS", W / 2, 640, 100, YELLOW, font="Anton")
    card(ctx, 780, 620, 0.85, "🥸", "LOST", RED, T, appear=pop(lt, 0.3), rot=0.06)
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "THE LOSER BECAME THE BOSS", W / 2, 1400, pop(lt, 1.0), size=50, rgb=RED)


def e_end(ctx, lt, dur, T):  # «Because before he got his spikes,» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.37, e_rabbit), (1.96, e_1990), (5.23, e_ohshima), (7.66, e_ears), (10.18, e_dog),
           (11.54, e_man), (14.59, e_park), (16.75, e_vote), (18.61, e_won), (20.18, e_owords), (23.77, e_trash),
           (25.48, e_villain), (27.64, e_eggman), (28.71, e_lost), (31.51, e_end)]
HOOK = "SONIC WAS ALMOST A RABBIT"
COLA = 0.02
SFX = [(1.4, "pop"), (18.65, "ding"), (27.3, "pop")]
CTA = 23.8  # justo después del «in other words», sobre el plano de la papelera (sin pill abajo)


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.03, 0.06, 0.20), floor=False)
    rays(ctx, W / 2, 1050, 1.0, SBLUE, 0.07)
    icon(ctx, "🐰", W / 2, 1100, 640, 1.0, rot=-0.12)
    thumb_circle(ctx, W / 2, 1100, 340, 330)
    thumb_arrow(ctx, 120, 1780, W / 2 - 200, 1330)
    thumb_vignette(ctx)
    thumb_text(ctx, [("SEGA'S", WHITE), "SECRET MASCOT?"], y=330)
