# Brainteasers cuantitativos · Patrones y lógica

## De qué trata (y qué sabrás hacer)

Estos acertijos no premian memorizar fórmulas: premian encontrar **la cantidad que no cambia** (un invariante: paridad, módulo, logaritmo) que colapsa un cálculo aparentemente enorme a una sola línea. La señal de reconocimiento es casi siempre la llave; el resto es aritmética.

Al terminar tendrás el reflejo de preguntarte "¿qué se conserva aquí?" antes de calcular, y reconocerás las firmas clásicas: emparejar para sumar (Gauss), paridad de divisores (cuadrados perfectos), el primo escaso (ceros de un factorial), y el módulo que decide un juego. Cada truco se construye desde un caso pequeño.

---

## Series y sumas: el truco de Gauss

¿Cuánto es $1+2+\cdots+n$? Empareja el primero con el último, el segundo con el penúltimo: cada par suma $n+1$, y hay $n/2$ pares:

$$1+2+\cdots+n=\frac{n(n+1)}{2}.$$

Para $n=100$: 50 pares de valor 101 → 5050. Dos hermanas que aparecen seguido:

$$\sum_{k=1}^n k^2=\frac{n(n+1)(2n+1)}{6}, \qquad \sum_{k=1}^n k^3=\left(\frac{n(n+1)}{2}\right)^2.$$

---

## Relojes

Dos manecillas a velocidades distintas: el minutero gira $6°/\text{min}$ y el horario $0.5°/\text{min}$, así que la velocidad **relativa** es $5.5°/\text{min}$.

| Pregunta | Fórmula |
|----------|---------|
| Ángulo a las H:M | $\lvert 30H-5.5M\rvert$ (toma el suplemento si $>180°$) |
| Primera superposición tras la hora $H$ | tiempo $=\dfrac{30H}{5.5}$ min |
| $k$-ésima superposición desde las 12:00 | $k\cdot\dfrac{720}{11}$ min |

A las 3:15: $\lvert 30\cdot3-5.5\cdot15\rvert=\lvert 90-82.5\rvert=7.5°$. El error típico es olvidar que el horario también se mueve.

---

## Cuadrados perfectos y paridad de divisores

**Invariante clave:** un número $n$ tiene un número **impar** de divisores si y solo si es un cuadrado perfecto. Por qué: cada divisor $d$ se empareja con $n/d$, así que vienen en parejas… salvo cuando $d=n/d$, es decir $d=\sqrt n$ (entero). Esa pareja "consigo misma" es la única que rompe la paridad.

Aplicación directa al problema de las bombillas: la bombilla $n$ se conmuta una vez por divisor, así que queda **encendida** $\iff n$ es cuadrado perfecto. Con $n$ bombillas, quedan $\lfloor\sqrt n\rfloor$ encendidas.

---

## Capas de un cubo

La capa exterior de un cubo $n\times n\times n$ es el total menos el cubo interior $(n-2)^3$:

$$\text{exterior}=n^3-(n-2)^3=6n^2-12n+8.$$

Para $n=10$: $1000-512=488$. Restar el interior es más limpio que contar caras (que sobrecontaría aristas y esquinas).

---

## Crecimiento exponencial — trabajo inverso

"El estanque de nenúfares se llena en 30 días duplicándose cada día; ¿cuánto si empiezas con 8 veces más?" La trampa es dividir $30/8$. El crecimiento es **multiplicativo**: $8=2^3$ equivale a **3 duplicaciones** de ventaja, así que $30-3=27$ días. Convertir un factor multiplicativo en una distancia aditiva es tomar el **logaritmo**.

---

## Principio del palomar

Con $k$ categorías necesitas $k+1$ objetos para garantizar que dos caigan en la misma. No es probabilidad: es una **garantía** del peor caso. La cantidad dentro de cada categoría no importa.

---

## Ceros finales de $n!$

Cada cero final es un factor 10 $=2\times5$. Los factores 2 abundan; el cuello de botella son los **5**. El exponente del primo 5 en $n!$ es

$$\left\lfloor\frac n5\right\rfloor+\left\lfloor\frac n{25}\right\rfloor+\left\lfloor\frac n{125}\right\rfloor+\cdots$$

Para $100!$: $20+4+0=24$ ceros. La regla general: el número de veces que un primo $p$ divide a $n!$ lo da esta suma de pisos (fórmula de Legendre).

---

## Juegos con invariante modular

Juego: por turnos sumáis $1$ a $M$ a un total; gana quien diga $N$. La estrategia controla los **hitos** $\{N,\,N-(M+1),\,N-2(M+1),\ldots\}$: si dejas al rival justo en un hito, responde lo que responda ($x$), tú juegas $(M+1)-x$ para volver al siguiente hito.

