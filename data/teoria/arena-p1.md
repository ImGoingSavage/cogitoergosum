# Acertijos matemáticos y razonamiento rápido

## De qué trata (y qué sabrás hacer)

Las entrevistas quant abren con acertijos de cálculo rápido. No miden si te sabes una fórmula: miden si **ves la estructura** que convierte un cálculo aparentemente largo en dos o tres pasos. La idea unificadora de toda esta lección es: *antes de calcular a fuerza bruta, busca la identidad que colapsa el problema* —una cancelación, un emparejamiento, un ciclo—.

Al terminar reconocerás de un vistazo las señales más comunes (sumas que telescopan, productos cerca de potencias de 10, potencias módulo $m$, conteos por posición) y tendrás el atajo a mano. Cada truco se construye desde un caso pequeño que puedes verificar a mano.

---

## Sumas telescópicas: cancelar en cadena

Una suma **telescópica** es aquella donde cada término cancela parte del siguiente, dejando solo los extremos. La señal es una fracción que se puede partir en dos.

Empieza con el caso atómico: $\dfrac{1}{k(k+1)}$. ¿Puedo escribirlo como una resta? Sí, por **fracciones parciales**:

$$\frac{1}{k(k+1)} = \frac{1}{k} - \frac{1}{k+1}.$$

(Verifícalo con $k=2$: $\tfrac12-\tfrac13=\tfrac16=\tfrac{1}{2\cdot3}$. ✓) Ahora suma desde $k=1$ hasta $n$ y observa la magia: cada $-\tfrac{1}{k+1}$ cancela el $+\tfrac{1}{k+1}$ del término que sigue.

$$\sum_{k=1}^{n}\frac{1}{k(k+1)} = \left(1-\tfrac12\right)+\left(\tfrac12-\tfrac13\right)+\cdots+\left(\tfrac1n-\tfrac1{n+1}\right) = 1 - \frac{1}{n+1} = \frac{n}{n+1}.$$

Para $n=99$: la suma es $99/100$. No sumaste 99 fracciones; viste que 97 de ellas se anulan. **Variantes** que también telescopan: $\sum \tfrac{1}{k(k+2)}=\tfrac12\!\left(1+\tfrac12-\tfrac1{n+1}-\tfrac1{n+2}\right)$ y $\sum\tfrac{1}{k(k+1)(k+2)}$.

---

## Cálculo mental con identidades algebraicas

El truco es **anclar en un múltiplo de 10** y dejar que el ajuste sea pequeño. Tres identidades cubren casi todo:

| Producto | Identidad | Ejemplo |
|---------|-----------|---------|
| $(a-b)(a+b)$ | $a^2-b^2$ | $97\times103 = 100^2-3^2 = 9991$ |
| $(a\pm b)^2$ | $a^2\pm2ab+b^2$ | $98^2=(100-2)^2=9604$ |
| $(a-b)^3$ | $a^3-3a^2b+3ab^2-b^3$ | $99^3\approx100^3-3\cdot100^2=970299$ |

Por qué funciona: si $a=100$, los términos con $a^2$ son fáciles y el resto ($b$ pequeño) se calcula de cabeza. La diferencia de cuadrados es la estrella —cualquier producto $x\cdot y$ se reescribe como $\left(\tfrac{x+y}2\right)^2-\left(\tfrac{x-y}2\right)^2$, así que $97\times103$ tiene centro $100$ y semiancho $3$.

---

## Potencias grandes módulo $m$

"Módulo $m$" significa quedarte solo con el **residuo** al dividir entre $m$ (la hora en un reloj es aritmética módulo 12). Para una potencia enorme como $4444^{4444}\bmod 9$ no calculas la potencia: explotas que los residuos **se ciclan**.

**Algoritmo en 3 pasos:**
1. **Reduce la base:** $b\bmod m$.
2. **Halla el período:** el ciclo de $(b\bmod m)^k\bmod m$ al subir $k$.
3. **Reduce el exponente** módulo ese período.

Ejemplo — $4444^{4444}\bmod 9$. Truco: módulo 9, un número $\equiv$ a la suma de sus dígitos.
- Base: $4444\to 4{+}4{+}4{+}4=16\to 7$. Así $4444\equiv 7$.
- Ciclo de $7^k\bmod 9$: $7,\,49\!\equiv\!4,\,7\cdot4\!=\!28\!\equiv\!1,\,$ y vuelve a $7$. **Período 3.**
- Exponente: $4444\bmod 3$. Suma de dígitos $16\to 1$, así que $4444\equiv 1\pmod 3$.
- Resultado: $7^{1}\bmod 9 = \mathbf{7}$.

Herramienta general: el **teorema de Euler** —si $\gcd(b,m)=1$, entonces $b^{\varphi(m)}\equiv 1\pmod m$—, que te da un período garantizado ($\varphi(m)$ = cuántos números $\le m$ son coprimos con $m$).

---

## Conteo de dígitos: cuenta por posición, nunca por número

