# Cómo arrancar: orientación, manos sucias, penúltimo paso y pensamiento ilusorio

*Lección redactada para CogitoErgoSum a partir de la sección 2.2 de Zeitz (Strategies for Getting Started). Cubre el contenido completo de la unidad.*

## El problema de la página en blanco

«No sé por dónde empezar» es el estado natural ante un problema de verdad (si supieras, sería ejercicio). Esta sección convierte ese estado en un **plan de acción inmediato** con cuatro jugadas: orientarse, ensuciarse las manos, mirar el penúltimo paso y pensar ilusoriamente.

---

## 1. Orientación: el primer paso obligatorio

Antes de atacar, **oriéntate**. La orientación consiste en tres búsquedas:

1. **¿Qué se pide?** Identifica con precisión la incógnita o la afirmación a demostrar. Lee el enunciado **varias veces** — los problemas buenos esconden información en palabras que la primera lectura resbala.
2. **¿Qué tipo de problema es?** Clasifícalo aunque sea burdamente: ¿es de existencia («demuestra que hay…»), de conteo, de optimización («el mayor valor…»), de imposibilidad, de determinación? Cada tipo tiene formas de respuesta distintas.
3. **¿Qué forma tendría una respuesta?** Anticipa: ¿un número?, ¿una construcción?, ¿un argumento de imposibilidad? Saber qué forma buscas filtra qué caminos tienen sentido.

La orientación toma minutos y ahorra horas: gran parte de los atascos largos son problemas mal leídos.

## 2. Ensúciate las manos (get your hands dirty)

**Qué significa exactamente:** experimenta con **casos concretos y pequeños**. Calcula n = 1, 2, 3, 4 a mano. Tabula. Dibuja las primeras configuraciones. Juega algunas rondas del juego.

**Por qué le gana a quedarse pensando:** los datos generados a mano son la **materia prima de las conjeturas**. El patrón que necesitas casi nunca se ve en el enunciado abstracto; se ve en la tabla que tú fabricaste. Pensar sin datos es girar en seco; los casos pequeños le dan tracción a la intuición. Además, el acto físico de calcular rompe la parálisis (psicología de 2.1) y a menudo revela detalles del mecanismo del problema que ninguna contemplación encuentra.

Regla práctica: si llevas 5 minutos sin escribir nada, estás violando esta estrategia.

## 3. El penúltimo paso (penultimate step)

**Qué es:** en lugar de preguntar «¿qué hago primero?», pregunta:

> **¿Qué necesitaría tener justo ANTES del final?**

Esa cosa —el penúltimo paso— se convierte en tu **nueva meta**, más cercana que la original. Ejemplos del reflejo en acción:

- ¿Demostrar que un número es irracional? El penúltimo paso típico: una contradicción a partir de suponerlo p/q.
- ¿Demostrar que dos segmentos son iguales? Penúltimos pasos candidatos: triángulos congruentes que los contengan, o un círculo del que ambos sean radios.
- ¿Probar que un proceso termina? Penúltimo paso: un monovariante acotado.

Es la versión local de «trabajar hacia atrás» (Pólya): no hace falta construir toda la cadena hacia atrás; basta un eslabón para acercar la meta.

## 4. Pensamiento ilusorio (wishful thinking / make it easier)

**Qué es:** la estrategia descarada de **suponer que ya tienes lo que te falta** y estudiar las consecuencias. Sus dos formas típicas:

1. **«Supón que ya está resuelto.»** Imagina la solución terminada y pregunta qué propiedades tendría: ¿dónde estaría ese punto?, ¿qué forma tendría esa fórmula? Las propiedades de la solución imaginaria te dicen **dónde buscarla**. (Clásico en construcciones geométricas: dibuja la figura *ya construida* y analízala.)
2. **«Quita la restricción que estorba.»** ¿El problema sería fácil sin tal condición? Resuélvelo sin ella y luego pregunta cuánto cuesta reincorporarla. La versión relajada te enseña la estructura; la diferencia entre ambas versiones es exactamente la dificultad real del problema.

El pensamiento ilusorio no es autoengaño: es exploración con hipótesis prestadas, que se devuelven antes de escribir la solución final.

---

## El error clásico: confundir evidencia con demostración

Tras ensuciarte las manos dirás: «probé n = 1, 2, 3 y el patrón se cumple, así que queda demostrado». **Alto.** Lo que está bien: generar casos es exactamente el proceso correcto, y la conjetura que sale de ahí es oro. Lo que está mal: los casos **no demuestran** la afirmación general — solo la hacen plausible. Hay patrones que aguantan miles de casos y fallan después. El flujo completo es: casos → conjetura → **demostración** (inducción, argumento directo, contradicción… — las verás en §2.3). La tabla te dice *qué* es verdad; falta el argumento de *por qué*.

## Disparadores

- Página en blanco → orientación: qué se pide, qué tipo, qué forma tendría la respuesta.
- Enunciado abstracto, cero intuición → casos pequeños tabulados a mano.
- Meta clara pero lejana → ¿qué tendría justo antes del final?
- Una restricción hace todo difícil → quítala, resuelve, reincorpórala.
- «Ya quedó demostrado con 3 casos» → no: tienes conjetura, falta demostración.

## Síntesis

> **Chunk mínimo:** Cuatro jugadas contra la página en blanco: (1) **Orientación** — qué se pide, qué tipo de problema es (existencia/conteo/optimización/imposibilidad), qué forma tendría la respuesta; (2) **Ensúciate las manos** — casos pequeños tabulados a mano: son la materia prima de las conjeturas (5 min sin escribir = violación); (3) **Penúltimo paso** — ¿qué necesitaría tener justo ANTES del final? esa es tu nueva meta; (4) **Pensamiento ilusorio** — supón el problema ya resuelto y estudia qué propiedades tendría la solución, o quita la restricción que estorba y reincorpórala después. Y el alto obligatorio: los casos dan CONJETURA, no demostración.

---

*Antes del quiz: reconstruye de memoria las tres búsquedas de la orientación, por qué los casos pequeños le ganan a «quedarse pensando», la pregunta exacta del penúltimo paso y las dos formas del pensamiento ilusorio.*
