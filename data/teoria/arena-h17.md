# La causalidad según Pearl III: do-operator, back-door, front-door y do-calculus

## El do-operator (ver vs hacer)

- **P(Y|X=x)** = OBSERVAR: distribución de Y entre quienes *se ven* con X=x (peldaño 1, puede estar confundida).
- **P(Y|do(X=x))** = INTERVENIR: distribución de Y si *forzáramos* X=x en todos (peldaño 2, efecto causal).

Intervenir do(x) = **borrar las flechas que entran a X** y fijarlo (grafo "mutilado"), igual que la **aleatorización**. Confundir ambas es "correlación = causación". Ver [[do-operator-intervencion]].

## Identificación: las rutas para subir a Mount Intervention

**Identificar** = expresar P(Y|do(x)) con cantidades **observacionales** (sin do) usando el grafo.

1. **Back-door adjustment:** si Z cierra todos los caminos traseros (y no es descendiente de X), P(Y|do(x)) = Σ_z P(Y|x,z)P(z) (estandarización). Ver [[confundimiento-backdoor]].
2. **Front-door:** si un **mediador M** capta TODO el efecto X→M→Y, sin backdoors abiertos X-M y con M-Y bloqueado por X, se identifica el efecto **aunque el confundidor X-Y no esté medido**. Ejemplo: tabaco→alquitrán→cáncer con gen confundidor no observado. Ver [[criterio-puerta-delantera]].
3. **Variables instrumentales:** ante confundidor no medido, un instrumento válido (afecta X, solo influye en Y vía X). Caso histórico: el agua de **Dr. Snow** (cólera) como instrumento natural.
4. **do-calculus:** 3 reglas que eliminan do() usando el grafo; es **completo** — si el efecto es identificable, encuentra la fórmula; si no, lo demuestra. Back-door y front-door son **casos particulares**. Ver [[do-calculus]].

Si un efecto **no es identificable**, ni con datos infinitos se obtiene: faltan supuestos/variables o un experimento.

---

## Mini-ejemplo trabajado: back-door a mano

Un fármaco D y la recuperación Y, con la **edad Z** confundiendo (los viejos reciben más el fármaco *y* se recuperan menos). Tablas inventadas con números simples:

- Entre **jóvenes** (Z=joven): con fármaco se recupera el 80%; sin fármaco, el 70%. Efecto = +10 pp.
- Entre **viejos** (Z=viejo): con fármaco se recupera el 50%; sin fármaco, el 40%. Efecto = +10 pp.

Dentro de cada estrato de edad el fármaco ayuda +10 pp. Pero si **no** ajustas por edad, como los viejos (peor pronóstico) toman más el fármaco, la tasa cruda *del grupo tratado* puede salir **igual o peor** que la del no tratado: nace la paradoja de Simpson. La fórmula back-door P(Y|do(D)) = Σ_z P(Y|D,z)P(z) simplemente promedia el +10 pp de cada estrato **ponderando por cuántos hay de cada edad**, en lugar de por cuántos tratados hay. Ese cambio de ponderación *es* la corrección causal.

**Predicción antes de seguir:** si en vez de promediar por P(z) (la población) promediaras por P(z|D=1) (solo los tratados), ¿qué efecto estimarías? Respuesta: el ATT en vez del ATE; coinciden aquí porque el efecto es +10 pp homogéneo, pero divergen si el efecto varía con la edad.

## Prototipo, contraejemplo y caso borde

- **Prototipo (back-door correcto):** Z=edad es causa común de D y de Y, y la mides → ajustas y el sesgo desaparece.
- **Contraejemplo (ajustar de más sesga):** Z es un **collider** (D→Z←Y) o un **mediador** (D→Z→Y). Ajustar por un collider *abre* un camino espurio; ajustar por un mediador *borra* parte del efecto que querías medir. "Ajustemos por todo" es un error, no una precaución.
- **Caso borde (front-door):** el confundidor X→D y X→Y **no se mide**, pero existe un mediador M que capta todo el efecto D→M→Y. Aún sin medir X, el efecto se identifica. Es el borde que demuestra que "no medí el confundidor" no siempre es fatal.

## Errores típicos

- **Conceptual:** leer P(Y|D) (observar) como si fuera P(Y|do(D)) (intervenir) — el corazón de "correlación = causación".
- **De supuestos:** creer que más covariables = más rigor. El conjunto de ajuste lo decide **el grafo**, no la disponibilidad de datos.
- **Técnico:** ponderar la estandarización por P(z|D=1) cuando quieres el ATE poblacional (P(z)), o viceversa.

## Transferencia isomorfa

El do-operator no es solo de epidemiología; es la estructura de "intervenir vs observar" en cualquier dominio:

- **A/B test ↔ do(x):** aleatorizar el tratamiento en un experimento *es* borrar las flechas que entran a D — por eso el A/B test estima P(Y|do(D)) sin ajustar. Cuando no puedes aleatorizar (observacional), recuperas el back-door (conecta con [[arena-ads4]], A/B testing).
- **Data leakage ↔ ajustar por un collider:** incluir en un modelo una feature *posterior* al outcome (que ambos causan) infla el desempeño igual que ajustar por un collider infla una asociación espuria. El leakage es un collider disfrazado de feature (conecta con [[arena-dmls1]] y la regla "evitar leakage").
- **Selección de muestra ↔ condicionar en un collider:** filtrar la cohorte por una variable que el tratamiento y el resultado afectan (p. ej., "solo pacientes hospitalizados") abre el mismo sesgo de colisión.

Moraleja de la arista: *aleatorizar, evitar leakage y elegir bien la muestra son el mismo gesto causal — controlar qué flechas entran a la variable que te importa.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Efecto de actuar, no de observar? | Plantéalo como P(Y\|do(x)) |
| Confundidores **medidos** | Back-door adjustment (estandarización) |
| Confundidor **no medido** + mediador | Front-door |
| Confundidor no medido + instrumento | Variable instrumental |
| Grafo complejo, ¿identificable? | do-calculus (decide y da la fórmula) |
| "Ajustemos por todo" | No: colliders/mediadores sesgan; decide el grafo |

---

> **Síntesis:** el **do-operator** separa ver de hacer (do(x) = borrar flechas hacia X). **Identificar** un efecto es traducir P(Y|do(x)) a datos observacionales vía el grafo: **back-door** (ajuste por confundidores medidos), **front-door** (mediador que capta todo el efecto, sin medir el confundidor), **instrumentos** y, en general, el **do-calculus** (completo). Si no es identificable, ningún volumen de datos basta.

---

*Retrieval: (1) P(Y|X) vs P(Y|do(X)); (2) ¿qué le hace do() al grafo?; (3) ¿cuándo usar front-door y sus condiciones?; (4) ¿qué garantiza el do-calculus?*
