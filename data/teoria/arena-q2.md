# Bayes, tasas base y señales ruidosas

## El error más caro en data science

Antes de calcular el rendimiento de un modelo, pregunta siempre: **¿cuál es la prevalencia?**

Sin ella, la sensibilidad y la especificidad no te dicen si tu modelo es útil en producción.

---

## El teorema de Bayes aplicado a tests

Un test diagnóstico (o modelo de clasificación) tiene dos parámetros fundamentales:

- **Sensibilidad** = P(test positivo | condición presente) = P(+|E)
- **Especificidad** = P(test negativo | condición ausente) = P(-|¬E)

Lo que interesa en producción es el inverso:

- **VPP** (Valor Predictivo Positivo) = P(condición presente | test positivo) = P(E|+)
- **VPN** (Valor Predictivo Negativo) = P(condición ausente | test negativo) = P(¬E|-)

Por Bayes:

$$P(E|+) = \frac{P(+|E) \cdot P(E)}{P(+)}$$

donde el denominador es:

$$P(+) = \underbrace{P(+|E) \cdot P(E)}_{\text{verdaderos positivos}} + \underbrace{P(+|\neg E) \cdot P(\neg E)}_{\text{falsos positivos}}$$

---

## La tabla de contingencia: mejor que la fórmula

Para $N = 10\,000$ personas con prevalencia = 1%, sensibilidad = 90%, especificidad = 95%:

|                | Condición presente | Condición ausente | Total |
|----------------|-------------------|-------------------|-------|
| Test positivo  | 90 (VP)           | 495 (FP)          | 585   |
| Test negativo  | 10 (FN)           | 9405 (VN)         | 9415  |
| **Total**      | 100               | 9900              | 10000 |

$$\text{VPP} = \frac{90}{90 + 495} = \frac{90}{585} \approx 15.4\%$$

Con 90% de sensibilidad y 95% de especificidad, **solo 1 de cada 6 alertas es real** cuando la prevalencia es 1%.

---

## Por qué la prevalencia domina

El VPP depende críticamente de la prevalencia. Con mismos parámetros del test:

| Prevalencia | VPP   |
|-------------|-------|
| 0.1%        | 1.8%  |
| 1%          | 15.4% |
| 5%          | 48.6% |
| 10%         | 66.7% |
| 50%         | 94.7% |

Cuando la condición es rara, la mayoría de los positivos son falsos aunque el test sea bueno.

**Consecuencia práctica:** para aumentar el VPP sin cambiar el test, se subsegmenta la población (subir la prevalencia efectiva dentro del segmento aplicado).

---

## El Likelihood Ratio: una forma más ágil

El Likelihood Ratio positivo:

$$LR^+ = \frac{\text{sensibilidad}}{1 - \text{especificidad}} = \frac{P(+|E)}{P(+|\neg E)}$$

La regla de actualización en odds:

$$\text{odds posteriores} = LR^+ \times \text{odds previos}$$

donde los odds previos son $\frac{P(E)}{1-P(E)}$.

**Ventaja:** se puede encadenar para tests múltiples independientes: multiplica los $LR^+$ de cada test.

Para convertir odds de vuelta a probabilidad: $P = \frac{\text{odds}}{1 + \text{odds}}$.

---

## Caso de entrevista: modelo de fraude

Un modelo de detección de fraude tiene sensibilidad 97% y especificidad 99.8%. La tasa de fraude real en producción es 0.2%.

Tabla para $N = 1\,000\,000$:
- Condición presente: 2000 (fraudes)
- VP = 0.97 × 2000 = 1940
- FP = (1 - 0.998) × 998000 = 0.002 × 998000 = 1996

$$\text{VPP} = \frac{1940}{1940 + 1996} = \frac{1940}{3936} \approx 49.3\%$$

Con un modelo excelente (99.8% de especificidad), **la mitad de las alertas son falsas** en producción.

La única forma de mejorar esto sustancialmente sin cambiar el modelo: aplicarlo a segmentos de mayor riesgo (subir la prevalencia efectiva).