¿Cuántas veces aparece el dígito $1$ en $\{1,\ldots,100\}$? La trampa es contar número por número (el $11$ te confunde porque tiene dos unos). El método robusto cuenta **por posición**:
- **Unidades:** $1,11,21,\ldots,91$ → 10 unos.
- **Decenas:** $10,11,\ldots,19$ → 10 unos.
- **Centenas:** $100$ → 1 uno.
- **Total: 21.**

El $11$ aporta uno a la columna de unidades y otro a la de decenas, y así debe ser. Separar por columnas convierte un conteo ambiguo en tres conteos triviales.

---

## Series de potencias: derivar la geométrica

La **serie geométrica** es la base de muchas esperanzas y valoraciones:

$$\sum_{k=0}^{\infty} x^k = \frac{1}{1-x} \quad (|x|<1).$$

Intuición: la suma $1+x+x^2+\cdots$ llamada $S$ cumple $S = 1 + xS$ (saca un factor $x$ de la cola), de donde $S=\tfrac1{1-x}$. Ahora **deriva ambos lados respecto a $x$** —un truco para "meter un $k$" en la suma—:

$$\sum_{k=1}^{\infty} k\,x^{k-1} = \frac{1}{(1-x)^2}, \qquad\text{y multiplicando por } x:\qquad \sum_{k=1}^{\infty} k\,x^{k} = \frac{x}{(1-x)^2}.$$

Para $x=\tfrac12$: $\sum k\,(1/2)^k = \dfrac{1/2}{(1/2)^2}=2$. Esto reaparece en $E[\text{geométrica}]$ y en valorar una perpetuidad creciente (conecta con [[arena-q8]]).

---

## Producto telescópico $\prod(1-1/k^2)$

El mismo gesto de cancelación, pero multiplicando. Factoriza cada término como diferencia de cuadrados:

$$1-\frac{1}{k^2} = \frac{(k-1)(k+1)}{k^2}.$$

Al multiplicar de $k=2$ a $n$, los numeradores $(k+1)$ y $(k-1)$ se encajan con los denominadores vecinos (doble telescopio) y casi todo se anula:

$$\prod_{k=2}^{n}\left(1-\frac{1}{k^2}\right) = \frac{n+1}{2n} \xrightarrow{\,n\to\infty\,} \frac12.$$

---

## Suma de todos los dígitos de $\{1,\ldots,100\}$

Otra vez "por posición". Para sumar (no contar) todos los dígitos:
- $\{1\text{–}9\}$: $1+\cdots+9 = 45$.
- $\{10\text{–}99\}$: en **unidades** cada dígito $0$–$9$ aparece 9 veces $\Rightarrow 9\times45=405$; en **decenas** cada dígito $1$–$9$ aparece 10 veces $\Rightarrow 10\times45=450$; subtotal $855$.
- $\{100\}$: $1+0+0=1$.
- **Total: $901$.**

---

## Cuadrados en un tablero $n\times n$

Un cuadrado de lado $k$ cabe en $(n-k+1)^2$ posiciones (puede moverse $n-k+1$ pasos en cada eje). Suma sobre todos los lados:

$$\text{Total} = \sum_{k=1}^{n}(n-k+1)^2 = \sum_{j=1}^{n} j^2 = \frac{n(n+1)(2n+1)}{6}.$$

Para $n=8$: $\dfrac{8\cdot9\cdot17}{6}=204$. La identidad $\sum j^2=\tfrac{n(n+1)(2n+1)}6$ conviene tenerla de memoria.

---

## Problema del cumpleaños

En un grupo de $n$ personas, ¿probabilidad de que **al menos dos** compartan cumpleaños? Como casi siempre con "al menos", usa el complemento (todos distintos) y aproxima:

$$P(\text{coincidencia}) \approx 1 - e^{-n(n-1)/730}.$$

Umbral del 50%: $n(n-1) > 730\ln 2\approx 506$, que da $n\approx 23$. Lo contraintuitivo: lo que crece no es $n$, sino el número de **pares** $\binom{n}{2}\approx n^2/2$. Con 23 personas hay $\binom{23}{2}=253$ pares, y cada uno tiene chance $1/365$ de coincidir.

---

## Pesaje de bolas con balanza

Una balanza de dos platos da **tres** resultados (izquierda baja, derecha baja, equilibrio), así que cada pesada extrae información ternaria: con $k$ pesadas distingues hasta $3^k$ casos.

Para 8 bolas (una más pesada): $3^2=9>8$ → **2 pesadas bastan**. Estrategia $3\text{–}3\text{–}2$: pesa 3 contra 3. Si equilibran, la rara está entre las 2 restantes (1 pesada las separa). Si se inclina, la rara está entre esos 3 sospechosos (1 pesada basta). Pensar en binario ($2^k$) sobreestima las pesadas: la balanza no es una moneda.

---

## Hormigas en un polígono — simetría

$n$ hormigas, una en cada vértice de un polígono regular; cada una camina en sentido horario (CW) o antihorario (CCW) con probabilidad $1/2$. ¿Probabilidad de que ninguna choque? Solo dos configuraciones evitan todo choque: **todas CW** o **todas CCW**. De $2^n$ combinaciones igual de probables,

$$P(\text{sin choque}) = \frac{2}{2^n} = 2^{1-n}.$$

