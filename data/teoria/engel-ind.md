# Inducción: fuerte, fortalecida y descenso

*Lección redactada para CogitoErgoSum a partir del capítulo de inducción de Engel (Problem-Solving Strategies). Cubre el contenido completo de la unidad.*

## La idea central

La inducción matemática no es solo un método de demostración: es una **herramienta de descubrimiento**. Antes de demostrar, la inducción te dice dónde está la estructura; el paso inductivo a veces no cierra hasta que fortaleces la hipótesis, y ese forzamiento te revela qué era verdad desde el principio.

## Inducción ordinaria vs. fuerte

**Inducción ordinaria** (la estándar): demostrar P(n₀) (la base) y el paso P(n) ⇒ P(n+1). Con esto cubres todos los enteros ≥ n₀.

**Inducción fuerte**: el paso supone P(k) para **todo k ≤ n** (no solo para n), y de ahí deriva P(n+1). Es necesaria cuando el caso n+1 depende de varios predecesores, no solo del inmediato anterior:

- Recurrencias tipo Fibonacci (depende de n y n−1).
- «Cualquier entero ≥ 2 tiene un factor primo» (requiere suponer que todos los enteros menores ya se descomponen).
- Juegos con estado: la jugada óptima puede llevar a cualquier posición anterior, no solo a la anterior inmediata.

## Fortalecer la hipótesis

La paradoja del principiante: si el paso P(n) ⇒ P(n+1) «no cierra», a veces la solución es **demostrar algo más general**. Con una hipótesis más fuerte, el paso inductivo dispone de más información y resulta más fácil.

Ejemplo clásico: para demostrar que la suma de los ángulos de un polígono convexo de n lados es 180°(n−2), es más directo demostrar la versión triangulada (con la diagonal auxiliar) que atacar directamente la fórmula. La versión «más fuerte» (polígono descompuesto en triángulos) es la que el paso inductivo maneja bien.

Protocolo: si el paso falla, pregúntate «¿qué dato auxiliar habría necesitado en el paso?» Ese dato es la hipótesis fortalecida que debes demostrar junto con el enunciado principal.

## Inducción de Cauchy

Para demostrar la AM-GM (y otras desigualdades) sin conocer el caso general, Cauchy usó una estrategia de **dos fases**:

1. **Hacia adelante**: demuestra P(2) y luego que P(n) ⇒ P(2n) (duplicando variables).
2. **Hacia atrás**: demuestra que P(n) ⇒ P(n−1) (reduciendo una variable fijada como su promedio).

Las dos fases juntas cubren todos los naturales (si n está entre dos potencias de 2, se llega a él bajando desde la potencia superior). Es la variante correcta cuando el paso P(n)⇒P(n+1) no es natural pero duplicar sí lo es.

## Descenso infinito

Para demostrar que algo es **imposible**, supón un contraejemplo **mínimo** y construye uno estrictamente menor. Como no existe una sucesión infinita decreciente de enteros positivos, se llega a una contradicción. Es inducción fuerte vista del revés.

Usos: irracionalidad de √2, imposibilidad de ciertas ecuaciones diofánticas, demostración de que ciertos juegos son imposibles. La firma es «supongamos que existe una solución y sea la mínima» seguida de la construcción de una más pequeña.

## Las trampas clásicas

1. **Olvidar o equivocar la base**: la base no es opcional. P(1)⇒P(2)⇒… solo arranca si P(1) es verdad.
2. **Paso que no usa la hipótesis**: si puedes derivar P(n+1) sin asumir P(n), no es inducción —es una demostración directa del caso general.
3. **«Todos los caballos del mismo color»**: el paso n→n+1 falla en n=1→2 porque los dos subconjuntos {1,…,k} y {2,…,k+1} deben solaparse (para «transferir» el color), y con k=1 no se solapan. Verifica que el paso funcione **desde la base real**, no solo para n «grande».

## Disparadores

- «Demuestra para todo n ≥ 1» con una fórmula cerrada → inducción ordinaria, el paso es álgebra limpia.
- «Cada caso depende de los dos anteriores» (Fibonacci, recurrencias) → inducción fuerte.
- «El paso no cierra» → fortalecer la hipótesis: busca el dato auxiliar que necesitas.
- «Demuestra que es imposible» con enteros positivos → descenso infinito: supón mínimo y construye uno menor.
- «Desigualdad con n variables» sin paso n→n+1 natural → Cauchy: potencias de 2 + paso atrás.

## Síntesis

> **Chunk mínimo:** Inducción ordinaria: base + paso P(n)⇒P(n+1). Inducción fuerte: el paso supone todo P(k≤n), necesaria cuando el caso n+1 depende de varios anteriores (Fibonacci, factorización prima). Fortalecer la hipótesis: si el paso no cierra, conjetura un enunciado más general — más hipótesis en el paso → más fácil cerrarlo. Cauchy: potencias de 2 hacia adelante + paso atrás (n→n−1); cubre todos los naturales. Descenso infinito: para imposibilidad, supón mínimo y construye uno menor (contradicción con el mínimo). Trampas: base incorrecta, paso que no usa la hipótesis, solapamiento faltante en n=1→2.

---

*Antes del quiz: reconstruye de memoria la diferencia entre ordinaria y fuerte, cuándo fortalecer la hipótesis, la estrategia de Cauchy (dos fases) y el argumento del descenso infinito.*
