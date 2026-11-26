"""Behind the HUD · 017 (EN) — 3 Pokémon Facts You Didn't Know. Formato lista.
Sin dibujar ningún Pokémon ni logos: fichas con nombre + icono genérico (⚡ 🦏 🌙 🐍), cartas genéricas y letras.
Datos: Rhydon fue el primer Pokémon diseñado (Ken Sugimori; Guinness World Records, Red Bull, Nintendo Everything);
Clefairy estaba pensado como mascota y protagonizó el primer manga (Den of Geek, Bulbapedia);
Ekans = «snake» al revés y Arbok = «kobra» al revés (Bulbapedia, PokémonDB, Kotaku)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from anim import *  # noqa
from hud import *  # noqa

TAG = "BEHIND THE HUD // FILE 017-L"
SUBTITULO = subtitulo_hud
PINK = (1.0, 0.45, 0.75)
ELEC = (1.0, 0.86, 0.15)
TEAL = (0.20, 0.85, 0.80)


def card(ctx, x, y, s, emoji, name, col, T=0.0, appear=1.0, rot=0.0, crown=0.0):
    """Carta coleccionable genérica (sin marca): marco de color, icono y nombre."""
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * appear, s * appear)
    rrect(ctx, -150, -210, 300, 420, 26); fill(ctx, col)
    rrect(ctx, -132, -192, 264, 384, 18); fill(ctx, (0.10, 0.10, 0.16))
    rrect(ctx, -116, -170, 232, 210, 14); fill(ctx, (0.22, 0.22, 0.32))
    glow(ctx, 0, -65, 120, col, 0.35)
    icon(ctx, emoji, 0, -65, 150, 1.0)
    text(ctx, name, 0, 105, 56 if len(name) < 9 else 46, WHITE, font="Anton")
    for k in range(3):
        rrect(ctx, -100, 140 + k * 0, 200, 10, 5); fill(ctx, col, 0.5)
    if crown > 0.05:
        ctx.save(); ctx.translate(0, -250 - 20 * (1 - crown)); ctx.scale(crown, crown)
        icon(ctx, "👑", 0, 0, 120, 1.0)
        ctx.restore()
    ctx.restore()


def sketchbook(ctx, x, y, s, T, prog=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -300, -220, 600, 440, 20); fill(ctx, (0.96, 0.94, 0.86))
    for k in range(9):
        ctx.move_to(-280, -180 + k * 46); ctx.line_to(280, -180 + k * 46); stroke(ctx, (0.75, 0.82, 0.92), 2)
    # garabato genérico de «dinosaurio» que se va dibujando (no es ningún Pokémon)
    pts = [(-160, 120), (-150, 20), (-90, -40), (-20, -60), (40, -120), (90, -110), (80, -60), (130, -20), (150, 60), (110, 120)]
    n = max(2, int(len(pts) * clamp(prog)))
    ctx.move_to(*pts[0])
    for p in pts[1:n]:
        ctx.line_to(*p)
    stroke(ctx, (0.25, 0.25, 0.30), 9)
    text(ctx, "#001", 200, 170, 60, RED, font="Anton", shadow=False)
    ctx.restore()


def manga(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -300, 460, 600, 14); fill(ctx, WHITE)
    for (bx, by, bw, bh) in [(-210, -280, 420, 200), (-210, -60, 200, 180), (10, -60, 200, 180), (-210, 140, 420, 140)]:
        rrect(ctx, bx, by, bw, bh, 6); stroke(ctx, (0.1, 0.1, 0.12), 6)
    icon(ctx, "🌙", 0, -180, 130, 1.0)
    icon(ctx, "💬", -110, 30, 90, 1.0)
    icon(ctx, "⭐", 110, 30, 90, 1.0)
    text(ctx, "1996", 0, 215, 70, (0.1, 0.1, 0.12), font="Anton", shadow=False)
    ctx.restore()


def tv(ctx, x, y, s, T, emoji="⚡"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -280, -200, 560, 380, 30); fill(ctx, (0.15, 0.15, 0.20))
    rrect(ctx, -250, -170, 500, 320, 18); fill(ctx, (0.30, 0.55, 0.95))
    glow(ctx, 0, -10, 160, ELEC, 0.5)
    icon(ctx, emoji, 0, -10, 190, 1.0)
    ctx.move_to(-80, 180); ctx.line_to(-130, 240); stroke(ctx, (0.15, 0.15, 0.20), 14)
    ctx.move_to(80, 180); ctx.line_to(130, 240); stroke(ctx, (0.15, 0.15, 0.20), 14)
    ctx.restore()


def word_tiles(ctx, word, y, lt, flip_at, target, col):
    """Letras que se dan la vuelta para leer la palabra al revés."""
    n = len(word)
    size = 150
    gap = 16
    x0 = W / 2 - (n * size + (n - 1) * gap) / 2 + size / 2
    for i in range(n):
        p = clamp((lt - flip_at - i * 0.07) / 0.25)
        ch = word[i] if p < 0.5 else target[i]
        sx = abs(math.cos(p * math.pi))
        ctx.save(); ctx.translate(x0 + i * (size + gap), y); ctx.scale(max(0.05, sx), 1)
        tile(ctx, ch, 0, 0, size, pop(lt, 0.05 * i), col if p < 0.5 else LIME)
        ctx.restore()


# ---------- escenas ----------
def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.10, 0.02), floor=False)
    rays(ctx, W / 2, 620, T, ELEC, 0.06)
    card(ctx, W / 2, 700, 1.1, "⚡", "PIKACHU", ELEC, T, crown=1.0)
    icon(ctx, "❓", W / 2 + 230, 520, 140, 1.0)
    hud(ctx, T, TAG, ELEC)
    pill(ctx, "THE FACE OF POKÉMON?", W / 2, 1400, 1.0, size=52, rgb=ELEC)


def e_hook(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.06)]))


def e_hook2(ctx, lt, dur, T):  # «...the face of Pokémon.» — la corona tiembla
    camera(ctx, keyframes(lt, [(0, 1.12), (0.25, 1.0), (dur, 1.04)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.10, 0.02), floor=False)
    card(ctx, W / 2, 700, 1.1, "⚡", "PIKACHU", ELEC, T, rot=0.03 * math.sin(T * 20), crown=1.0)
    x_mark(ctx, W / 2, 425, 70, clamp((lt - 0.4) / 0.3))
    hud(ctx, T, TAG, ELEC)
    stamp(ctx, "NOT THE PLAN", W / 2, 1400, clamp((lt - 0.2) / 0.25), RED, size=74, rot=-0.06)


def l_intro(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.12, 0.03, 0.14))
    for i, (e, c) in enumerate([("🦏", (0.6, 0.6, 0.65)), ("🌙", PINK), ("🐍", (0.6, 0.35, 0.9))]):
        card(ctx, 250 + i * 290, 660, 0.72, e, ["#1", "#2", "#3"][i], c, T, appear=pop(lt, 0.1 + i * 0.18), rot=(i - 1) * 0.08)
    badge(ctx, "POKÉMON FACTS", W / 2, 400, pop(lt, 0.0), size=66, bg=PINK)
    hud(ctx, T, TAG, PINK)
    pill(ctx, "YOU DIDN'T KNOW", W / 2, 1400, pop(lt, 0.1), size=56, rgb=PINK)


def l_num(n, col):
    def f(ctx, lt, dur, T):
        camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.0), (dur, 1.05)]), W / 2, 960)
        bg_arcade(ctx, T, (0.05, 0.03, 0.12), floor=False)
        rays(ctx, W / 2, 620, T, col, 0.08)
        text(ctx, "FACT", W / 2, 440, 90, WHITE, font="Anton")
        big_number(ctx, f"#{n}", W / 2, 690, 300, col, pop(lt, 0.0))
        hud(ctx, T, TAG, col)
    return f


def e_first(ctx, lt, dur, T):  # «The very first Pokémon ever drawn...»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_blueprint(ctx, T)
    sketchbook(ctx, W / 2, 640, 1.0, T, prog=lt / 1.6)
    icon(ctx, "✏️", W / 2 + 230 - 60 * math.sin(T * 6), 520, 110, 1.0)
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "THE FIRST DESIGN EVER", W / 2, 1400, pop(lt, 0.2), size=52, rgb=TEAL)


def e_notstarter(ctx, lt, dur, T):  # «...wasn't Pikachu or a starter.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.10, 0.04, 0.10), floor=False)
    for i, (e, c) in enumerate([("⚡", ELEC), ("🔥", ORANGE), ("💧", (0.3, 0.6, 1.0)), ("🌿", GREEN)]):
        x = 175 + i * 243
        card(ctx, x, 640, 0.62, e, "", c, T, appear=pop(lt, i * 0.1), rot=(i - 1.5) * 0.06)
        x_mark(ctx, x, 640, 85, clamp((lt - 0.6 - i * 0.12) / 0.25))
    hud(ctx, T, TAG, RED)
    stamp(ctx, "NOPE", W / 2, 1400, clamp((lt - 0.5) / 0.25), RED, size=86, rot=-0.06)


def e_rhydon(ctx, lt, dur, T):  # «It was Rhydon, the rock rhino.»
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.08, 0.10), floor=False)
    rays(ctx, W / 2, 620, T, (0.7, 0.7, 0.75), 0.08)
    card(ctx, W / 2, 640, 1.15, "🦏", "RHYDON", (0.65, 0.65, 0.70), T, appear=pop(lt, 0.0))
    hud(ctx, T, TAG, YELLOW)
    stamp(ctx, "POKÉMON #1 EVER", W / 2, 1400, clamp((lt - 0.4) / 0.25), YELLOW, size=70, rot=-0.06)


def e_clefairy(ctx, lt, dur, T):  # «Clefairy was planned as the Pokémon mascot.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.07)]), W / 2, 960)
    bg_arcade(ctx, T, (0.14, 0.04, 0.12), floor=False)
    rays(ctx, W / 2, 620, T, PINK, 0.07)
    card(ctx, W / 2, 700, 1.1, "🌙", "CLEFAIRY", PINK, T, crown=ease_back(clamp((lt - 0.6) / 0.4)))
    hud(ctx, T, TAG, PINK)
    pill(ctx, "THE ORIGINAL MASCOT PLAN", W / 2, 1400, pop(lt, 0.2), size=50, rgb=PINK)


def e_manga(ctx, lt, dur, T):  # «It even starred in the first Pokémon manga.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    manga(ctx, W / 2, 640, 0.95 * pop(lt, 0.0) + 0.0001, T)
    hud(ctx, T, TAG, PINK)
    pill(ctx, "STAR OF THE FIRST MANGA", W / 2, 1400, pop(lt, 0.2), size=50, rgb=PINK)


def e_anime(ctx, lt, dur, T):  # «Then the anime gave Pikachu to Ash, and kids went crazy for it.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    bg_arcade(ctx, T, (0.05, 0.08, 0.16))
    tv(ctx, W / 2, 600, 1.0, T)
    k = clamp((lt - 2.0) / 1.0)
    for i in range(14):
        a = i * 2.4 + T
        r = 330 + 40 * math.sin(T * 3 + i)
        icon(ctx, ["❤️", "⭐", "⚡"][i % 3], W / 2 + r * math.cos(a), 600 + r * 0.7 * math.sin(a), 70, k)
    hud(ctx, T, TAG, ELEC)
    pill(ctx, "THE ANIME CHANGED EVERYTHING", W / 2, 1400, pop(lt, 0.2), size=46, rgb=ELEC)


def e_owords(ctx, lt, dur, T):  # «In other words, a pink fairy almost became the most famous Pokémon on Earth.»
    camera(ctx, keyframes(lt, [(0, 1.7), (0.3, 1.0), (dur, 1.08)]) + 0.012 * math.sin(T * 45) * (lt < 0.45), W / 2, 960)
    bg_arcade(ctx, T, (0.18, 0.02, 0.10), floor=False)
    rays(ctx, W / 2, 600, T, PINK, 0.10)
    card(ctx, 300, 680, 0.85, "🌙", "CLEFAIRY", PINK, T, rot=-0.08)
    card(ctx, 780, 680, 0.85, "⚡", "PIKACHU", ELEC, T, rot=0.08)
    m = ease(clamp((lt - 1.2) / 1.6))
    cx = lerp(300, 780, m)
    icon(ctx, "👑", cx, 470 - 50 * math.sin(m * math.pi), 120, 1.0)
    icon(ctx, "🌍", W / 2, 880, 110, pop(lt, 2.4))
    hud(ctx, T, TAG, PINK)
    stamp(ctx, "SO CLOSE", W / 2, 1400, clamp((lt - 0.7) / 0.25), YELLOW, size=80, rot=-0.06)


def e_hidden(ctx, lt, dur, T):  # «Some Pokémon names are hidden words.»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 960)
    bg_blueprint(ctx, T)
    for i, ch in enumerate("?????"):
        tile(ctx, ch, 230 + i * 155, 560 + 30 * math.sin(T * 4 + i), 140, pop(lt, i * 0.08), TEAL, rot=0.1 * math.sin(T * 3 + i))
    icon(ctx, "🔍", W / 2 + 200, 800, 150, pop(lt, 0.5))
    hud(ctx, T, TAG, TEAL)
    pill(ctx, "HIDDEN WORDS", W / 2, 1400, pop(lt, 0.2), size=58, rgb=TEAL)


def e_ekans(ctx, lt, dur, T):  # «Ekans is snake backwards,»
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.05)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.03, 0.14), floor=False)
    ficha(ctx, "EKANS", "POKÉMON #23", W / 2 - 60, 520, pop(lt, 0.0), emoji="🐍", accent=(0.7, 0.4, 1.0), w=640)
    word_tiles(ctx, "EKANS", 780, lt, 0.7, "SNAKE", (0.7, 0.4, 1.0))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "BACKWARDS = SNAKE", W / 2, 1400, pop(lt, 1.0), size=56, rgb=LIME)


def e_arbok(ctx, lt, dur, T):  # «and Arbok is kobra backwards.»
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_arcade(ctx, T, (0.08, 0.03, 0.14), floor=False)
    ficha(ctx, "ARBOK", "POKÉMON #24", W / 2 - 60, 520, pop(lt, 0.0), emoji="🐍", accent=(0.85, 0.3, 0.9), w=640)
    word_tiles(ctx, "ARBOK", 780, lt, 0.8, "KOBRA", (0.85, 0.3, 0.9))
    hud(ctx, T, TAG, LIME)
    pill(ctx, "BACKWARDS = KOBRA", W / 2, 1400, pop(lt, 1.1), size=56, rgb=LIME)


def e_end(ctx, lt, dur, T):  # «So next time you open your Pokédex, remember that» -> bucle
    hero(ctx, T, keyframes(lt, [(0, 1.06), (dur, 1.0)]))


ESCENAS = [(0.0, e_hook), (1.50, e_hook2), (3.03, l_intro), (5.43, l_num(1, TEAL)), (5.93, e_first),
           (8.00, e_notstarter), (9.76, e_rhydon), (11.48, l_num(2, PINK)), (12.06, e_clefairy),
           (14.31, e_manga), (16.52, e_anime), (20.08, e_owords), (24.54, l_num(3, LIME)),
           (25.40, e_hidden), (27.37, e_ekans), (29.08, e_arbok), (31.01, e_end)]
HOOK = "PIKACHU WASN'T THE PLAN"
LISTA = [(5.43, "1/3"), (11.48, "2/3"), (24.54, "3/3")]
CTA = 24.6
COLA = 0.02
SFX = [(5.45, "ding"), (9.8, "pop"), (11.5, "ding"), (24.56, "ding"), (28.1, "pop"), (29.9, "pop")]


def MINIATURA(ctx):
    bg_arcade(ctx, 1.0, (0.12, 0.10, 0.02), floor=False)
    rays(ctx, W / 2, 1000, 1.0, ELEC, 0.06)
    card(ctx, W / 2 - 210, 1100, 1.15, "⚡", "PIKACHU", ELEC, 0.0, rot=-0.08)
    card(ctx, W / 2 + 230, 1120, 1.15, "🌙", "CLEFAIRY", PINK, 0.0, rot=0.08, crown=1.0)
    thumb_circle(ctx, W / 2 + 230, 820, 120, 110)
    thumb_arrow(ctx, 140, 1760, W / 2 + 120, 880)
    thumb_vignette(ctx)
    thumb_text(ctx, [("PIKACHU WASN'T", WHITE), "THE PLAN?"], y=330)