---

## Comunicar el resultado a no-estadísticos

Un resultado útil no es solo "VPP = 49%". Es:

*"De cada 100 transacciones que el modelo marca como fraude, aproximadamente 49 son fraude real y 51 son legítimas. El 51% de las alertas consumirá tiempo del equipo de revisión sin resultado. Podemos subir esta proporción si nos enfocamos en los segmentos de mayor riesgo."*

---

## Prototipo, contraejemplo y caso borde

- **Prototipo:** test bueno (sens 90%, esp 95%) sobre condición rara (prev 1%) → VPP bajo (~15%). La tabla de contingencia lo revela de inmediato: los falsos positivos nacen de una base enorme de sanos.
- **Contraejemplo (la trampa del backtest balanceado):** mides el modelo en un set 50/50 y obtienes "precisión 92%". En producción la prevalencia es 0.2% y la precisión real (VPP) colapsa. *El balance artificial es un cambio de tasa base disfrazado de métrica.*
- **Caso borde (prevalencia → 0):** por buena que sea la especificidad, si la condición casi no existe, casi todo positivo es falso. El límite VPP→0 cuando prev→0 con esp<100% es la prueba de que **ninguna calidad de test salva a una base demasiado rara**; solo subir la prevalencia efectiva (segmentar) lo hace.

## Errores típicos

- **Conceptual:** confundir sensibilidad P(+|E) con VPP P(E|+) — invertir el condicional. Es el mismo error que leer P(datos|H₀) como P(H₀|datos).
- **Técnico:** olvidar el segundo sumando del denominador (los falsos positivos P(+|¬E)·P(¬E)); sin él, el VPP sale inflado.
- **De supuestos:** reportar precisión de un set balanceado como si fuera la de producción, sin declarar la prevalencia real.

## Transferencia isomorfa

La estructura "una señal ruidosa contra una base abrumadora" reaparece en todo dominio donde hay clases desbalanceadas:

- **VPP ↔ precision de un clasificador:** el VPP *es* la precision en ML; un modelo de fraude con AUC alta puede tener precision baja en producción por la misma tasa base (conecta con [[arena-htd4]], donde el *prediction bias* y el desbalance distorsionan la métrica online).
- **LR⁺ encadenado ↔ Bayes secuencial:** multiplicar likelihood ratios de tests independientes es exactamente actualizar odds tras cada cara observada en la moneda de dos caras (conecta con [[arena-q4]], moneda 999+1).
- **Odds ratio ↔ hazard ratio de Cox:** el LR⁺ vive en el mundo de los odds; el mismo gesto multiplicativo aparece al combinar riesgos en [[arena-h8]].
- **Tasa base clínica ↔ alerta de fraude ↔ trading signal:** "1 de cada 6 alertas es real" es el mismo PPV que en cribado médico (conecta con [[arena-h13]]).

Moraleja de la arista: *una señal nunca habla sola; siempre discute con la tasa base, y cuando la base es rara, la base gana.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "El modelo tiene X% de precisión" | Pregunta: ¿en qué distribución? ¿Cuál es la prevalencia en producción? |
| "Precisión en backtesting balanceado" | No es VPP real: el balance artificial infla la precisión percibida |
| "¿Es bueno este test?" | Crea la tabla de contingencia con la prevalencia real |
| "¿Cómo mejoramos el VPP?" | Dos opciones: mejor especificidad, o aplicar el test a subpoblación con mayor prevalencia |

---

## Ejercicio de consolidación

Un modelo de NLP detecta reseñas falsas. Sensibilidad 85%, especificidad 92%. En una plataforma grande, 3% de las reseñas son falsas.

Calcula el VPP antes de leer la solución.

*Respuesta: N=10000: 300 falsas → 255 VP. 9700 reales → 776 FP. VPP = 255/(255+776) ≈ 24.7%. Solo 1 de 4 alertas es una reseña falsa real.*
