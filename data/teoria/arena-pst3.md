# Experimentos estadísticos: A/B tests y tests de permutación

## De qué trata esta lección (y qué sabrás hacer al final)

La página B convirtió 50% y la A 30%. ¿La B es mejor, o es suerte con 10 usuarios por grupo? Esta lección construye, desde cero, cómo responder esa pregunta **sin fórmulas**: el **test de permutación**, que materializa la hipótesis nula barajando las etiquetas de grupo y mide si la diferencia observada es de las que el azar produce con facilidad. Es la forma más intuitiva de entender qué es un p-valor: no se deriva, se **fabrica**.

Al terminar podrás: (1) montar un A/B test y plantear su H0; (2) ejecutar un test de permutación y leer su p-valor como una fracción de barajadas; (3) razonar errores tipo I/II, potencia y tamaño del efecto; y (4) reconocer el enemigo número uno del data scientist —la **multiplicidad** (probar demasiado garantiza falsos positivos)— y su antídoto, el holdout. Cada idea entra por su intuición; no hace falta teoría previa de tests.

> Comparte raíz con la teoría de tests óptimos ([[arena-cb3]]) y con los IC/p-valor clásicos ([[arena-dg3]]), pero por la vía del remuestreo.

## El A/B test y la hipótesis nula

Un **A/B test** compara dos (o más) tratamientos —página A vs B, fármaco vs placebo— asignando sujetos **al azar** a cada grupo y midiendo una métrica. La **hipótesis nula (H0)** dice que no hay diferencia: cualquier discrepancia observada es producto del azar. El objetivo es reunir evidencia para **rechazarla**.

Conviene elegir bien la métrica: a veces se usa una **variable proxy** (p.ej. tiempo en página como sustituto de "comprará") cuando la verdadera es cara o lenta de medir.

## El test de permutación: significancia por remuestreo

En lugar de fórmulas, se puede contestar "¿es real esta diferencia o es azar?" **barajando los datos**. El test de permutación encarna literalmente la H0 (que los grupos son intercambiables):

1. **Combina** los resultados de todos los grupos en un solo conjunto.
2. **Baraja** y reparte, **sin reemplazo**, un remuestreo del tamaño del grupo A; del resto, uno del tamaño de B (y C, D…).
3. Calcula el **estadístico** de interés (p.ej. diferencia de medias) para esos grupos barajados → una iteración.
4. Repite **R** veces → la **distribución de permutación** del estadístico.
5. Compara la **diferencia observada** con esa distribución.

**Conclusión:** si la diferencia observada cae **dentro** del grueso de las permutaciones, el azar podría explicarla (no significativa). Si cae **fuera** de casi todas, el azar no la explica → **estadísticamente significativa**.

Ventaja: no asume normalidad ni tamaños de grupo iguales; sirve para datos numéricos o binarios. Variantes: permutación **exhaustiva** (todas las divisiones posibles, solo para n chico) y **bootstrap** (muestreando con reemplazo).

## p-valor y significancia

El **p-valor** es la probabilidad de observar un resultado **tan o más extremo** que el real **suponiendo H0 cierta**. En el test de permutación es directamente la fracción de permutaciones cuyo estadístico iguala o supera al observado. No es la probabilidad de que H0 sea cierta. El umbral α (típico 0.05) es la tasa de falsos positivos que se está dispuesto a tolerar.

## Errores, potencia y tamaño de muestra

- **Error Tipo I:** declarar real un efecto que es azar (falso positivo, prob. α).
- **Error Tipo II:** no detectar un efecto real (falso negativo, prob. β).
- **Tamaño del efecto (effect size):** la magnitud mínima de diferencia que quieres poder detectar.
- **Potencia:** probabilidad de detectar un efecto dado, con un tamaño de muestra dado = 1−β. Más n → más potencia; efectos más pequeños exigen más n.

## El peligro de la multiplicidad

Si pruebas **muchas** comparaciones, subgrupos, variables o modelos, **algo saldrá "significativo" por puro azar** ("si torturas los datos lo suficiente, confiesan"). Es la causa de muchos resultados irreproducibles. Para el data scientist:

- En **modelado predictivo**, el antídoto es la **validación cruzada** y un **holdout** etiquetado: si el efecto era ilusorio, no sobrevive en datos no vistos.
- Sin holdout, hay que ser consciente de que cuanto más consultas los datos, más manda el azar, y usar **remuestreo/simulación** como benchmark del azar.
- La **False Discovery Rate (FDR)** y ajustes como **Bonferroni** controlan la tasa de descubrimientos falsos, aunque para el DS suelen ser demasiado rígidos frente al holdout.

## Otras pruebas

- **ANOVA:** generaliza la comparación a **más de dos grupos** (¿difiere alguno?); su versión por remuestreo baraja entre todos los grupos.
- **Chi-cuadrado:** prueba diferencias entre **conteos/proporciones categóricas** (tablas de frecuencias observadas vs esperadas).

---

## Mini-ejemplo trabajado: test de permutación a mano

