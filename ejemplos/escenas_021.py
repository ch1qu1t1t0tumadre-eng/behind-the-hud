"""Behind the HUD · 021 (EN) — 3 Minecraft Facts You Didn't Know. Formato lista.
Sin dibujar mobs ni bloques de Minecraft: gato y fantasma en emoji, cubos genéricos, ondas de sonido, letras.
Datos: la primera versión de prueba de Notch (2009) se llamó «Cave Game» (Sportskeeda, Minecraft Wiki);
los sonidos del Ghast son el gato de C418 (Daniel Rosenfeld) al despertarlo (AMA de C418 en Reddit, 14/12/2011;
Minecraft Wiki); las explosiones del Creeper son disparos con el tono bajado (C418 en Twenty Thousand Hertz, vía PC Gamer)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 021-L"
SUBTITULO = subtitulo_hud
GRASS = (0.35, 0.80, 0.30)
NETHER = (0.85, 0.20, 0.15)


def cubes(ctx, T, a=0.35):
    for i in range(9):
        x = 80 + (i * 137) % 940
        y = 1650 + 40 * math.sin(T + i)
        rrect(ctx, x, y, 90, 90, 6); fill(ctx, GRASS if i % 2 else (0.55, 0.38, 0.22), a)


def waves(ctx, x, y, T, n=3, rgb=WHITE, a=0.8):
    for k in range(n):
        r = 70 + k * 45 + 10 * math.sin(T * 6 - k)
        ctx.arc(x, y, r, -0.7, 0.7); stroke(ctx, rgb, 10, a * (1 - k * 0.25))


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.03, 0.03), floor=False)
    rays(ctx, W / 2, 640, T, NETHER, 0.06)
    icon(ctx, "😼", W / 2 - 200, 680, 260, 1.0)
    waves(ctx, W / 2 - 40, 680, T)
    icon(ctx, "👻", W / 2 + 230, 640 + 20 * math.sin(T * 2), 260, 1.0)
    hud(ctx, T, TAG, NETHER)
    pill(ctx, "A CAT = A MONSTER?", W / 2, 1400, 1.0, size=56, rgb=NETHER)


def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e_hook2(ctx, lt, dur, T):  # «...voiced by a cat.»
    camera(ctx, keyframes(lt, [(0, 1.15), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.03, 0.03), floor=False)
    icon(ctx, "😼", W / 2, 640, 380, 1.0)
    icon(ctx, "🎙️", W / 2 + 260, 760, 160, pop(lt, 0.2))
    hud(ctx, T, TAG, NETHER)
    stamp(ctx, "VOICED BY A CAT", W / 2, 1400, clamp((lt - 0.2) / 0.25), YELLOW, size=72, rot=-0.06)


def l_intro(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.10, 0.05))
    for i, (e, c) in enumerate([("⛏️", GRASS), ("🐱", NETHER), ("💥", YELLOW)]):
        card(ctx, 250 + i * 290, 680, 0.72, e, ["#1", "#2", "#3"][i], c, T, appear=pop(lt, 0.1 + i * 0.18), rot=(i - 1) * 0.08)
    badge(ctx, "MINECRAFT FACTS", W / 2, 400, pop(lt, 0.0), size=66, bg=(0.25, 0.6, 0.25))
    hud(ctx, T, TAG, GRASS)
    pill(ctx, "YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=56, rgb=GRASS)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 440, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 690, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


def e_name(ctx, lt, dur, T):  # «Minecraft wasn't always called Minecraft.» + «In 2009, Notch's very first test version was named Cave Game.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_blueprint(ctx, T)
    word_tiles(ctx, "MINECRAFT", 620, lt, 5.4, "CAVE GAME", GRASS, size=104, gap=10)
    calendar_page(ctx, W / 2, 870, 0.5, "FIRST TEST", "2009", "", GRASS, pop(lt, 2.3))
    hud(ctx, T, TAG, GRASS)
    pill(ctx, "ITS FIRST NAME: CAVE GAME" if lt > 5.6 else "NOT ITS FIRST NAME", W / 2, 1400, pop(lt, 0.2), size=50, rgb=GRASS)


def e_ghast(ctx, lt, dur, T):  # «The crying Ghasts in the Nether?»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_arcade(ctx, T, (0.22, 0.04, 0.03), floor=False)
    rays(ctx, W / 2, 640, T, NETHER, 0.08)
    icon(ctx, "👻", W / 2, 640 + 30 * math.sin(T * 2), 360, pop(lt, 0.0))
    icon(ctx, "💧", W / 2 - 60, 780, 70, clamp((lt - 0.5) / 0.3))
    waves(ctx, W / 2 + 200, 640, T, rgb=(1, 0.8, 0.8))
    hud(ctx, T, TAG, NETHER)
    pill(ctx, "THE CRYING GHASTS", W / 2, 1400, pop(lt, 0.2), size=58, rgb=NETHER)


def e_c418(ctx, lt, dur, T):  # «Composer C418 recorded his own cat, who made weird noises after being woken up from a nap.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    ficha(ctx, "C418", "MINECRAFT'S COMPOSER", W / 2 - 60, 480, pop(lt, 0.0), emoji="🎹", accent=(0.6, 0.5, 1.0), w=640)
    awake = lt > 2.6
    icon(ctx, "😾" if awake else "😴", W / 2 - 150, 800, 220, pop(lt, 0.8))
    if not awake:
        icon(ctx, "💤", W / 2 - 40, 690, 90, pop(lt, 1.0))
    icon(ctx, "🎙️", W / 2 + 190, 800, 170, pop(lt, 1.3))
    if awake:
        waves(ctx, W / 2 + 10, 800, T)
    hud(ctx, T, TAG, (0.6, 0.5, 1.0))
    pill(ctx, "HIS SLEEPY CAT", W / 2, 1400, pop(lt, 0.4), size=58, rgb=(0.6, 0.5, 1.0))


def e_owords(ctx, lt, dur, T):  # «In other words, the screams that scared you in the Nether came from a sleepy cat.»
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.20, 0.03, 0.05), floor=False)
    rays(ctx, W / 2, 620, T, NETHER, 0.12)
    icon(ctx, "👻", 300, 640, 260, 1.0)
    text(ctx, "=", W / 2, 640, 160, WHITE, font="Anton", a=pop(lt, 1.0))
    icon(ctx, "😾", 780, 640, 260, pop(lt, 1.4))
    hud(ctx, T, TAG, NETHER)
    stamp(ctx, "IT WAS A CAT", W / 2, 1400, clamp((lt - 2.0) / 0.25), YELLOW, size=84, rot=-0.06)


def e_creeper(ctx, lt, dur, T):  # «Creeper explosions aren't real explosions at all.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]) + 0.012 * math.sin(T * 50) * (lt < 0.6), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.12, 0.05), floor=False)
    icon(ctx, "💥", W / 2, 640, 380, pop(lt, 0.0))
    x_mark(ctx, W / 2, 640, 190, clamp((lt - 1.0) / 0.3))
    hud(ctx, T, TAG, GRASS)
    pill(ctx, "NOT A REAL EXPLOSION", W / 2, 1400, pop(lt, 0.8), size=54, rgb=GRASS)


def e_gunshot(ctx, lt, dur, T):  # «They're ordinary gunshot sounds from the internet, pitched way down.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    rrect(ctx, 140, 420, 800, 260, 24); fill(ctx, (0.05, 0.06, 0.12), 0.9)
    for i in range(40):
        h = (60 + 90 * abs(math.sin(i * 1.7 + T * 4))) * (1.0 - 0.5 * clamp((lt - 1.4) / 1.0))
        rrect(ctx, 170 + i * 19, 550 - h / 2, 12, h, 6); fill(ctx, YELLOW)
    text(ctx, "GUNSHOT.WAV", W / 2, 455, 40, WHITE, font="Anton", shadow=False)
    # control de tono que baja
    rrect(ctx, W / 2 - 300, 800, 600, 24, 12); fill(ctx, (0.3, 0.3, 0.4))
    kx = W / 2 + 250 - 500 * ease(clamp((lt - 1.2) / 1.2))
    circle(ctx, kx, 812, 34); fill(ctx, LIME)
    text(ctx, "PITCH ↓", W / 2, 900, 64, LIME, font="Anton")
    hud(ctx, T, TAG, YELLOW)


def e_end(ctx, lt, dur, T):  # «So next time something screams in Minecraft, remember that» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.85, e_hook2), (3.26, l_intro), (5.66, l_num(1, GRASS)), (6.17, e_name),
           (12.32, l_num(2, NETHER)), (12.87, e_ghast), (14.50, e_c418), (19.40, e_owords),
           (23.38, l_num(3, YELLOW)), (24.07, e_creeper), (26.45, e_gunshot), (29.40, e_end)]
HOOK = "A CAT VOICED THIS MONSTER"
LISTA = [(5.66, "1/3"), (12.32, "2/3"), (23.38, "3/3")]
CTA = 23.45
COLA = 0.02
SFX = [(5.68, "ding"), (11.7, "pop"), (12.34, "ding"), (17.1, "pop"), (23.40, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.16, 0.03, 0.03), floor=False)
    rays(ctx, W / 2, 1000, 1.0, NETHER, 0.06)
    icon(ctx, "😾", W / 2 - 210, 1120, 360, 1.0)
    icon(ctx, "👻", W / 2 + 240, 1060, 360, 1.0)
    thumb_circle(ctx, W / 2 - 210, 1120, 220, 220)
    thumb_arrow(ctx, 150, 1780, W / 2 - 330, 1330)
    thumb_vignette(ctx)
    thumb_text(ctx, [("A CAT MADE", WHITE), "THIS SOUND?"], y=330)
