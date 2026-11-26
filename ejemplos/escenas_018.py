"""Behind the HUD · 018 (EN) — Mario Wasn't Called Mario At First. Formato historia.
Sin dibujar a Mario ni a Donkey Kong: fichas, recreativa genérica, manual, almacén, etiquetas de nombre.
Datos: en Donkey Kong (1981) el héroe se llamaba «Jumpman» en el manual inglés; Nintendo of America le puso
«Mario» por Mario Segale, casero de su almacén cerca de Seattle, que discutió con Minoru Arakawa por el alquiler
atrasado; Nintendo lo confirmó en 2015; Segale bromeó en 1993 (Seattle Times) con que seguía esperando sus royalties
(Wikipedia «Mario Segale», History.com, Mental Floss, GameSpot)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 018"
SUBTITULO = subtitulo_hud
MRED = (0.95, 0.22, 0.22)


def name_tag(ctx, x, y, s, name, struck=0.0, appear=1.0, col=MRED):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * appear, s * appear)
    rrect(ctx, -330, -150, 660, 300, 30); fill(ctx, col)
    text(ctx, "HELLO", 0, -95, 64, WHITE, font="Anton", shadow=False)
    text(ctx, "MY NAME IS", 0, -40, 40, WHITE, font="Anton", shadow=False)
    rrect(ctx, -300, 0, 600, 130, 14); fill(ctx, WHITE)
    text(ctx, name, 0, 65, 100 if len(name) < 8 else 84, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    if struck > 0:
        ctx.move_to(-260, 65); ctx.line_to(-260 + 520 * clamp(struck), 65); stroke(ctx, RED, 18)
    ctx.restore()


def manual(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(-0.05)
    rrect(ctx, -250, -330, 500, 660, 16); fill(ctx, (0.96, 0.93, 0.82))
    rrect(ctx, -250, -330, 500, 110, 16); fill(ctx, (0.15, 0.15, 0.20))
    text(ctx, "INSTRUCTIONS", 0, -275, 54, WHITE, font="Anton", shadow=False)
    for k in range(7):
        rrect(ctx, -200, -170 + k * 50, 400 - (k % 3) * 70, 16, 8); fill(ctx, (0.6, 0.6, 0.62))
    rrect(ctx, -210, 200, 420, 100, 12); fill(ctx, YELLOW)
    text(ctx, "JUMPMAN", 0, 250, 80, (0.12, 0.12, 0.16), font="Anton", shadow=False)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.04), floor=False)
    rays(ctx, W / 2, 640, T, MRED, 0.06)
    name_tag(ctx, W / 2, 640, 1.2, "MARIO", struck=1.0)
    icon(ctx, "❓", W / 2 + 330, 440, 130, 1.0)
    hud(ctx, T, TAG, MRED)
    pill(ctx, "HIS FIRST NAME WAS DIFFERENT", W / 2, 1400, 1.0, size=48, rgb=MRED)


def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e2(ctx, lt, dur, T):  # «...at first.» primer corte
    camera(ctx, keyframes(lt, [(0, 1.15), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.04), floor=False)
    name_tag(ctx, W / 2, 640, 1.2, "???")
    hud(ctx, T, TAG, MRED)
    stamp(ctx, "NOT MARIO", W / 2, 1400, clamp((lt - 0.1) / 0.25), RED, size=80, rot=-0.06)


def e3(ctx, lt, dur, T):  # «In 1981, Nintendo put Donkey Kong in arcades.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.12))
    cabinet(ctx, W / 2 + 150, 600, 0.62, T, marquee="DONKEY KONG", col=(0.75, 0.15, 0.15))
    calendar_page(ctx, 250, 560, 0.75, "ARCADES", "1981", "", MRED, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "DONKEY KONG · 1981", W / 2, 1400, pop(lt, 0.2), size=56, rgb=YELLOW)


def e4(ctx, lt, dur, T):  # «The hero was a tiny carpenter with a mustache,»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    ficha(ctx, "THE HERO", "A TINY CARPENTER", W / 2, 470, pop(lt, 0.0), emoji="🔨", accent=MRED, w=760)
    icon(ctx, "🔨", W / 2 - 170, 760, 170, pop(lt, 0.3), rot=0.4 * math.sin(T * 8))
    icon(ctx, "🥸", W / 2 + 170, 760, 170, pop(lt, 0.6))
    hud(ctx, T, TAG, MRED)
    pill(ctx, "CARPENTER + MUSTACHE", W / 2, 1400, pop(lt, 0.3), size=52, rgb=MRED)


def e5(ctx, lt, dur, T):  # «and the English manual just called him Jumpman.»
    camera(ctx, keyframes(lt, [(0, 1.0), (1.2, 1.0), (dur, 1.18)]), W / 2, 960 - 40 * clamp((lt - 1.2) / 1.0))
    bg_arcade(ctx, T, (0.08, 0.06, 0.03), floor=False)
    manual(ctx, W / 2, 640, 0.92, T)
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "JUMPMAN", W / 2, 1400, clamp((lt - 1.3) / 0.25), YELLOW, size=86, rot=-0.06)


def e6(ctx, lt, dur, T):  # «But Nintendo of America had a problem.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.06, 0.12), floor=False)
    warehouse(ctx, W / 2, 760, 1.0, 0.0, T)
    icon(ctx, "⚠️", W / 2, 430, 160, pop(lt, 0.4))
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "NINTENDO OF AMERICA", W / 2, 1400, pop(lt, 0.1), size=56, rgb=ORANGE)


def e7(ctx, lt, dur, T):  # «They were late on the rent for their warehouse near Seattle, Washington.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    calendar_page(ctx, W / 2 - 180, 620, 0.95, "RENT", "DUE", "SEATTLE, WA", RED, pop(lt, 0.0))
    icon(ctx, "💸", W / 2 + 230, 560, 160, pop(lt, 0.3))
    stamp(ctx, "LATE", W / 2 - 180, 640, clamp((lt - 0.7) / 0.25), RED, size=110, rot=-0.2)
    hud(ctx, T, TAG, RED)
    pill(ctx, "THE RENT WAS LATE", W / 2, 1400, pop(lt, 0.2), size=56, rgb=RED)


def e8(ctx, lt, dur, T):  # «Their landlord, a man named Mario Segale, showed up and argued with the boss.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]) + 0.006 * math.sin(T * 40) * (lt > 2.6), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.05, 0.03), floor=False)
    ficha(ctx, "MARIO SEGALE", "THE LANDLORD", W / 2, 480, pop(lt, 0.0), emoji="🏢", accent=ORANGE, w=820)
    for i, e in enumerate(["💢", "😠", "💢"]):
        icon(ctx, e, W / 2 - 220 + i * 220, 780 + 20 * math.sin(T * 9 + i), 140, pop(lt, 2.4 + i * 0.12))
    hud(ctx, T, TAG, ORANGE)
    pill(ctx, "AN ANGRY LANDLORD", W / 2, 1400, pop(lt, 2.3), size=56, rgb=ORANGE)


def e9(ctx, lt, dur, T):  # «Soon after, the team gave Jumpman a brand new name.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.03, 0.04), floor=False)
    flip = clamp((lt - 1.4) / 0.3)
    name_tag(ctx, W / 2, 640, 1.2, "JUMPMAN" if flip < 0.5 else "MARIO", struck=clamp((lt - 0.6) / 0.6) if flip < 0.5 else 0.0)
    if flip >= 0.5:
        rays(ctx, W / 2, 640, T, YELLOW, 0.10)
        name_tag(ctx, W / 2, 640, 1.2, "MARIO")
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "A BRAND NEW NAME", W / 2, 1400, pop(lt, 0.2), size=56, rgb=YELLOW)


def e10(ctx, lt, dur, T):  # «In other words, gaming's most famous hero is named after an angry landlord.»
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.04), floor=False)
    rays(ctx, W / 2, 620, T, MRED, 0.12)
    name_tag(ctx, W / 2, 560, 1.0, "MARIO")
    arrow(ctx, W / 2, 740, W / 2, 820, pop(lt, 1.2), WHITE, 10)
    icon(ctx, "🏢", W / 2 - 90, 900, 120, pop(lt, 1.6))
    icon(ctx, "😠", W / 2 + 90, 900, 120, pop(lt, 1.8))
    hud(ctx, T, TAG, MRED)
    stamp(ctx, "NAMED AFTER HIM", W / 2, 1400, clamp((lt - 2.4) / 0.25), YELLOW, size=70, rot=-0.06)


def e11(ctx, lt, dur, T):  # «Years later, Segale joked that he was still waiting for his royalty checks.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "📭", W / 2 - 150, 620, 260, pop(lt, 0.0))
    icon(ctx, "⏳", W / 2 + 200, 600, 180, pop(lt, 0.4), rot=0.2 * math.sin(T * 3))
    calendar_page(ctx, W / 2 + 200, 820, 0.45, "SEATTLE TIMES", "1993", "", (0.3, 0.3, 0.35), pop(lt, 0.8))
    hud(ctx, T, TAG, YELLOW)
    pill(ctx, "\"STILL WAITING FOR MY CHECKS\"", W / 2, 1400, pop(lt, 1.0), size=44, rgb=YELLOW)


def e12(ctx, lt, dur, T):  # «And that's the real reason» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.94, e2), (2.27, e3), (5.65, e4), (8.23, e5), (10.51, e6), (12.44, e7),
           (15.53, e8), (19.82, e9), (22.68, e10), (27.19, e11), (30.97, e12)]
HOOK = "MARIO WASN'T HIS NAME"
CTA = 26.7
COLA = 0.02
SFX = [(2.3, "pop"), (13.5, "pop"), (17.9, "pop"), (21.3, "ding")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.14, 0.03, 0.04), floor=False)
    rays(ctx, W / 2, 1000, 1.0, MRED, 0.06)
    name_tag(ctx, W / 2, 1060, 1.35, "MARIO", struck=1.0)
    thumb_circle(ctx, W / 2, 1150, 360, 120)
    thumb_arrow(ctx, 160, 1760, W / 2 - 200, 1260)
    thumb_vignette(ctx)
    thumb_text(ctx, [("THAT WASN'T", WHITE), "HIS NAME?"], y=330)
