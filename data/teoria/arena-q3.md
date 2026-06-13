# Brainteasers cuantitativos · Patrones y lógica

## Series y sumas

El truco de Gauss resuelve cualquier suma aritmética en segundos: empareja el primero con el último, el segundo con el penúltimo… todos los pares suman lo mismo.

**Suma 1+2+…+n** = n(n+1)/2. Para n=100: 50 pares de valor 101 → 5050.

Fórmulas complementarias que aparecen en entrevista:
- Σk² = n(n+1)(2n+1)/6
- Σk³ = [n(n+1)/2]²

---

## Relojes

Velocidades absolutas: minutero = **6°/min**; horario = **0.5°/min**. Velocidad relativa del minutero sobre el horario = **5.5°/min**.

| Pregunta | Fórmula |
|----------|---------|
| Ángulo en horas H:M | \|30H − 5.5M\| (y su suplemento si >180) |
| Primera superposición tras hora H | Ventaja = 30H grados; tiempo = 30H/5.5 min |
| k-ésima superposición desde 12:00 | k × 720/11 minutos |

A las 3:15: ángulo = \|30×3 − 5.5×15\| = \|90 − 82.5\| = **7.5°**.

---

## Cuadrados perfectos y paridad de divisores

**Invariante clave:** el número n tiene número *impar* de divisores si y solo si n es cuadrado perfecto. Razón: cada divisor d se empareja con n/d; el emparejamiento falla solo cuando d = n/d, es decir d = √n (entero).

Aplicación directa al problema de las bombillas: la bombilla n queda encendida ⟺ n es cuadrado perfecto.

Con n bombillas → **⌊√n⌋** quedan encendidas.

---

## Capas de cubos y geometría discreta

Capa exterior de un cubo n×n×n:

> exterior = n³ − (n−2)³ = 6n² − 12n + 8

Para n=10: 1000 − 512 = **488**. Para n=3: 27 − 1 = 26. Para n=2: 8 − 0 = 8.

---

## Crecimiento exponencial — trabajo inverso

"El estanque se llena en 30 días; ¿en cuántos si empiezas con 8 ranas?"

Clave: 8 = 2³ equivale a 3 días de ventaja. Respuesta: 30 − 3 = **27 días**.

El error frecuente es dividir el tiempo (30/8), olvidando que el crecimiento es multiplicativo, no aditivo.

---

## Principio del palomar

Con **k** colores necesitas **k + 1** objetos para garantizar un par. La cantidad dentro de cada color no importa.

Versión inversa: si quieres garantizar uno de *cada* color (todos representados), necesitas saber el mínimo total.

---

## Ceros finales de n!

Cada cero final = un factor 10 = 2×5. Los 2s abundan; el cuello de botella son los 5s.

Exponente de p=5 en n!: **⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …**

Para 100!: 20 + 4 + 0 = **24 ceros**.

---

## Juegos de estrategia con invariante modular

Juego: turnos para decir números; quien diga N gana; cada turno aumenta en 1–M.

**Jugada:** controla los hitos {N, N−(M+1), N−2(M+1), …}. Ve primero si el primero de esos hitos es alcanzable en tu primer turno; de lo contrario ve segundo. Siempre responde x rival con (M+1)−x.

Para el juego a 50 con M=10: hitos = {6, 17, 28, 39, 50}. Ve primero y llama 6.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Suma de 1 a n" | Gauss pairing: n(n+1)/2 |
| "Ángulo entre manecillas" | Velocidad relativa 5.5°/min |
| "¿Cuántos objetos quedan ON/OFF?" | Contar divisores → paridad → cuadrado perfecto |
| "Capa exterior de un cubo" | n³ − (n−2)³ |
| "Crecimiento que duplica" | Logaritmo del factor = días de ventaja |
| "Garantizar un par de k colores" | k+1 objetos (palomar) |
| "Ceros finales de n!" | Contar factores del primo más escaso |

---

> **Síntesis:** Los brainteasers cuantitativos no prueban memorización: prueban si puedes encontrar el invariante correcto (paridad, módulo, logaritmo) y usarlo para colapsar el problema. La señal de reconocimiento es casi siempre la llave.

---

*Retrieval: para consolidar, cierra esta página y responde: (1) fórmula de Gauss, (2) velocidad relativa de manecillas, (3) criterio de bombilla encendida, (4) ceros en 100!.*
