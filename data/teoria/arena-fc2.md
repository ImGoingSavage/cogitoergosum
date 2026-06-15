# Probabilidad geométrica

## De qué trata (y qué sabrás hacer)

La probabilidad geométrica traduce el azar en **longitudes, áreas y volúmenes**: en vez de contar casos, mides regiones. La pregunta "¿probabilidad de que…?" se vuelve "¿qué fracción de esta figura cumple la condición?". Pero hay una trampa filosófica: *"al azar" no significa nada hasta que fijas respecto a qué eres uniforme* (la paradoja de Bertrand).

Al terminar sabrás montar el espacio muestral como una región, medir la probabilidad como un cociente de áreas, reconocer cuándo un problema está mal planteado, y conectar todo con Monte Carlo. Cada resultado se construye desde su dibujo.

---

## La aguja de Buffon

Dejas caer una aguja de longitud $L$ sobre un suelo con líneas paralelas separadas $d$ (con $L\le d$). ¿Probabilidad de que la aguja cruce una línea?

$$P(\text{cruce})=\frac{2L}{\pi d}.$$

Cómo sale: describe la aguja con dos uniformes — la distancia $x$ del centro a la línea más cercana ($\text{Unif}[0,d/2]$) y el ángulo $\theta$ ($\text{Unif}[0,\pi/2]$). La aguja cruza si $x<\tfrac{L}{2}\cos\theta$. Integrando esa condición sobre el rectángulo de $(x,\theta)$ aparece el $\pi$. Para $L=d$: $P=\tfrac2\pi\approx 63.7\%$. Curiosamente, esto permite **estimar $\pi$** lanzando agujas: $\pi\approx \tfrac{2Ln}{dc}$ con $c$ cruces en $n$ lanzamientos.

---

## Par uniforme en un cuadrado

$X,Y$ i.i.d. $\text{Unif}[0,1]$. La probabilidad de que estén a distancia menor que $r$:

$$P(|X-Y|<r)=2r-r^2 \quad (0<r<1).$$

Dibújalo: la condición $|X-Y|<r$ es una **banda** alrededor de la diagonal del cuadrado. Su complemento son dos triángulos de cateto $1-r$, con área total $(1-r)^2$. Así $P=1-(1-r)^2=2r-r^2$. Para $r=0.3$: $P=0.51$.

---

## La paradoja de Bertrand

Trazas una cuerda "al azar" en un círculo de radio $R$. ¿Probabilidad de que sea más larga que el lado del triángulo equilátero inscrito ($\sqrt3\,R$)? La respuesta **depende del método** de aleatorización:

| Cómo eliges la cuerda | $P(\text{cuerda}>\sqrt3 R)$ |
|--------------------|-----------------|
| Dos puntos al azar en la circunferencia | $1/3$ |
| Punto medio al azar en el disco | $1/4$ |
| Distancia al centro al azar en $[0,R]$ | $1/2$ |

Los tres son correctos **dado su modelo**. La paradoja enseña la lección más importante de la probabilidad geométrica: "uniforme" no está definido sin especificar **qué** objeto se distribuye uniformemente (ángulo, área o radio). Es un error de planteamiento, no de cálculo.

---

## Rango de varias uniformes

Con $X_1,X_2,X_3\sim\text{Unif}[0,1]$, el rango $X_{(3)}-X_{(1)}$ tiene esperanza

$$E[\text{rango}]=E[X_{(3)}]-E[X_{(1)}]=\tfrac34-\tfrac14=\tfrac12,$$

por linealidad (no necesitas la conjunta). En general $E[X_{(n)}-X_{(1)}]=\tfrac{n-1}{n+1}$, y $P(\text{rango}<r)=r^2(3-2r)$ para tres puntos.

---

## Monte Carlo para $\pi$

Lanzas puntos uniformes en $[-1,1]^2$ (cuadrado de área 4) y cuentas cuántos caen en el círculo inscrito de radio 1 (área $\pi$). Como $P(\text{dentro})=\pi/4$:

