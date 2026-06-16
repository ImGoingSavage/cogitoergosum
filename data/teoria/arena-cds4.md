# Toolkit práctico: visualización, storytelling y Git

## De qué trata esta lección (y qué sabrás hacer al final)

Un científico de datos no solo modela: **abre datos, los limpia, los comunica y versiona su trabajo**. Una entrevista de DS asume que ya dominas ese toolkit y lo prueba de refilón ("¿qué gráfico usarías?", "¿cómo deshaces un commit?"). Esta lección lo construye desde cero, con un hilo que une visualización, storytelling, pandas y Git/Bash: elegir la representación correcta es elegir *cuánta estructura mostrar*, y eso resulta ser el mismo trade-off sesgo-varianza que gobierna el modelado.

Al terminar podrás: (1) elegir el gráfico según datos + narrativa + audiencia, no por gusto; (2) ver por qué el ancho de bin de un histograma es una perilla de sesgo-varianza para el ojo; (3) envolver números en una historia que mueva a la acción; y (4) ejecutar el flujo Git mínimo (init → add → commit → push) y leer la historia con `git log`. Cada herramienta entra por su motivación, no como lista de comandos.

## Visualización: elegir el gráfico correcto

La fuerza de un gráfico no está en lo bonito, sino en su **adecuación a los datos, la narrativa y la audiencia**. El tipo de gráfico no es decorativo: cambia la comprensión y el impacto. La pregunta correcta no es "¿qué gráfico me gusta?" sino "¿qué estructura del dato quiero que salte a la vista, y para quién?".

| Gráfico | Para qué | Cuándo usarlo |
|---------|----------|---------------|
| **Barras** | comparar cantidades entre categorías | pocas categorías; proporciones relativas. Eje Y desde 0; horizontal si etiquetas largas |
| **Líneas** | tendencias y series de tiempo | relación entre dos variables numéricas o cambio en el tiempo. Pocas líneas, usa marcadores |
| **Dispersión (scatter)** | relación/correlación entre dos numéricas | ver correlación o su ausencia; añade línea de tendencia, color por categoría |
| **Histograma** | distribución de UNA variable numérica | ver sesgo (skewness), kurtosis, outliers. El **tamaño del bin** cambia todo |
| **Densidad (KDE)** | distribución suavizada | alternativa continua al histograma |
| **Pastel** | proporción de un todo | pocas categorías; úsalo con cautela |

Herramientas: **Matplotlib** y **Seaborn** (Python) para código; Tableau / Power BI para dashboards interactivos.

## Data storytelling

Un gráfico solo no convence: **datos + narrativa** mueven a la acción. Marco escenario-base:
1. **Conoce a tu audiencia** (técnica vs ejecutiva) y adapta el nivel.
2. **Elige el gráfico** que sirva a la narrativa, no al revés.
3. **Mantén la simplicidad** — un mensaje claro por visual.
4. Convierte números en una **historia** con contexto y recomendación.

## Pandas: abrir y limpiar datos

Pandas es la navaja del DS en Python: leer archivos (`read_csv`), `DataFrame`, filtrar, `groupby`, `merge`, detectar faltantes (`isnull().sum()`), agregar y transformar. Es la base sobre la que se hace el feature engineering [[arena-cds1]].

## Git: control de versiones

El backbone de cualquier flujo de DS moderno. Flujo mínimo de un repo local:

1. `git init` — inicia un repo en el directorio (o `git clone <url>` para copiar uno remoto).
2. Crea/edita archivos.
3. `git add .` — mueve cambios al **staging area** (deshacer: `git reset HEAD <archivo>`).
4. `git commit -m "mensaje"` — confirma al repositorio. El mensaje es **permanente**: sé cuidadoso.

Enlazar con remoto (GitHub):
- `git remote add origin <url>` — vincula el repo local con el remoto.
- `git push -u origin master` — sube los cambios (backup + colaboración).
- `git pull` — baja cambios del remoto.

**Inspeccionar historia:** `git log` con flags — `git log -3 archivo.py` (últimos 3 commits del archivo), `git log --since YYYY-MM-DD`, `git log --author=<nombre>`. Para ayuda de cualquier comando: `git <comando> --help`.

> Nota práctica: al crear el repo remoto en GitHub **no** lo inicialices con README/.gitignore/License si vas a empujar uno local — evita conflictos al primer push.

## Shell/Bash: pegamento del flujo

Bash conecta las piezas: navegar (`cd`, `ls`), mover/copiar archivos, lanzar scripts (`python app.py`), encadenar comandos con pipes, y automatizar tareas repetitivas. En MLOps [[arena-cds3]] los comandos de Docker (`docker build`, `docker run`) se ejecutan desde aquí.

