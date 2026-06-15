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

## Mini-ejemplo trabajado: el problema de las bombillas a mano

100 bombillas apagadas; en la pasada k accionas cada bombilla múltiplo de k. La bombilla n cambia de estado una vez por cada divisor de n. Toma n=12: divisores {1,2,3,4,6,12} → 6 conmutaciones → termina **apagada**. Toma n=9: divisores {1,3,9} → 3 conmutaciones → termina **encendida**.

La estructura profunda: cada divisor d se empareja con n/d, así que los divisores vienen en parejas y el conteo es **par**… salvo cuando d = n/d, es decir cuando d = √n es entero. Por eso el invariante es la **paridad del número de divisores**, y solo los cuadrados perfectos la rompen.

**Predicción antes de seguir:** entre 1 y 100, ¿cuántas bombillas quedan encendidas? Respuesta: ⌊√100⌋ = **10** (las que son 1², 2², …, 10²). No hace falta simular 100 pasadas: el invariante colapsa el problema a una raíz cuadrada.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "¿cuántos quedan encendidos / cuántas veces se conmuta?" → cuenta divisores y mira la **paridad** (cuadrado perfecto ⟺ impar).
- **Contraejemplo (tentación aditiva):** "el estanque se llena en 30 días, ¿y con 8 ranas?" tienta a dividir 30/8. Pero el crecimiento es multiplicativo: 8 = 2³ son solo **3 duplicaciones** de ventaja → 27 días. Confundir aditivo con multiplicativo es el error clásico.
- **Caso borde (n!):** los ceros finales de n! no se cuentan con los 2 (abundan) sino con el primo **más escaso**, el 5. El borde revela cuál factor es el cuello de botella.

## Errores típicos

- **Conceptual:** buscar una fórmula cerrada cuando el problema pide hallar un **invariante** (paridad, módulo, logaritmo) que colapsa el conteo.
- **Técnico:** en el ángulo del reloj, olvidar que el horario también se mueve (0.5°/min) y usar solo 30H; o no tomar el suplemento cuando el ángulo supera 180°.
- **De interpretación:** tratar el crecimiento exponencial como lineal (dividir el tiempo) en problemas de duplicación.

## Transferencia isomorfa

Un brainteaser bien hecho entrena el reflejo de **buscar la cantidad que no cambia**, y ese reflejo es transversal:

- **Paridad de divisores ↔ invariante de bucle:** "lo que permanece par/impar pase lo que pase" es el mismo argumento que un *loop invariant* al probar correctitud de un algoritmo (conecta con [[arena-cc3]], donde la recurrencia se sostiene sobre una invariante de estado).
- **Principio del palomar ↔ colisiones de hash:** "k+1 objetos en k cajas garantizan un par" es exactamente por qué un hash con más claves que buckets *debe* colisionar (conecta con [[arena-sd2]], hashing/sharding).
- **Aritmética modular del juego de Nim ↔ estados ganadores:** controlar los hitos {N, N−(M+1), …} es razonar módulo (M+1), el mismo módulo que decide quién gana en juegos combinatorios.
- **Logaritmo como "días de ventaja" ↔ escala √T y vida media:** convertir un factor multiplicativo en una distancia aditiva (log) es el mismo truco que escalar volatilidad o vida media en el tiempo.

Moraleja de la arista: *cuando un conteo explota, no lo enumeres: busca la cantidad invariante (paridad, módulo, log) que lo colapsa a una sola línea.*

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
