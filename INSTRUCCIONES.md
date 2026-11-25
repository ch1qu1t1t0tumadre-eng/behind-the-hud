# Behind the HUD — producción diaria de Shorts

Canal: **Behind the HUD** (@BehindtheHUD-c1n) · Studio: https://studio.youtube.com/channel/UCToBFcTJkGZYSeYUOt2AXnA
Nicho: *The hidden reasons behind video games*: curiosidades de videojuegos (historia, desarrollo, fallos, récords, empresas, diseñadores).
**Todo lo que sale en el vídeo va en inglés americano** (guion, voz, textos, título, descripción, hashtags). Al dueño se le habla en español (España).
Ritmo: **1 Short al día**, publicado a las **20:00** (Europe/Madrid), subido como **privado + programado**.

## 0. Preparación
```bash
cd /home/claude/behind-the-hud && bash pipeline/setup.sh
```
Lee `agenda.md` (huecos ya ocupados) y `temas_usados.md` (no repetir).

## 1. Créditos de ElevenLabs (cuenta compartida con «Wait, What.»)
`account_get_usage` del conector ElevenLabs → `libres = character_limit - character_count`.
**Vídeos que se pueden hacer hoy = min(1, (libres − 3000) // 850)**. Los 3000 son la reserva para «Wait, What.».
Si sale 0 o menos, no hagas nada y avisa al dueño (cuándo se renuevan los créditos: `next_character_count_reset_unix`).

## 2. Tema y guion (skills yt-shorts-hook-writer + yt-shorts-scripter, adaptadas a videojuegos)
- Tema: protagonista famoso (juego, consola, empresa o diseñador) + giro inesperado. Rota épocas y temas: arcade, consolas, PC, empresas, diseñadores, bugs, récords, ventas, censura, desarrollo, hardware.
- **Dato verificado con WebSearch en 2 fuentes** antes de escribir. Nada inventado, nada de rumores.
- Formato BUCLE: la primera frase es el gancho (famoso + giro), «In other words…» como 2.º gancho a mitad, mini-giro cada 2–3 frases, sin llamadas a la acción en la voz (el aviso Subscribe/Like/Share va solo en pantalla, ver paso 4), y la última frase se corta para enlazar con la primera.
- 125–140 palabras (680–780 caracteres). Protagonista nombrado 4–7 veces. Etiquetas de ElevenLabs v4: `[intrigued]` al inicio y `[dramatic]` antes de «In other words». Guarda el texto en `trabajo/<id>/voz.txt`.
- Ejemplos: `ejemplos/guion_v01.txt` … `guion_v03.txt`.

## 3. Voz
- Conector ElevenLabs: `creative_create_flow` → `creative_generate_speech` (model `eleven_v4`, voice Dean `hqsADTrqjrr0sI9LFcYV`, **generations_count 1**; nunca repetir la llamada para reintentar).
- `creative_transcribe_audio` (eleven_scribe_v1, `connect_from` el nodo de voz). Cuando termine, `creative_get_flow_run_status` una vez para sacar las URLs.
- `curl` del mp3 → `trabajo/<id>/voz.mp3` y del `words_download_url` → `trabajo/<id>/words.json`.
- `python3 pipeline/acelerar.py trabajo/<id>` (quita silencios y acelera a ~195 ppm). Duración final 36–46 s.

## 4. Animación (skill shorts-visual-director, estilo Behind the HUD)
- `trabajo/<id>/escenas.py` empieza con:
  ```python
  import math, os, sys
  sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
  from anim import *  # noqa
  from hud import *  # noqa
  TAG = "BEHIND THE HUD // FILE 0NN"
  SUBTITULO = subtitulo_hud   # subtítulos propios del canal (obligatorio)
  ```
- **Subtítulos**: `SUBTITULO = subtitulo_hud` (definido en `hud.py`). Hay 5 estilos gamer que cambian en cada frase: NEÓN, ARCADE (pixel, letra a letra), GLITCH, panel HUD y COMBO, que es dorado y se usa siempre para números y años. No uses el subtítulo amarillo de «Wait, What.».
- Estilo: fondos `bg_arcade`, `bg_desert`, `bg_blueprint`, `bg_dark`; marco `hud(ctx, T, TAG, color)` en todas las escenas; contadores con `big_number`; `ficha()` para cada persona nombrada; palabra gigante amarilla (la pone anim.py).
- 15–18 escenas, cada una ≤ 3,5 s, cambio de plano cuando cambia la frase (tiempos de `words.json`). **La última escena = la primera** (bucle). El «In other words» lleva el plano más fuerte (zoom rápido + rayos).
- **Aviso SUBSCRIBE · LIKE · SHARE (petición del dueño, 25/11/2026): solo en pantalla, sin voz.** `anim.py` lo pone solo en todos los Shorts: un panel animado de 2,6 s abajo (y ≈ 1420) a mitad del vídeo, con un botón SUBSCRIBE que se pulsa, LIKE y SHARE, más un «pop». Para moverlo, pon en escenas.py `CTA = <segundos>`: mejor justo después del «In other words» o al empezar el dato 2/3. Nunca en los 3 primeros segundos ni en los 3 últimos, para no romper el gancho ni el bucle. `CTA = None` lo quita. Nunca digas «like», «subscribe» ni «share» en la voz.
- Cámara siempre centrada en `cy = 960`. Gráficos en y 250–900 y etiquetas en y 1300–1450. **La franja 950–1170 queda libre para el subtítulo.**
- **Prohibido**: personajes con copyright, logos, carátulas, sprites originales de juegos, fotos de personas reales. Dibuja versiones genéricas o propias (ver los alienígenas de `hud.py` y la consola portátil de `ejemplos/escenas_v03.py`). Para un juego concreto, usa su nombre en texto, nunca su arte.
- Revisa los previews: `python3 pipeline/anim.py trabajo/<id> preview t1 t2 …` (uno por escena) → hoja de contactos → corrige solapes, texto cortado, cosas tapadas por el subtítulo. Después haz el render final con `python3 pipeline/anim.py trabajo/<id>`, que genera `short.mp4`.
- Miniatura: función `MINIATURA(ctx)` en escenas.py con `thumb_text` (2 líneas que no desvelen la respuesta ni digan algo falso), `thumb_circle` y `thumb_arrow` → `python3 pipeline/miniatura.py trabajo/<id>/escenas.py trabajo/<id>/miniatura.jpg`.

## 5. Publicar los archivos (rama `media`)
```bash
cd /home/claude/behind-the-hud
git fetch -q --depth 1 origin media && git checkout -q -B media origin/media || git checkout -q --orphan media
git rm -rfq --cached . >/dev/null 2>&1; mkdir -p media
cp trabajo/<id>/short.mp4 media/<id>.mp4; cp trabajo/<id>/miniatura.jpg media/<id>.jpg
git add media/<id>.mp4 media/<id>.jpg && git commit -qm "media <id>" && git -c push.negotiate=true push -q -f origin media
SHA=$(git rev-parse HEAD); git checkout -qf main
```
URL raw: `https://raw.githubusercontent.com/ch1qu1t1t0tumadre-eng/behind-the-hud/$SHA/media/<id>.mp4`. El .jpg tiene la misma ruta con extensión .jpg.
Después de subir a YouTube, se puede vaciar la rama `media` (opcional).

## 6. Subir a YouTube Studio (navegador integrado, `mcp__remote-devices__Claude_Browser__*`)
Carga antes la skill built-in-browser. **Comprueba que el canal que se ve es «Behind the HUD»** (`#entity-name`). Si es otro, para y avisa.
1. `navigate` → `https://studio.youtube.com/channel/UCToBFcTJkGZYSeYUOt2AXnA/videos/upload?d=ud`
2. `javascript_tool` (inyecta el archivo):
```js
const r = await fetch('URL_RAW_MP4');
window.__v = new File([await r.blob()], 'ID.mp4', {type:'video/mp4'});
if(!window.__origClick) window.__origClick = HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click = function(){ if(this.type==='file' && window.__v){ const dt=new DataTransfer(); dt.items.add(window.__v); this.files=dt.files; window.__v=null; setTimeout(()=>{this.dispatchEvent(new Event('input',{bubbles:true}));this.dispatchEvent(new Event('change',{bubbles:true}))},50); return;} return window.__origClick.call(this); };
'ok '+r.status
```
3. `javascript_tool`: `function all(...)` (abajo) y luego `all(document,'#select-files-button')[0].click()`. Espera unos 5 s hasta que aparezcan los `#textbox` del diálogo.
4. Título, descripción y audiencia con JS. **No teclees en estos campos**, porque el autocompletado de hashtags estropea el texto:
```js
function all(root,sel,out=[]){root.querySelectorAll(sel).forEach(x=>out.push(x));root.querySelectorAll('*').forEach(x=>{if(x.shadowRoot)all(x.shadowRoot,sel,out)});return out}
function setBox(el,text){el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,text);el.dispatchEvent(new Event('input',{bubbles:true}));el.blur();}
const [t,d]=all(document,'ytcp-uploads-dialog #textbox'); setBox(t,'TITULO'); await new Promise(r=>setTimeout(r,400)); setBox(d,'DESCRIPCION');
all(document,'ytcp-uploads-dialog tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]')[0].click();
```
   - **Título** (skill shorts-metadata-optimizer): ≤ 60 caracteres, en forma de pregunta o afirmación que no desvele la respuesta, con un emoji al final y ` #shorts`.
   - **Descripción**: el gancho en la línea 1; 1–2 líneas con el dato; `Sources: …`; hashtags `#shorts #gaming #<tema> #retrogaming #gamingfacts` (3–5 en total más #shorts).
5. Miniatura: repite la inyección del paso 2 con la URL raw del .jpg (`type:'image/jpeg'`) y pulsa `all(document,'ytcp-uploads-dialog ytcp-thumbnail-uploader #select-button')[0].click()`. Espera 6 s.
6. «Mostrar más» (`ytcp-uploads-dialog #toggle-button`). Categoría: clic en `ytcp-uploads-dialog ytcp-form-select#category ytcp-dropdown-trigger` → opción con texto exacto «Videojuegos». Etiquetas: `find` «Añade una etiqueta» → clic → `type` 8–12 etiquetas separadas por comas y terminadas en coma → tecla Return.
7. Pulsa «Siguiente» (`ytcp-uploads-dialog #next-button`) 3 veces → «Programar». Abre la sección de programación y pon la fecha y la hora del hueco (20:00, Europe/Madrid) → «Programar». Comprueba en la lista de contenido que el vídeo sale como «Programado» y que se ven el título y la miniatura.
   - Si no consigues programarlo, déjalo en **Privado** (radio `PRIVATE` → `#done-button`) y avisa al dueño.

## 7. Cierre
- Añade cada vídeo a `agenda.md` y a `temas_usados.md`; copia `escenas.py` y `voz.txt` a `ejemplos/` (como `escenas_<id>.py` y `guion_<id>.txt`). Haz commit y push a `main`.
- Manda un `SendUserMessage` en español: título, hora de publicación y enlace de cada vídeo, créditos de ElevenLabs que quedan y cualquier problema.
- **Nunca publiques nada como público directamente** y nunca subas a otro canal. Nunca escribas contraseñas ni códigos. Si el navegador no responde, deja los vídeos en la rama `media` y manda al dueño los enlaces raw.
