# El principio del palomar

*Lección redactada para CogitoErgoSum a partir de la sección 3.3 de Zeitz (The Pigeonhole Principle). Cubre el contenido completo de la unidad.*

## Las dos versiones

**Palomar básico:** si colocas **más palomas que casilleros** (n+1 palomas en n casilleros), algún casillero recibe **al menos dos** palomas.

**Versión fuerte:** si colocas n objetos en k cajas, alguna caja recibe **al menos ⌈n/k⌉** objetos (el techo de n/k). Ejemplo: 25 personas en 7 días de la semana → algún día cumple ⌈25/7⌉ = 4 o más.

Ambas se prueban en una línea (si todas las cajas tuvieran menos, el total no alcanza). El principio es **trivial**; ningún problema de palomar es difícil por el principio.

## La forma general de los problemas que resuelve

> «**Garantiza que existen dos** (o k) objetos **con la misma propiedad** / suficientemente cercanos / cuya diferencia cumple tal cosa.»

Palabras como *garantiza*, *siempre*, *al menos dos*, *forzosamente* en un contexto de existencia son el grito del palomar. La conclusión típica es de existencia pura: no sabrás *cuáles* dos objetos, solo que los hay.

## El verdadero trabajo: diseñar las cajas

El problema **nunca te da las cajas** — te da palomas (los objetos) y una conclusión deseada. Diseñar la partición correcta del espacio es todo el arte. Una **buena caja** cumple tres requisitos:

1. **Las cajas agotan todos los casos**: todo objeto cae en alguna (es una partición legítima del espacio de posibilidades).
2. **Hay pocas cajas** — estrictamente menos que objetos (si no, el principio no dispara).
3. **Dos objetos en la misma caja fuerzan EXACTAMENTE la conclusión pedida**: la caja está diseñada de modo que compartirla signifique «misma propiedad» o «suficientemente cerca».

El flujo de trabajo: lee la conclusión deseada («dos a distancia ≤ √2», «dos cuya diferencia es múltiplo de 7») y pregunta: *¿qué tendrían que compartir dos objetos para que eso sea automático?* Esa respuesta define la caja; luego cuenta cuántas cajas salen y verifica que sean menos que los objetos.

## Ejemplo resuelto: cinco puntos en el cuadrado

**Problema:** cinco puntos están dentro de un cuadrado de lado 2. Demuestra que hay dos a distancia ≤ √2.

**Diseño de cajas:** quiero que «compartir caja» fuerce «distancia ≤ √2». Un cuadradito de lado 1 tiene diagonal √2 — dos puntos dentro de él jamás distan más que eso. **Parte el cuadrado de lado 2 en cuatro cuadraditos de lado 1** (la cuadrícula 2×2). Son 4 cajas que agotan el cuadrado, y tengo 5 puntos: dos caen en el mismo cuadradito, y por la diagonal distan ≤ √2. ∎

Verifica los tres requisitos: agotan (✓, cuadrícula), pocas (4 < 5 ✓), compartir fuerza la conclusión (✓, diagonal). Así se ve un palomar bien armado.

## Ejemplos del repertorio clásico

- **Diferencia divisible:** entre cualesquiera n+1 enteros hay dos cuya diferencia es múltiplo de n. Cajas = los n **residuos módulo n**; dos números con el mismo residuo difieren en un múltiplo. (Las cajas aritméticas casi siempre son residuos.)
- **Conocidos en una fiesta:** entre n personas (n ≥ 2) siempre hay dos con el mismo número de conocidos. Cajas = números posibles de conocidos {0, …, n−1}… que parecen n cajas para n personas. **Refinamiento típico:** 0 y n−1 **se excluyen mutuamente** (no puede haber a la vez alguien que no conoce a nadie y alguien que conoce a todos), así que solo n−1 valores son simultáneamente posibles — y el palomar dispara. Este truco (algunos valores de caja incompatibles entre sí reducen las cajas reales) reaparece constantemente.
- **Subconjunto con suma fija, sucesiones, decimales periódicos:** los residuos de potencias, las sumas parciales módulo n («de n enteros, algunos consecutivos suman múltiplo de n»: cajas = residuos de las sumas parciales) — el palomar es el motor existencial de la teoría de números elemental.

## El primer movimiento al sospechar palomar

1. Identifica las **palomas** (¿qué objetos hay que comparar?) y cuéntalas.
2. Lee la conclusión y pregunta qué deberían **compartir** dos objetos para forzarla.
3. Diseña las cajas con esa propiedad; cuéntalas.
4. ¿Palomas > cajas? Dispara. ¿No alcanza? Refina: cajas más gruesas, o busca valores incompatibles que reduzcan cajas, o usa la versión fuerte.

## Errores comunes

- Cajas que **no agotan** los casos (un objeto sin caja invalida todo).
- Cajas tales que compartirlas **no** implica la conclusión (palomar dispara… hacia nada).
- Olvidar la versión fuerte cuando piden «al menos k» con k > 2.

## Síntesis

> **Chunk mínimo:** n+1 palomas en n casilleros ⇒ dos comparten; versión fuerte: n objetos en k cajas ⇒ alguna recibe ⌈n/k⌉. El principio es trivial; TODO el arte es diseñar las cajas: deben (1) agotar los casos, (2) ser menos que los objetos, (3) hacer que compartir caja fuerce EXACTAMENTE la conclusión. Flujo: lee la conclusión → ¿qué compartirían dos objetos para forzarla? → esa es la caja. Clásicos: 5 puntos en cuadrado de lado 2 → cuadrícula 2×2, diagonal √2; diferencias divisibles → cajas = residuos mod n; conocidos en la fiesta → 0 y n−1 incompatibles reducen las cajas. Gatillo verbal: «garantiza / siempre / al menos dos».

---

*Antes del quiz: reconstruye de memoria las dos versiones, la forma general de los enunciados que lo piden, los tres requisitos de una buena caja y la solución completa de los cinco puntos.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El palomar es conteo con tension: demasiados objetos para pocas cajas. Su hogar natural esta en [[arena-b1]] (conteo y probabilidad), se vuelve tecnica de competencia en [[aime-cnt]], y aparece como criterio de imposibilidad junto a biyecciones y particiones en [[zeitz-62]].
<!-- GRAFO_CONEXO_OLEADA3_END -->
