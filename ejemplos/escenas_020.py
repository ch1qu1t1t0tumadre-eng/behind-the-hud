"""Behind the HUD · 020 (EN) — Among Us Almost Died. Formato historia.
Sin dibujar a los tripulantes de Among Us ni logos: lápida, nave en emoji, personas genéricas, gráficas y contadores.
Datos: Innersloth (3 personas) lanzó Among Us en junio de 2018 con poca atención; en Steam tuvo picos de 17 jugadores
a la vez en sus primeros meses (dic. 2018); en 2020 explotó gracias a streamers de Twitch (1,5 M jugadores simultáneos
en septiembre); Innersloth anunció Among Us 2 en agosto de 2020 y lo canceló un mes después para centrarse en el
original (GameSpot, Engadget, Game Developer, Sportskeeda/SteamDB, Inverse)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 020"
SUBTITULO = subtitulo_hud
SUS = (0.95, 0.25, 0.25)
SPACE = (0.35, 0.75, 1.0)


def people(ctx, x, y, n, size, appear_lt, col=WHITE):
    for i in range(n):
        icon(ctx, "🧑‍💻", x + (i - (n - 1) / 2) * size * 1.2, y, size, pop(appear_lt, i * 0.12))


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 960)
    bg_night(ctx, T)
    rays(ctx, W / 2, 640, T, SUS, 0.05)
    tombstone(ctx, W / 2, 700, 0.85, ["AMONG US", "2018"], T)
    icon(ctx, "🚀", W / 2 + 280, 520, 140, 1.0)
    hud(ctx, T, TAG, SUS)
    pill(ctx, "IT ALMOST DIED", W / 2, 1400, 1.0, size=58, rgb=SUS)


def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e2(ctx, lt, dur, T):  # «...before anyone played it.»
    camera(ctx, keyframes(lt, [(0, 1.15), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_night(ctx, T)
    big_number(ctx, "0", W / 2, 640, 340, SUS, pop(lt, 0.0))
    text(ctx, "PLAYERS", W / 2, 830, 80, WHITE, font="Anton")
    hud(ctx, T, TAG, SUS)
    stamp(ctx, "NOBODY", W / 2, 1400, clamp((lt - 0.2) / 0.25), RED, size=90, rot=-0.06)


def e3(ctx, lt, dur, T):  # «In 2018, a tiny studio of three people called Innersloth released Among Us.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    ficha(ctx, "INNERSLOTH", "A STUDIO OF 3 PEOPLE", W / 2, 470, pop(lt, 0.0), emoji="🦥", accent=SPACE, w=780)
    people(ctx, W / 2, 760, 3, 150, lt - 0.6)
    hud(ctx, T, TAG, SPACE)
    pill(ctx, "AMONG US · 2018", W / 2, 1400, pop(lt, 3.0), size=56, rgb=SPACE)


def e4(ctx, lt, dur, T):  # «Almost nobody showed up.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_night(ctx, T)
    rrect(ctx, W / 2 - 330, 440, 660, 420, 26); fill(ctx, (0.08, 0.10, 0.18))
    text(ctx, "LOBBY", W / 2, 500, 64, WHITE, font="Anton")
    for i in range(10):
        cx, cy = W / 2 - 240 + (i % 5) * 120, 610 + (i // 5) * 140
        circle(ctx, cx, cy, 44); stroke(ctx, (0.35, 0.40, 0.55), 6, 0.9)
    icon(ctx, "🦗", W / 2 + 200, 820, 90, pop(lt, 0.5))
    hud(ctx, T, TAG, SUS)
    pill(ctx, "EMPTY LOBBIES", W / 2, 1400, pop(lt, 0.2), size=58, rgb=SUS)


def e5(ctx, lt, dur, T):  # «In its first months on Steam, Among Us peaked at just seventeen players at once.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.12))
    v = int(counter(lt - 1.0, 0, 17, 1.0)) if lt > 1.0 else 0
    big_number(ctx, str(v), W / 2, 600, 320, SPACE, 1.0)
    text(ctx, "PLAYERS AT ONCE", W / 2, 790, 66, WHITE, font="Anton")
    hud(ctx, T, TAG, SPACE)
    pill(ctx, "PEAK ON STEAM", W / 2, 1400, pop(lt, 0.4), size=58, rgb=SPACE)


def e6(ctx, lt, dur, T):  # «The team was ready to move on.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    icon(ctx, "📦", W / 2, 640, 300, pop(lt, 0.0))
    badge(ctx, "NEXT PROJECT →", W / 2, 880, pop(lt, 0.5), size=60, bg=(0.35, 0.35, 0.45))
    hud(ctx, T, TAG, YELLOW)


def e7(ctx, lt, dur, T):  # «Then in 2020, big streamers on Twitch started playing it, and the game exploded.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt > 3.6), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.16))
    calendar_page(ctx, 220, 520, 0.55, "THEN", "2020", "", (0.55, 0.3, 0.95), pop(lt, 0.0))
    rrect(ctx, 560, 420, 160, 60, 14); fill(ctx, RED)
    text(ctx, "● LIVE", 640, 450, 40, WHITE, font="Anton", shadow=False)
    line_chart(ctx, 180, 900, 720, 300, [0.02, 0.02, 0.03, 0.03, 0.05, 0.2, 0.55, 1.0], clamp((lt - 0.8) / 3.0), LIME)
    hud(ctx, T, TAG, LIME)
    stamp(ctx, "EXPLODED", W / 2, 1400, clamp((lt - 3.6) / 0.25), LIME, size=86, rot=-0.06)


def e8(ctx, lt, dur, T):  # «Millions of people around the world were suddenly hunting the impostor.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_night(ctx, T)
    icon(ctx, "🌍", W / 2, 620, 300, pop(lt, 0.0), rot=0.1 * T)
    for i in range(8):
        a = i * math.pi / 4 + T * 0.6
        icon(ctx, "🕵️", W / 2 + 270 * math.cos(a), 620 + 230 * math.sin(a), 80, pop(lt, 0.2 + i * 0.08))
    hud(ctx, T, TAG, SUS)
    pill(ctx, "WHO'S THE IMPOSTOR?", W / 2, 1400, pop(lt, 1.0), size=56, rgb=SUS)


def e9(ctx, lt, dur, T):  # «In other words, Among Us became a hit two years after it flopped.»
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.16, 0.02, 0.06), floor=False)
    rays(ctx, W / 2, 620, T, SUS, 0.12)
    calendar_page(ctx, 300, 640, 0.8, "FLOP", "2018", "", (0.4, 0.4, 0.45), 1.0)
    arrow(ctx, 470, 640, 610, 640, pop(lt, 0.8), WHITE, 12)
    calendar_page(ctx, 780, 640, 0.8, "HIT", "2020", "", LIME, pop(lt, 1.2))
    hud(ctx, T, TAG, SUS)
    stamp(ctx, "2 YEARS LATE", W / 2, 1400, clamp((lt - 1.8) / 0.25), YELLOW, size=80, rot=-0.06)


def e10(ctx, lt, dur, T):  # «Innersloth had even announced Among Us 2.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.14), floor=False)
    card(ctx, W / 2, 680, 1.1, "🚀", "AMONG US 2", SPACE, T, appear=pop(lt, 0.0))
    hud(ctx, T, TAG, SPACE)
    pill(ctx, "ANNOUNCED · AUG 2020", W / 2, 1400, pop(lt, 0.4), size=54, rgb=SPACE)


def e11(ctx, lt, dur, T):  # «They canceled it, and put everything into the original game instead.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.06, 0.14), floor=False)
    card(ctx, 300, 680, 0.85, "🚀", "AMONG US 2", (0.4, 0.4, 0.45), T, rot=-0.08)
    x_mark(ctx, 300, 680, 140, clamp((lt - 0.2) / 0.3))
    arrow(ctx, 470, 680, 610, 680, pop(lt, 0.9), WHITE, 12)
    card(ctx, 780, 680, 0.85, "🚀", "AMONG US", SUS, T, appear=pop(lt, 1.2), rot=0.08)
    hud(ctx, T, TAG, SUS)
    stamp(ctx, "CANCELED", W / 2, 1400, clamp((lt - 0.3) / 0.25), RED, size=86, rot=-0.06)


def e12(ctx, lt, dur, T):  # «And that's why» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.50, e2), (2.75, e3), (7.85, e4), (9.28, e5), (13.52, e6), (15.14, e7),
           (19.94, e8), (23.31, e9), (26.79, e10), (28.86, e11), (31.73, e12)]
HOOK = "AMONG US ALMOST DIED"
CTA = 26.4
COLA = 0.02
SFX = [(12.0, "ding"), (18.9, "pop"), (29.0, "pop")]


def MINIATURA(ctx):
    bg_night(ctx, 1.0)
    rays(ctx, W / 2, 1000, 1.0, SUS, 0.06)
    tombstone(ctx, W / 2, 1150, 1.5, ["AMONG US", "2018"], 0.0)
    thumb_circle(ctx, W / 2, 1100, 260, 200)
    thumb_arrow(ctx, 150, 1760, W / 2 - 160, 1260)
    thumb_vignette(ctx)
    thumb_text(ctx, [("AMONG US", WHITE), "ALMOST DIED?"], y=330)
