# Arena Quant · Brainteasers: trucos, invariantes y conteo

## De qué trata (y qué sabrás hacer)

Estos acertijos casi nunca piden resolver ecuaciones: piden **ver el truco** — la cantidad que se conserva o la reformulación que colapsa el problema. El reflejo a entrenar es preguntarte "¿qué no cambia aquí?" antes de tomar el lápiz. Una ley de conservación bien vista resuelve en una línea lo que el álgebra haría en una página.

Al terminar reconocerás las firmas: conservación (trasvases, desplazamiento de agua), invariantes de conteo (cada operación cambia el total en 1), reformular geometría desdoblándola, y Fibonacci cuando "la última pieza" bifurca en dos casos. Cada idea se construye desde un caso concreto.

---

## Conservación — sigue lo que no cambia

- **Copa de vino blanco y copa de tinto, 100 ml cada una. Pasas 5 ml de tinto al blanco, mezclas, y devuelves 5 ml de la mezcla. ¿Hay más blanco en la copa de tinto o tinto en la de blanco?** Truco: al final cada copa vuelve a tener 100 ml. Lo que falta de blanco en su copa **está** en la otra, y viceversa: **exactamente iguales**. Cero álgebra — solo conservación de volumen.
- **Estás en un bote en una piscina con un ancla; tiras el ancla al fondo. ¿Sube o baja el nivel del agua?** Flotando, el ancla desplaza agua según su **peso**; en el fondo, según su **volumen**. Como es más densa que el agua, en el bote desplazaba más, así que al hundirla el nivel **baja**.

---

## Invariantes de conteo

- **Tableta de chocolate de $n$ cuadritos: ¿cuántas roturas para separarlos todos?** Cada rotura aumenta el número de piezas en exactamente 1. De 1 pieza a $n$ piezas hacen falta siempre $n-1$ roturas, **sin importar** la estrategia. Es el invariante más limpio del capítulo.
- **Pesas para equilibrar todo entero de 1 a 40 en un solo platillo:** cada pesa entra o no (binario) → $1,2,4,8,16,32$ (6 pesas; con 5 solo cubres $2^5=32<40$).
- **Si puedes poner pesas en ambos platillos** (cada una suma, resta o no participa → ternario): $1,3,9,27$ bastan, porque $3^4=81\ge 2\cdot40+1$.

---

## Reformular geometría: desdoblar

**Una hormiga va de una esquina a la opuesta de un cubo de lado 1, caminando por la superficie. ¿Distancia mínima?** Desdobla dos caras del cubo en un plano: el camino se vuelve la hipotenusa de un rectángulo $1\times 2$, así que la distancia es $\sqrt{1^2+2^2}=\sqrt5$. Aplanar convierte un problema 3D en uno de Pitágoras.

---

## Series infinitas que se suman solas

**Bebemos una pinta por turnos: yo tomo la mitad, tú la mitad de lo que queda, yo la mitad de lo que queda…** Yo bebo $\sum_k \tfrac{1}{2^{2k+1}}$ y tú la mitad de eso, así que yo bebo el **doble**: $\tfrac23$ y $\tfrac13$. La pinta entera se consume porque $\sum_k \tfrac1{2^k}=1$ — la serie geométrica cierra el problema sin sumar término a término.

---

## Recurrencias: Fibonacci escondido

- **Subes $n$ escalones de 1 o 2 en 2. ¿De cuántas formas?** El último paso fue de 1 (desde $n-1$) o de 2 (desde $n-2$): $p(n)=p(n-1)+p(n-2)$, con $p(1)=1,p(2)=2$. Es **Fibonacci** ($p(n)=F_{n+1}$).
- **¿De cuántas formas embaldosas un tablero $2\times n$ con dominós?** Misma recurrencia → también Fibonacci. Regla: cuando "la última pieza es de un tipo u otro", suele aparecer Fibonacci.

---

## Trampas de promedio