Para un triángulo ($n=3$): $2/8=1/4$. La simetría ("solo las dos uniformes funcionan") evita enumerar.

---

## Mini-ejemplo trabajado: telescopio que colapsa 99 términos en 2

Quieres $\sum_{k=1}^{99} \frac{1}{k(k+1)}$. En vez de sumar 99 fracciones, descompón cada término:

$$\frac{1}{k(k+1)} = \frac{1}{k} - \frac{1}{k+1}.$$

Al sumar, cada $-\tfrac{1}{k+1}$ cancela el $+\tfrac{1}{k+1}$ del término siguiente:

$$\left(\tfrac11-\tfrac12\right)+\left(\tfrac12-\tfrac13\right)+\cdots+\left(\tfrac1{99}-\tfrac1{100}\right) = 1 - \tfrac1{100} = \frac{99}{100}.$$

Solo sobreviven el primer y el último término. El "trabajo" es ver la **fracción parcial**, no sumar.

**Predicción antes de seguir:** ¿qué tienen en común el telescopio, contar cuadrados perfectos por paridad de divisores y los productos $\prod(1-1/k^2)$? Respuesta: todos **colapsan una operación larga a sus extremos** al revelar una estructura que se cancela o se empareja. Es el mismo reflejo de "buscar la cantidad invariante que evita enumerar" — el corazón de los brainteasers cuantitativos.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** suma de la forma $\tfrac{1}{k(k+1)}$ o producto $(1-1/k^2)$ → fracciones parciales → telescopio.
- **Contraejemplo (contar por número, no por posición):** para "cuántos dígitos $1$ en $\{1,\ldots,100\}$", contar número por número se enreda; el $11$ aporta a dos posiciones. Cuenta **por posición** (unidades, decenas…).
- **Caso borde (balanza ternaria):** $k$ pesadas distinguen $3^k$ bolas, no $2^k$ — la balanza da tres resultados. Pensar en binario sobreestima las pesadas.

## Errores típicos

- **Conceptual:** intentar sumar/multiplicar a fuerza bruta cuando hay una identidad que colapsa (telescopio, diferencia de cuadrados).
- **Técnico:** en potencias mod $m$, no reducir el exponente módulo el **período** del ciclo de residuos (Euler).
- **De interpretación:** en el cumpleaños, pensar que el tamaño del grupo ($n$) es lo que crece, cuando lo que crece es el número de **pares** ($\sim n^2/2$).

## Transferencia isomorfa

- **Telescopio ↔ invariante que colapsa el conteo:** cancelar términos intermedios es el mismo gesto que la paridad de divisores o un módulo que evita enumerar (conecta con [[arena-q3]]).
- **Balanza $3^k$ ↔ cota de información / $\log_3$:** cada pesada extrae $\log_2 3$ bits; el límite del canal fija el mínimo de pruebas (conecta con [[arena-q13]]).
- **Cumpleaños (pares $\sim n^2/2$) ↔ colisiones de hash:** el umbral $\sqrt N$ de colisiones es el mismo conteo de pares (conecta con [[arena-fc1]] y [[arena-fc3]]).
- **$\sum k\,x^k = x/(1-x)^2$ ↔ esperanza geométrica y perpetuidad:** derivar la serie geométrica da $E[\text{geométrica}]$ y el valor de un flujo creciente (conecta con [[arena-q5]] y [[arena-q8]]).

Moraleja de la arista: *antes de calcular, busca la identidad que colapsa —telescopio, diferencia de cuadrados, módulo—; el esfuerzo está en reconocer el patrón, no en sumar.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Suma de forma $\tfrac{1}{k(k+1)}$ | Fracciones parciales → telescopio |
| Multiplicación cerca de potencia de 10 | $(a\pm b)(a\mp b)=a^2-b^2$ o $(a\pm b)^2$ |
| Potencia mod $m$ | Reduce base, halla período, reduce exponente |
| "Cuántos dígitos $d$ en $\{1..n\}$" | Cuenta por posición |
| $\sum k\,x^k$ | Derivar $\sum x^k$ e igualar |
| Cuadrados en tablero $n\times n$ | $\sum j^2 = \tfrac{n(n+1)(2n+1)}{6}$ |
| "Umbral de cumpleaños" | $\sqrt{2N\ln 2}\approx 23$ para $N=365$ |
| Pesaje con balanza, $k$ pesadas | Máximo $3^k$ objetos |
| Hormigas en polígono sin choque | $2/2^n$ |

---

> **Síntesis:** Los acertijos cuantitativos casi siempre tienen un atajo algebraico o combinatorio. La señal de reconocimiento es la clave: suma de la forma $\tfrac{1}{k(k+1)}$ → telescopio; multiplicación cerca de múltiplo de 10 → diferencia de cuadrados; potencia mod $m$ → ciclo de residuos. Busca el patrón antes de calcular.

---

*Retrieval: sin mirar, calcula (1) $\sum_{k=1}^{99} \tfrac{1}{k(k+1)}$; (2) $97^2$ mentalmente; (3) $7^{100}\bmod 9$; (4) número de cuadrados en un tablero $5\times5$.*
