"""Behind the HUD · 019 (EN) — 3 Fortnite Facts You Didn't Know. Formato lista.
Sin logos ni personajes de Fortnite: isla genérica con tormenta, fuertes de bloques, zombis en emoji, escenario.
Datos: Fortnite empezó como Save the World (cooperativo contra zombis, en desarrollo desde 2011); Battle Royale se
hizo en unos dos meses tras el lanzamiento de Save the World (julio 2017) y salió el 26/09/2017 (Ed Zobrist, GDC 2018,
vía PC Gamer y PCGamesN); el concierto Astronomical de Travis Scott (abril 2020) tuvo 12,3 M de jugadores a la vez,
récord del juego (Epic Games vía PC Gamer, GameSpot, ESPN)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 019-L"
SUBTITULO = subtitulo_hud
STORM = (0.62, 0.30, 1.0)
SKY = (0.25, 0.65, 1.0)


def island(ctx, x, y, s, T, storm=0.6):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 40, 380, 150); fill(ctx, (0.15, 0.45, 0.85))
    ellipse(ctx, 0, 20, 330, 120); fill(ctx, (0.95, 0.85, 0.55))
    ellipse(ctx, 0, 0, 290, 100); fill(ctx, (0.30, 0.75, 0.35))
    for (bx, by) in [(-120, -10), (60, -30), (150, 20), (-30, 30)]:
        rrect(ctx, bx - 26, by - 40, 52, 46, 6); fill(ctx, (0.85, 0.55, 0.30))
        ctx.move_to(bx - 32, by - 40); ctx.line_to(bx, by - 70); ctx.line_to(bx + 32, by - 40); ctx.close_path(); fill(ctx, (0.7, 0.2, 0.2))
    r = 360 - 160 * storm
    ctx.arc(0, 10, r + 20 * math.sin(T * 2), 0, 2 * math.pi); stroke(ctx, STORM, 16, 0.85)
    ctx.restore()


def fort(ctx, x, y, s, prog=1.0, T=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    n = int(12 * clamp(prog))
    k = 0
    for row in range(3):
        for col in range(4):
            if k >= n:
                break
            rrect(ctx, -200 + col * 100, -row * 90, 94, 84, 8); fill(ctx, (0.72, 0.48, 0.25))
            ctx.move_to(-200 + col * 100 + 10, -row * 90 + 42); ctx.line_to(-200 + col * 100 + 84, -row * 90 + 42)
            stroke(ctx, (0.5, 0.32, 0.15), 5)
            k += 1
    ctx.restore()


def stage(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i in range(5):
        a = -0.9 + i * 0.45 + 0.15 * math.sin(T * 2 + i)
        ctx.move_to(0, -320); ctx.line_to(600 * math.sin(a), 300); ctx.line_to(600 * math.sin(a + 0.12), 300); ctx.close_path()
        fill(ctx, [STORM, SKY, YELLOW, PINK if 'PINK' in globals() else (1, 0.4, 0.7), LIME][i], 0.18)
    rrect(ctx, -360, 200, 720, 100, 14); fill(ctx, (0.15, 0.15, 0.22))
    icon(ctx, "🎤", 0, 60, 200, 1.0)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.08, 0.18), floor=False)
    island(ctx, W / 2, 720, 1.0, T, 0.5)
    calendar_page(ctx, W / 2 + 310, 540, 0.55, "BUILT IN", "2", "MONTHS", STORM)
    hud(ctx, T, TAG, STORM)
    pill(ctx, "FORTNITE BATTLE ROYALE", W / 2, 1400, 1.0, size=52, rgb=STORM)


def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e_hook2(ctx, lt, dur, T):  # «...in just two months.»
    camera(ctx, keyframes(lt, [(0, 1.15), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.08, 0.18), floor=False)
    rays(ctx, W / 2, 620, T, STORM, 0.08)
    calendar_page(ctx, W / 2, 640, 1.2, "BUILT IN", "2", "MONTHS", STORM)
    hud(ctx, T, TAG, STORM)
    stamp(ctx, "ONLY 2 MONTHS", W / 2, 1400, clamp((lt - 0.1) / 0.25), YELLOW, size=76, rot=-0.06)


def l_intro(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.04, 0.16))
    for i, (e, c) in enumerate([("🧟", GREEN), ("⏱️", STORM), ("🎤", YELLOW)]):
        card(ctx, 250 + i * 290, 680, 0.72, e, ["#1", "#2", "#3"][i], c, T, appear=pop(lt, 0.1 + i * 0.18), rot=(i - 1) * 0.08)
    badge(ctx, "FORTNITE FACTS", W / 2, 400, pop(lt, 0.0), size=66, bg=STORM)
    hud(ctx, T, TAG, STORM)
    pill(ctx, "YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=56, rgb=STORM)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 440, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 690, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


def e_zombie(ctx, lt, dur, T):  # «Fortnite started as a zombie game.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.12, 0.05), floor=False)
    for i in range(5):
        icon(ctx, "🧟", 180 + i * 180 + 20 * math.sin(T * 3 + i), 700 + 30 * math.sin(T * 5 + i * 2), 170, pop(lt, i * 0.1))
    badge(ctx, "ZOMBIE GAME", W / 2, 470, pop(lt, 0.3), size=70, bg=GREEN)
    hud(ctx, T, TAG, GREEN)
    pill(ctx, "IT STARTED WITH ZOMBIES", W / 2, 1400, pop(lt, 0.2), size=52, rgb=GREEN)


def e_forts(ctx, lt, dur, T):  # «In Save the World, you teamed up with friends and built forts to survive waves of monsters.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.06, 0.10, 0.06), floor=False)
    ficha(ctx, "SAVE THE WORLD", "CO-OP VS ZOMBIES", W / 2 - 70, 480, pop(lt, 0.0), emoji="🛡️", accent=GREEN, w=640)
    fort(ctx, W / 2 + 20, 820, 1.05, prog=(lt - 0.8) / 2.0, T=T)
    for i in range(3):
        icon(ctx, "🙂", 240 + i * 300, 640, 90, pop(lt, 0.4 + i * 0.15))
    icon(ctx, "🧟", 940, 860 + 15 * math.sin(T * 6), 120, pop(lt, 2.4))
    hud(ctx, T, TAG, GREEN)
    pill(ctx, "BUILD · DEFEND · SURVIVE", W / 2, 1400, pop(lt, 0.3), size=52, rgb=GREEN)


def e_side(ctx, lt, dur, T):  # «Battle Royale was a quick side project,»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    rrect(ctx, W / 2 - 330, 420, 660, 420, 30); fill(ctx, (0.12, 0.10, 0.20))
    text(ctx, "MAIN GAME", W / 2, 490, 64, WHITE, font="Anton")
    rrect(ctx, W / 2 - 280, 540, 560, 120, 18); fill(ctx, GREEN, 0.8)
    text(ctx, "SAVE THE WORLD", W / 2, 600, 58, WHITE, font="Anton")
    p = pop(lt, 0.6)
    rrect(ctx, W / 2 - 180, 700, 360 * p + 0.01, 100, 16); fill(ctx, STORM, 0.9)
    if p > 0.5:
        text(ctx, "SIDE MODE", W / 2, 750, 46, WHITE, font="Anton")
    hud(ctx, T, TAG, STORM)
    pill(ctx, "JUST A SIDE PROJECT", W / 2, 1400, pop(lt, 0.4), size=56, rgb=STORM)


def e_two(ctx, lt, dur, T):  # «built in about two months after Save the World came out in July 2017.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    calendar_page(ctx, 260, 560, 0.75, "2017", "JUL", "SAVE THE WORLD", GREEN, pop(lt, 0.0))
    calendar_page(ctx, 820, 560, 0.75, "2017", "SEP", "BATTLE ROYALE", STORM, pop(lt, 0.9))
    p = ease(clamp((lt - 0.3) / 2.6))
    rrect(ctx, 240, 820, 600, 34, 17); fill(ctx, (0.25, 0.25, 0.32))
    rrect(ctx, 240, 820, 600 * p + 0.01, 34, 17); fill(ctx, YELLOW)
    text(ctx, "≈ 2 MONTHS", W / 2, 920, 64, YELLOW, a=clamp((lt - 1.0) / 0.4), font="Anton")
    hud(ctx, T, TAG, YELLOW)


def e_owords(ctx, lt, dur, T):  # «In other words, the biggest game in the world started as a bonus mode.»
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.20), floor=False)
    rays(ctx, W / 2, 620, T, STORM, 0.12)
    icon(ctx, "🌍", W / 2, 620, 300, pop(lt, 0.0))
    icon(ctx, "🏆", W / 2 + 230, 470, 140, pop(lt, 0.8))
    hud(ctx, T, TAG, STORM)
    stamp(ctx, "A BONUS MODE", W / 2, 1400, clamp((lt - 2.0) / 0.25), YELLOW, size=80, rot=-0.06)


def e_concert(ctx, lt, dur, T):  # «In 2020, a Travis Scott concert inside Fortnite»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.02, 0.16), floor=False)
    stage(ctx, W / 2, 700, 0.9, T)
    ficha(ctx, "TRAVIS SCOTT", "ASTRONOMICAL · 2020", W / 2 - 70, 480, pop(lt, 0.2), emoji="🎤", accent=YELLOW, w=640)
    hud(ctx, T, TAG, YELLOW)


def e_players(ctx, lt, dur, T):  # «pulled in twelve point three million players at the same time,»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.04, 0.08, 0.16))
    v = int(counter(lt, 0, 12300000, 2.2))
    big_number(ctx, f"{v:,}", W / 2, 560, 120, SKY, 1.0)
    text(ctx, "PLAYERS AT ONCE", W / 2, 690, 64, WHITE, font="Anton")
    for i in range(18):
        icon(ctx, "🙋", 120 + (i % 9) * 105, 800 + (i // 9) * 90, 70, pop(lt, 0.1 + i * 0.06))
    hud(ctx, T, TAG, SKY)


def e_record(ctx, lt, dur, T):  # «an all-time record.»
    camera(ctx, keyframes(lt, [(0, 1.25), (0.3, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.08, 0.02), floor=False)
    rays(ctx, W / 2, 640, T, YELLOW, 0.1)
    icon(ctx, "🏆", W / 2, 660, 420, pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "ALL-TIME RECORD", W / 2, 1400, clamp((lt - 0.2) / 0.25), YELLOW, size=70, rot=-0.06)


def e_end(ctx, lt, dur, T):  # «And it all started because» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.57, e_hook2), (3.08, l_intro), (5.55, l_num(1, GREEN)), (6.08, e_zombie),
           (8.10, e_forts), (13.01, l_num(2, STORM)), (13.55, e_side), (15.70, e_two), (19.69, e_owords),
           (23.59, l_num(3, YELLOW)), (24.31, e_concert), (27.47, e_players), (30.89, e_record), (31.96, e_end)]
HOOK = "FORTNITE: MADE IN 2 MONTHS"
LISTA = [(5.55, "1/3"), (13.01, "2/3"), (23.59, "3/3")]
CTA = 23.7
COLA = 0.02
SFX = [(5.57, "ding"), (13.03, "ding"), (23.61, "ding"), (30.9, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.05, 0.08, 0.18), floor=False)
    rays(ctx, W / 2, 1000, 1.0, STORM, 0.06)
    island(ctx, W / 2, 1150, 1.35, 0.3, 0.5)
    calendar_page(ctx, W / 2 + 250, 860, 0.8, "BUILT IN", "2", "MONTHS", STORM)
    thumb_circle(ctx, W / 2 + 250, 870, 170, 170)
    thumb_arrow(ctx, 150, 1760, W / 2 + 120, 980)
    thumb_vignette(ctx)
    thumb_text(ctx, [("FORTNITE WAS", WHITE), "A SIDE PROJECT?"], y=330)