- **Una vuelta a 30 mph; ¿a qué velocidad la segunda para promediar 60 mph en total?** Es **imposible**: 2 millas a 60 mph tomarían 2 minutos, pero la primera milla a 30 mph ya consumió esos 2 minutos. La velocidad media es la **media armónica** de las velocidades, no la aritmética. La tentación de promediar $\tfrac{30+v}{2}=60$ ignora que el invariante real es el **tiempo**, no la velocidad.

---

## Prototipo, contraejemplo y caso borde del invariante

El hilo que une casi todo es **buscar la cantidad que no cambia**. Para no confundir "invariante real" con "patrón aparente":

- **Prototipo:** las roturas de chocolate. Cada operación cambia el conteo de piezas en exactamente $+1$ → el total de roturas ($n-1$) no depende del camino. Invariante limpio.
- **Contraejemplo (parece invariante, no lo es):** "promediar 30 mph y $v$ da 60". La tentación es promediar la *velocidad*; el invariante real es el **tiempo** ($=$ distancia/velocidad), y por eso sale media armónica. Cuando el "promedio obvio" choca con la conservación correcta, gana la conservación.
- **Caso borde (pesas):** con 5 pesas binarias cubres $2^5=32<40$ → falla por uno. El borde (¿alcanza justo?) revela que la cota es exacta, no aproximada.

## Errores típicos

- **Conceptual:** intentar resolver con álgebra un problema que pide *mirada*. Si te ves planteando sistemas de ecuaciones, probablemente no viste el invariante.
- **De interpretación:** promediar velocidades aritméticamente (es media armónica), o confundir "desplaza por peso" con "desplaza por volumen" (ancla en el bote).
- **Técnico:** en recurrencias de escalones/dominó, equivocar los casos base ($p(1)=1,p(2)=2$) y desfasar el índice de Fibonacci.

## Transferencia isomorfa

- **Invariante "cada operación cambia el conteo en 1" ↔ DS&A:** contar componentes conexas en un grafo (cada arista que une dos componentes baja el conteo en 1) es el mismo invariante que las roturas de chocolate (conecta con [[arena-cc2]]).
- **Media armónica ↔ sistemas:** el throughput de un pipeline con etapas de distinta velocidad se promedia como media armónica, no aritmética — el mismo error de "promediar velocidades" reaparece al calcular latencia/QPS (conecta con [[arena-sd1]]).
- **Fibonacci "la última pieza es de dos tipos" ↔ conteo de caminos:** $p(n)=p(n-1)+p(n-2)$ es isomorfa a contar secuencias binarias sin dos ceros seguidos, que aparece en codificación y en programación dinámica (conecta con [[arena-cc3]]).

Moraleja de la arista: *un invariante es una ley de conservación disfrazada; encontrar "qué se conserva" colapsa el acertijo igual que la energía colapsa un problema de física.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "trasvases / mezclas" | conservación: las cantidades finales fijan el resultado |
| "¿cuántas roturas/cortes?" | invariante: cada operación cambia el conteo en 1 |
| "pesas para cubrir $1..N$" | un platillo → binario; dos platillos → ternario |
| "camino sobre una superficie 3D" | desdobla a un plano, usa Pitágoras |
| "una pieza de dos tipos / subir escalones" | recurrencia → Fibonacci |
| "promediar velocidades" | media armónica, no aritmética |

---

> ❧ **Síntesis:** el brainteaser no pide cálculo sino *mirada*. Busca la cantidad conservada (vino, agua, piezas), reformula la geometría desdoblándola, y reconoce a Fibonacci cuando "la última pieza" bifurca en dos casos. Y desconfía siempre del promedio aritmético de velocidades.

---

*Retrieval: cierra la página y responde — (1) ¿más blanco en el tinto o al revés?; (2) roturas para $n$ cuadritos; (3) distancia mínima de la hormiga en el cubo; (4) por qué la segunda vuelta a 60 mph es imposible.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

Los brainteasers de invariantes y conteo se conectan hacia atras con [[zeitz-34]] y [[engel-inv]], donde se aprende a nombrar lo que no cambia. [[engel-color]] muestra invariantes visuales por coloracion, y [[zeitz-31]] agrega simetria como compresion de casos antes de contar.
<!-- GRAFO_CONEXO_OLEADA3_END -->
