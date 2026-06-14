# Toolkit práctico: visualización, storytelling y Git

## Visualización: elegir el gráfico correcto

La fuerza de un gráfico está en su **adecuación a los datos, la narrativa y la audiencia**. El tipo de gráfico no es decorativo: cambia la comprensión y el impacto.

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
