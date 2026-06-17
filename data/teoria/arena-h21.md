# The Mixtape III: variables instrumentales y regresión discontinua

> Diseños que rompen la dependencia del **CIA** (supuesto-seleccion-en-observables-cia) con variación **como-si exógena**.

## De qué trata esta lección (y qué sabrás hacer al final)

¿Y si no mediste todos los confundidores —ni puedes? Esta lección construye, desde cero, los dos diseños que estiman efectos causales **sin** depender del CIA, aprovechando variación "como-si aleatoria" que el mundo regala: la **variable instrumental** (2SLS) y la **regresión discontinua** (RDD). La idea unificadora: ambos cambian el supuesto incómodo ("medí los confundidores") por otro más defendible (un instrumento limpio, o un umbral que nadie manipula), a cambio de un efecto **local**.

Al terminar podrás: (1) ejecutar las dos etapas de 2SLS y verificar sus tres condiciones (relevancia, exclusión, independencia); (2) reconocer un instrumento débil (F<10) y por qué es peligroso; (3) distinguir RDD sharp de fuzzy y leer el salto en el cutoff; y (4) saber qué detecta el test de McCrary. El estimador de Wald entra por un ejemplo numérico. Es la salida cuando el CIA de [[arena-h20]] no es creíble.

## Variables instrumentales (2SLS)

Para un tratamiento **endógeno** (confundidor no medido o causalidad inversa), un **instrumento Z** aporta variación exógena. Ver variable-instrumental.

**2SLS:** (1ª etapa) D ~ Z → D̂ (parte de D movida solo por Z); (2ª etapa) Y ~ D̂. Tres condiciones:
- **Relevancia** (Z→D, testeable en la 1ª etapa).
- **Exclusión** (Z afecta Y solo vía D).
- **Independencia** (Z como-si aleatorio respecto a confundidores).

Bajo **monotonicidad** (sin defiers) estima el **LATE** (efecto en los **compliers**, no ATE). **Instrumentos débiles** (relevancia baja) amplifican sesgo y varianza → exige **F>10** en la 1ª etapa. La **forma reducida** (Y~Z) es diagnóstico: IV ≈ (Y~Z)/(D~Z). Ver instrumentos-debiles-2sls.

## Regresión discontinua (RDD)

El tratamiento se asigna por un **umbral** (cutoff) en una **running variable**. Las unidades justo arriba/abajo son comparables (**aleatorización local**) → el **salto** en E[Y] en el cutoff es el efecto. Ver regresion-discontinua-rdd.

- **Sharp:** cruzar el umbral **determina** el tratamiento (0→1); efecto = salto en Y.
- **Fuzzy:** cambia la **probabilidad** de tratamiento → se estima por **IV** (cutoff como instrumento); LATE en el umbral.

**Supuestos/diagnósticos:** **no manipulación** (test de densidad de **McCrary**: sin bunching en el cutoff), **continuidad** de potenciales y covariables (placebo de covariables, cutoffs falsos), **bandwidth** (sesgo↔varianza) y **polinomios locales** de bajo grado (no globales de alto grado). Efecto **local** al umbral. Ventaja sobre matching: **no exige CIA** (cubre confundidores no observados).

Ejemplos: **Medicare a los 65** (Card et al.), **regla de Maimónides** para tamaño de clase (Angrist-Lavy).

---

## Mini-ejemplo trabajado: el estimador de Wald a mano

Un email aleatorio Z anima a usar una app de ahorro (tratamiento D); quieres el efecto de *usar la app* sobre el saldo Y, pero quién la usa es endógeno (los ahorradores la usan más). Datos:

- **Forma reducida** (efecto del email sobre Y): E[Y|Z=1] − E[Y|Z=0] = \$120 − \$100 = **+\$20**.
- **Primera etapa** (efecto del email sobre el uso): E[D|Z=1] − E[D|Z=0] = 0.50 − 0.10 = **+0.40**.

**IV (Wald)** = 20 / 0.40 = **+\$50**. El email subió el saldo \$20 *en promedio*, pero solo el 40% extra empezó a usar la app por el email; el efecto **sobre esos compliers** es 20/0.40 = \$50. No es el ATE: es el LATE de quienes el email movió.

**Predicción antes de seguir:** si la primera etapa fuera floja (0.50 − 0.45 = 0.05, instrumento débil), ¿qué pasa con el IV? 20/0.05 = \$400, y un error mínimo en el numerador se amplifica ×20 → estimación inestable. Por eso se exige **F>10**.

## Prototipo, contraejemplo y caso borde

- **Prototipo (RDD sharp):** un umbral que *determina* el tratamiento (Medicare a los 65) → el salto en Y en el cutoff es el efecto, sin necesitar CIA.
- **Contraejemplo (exclusión violada):** un "instrumento" que afecta Y por otra vía — el email también recuerda al usuario revisar gastos (efecto directo sobre el saldo). Deja de ser válido aunque la primera etapa sea fuerte.
- **Caso borde (RDD con manipulación):** si la gente puede colocarse justo encima del corte (amontonamiento), la comparación local se rompe → el test de **McCrary** lo detecta.

## Errores típicos

- **Conceptual:** reportar el IV/RDD-fuzzy como ATE cuando es un **LATE** (compliers / efecto local al umbral).
- **Técnico:** ignorar la fuerza del instrumento (F<10) o ajustar la RDD con polinomios globales de alto grado en vez de locales.
- **De supuestos:** no chequear exclusión (IV) ni no-manipulación/continuidad (RDD).

## Transferencia isomorfa

IV y RDD son experimentos naturales que reaparecen en producto y finanzas:

- **Encouragement design ↔ IV:** un empujón aleatorio (notificación que sube la adopción) es un instrumento; el análisis intent-to-treat / complier es 2SLS aplicado a un experimento (conecta con [[arena-ads4]], A/B testing).
- **RDD ↔ umbrales de producto:** "envío gratis por compras > \$50" o "tier premium a partir de X puntos" crean un corte que funciona como experimento natural sobre el comportamiento.
- **Instrumento débil ↔ experimento sin potencia:** una primera etapa floja es el gemelo de un A/B con efecto diminuto y mucho ruido — los IC se vuelven inútiles.

Moraleja de la arista: *IV y RDD compran causalidad sin medir los confundidores, a cambio de un efecto local (compliers/umbral) y de instrumentos que deben ser fuertes y limpios.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Tratamiento endógeno + instrumento creíble | IV/2SLS (relevancia/exclusión/independencia) |
| Primera etapa floja | Instrumento débil (F>10); IC inestables |
| Efecto IV/RDD fuzzy | Es un LATE (compliers/umbral), no ATE |
| Tratamiento por un corte en una variable | RDD (salto en el cutoff) |
| ¿Pueden manipular la running variable? | Test de McCrary (densidad) |
| Especificar la RDD | Bandwidth + polinomio local, no global |

---

> **Síntesis:** **IV/2SLS** usa un instrumento (relevancia+exclusión+independencia) para extraer variación exógena del tratamiento endógeno; bajo monotonicidad estima el **LATE** y exige instrumentos fuertes (**F>10**). **RDD** explota un umbral (aleatorización local): **sharp** (determinista) o **fuzzy** (probabilidad→IV), con diagnósticos de **no manipulación (McCrary)**, continuidad y bandwidth/polinomio local. Ambos identifican **sin CIA**, a costa de un efecto **local**.

---

*Retrieval: (1) las dos etapas de 2SLS y las 3 condiciones; (2) ¿qué es un instrumento débil?; (3) RDD sharp vs fuzzy; (4) ¿qué detecta el test de McCrary?*
