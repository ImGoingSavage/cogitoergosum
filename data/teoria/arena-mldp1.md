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