Para el juego a 50 con $M=10$: los hitos son $\{6,17,28,39,50\}$. Ve primero y di 6; luego mantén el módulo. Razonar módulo $(M+1)$ es el corazón de muchos juegos combinatorios.

---

## Mini-ejemplo trabajado: el problema de las bombillas a mano

100 bombillas apagadas; en la pasada $k$ accionas cada bombilla múltiplo de $k$. La bombilla $n$ cambia de estado una vez por cada divisor de $n$. Toma $n=12$: divisores $\{1,2,3,4,6,12\}$ → 6 conmutaciones → termina **apagada**. Toma $n=9$: divisores $\{1,3,9\}$ → 3 conmutaciones → termina **encendida**.

La estructura profunda: cada divisor $d$ se empareja con $n/d$, así que los divisores vienen en parejas y el conteo es **par**… salvo cuando $d=n/d$, es decir cuando $d=\sqrt n$ es entero. Por eso el invariante es la **paridad del número de divisores**, y solo los cuadrados perfectos la rompen.

**Predicción antes de seguir:** entre 1 y 100, ¿cuántas bombillas quedan encendidas? Respuesta: $\lfloor\sqrt{100}\rfloor=10$ (las que son $1^2,2^2,\ldots,10^2$). No hace falta simular 100 pasadas: el invariante colapsa el problema a una raíz cuadrada.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "¿cuántos quedan encendidos / cuántas veces se conmuta?" → cuenta divisores y mira la **paridad** (cuadrado perfecto $\iff$ impar).
- **Contraejemplo (tentación aditiva):** "el estanque se llena en 30 días, ¿y con 8 veces más?" tienta a dividir $30/8$. Pero el crecimiento es multiplicativo: $8=2^3$ son solo **3 duplicaciones** de ventaja → 27 días.
- **Caso borde ($n!$):** los ceros finales de $n!$ no se cuentan con los 2 (abundan) sino con el primo **más escaso**, el 5. El borde revela cuál factor es el cuello de botella.

## Errores típicos

- **Conceptual:** buscar una fórmula cerrada cuando el problema pide hallar un **invariante** (paridad, módulo, logaritmo) que colapsa el conteo.
- **Técnico:** en el ángulo del reloj, olvidar que el horario también se mueve ($0.5°/\text{min}$) y usar solo $30H$; o no tomar el suplemento cuando el ángulo supera $180°$.
- **De interpretación:** tratar el crecimiento exponencial como lineal (dividir el tiempo) en problemas de duplicación.

## Transferencia isomorfa

Un brainteaser bien hecho entrena el reflejo de **buscar la cantidad que no cambia**, transversal a todo:

- **Paridad de divisores ↔ invariante de bucle:** "lo que permanece par/impar pase lo que pase" es el mismo argumento que un *loop invariant* al probar correctitud de un algoritmo (conecta con [[arena-cc3]]).
- **Principio del palomar ↔ colisiones de hash:** "$k+1$ objetos en $k$ cajas garantizan un par" es por qué un hash con más claves que buckets *debe* colisionar (conecta con [[arena-sd2]]).
- **Aritmética modular del juego ↔ estados ganadores:** controlar los hitos $\{N,N-(M+1),\ldots\}$ es razonar módulo $(M+1)$, el módulo que decide quién gana.
- **Logaritmo como "días de ventaja" ↔ escala $\sqrt T$ y vida media:** convertir un factor multiplicativo en una distancia aditiva (log) es el mismo truco que escalar volatilidad o vida media (conecta con [[arena-q11]]).

Moraleja de la arista: *cuando un conteo explota, no lo enumeres: busca la cantidad invariante (paridad, módulo, log) que lo colapsa a una sola línea.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Suma de 1 a $n$" | Gauss: $\tfrac{n(n+1)}{2}$ |
| "Ángulo entre manecillas" | Velocidad relativa $5.5°/\text{min}$ |
| "¿Cuántos objetos quedan ON/OFF?" | Contar divisores → paridad → cuadrado perfecto |
| "Capa exterior de un cubo" | $n^3-(n-2)^3$ |
| "Crecimiento que duplica" | Logaritmo del factor = días de ventaja |
| "Garantizar un par de $k$ colores" | $k+1$ objetos (palomar) |
| "Ceros finales de $n!$" | Contar factores del primo más escaso (5) |

---

> **Síntesis:** Los brainteasers cuantitativos no prueban memorización: prueban si puedes encontrar el invariante correcto (paridad, módulo, logaritmo) y usarlo para colapsar el problema. La señal de reconocimiento es casi siempre la llave.

---

*Retrieval: cierra esta página y responde: (1) fórmula de Gauss; (2) velocidad relativa de las manecillas; (3) criterio de bombilla encendida; (4) ceros en $100!$.*
