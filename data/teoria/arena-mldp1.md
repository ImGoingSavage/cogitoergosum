# Patrones de representación de datos y de problemas

Un *design pattern* de ML nombra un problema recurrente y su solución probada (con sus trade-offs). Estos seis representan la **entrada** y la **salida** del modelo.

## Hashed Feature — categóricas problemáticas

Para una categórica de **alta cardinalidad**, con **vocabulario incompleto** o **cold-start** (hospital_id, aeropuerto), one-hot falla. Solución: aplica un **hash de huella** (FarmHash: determinista y portable, **no** criptográfico — MD5 lleva *salt* y no es reproducible) y toma el **módulo** del número de buckets. Aceptas **colisiones** a cambio de robustez ante valores nuevos, tamaño acotado y cold-start.

- Regla: ~5 entradas por bucket; trata `num_buckets` como **hiperparámetro**.
- No basta subir buckets: con 347 aeropuertos y 100.000 buckets aún hay 45% de colisión.
- Si la categórica es muy **sesgada** (ORD vs un aeropuerto pequeño), añade una **feature agregada** (p.ej. probabilidad de a-tiempo por aeropuerto).

## Embeddings — representación densa aprendida

Mapea datos de alta cardinalidad (categóricas, texto, imágenes) a un espacio de **menor dimensión y aprendido**, donde la **cercanía codifica similitud** relevante. Frente a one-hot (disperso, sin similitud), mejora el aprendizaje de patrones. El tamaño del embedding es un hiperparámetro.

## Feature Cross y Multimodal Input

- **Feature Cross:** combinar (cruzar) categóricas para crear una conjunción; permite a un **modelo lineal** aprender relaciones no lineales. Los cruces grandes se acotan con hashing o embeddings.
- **Multimodal Input:** combinar datos de distintas **modalidades** (texto + imagen + tabular) concatenando sus representaciones, o representar un dato de varias formas a la vez.

## Reframing — cambiar la representación de la SALIDA

- **Regresión → clasificación:** cuando la salida es probabilística/multimodal (lluvia: a veces 0.3 cm, a veces 0.5 cm), clasifica sobre **buckets** (p.ej. 512-way) y obtén una **PDF** en vez de un solo número. El ancho del bin gobierna la precisión; PDF afilada → quédate con la regresión.
- **Clasificación → regresión:** cuando el objetivo real es continuo (recomendar por **fracción de vídeo vista**, no por *click*, para evitar clickbait). Cuidado con el **label bias** al cambiar el objetivo.
- Alternativa: **multitask learning** (varias cabezas y pérdidas: hacer ambas a la vez).

## Multilabel — más de una etiqueta por ejemplo

Distinto de multiclase (una de N, **softmax**, argmax). En multilabel un ejemplo puede tener **varias** etiquetas → capa de salida **sigmoid** (cada valor independiente 0-1), etiqueta **multi-hot**, y se aplica un **umbral por clase**.

---

## Mini-ejemplo trabajado: por qué subir buckets no salva el hashing

Tienes 347 aeropuertos (alta cardinalidad, con cold-start: aparecen nuevos). One-hot es frágil. Aplicas un **hash de huella** y módulo `num_buckets`. ¿Cuántos buckets para evitar colisiones? La intuición dice "muchos", pero choca con la **paradoja del cumpleaños**:

- Con `num_buckets = 100 000` (¡300× más que aeropuertos!), la probabilidad de que *algún* par colisione sigue siendo ~**45%**.
- Regla práctica: apunta a ~5 entradas por bucket y trata `num_buckets` como **hiperparámetro**, aceptando que habrá colisiones a cambio de tamaño acotado y robustez ante valores nuevos.

Si la categórica es muy **sesgada** (ORD mueve millones, un aeródromo rural casi nada), la colisión duele más; lo compensas con una **feature agregada** (p. ej. probabilidad histórica de salir a tiempo por aeropuerto).

**Predicción antes de seguir:** ¿qué patrón usarías si lo que importa es que "JFK se parezca a EWR" (similitud entre aeropuertos)? No hashing: un **embedding**, donde la cercanía en el espacio aprendido *codifica* similitud — algo que el hash, deliberadamente, destruye.

## Prototipo, contraejemplo y caso borde

- **Prototipo (hashed feature):** categórica enorme con cold-start y sin necesidad de similitud → hash de huella + módulo.
- **Contraejemplo (hash donde toca embedding):** usar hashing cuando necesitas similitud entre categorías → pierdes justo la estructura que querías; ahí va un embedding.
- **Caso borde (salida bimodal):** predecir lluvia que a veces es 0.3 cm y a veces 0.5 cm con regresión da un promedio sin sentido → **reframing** a clasificación por buckets devuelve una PDF útil.

## Errores típicos

- **Conceptual:** confundir multiclase (una de N, **softmax**) con multilabel (varias, **sigmoid** + multi-hot + umbral por clase).
- **Técnico:** usar un hash criptográfico con salt (MD5) en vez de uno de huella determinista (FarmHash) → no reproducible entre entrenamiento y serving.
- **De encuadre:** optimizar clicks cuando el valor real es continuo (fracción de vídeo vista) → clickbait; reencuadra clasificación→regresión (cuidado con el label bias).

## Transferencia isomorfa

Estos patrones de representación son ideas que ya viste en otros disfraces:

- **Hashed Feature ↔ hash table / Bloom filter:** cambiar tamaño acotado por colisiones es exactamente el trade-off memoria-precisión de una tabla hash (conecta con [[arena-cc1]], hashing como memoria).
- **Embeddings ↔ búsqueda por similitud / vecino más cercano:** un espacio donde la distancia codifica similitud es la base del nearest-neighbor y de la recuperación semántica.
- **Reframing regresión→clasificación ↔ predecir una distribución:** devolver una PDF por buckets en vez de un punto es elegir modelar incertidumbre, como cuando una esperanza puntual no basta (conecta con [[arena-q1]]).

Moraleja de la arista: *elige la representación por la pregunta —hashing para robustez barata, embeddings para similitud, reframing para alinear la salida con el negocio—; subir buckets no vence al cumpleaños.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Categórica enorme / cold-start | Hashed Feature (hash de huella + módulo) |
| Importa la similitud entre ítems | Embeddings (denso, aprendido) |
| Modelo lineal, relación no lineal | Feature Cross |
| Salida incierta/bimodal | Reframing: regresión → clasificación (PDF) |
| Optimizo clicks pero quiero valor real | Reframing: clasificación → regresión |
| Un ejemplo con varias etiquetas | Multilabel: sigmoid + multi-hot + umbral |

---

> **Síntesis:** La **entrada** se representa con **Hashed Feature** (alta cardinalidad/cold-start, aceptando colisiones), **Embeddings** (denso y aprendido, preserva similitud), **Feature Cross** (no linealidad para modelos simples) y **Multimodal Input**. La **salida** se reencuadra con **Reframing** (regresión↔clasificación, según incertidumbre y alineación con el negocio) y **Multilabel** (sigmoid + multi-hot, distinto del softmax de multiclase).

---

*Retrieval: (1) ¿qué tres problemas resuelve Hashed Feature y por qué hash de huella?; (2) embedding vs one-hot; (3) ¿cuándo reformular regresión↔clasificación?; (4) sigmoid vs softmax y por qué.*