Página A convierte 3/10 (30%), página B 5/10 (50%). Diferencia observada = 20 pp. ¿Real o azar? La H0 dice que las dos páginas son **intercambiables**, así que el grupo no debería importar:

1. Junta los 20 usuarios (8 conversiones, 12 no) en una sola urna.
2. Baraja y reparte 10 al "grupo A" y 10 al "B", **sin reemplazo**.
3. Calcula la diferencia de tasas de esa repartición aleatoria → una iteración.
4. Repite R=10 000 veces → la distribución de diferencias *bajo puro azar*.
5. El **p-valor** es la fracción de permutaciones con diferencia ≥ 20 pp.

Si, digamos, el 18% de las permutaciones alcanzan ±20 pp, p≈0.18: el azar explica fácilmente la diferencia → **no significativa** (con n=10 por grupo casi nada lo es).

**Predicción antes de seguir:** ¿por qué barajar etiquetas encarna exactamente la H0? Respuesta: porque si A y B no difieren, la etiqueta "A/B" es solo un *post-it* intercambiable; la distribución de diferencias que generas al rebarajar es literalmente "qué tan grande sería la diferencia si el grupo no significara nada". El test no asume una fórmula: *construye* el azar.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "¿la diferencia A vs B es real?" → permutación (baraja etiquetas, R veces, compara) sin asumir normalidad.
- **Contraejemplo (multiplicidad):** prueba 20 subgrupos y ~1 saldrá "significativo" a α=0.05 por puro azar; reportar solo ese es el "vast search effect". El antídoto del DS es un holdout / validación cruzada.
- **Caso borde (proxy mal elegido):** optimizar "tiempo en página" como sustituto de "compra" puede subir el proxy y bajar la venta si no están bien alineados. El borde recuerda validar la métrica subrogada.

## Errores típicos

- **Conceptual:** leer el p-valor como P(H0 cierta); es P(diferencia tan extrema | H0).
- **Técnico:** parar el experimento en cuanto cruza p<0.05 (peeking): mirar repetidamente infla el error tipo I igual que la multiplicidad.
- **De supuestos:** dimensionar el test sin potencia y concluir "no hay efecto" cuando solo faltó n (error tipo II por baja potencia).

## Transferencia isomorfa

- **Test de permutación ↔ p-valor de Neyman-Pearson:** ambos preguntan "¿qué tan extremo es esto bajo H0?"; la permutación construye la distribución nula empíricamente en vez de derivarla (conecta con [[arena-cb3]] y [[arena-dg3]]).
- **H0 "grupos intercambiables" ↔ aleatorización / do-operator:** asignar al azar es lo que vuelve las etiquetas intercambiables y estima un efecto causal sin confundidores (conecta con [[arena-h17]]).
- **Multiplicidad / peeking ↔ monitoreo de muchas señales:** vigilar muchas métricas garantiza falsas alarmas; el control es el mismo (FDR/Bonferroni o holdout) que en observabilidad (conecta con [[arena-obs1]]).
- **Potencia / tamaño del efecto ↔ MDE de un rollout:** fijar el efecto mínimo detectable antes de lanzar es diseñar el experimento de despliegue (conecta con [[arena-dmls3]]).

Moraleja de la arista: *barajar las etiquetas materializa la H0 y fabrica el azar; lo difícil no es el test, es no engañarte probando demasiado (multiplicidad y peeking).*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿La diferencia A vs B es real o azar?" | Test de permutación: baraja, reparte, compara R veces |
| "No quiero asumir normalidad" | Permutación / bootstrap en vez de t-test |
| "La métrica verdadera es cara/lenta de medir" | Variable proxy (valida su asociación) |
| "¿Cuántos usuarios necesito en el test?" | Potencia: fija efecto, α y β → despeja n |
| "Probé 20 subgrupos y uno salió significativo" | Multiplicidad → holdout / cross-validation / FDR |
| "Comparar más de dos grupos" | ANOVA (o permutación entre grupos) |
| "Diferencias entre proporciones por categoría" | Chi-cuadrado |

---

> **Síntesis:** Un A/B test asigna sujetos al azar y plantea una H0 de "no hay diferencia". El **test de permutación** la evalúa sin fórmulas: combina los grupos, los baraja R veces y mira si la diferencia observada queda dentro (azar) o fuera (significativa) de la distribución permutada — sin asumir normalidad. El **p-valor** es P(resultado tan extremo \| H0). Hay que dimensionar el experimento por **potencia** (efecto, α, β, n) y, sobre todo, cuidarse de la **multiplicidad**: probar mucho garantiza falsos positivos, que se controlan con holdout/validación cruzada o ajustes tipo Bonferroni/FDR.

---

*Retrieval: cierra y responde: (1) enumera los pasos de un test de permutación; (2) ¿qué representa la H0 al combinar los grupos?; (3) define potencia y qué la aumenta; (4) ¿por qué la multiplicidad produce falsos positivos y cómo se controla en DS?*