$$\pi\approx 4\cdot\frac{\#\{\text{puntos dentro del círculo}\}}{\#\{\text{total}\}}.$$

El error estándar cae como $1/\sqrt n$ (es una proporción binomial), así que con $n=10\,000$ el error típico es $\approx0.016$ y necesitas $n\approx10^6$ para 3 decimales. Monte Carlo es **lento** pero su error no empeora con la dimensión, por eso domina en integrales de muchas variables.

---

## El palo roto (broken stick)

Rompes un palo en 3 piezas con dos cortes uniformes. ¿Probabilidad de que formen triángulo?

$$P=\frac14.$$

Cómo: con cortes $U_1<U_2$, las piezas son $U_1$, $U_2-U_1$, $1-U_2$. Forman triángulo si **cada una es menor que $\tfrac12$** (ninguna domina a las otras dos juntas, que es la desigualdad triangular). Esa región ocupa un cuarto del espacio muestral. La condición "ninguna pieza $>\tfrac12$" es la misma desigualdad triangular disfrazada.

---

## Distancia esperada al centro de un disco

Punto uniforme en un disco de radio $R$. La trampa: el radio **no** es uniforme, porque hay más área lejos del centro. $P(d\le r)=\tfrac{\pi r^2}{\pi R^2}=\tfrac{r^2}{R^2}$, así que la densidad del radio es $f(r)=\tfrac{2r}{R^2}$. Entonces

$$E[d]=\int_0^R r\cdot\frac{2r}{R^2}\,dr=\frac{2R}{3}.$$

---

## Ley del arcoseno (la más contraintuitiva)

Para un movimiento browniano $B_t$ en $[0,1]$, sea $\tau$ la fracción del tiempo que pasa por encima de cero. Uno esperaría que $\tau$ ronde $\tfrac12$ (mitad arriba, mitad abajo). Es al revés:

$$P(\tau\le x)=\frac{2}{\pi}\arcsin(\sqrt x), \qquad \tau\sim\text{Beta}(\tfrac12,\tfrac12),$$

con moda en 0 y en 1. Lo **más** probable es que el browniano pase casi todo el tiempo de un solo lado, no alternando. El azar acumulado es "pegajoso": rachas largas son lo normal, no la excepción.

---

## Mini-ejemplo trabajado: Bertrand y por qué "aleatorio" no basta

¿Probabilidad de que una cuerda al azar de un círculo sea más larga que el lado del triángulo inscrito ($\sqrt3\,R$)? La respuesta depende de **cómo** eliges la cuerda:

- Dos puntos al azar en la circunferencia → $\tfrac13$.
- Punto medio al azar en el disco → $\tfrac14$.
- Distancia al centro al azar en $[0,R]$ → $\tfrac12$.

Los tres cálculos son correctos; lo que cambia es qué objeto se distribuye uniformemente (ángulo, área, radio). "Cuerda aleatoria" no define una probabilidad hasta que fijas el espacio de muestreo.

**Predicción antes de seguir:** ¿es la paradoja de Bertrand un error de cálculo o de planteamiento? Respuesta: de **planteamiento** — la pregunta está mal especificada. Es el mismo defecto que un prior impropio mal definido: sin un modelo probabilístico explícito, el cálculo condicional es inválido aunque el álgebra sea correcta. "Uniforme respecto a qué" es siempre la primera pregunta.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos uniformes → punto en el cuadrado; "qué fracción cumple la condición" es un área (Romeo-Julieta $\tfrac7{16}$, palo roto $\tfrac14$).
- **Contraejemplo (Bertrand):** "elige al azar" sin especificar la geometría no tiene respuesta única.
- **Caso borde (ley del arcoseno):** el browniano NO alterna de signo equitativamente; lo más probable es que pase casi todo el tiempo de un lado ($\text{Beta}(\tfrac12,\tfrac12)$, moda en 0 y 1). El borde desafía la intuición de "se reparte 50/50".

## Errores típicos

- **Conceptual:** suponer "uniforme en el radio" en problemas de disco; la densidad del radio es $\tfrac{2r}{R^2}$ (más área lejos del centro).
- **Técnico:** integrar a ciegas en vez de dibujar la región y restar áreas/triángulos.
- **De supuestos:** confiar en Monte Carlo para 3 decimales con pocas muestras; el error cae como $1/\sqrt n$ ($n\approx10^6$ para 3 decimales).

## Transferencia isomorfa

- **Probabilidad como área ↔ integración Monte Carlo:** estimar $\pi$ con $4\cdot(\text{hits}/n)$ es estimar una integral como fracción de puntos en una región (conecta con [[arena-q10]]).
- **Error Monte Carlo $1/\sqrt n$ ↔ error estándar de la media:** la lentitud de Monte Carlo es la misma $\sqrt n$ del SE y del bootstrap (conecta con [[arena-pst2]]).
- **Ley del arcoseno ↔ movimiento browniano:** la fracción de tiempo positivo de un BM es $\text{Beta}(\tfrac12,\tfrac12)$, un resultado de procesos estocásticos (conecta con [[arena-q11]]).
- **Bertrand (modelo mal definido) ↔ prior impropio:** ambos enseñan que sin un modelo probabilístico explícito el cálculo es vacío (conecta con [[arena-fc3]]).

Moraleja de la arista: *en probabilidad geométrica, dibuja y mide áreas; pero antes pregunta "¿uniforme respecto a qué?" — Bertrand cae si no lo haces.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Aguja sobre líneas paralelas" | Buffon: $\tfrac{2L}{\pi d}$ |
| "$P(\text{dos uniformes están cerca})$" | $2r-r^2$ para $|X-Y|<r$ en $[0,1]$ |
| "Cuerda aleatoria y triángulo" | Bertrand: depende del modelo |
| "Monte Carlo para estimar $\pi$" | $4\times(\text{hits en círculo})/n$ |
| "3 piezas forman triángulo" | $P=\tfrac14$ |
| "Dos personas llegan en $[0,T]$" | $P(\text{encuentro})=1-\big(\tfrac{T-d}{T}\big)^2$ |
| "$E[\text{distancia al centro en disco}]$" | $\tfrac{2R}{3}$ |
| "Fracción del tiempo BM $>0$" | Ley del arcoseno: $\text{Beta}(\tfrac12,\tfrac12)$ |
| "$E[|U-V|]$ para uniformes" | $\tfrac13$ |

---

> **Síntesis:** La probabilidad geométrica conecta el azar con el área/volumen. Resultados clave: Buffon ($\tfrac{2L}{\pi d}$), par uniforme ($2r-r^2$), palo roto ($\tfrac14$), Bertrand (la pregunta mal planteada), Monte Carlo ($4\cdot\text{hits}/n$). La ley del arcoseno es la más contraintuitiva: el browniano no "alterna" — tiende a quedarse en el mismo semiplano.

---

*Retrieval: cierra y responde: (1) $P(\text{aguja de longitud 1 cruza líneas separadas 2})$; (2) $P(|X-Y|<0.5)$ para $X,Y\sim\text{Unif}[0,1]$; (3) $P(\text{palo roto forma triángulo})$; (4) $E[\text{distancia Manhattan en }[0,1]^2]$.*
