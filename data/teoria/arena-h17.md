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