---

## Mini-ejemplo trabajado: el tamaño del bin cambia la historia

Tienes 200 tiempos de respuesta. Un histograma con **5 bins** anchos los aplana en una sola joroba: "distribución unimodal". El mismo dato con **80 bins** se vuelve dentado y ruidoso: cada pico es un artefacto de pocos puntos. Con ~15 bins aparece la verdad: dos modos (usuarios rápidos en caché, lentos sin caché).

El bin es una **perilla de suavizado**: pocos bins = mucho sesgo (escondes estructura), muchos bins = mucha varianza (inventas estructura). El histograma honesto vive en medio.

**Predicción antes de seguir:** ¿esta tensión te recuerda a algún parámetro de modelado? Respuesta: es **exactamente** el trade-off sesgo-varianza — el ancho de bin es a un histograma lo que K es a KNN o λ a un suavizador: bins anchos ↔ K grande (suave, sesgado), bins finos ↔ K=1 (dentado, varianza alta). Elegir el bin es elegir flexibilidad, y el ojo puede engañarse igual que un modelo puede sobreajustar.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** elegir gráfico según estructura → barras (comparar categorías), líneas (tendencia temporal), scatter (correlación), histograma (distribución).
- **Contraejemplo (gráfico que miente):** un eje Y que no empieza en 0 en un gráfico de barras exagera diferencias pequeñas; el gráfico "correcto" mal configurado engaña.
- **Caso borde (pastel con muchas categorías):** el ojo no compara bien ángulos; con >4 categorías un gráfico de barras comunica mejor que un pastel.

## Errores típicos

- **Conceptual:** elegir el gráfico primero y forzar la narrativa, en vez de dejar que la estructura del dato y la audiencia lo dicten.
- **Técnico:** un único bin/escala sin probar alternativas; el histograma "por defecto" puede ocultar bimodalidad.
- **De interpretación:** confundir correlación visible en un scatter con causalidad.

## Transferencia isomorfa

- **Ancho de bin ↔ flexibilidad / sesgo-varianza:** suavizar de más esconde estructura, de menos inventa ruido, como K en KNN o λ en un spline (conecta con [[arena-isl1]]).
- **Git (log inmutable de commits) ↔ versionado y reproducibilidad:** la historia append-only de Git es el mismo principio de auditoría que versionar modelo+pipeline en MLOps (conecta con [[arena-cds3]]).
- **Elegir el gráfico según la estructura ↔ elegir la herramienta según el problema:** "barras para comparar, líneas para tendencia" es el mismo reflejo de reconocimiento que "ventana deslizante para subarreglos, hashing para memoria".
- **Storytelling con audiencia ↔ comunicación bajo presión (Nivel E):** adaptar el nivel técnico a quien escucha es la competencia que la simulación de entrevista entrena.

Moraleja de la arista: *el ancho de bin es una perilla de sesgo-varianza para el ojo; suaviza demasiado y escondes la verdad, suaviza poco e inventas ruido.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Comparar cantidades entre categorías" | Barras (eje Y desde 0) |
| "Cambio en el tiempo / tendencia" | Línea (serie de tiempo) |
| "¿Están correlacionadas dos variables?" | Scatter + línea de tendencia |
| "Ver la distribución / sesgo / outliers" | Histograma (cuida el bin) |
| "La audiencia es ejecutiva" | Simplifica; narrativa + recomendación |
| "Guardar progreso y compartir código" | `git add`/`commit`/`push` a remoto |
| "Ver quién cambió qué y cuándo" | `git log` con flags (--author, --since) |
| "Automatizar tareas repetitivas" | Script de Bash |

---

> **Síntesis:** El toolkit que sostiene el día a día del DS: visualización (elegir el gráfico según datos+narrativa+audiencia — barras para comparar, líneas para tendencias, scatter para correlación, histograma para distribución) envuelta en **storytelling** que convierte números en decisiones; **pandas** para abrir y limpiar datos; y **Git** como control de versiones (init/add/commit/push, `git log` para historia) más **Bash** como pegamento que lanza scripts y comandos. Son las habilidades que una entrevista de DS asume que ya dominas.

---

*Retrieval: cierra y responde: (1) ¿qué gráfico para comparar categorías, para tendencia temporal y para distribución?; (2) ¿qué tres cosas debe servir un buen gráfico?; (3) ordena el flujo Git mínimo de init a push; (4) ¿qué hace `git reset HEAD <archivo>`?*
