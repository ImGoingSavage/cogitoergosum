# Apuestas, colas y azar

## De qué trata (y qué sabrás hacer)

Este bloque revela una grieta entre dos cosas que la intuición confunde: **probabilidad** ("¿pasa?") y **esperanza** ("¿en cuánto tiempo / con qué valor medio?"). Verás casos donde algo pasa con probabilidad 1 pero su tiempo esperado es infinito, y estrategias que parecen infalibles pero no crean valor. También entra la teoría de colas, que gobierna la latencia de cualquier sistema con llegadas y servicio.

Al terminar sabrás calcular la ventaja de la casa en juegos, por qué la martingala (doblar) no funciona, cómo crecen las rachas, y la Ley de Little ($L=\lambda W$) que ata cola y espera en todo sistema estable. Cada idea se construye desde un caso concreto.

---

## Chuck-a-luck — esperanza negativa garantizada

Apuestas \$1 a un número $k$ y se tiran tres dados; cobras \$1 por cada dado que muestre $k$, y pierdes tu \$1 si ninguno sale. La intuición ("si aparece, gano") olvida ponderar por la frecuencia. Con $P(j\text{ aciertos})$ binomial$(3,\tfrac16)$:

$$E=(-1)\tfrac{125}{216}+(1)\tfrac{75}{216}+(2)\tfrac{15}{216}+(3)\tfrac{1}{216}=-\frac{17}{216}\approx -7.9\%.$$

Pierdes casi 8 centavos por dólar: el "si aparece gano" es una ilusión porque lo más probable ($\approx58\%$) es que no aparezca ninguno.

---

## Juego audaz vs. tímido

Juegas con desventaja ($p<\tfrac12$) y quieres pasar de \$$k$ a \$$N$. Sorprendentemente, **apostar fuerte es mejor que apostar poco**:
- **Tímido** (\$1 por ronda): das al casino muchísimas oportunidades de erosionarte; $P(\text{éxito})$ es exponencialmente mala.
- **Audaz** (apuesta el máximo que te acerque a la meta): minimiza el número de rondas y por tanto la mordida acumulada del casino.

Para $p=0.4$, $k=10$, $N=20$: audaz $\approx40\%$, tímido $\approx0.003\%$. Con la casa en contra, cuanto menos juegues, mejor.

---

## Estrategia de doblaje (martingala)

Apuesta \$1; si pierdes, dobla; si ganas, recuperas \$1 neto y reinicias. Parece infalible. Con capital finito $M$:

$$E[\text{resultado}]=(-M)\,P(\text{ruina})+1\cdot P(\text{ganar})=0$$

en un juego justo. La martingala **no crea valor esperado**; solo transfiere el riesgo a una cola pesada: casi siempre ganas \$1, y de vez en cuando lo pierdes todo. La suma cuadra exactamente en cero (o negativo con comisión).

---

## Rachas de caras en $n$ lanzamientos

Moneda justa, $n$ tiros. ¿Longitud esperada de la racha más larga de caras? Hay $\approx n$ ventanas donde podría empezar una racha de $k$, cada una con probabilidad $2^{-k}$; esperas ver una cuando $n\cdot 2^{-k}\approx1$:

$$E[\text{racha máxima}]\approx \log_2 n.$$

Para $n=1000$: $\approx10$; para $n\approx10^6$: $\approx20$. Las rachas son más frecuentes de lo que la intuición sugiere — 10 caras seguidas son **esperables** en muestras grandes, no una anomalía.

---

## Tiempo de primer retorno a 0

Caminata aleatoria simétrica. La probabilidad de volver al origen en exactamente $2n$ pasos es $\binom{2n}{n}/4^n$. Lo notable:

$$P(\text{volver alguna vez})=1, \qquad E[T_0]=\infty.$$

Vuelve **seguro**, pero el tiempo esperado de retorno es **infinito** (se llama recurrencia nula). Es la grieta probabilidad/esperanza en estado puro, y la versión discreta del primer toque del browniano (conecta con [[arena-p3]]).

---

## Colas M/M/1

Llegadas a tasa $\lambda$, servicio a tasa $\mu$, **utilización** $\rho=\lambda/\mu$ (estable solo si $\rho<1$). En equilibrio:

| Métrica | Fórmula |
|---------|---------|
| $P(\text{vacío})$ | $1-\rho$ |
| $E[\text{en sistema}]\ L$ | $\rho/(1-\rho)$ |
| $E[\text{en cola}]\ L_q$ | $\rho^2/(1-\rho)$ |
| $E[\text{tiempo en sistema}]\ W$ | $1/(\mu-\lambda)$ |

La **Ley de Little** ata todo: $L=\lambda W$ (en cualquier sistema en equilibrio, sin asumir la distribución de servicio). Lo crítico es que $L=\rho/(1-\rho)$ **explota** cuando $\rho\to1$: cerca de la saturación, un poco más de carga multiplica la espera.

---

## El problema del ascensor (ocupación)

$k$ ascensores, $m$ personas; cada una elige uno al azar. ¿Cuántos ascensores se usan? Un ascensor queda sin usar si las $m$ personas lo evitan ($(1-1/k)^m$), así que

$$E[\text{ascensores usados}]=k\left(1-\left(1-\tfrac1k\right)^m\right).$$

Para $k=m=10$: $\approx6.5$. Es el mismo conteo que cajas y bolas (conecta con [[arena-fc1]]).

---

## Mini-ejemplo trabajado: la Ley de Little en una cola M/M/1

Un servidor recibe $\lambda=4$ solicitudes/hora y atiende a $\mu=5$/hora. La utilización $\rho=\lambda/\mu=0.8$. Las métricas salen casi solas:

- $E[\text{en sistema}]\ L=\rho/(1-\rho)=0.8/0.2=4$ solicitudes.
- $E[\text{tiempo en sistema}]\ W=1/(\mu-\lambda)=1/(5-4)=1$ hora.
- Verifica con **Ley de Little**: $L=\lambda W=4\times1=4$. ✓

Little ($L=\lambda W$) conecta cuántos hay en el sistema con cuánto esperan, sin asumir la distribución de servicio — vale en cualquier sistema en equilibrio.

**Predicción antes de seguir:** si la utilización sube de $\rho=0.8$ a $\rho=0.95$, ¿el tiempo de espera sube $\sim19\%$ o se dispara? Respuesta: **se dispara** — $L=\rho/(1-\rho)$ explota cuando $\rho\to1$ (de 4 a 19 en sistema). La latencia no crece lineal con la carga; cerca de la saturación, una pizca más de tráfico multiplica la espera. Por eso los sistemas se mantienen lejos de $\rho=1$ (conecta con [[arena-sre4]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sistema de llegadas/servicio en equilibrio → M/M/1 + Ley de Little ($L=\lambda W$); estable solo si $\rho<1$.
- **Contraejemplo (martingala "infalible"):** doblar tras cada pérdida parece garantizar ganar \$1, pero con capital finito $E[\text{pérdida}]$ no es positiva; solo empuja el riesgo a una cola rara y enorme (ruina = pierdes todo).
- **Caso borde (recurrencia nula):** la caminata aleatoria vuelve al origen con probabilidad 1, pero $E[T_0]=\infty$. El borde separa "seguro que pasa" de "en tiempo esperado finito".

## Errores típicos

- **Conceptual:** creer que la martingala (doblar) crea valor esperado positivo; solo redistribuye riesgo a la cola.
- **Técnico:** con desventaja ($p<\tfrac12$), jugar tímido (apostar poco muchas veces); el juego audaz domina porque da menos oportunidades a la casa.
- **De interpretación:** subestimar rachas: la racha más larga en $n$ lanzamientos crece como $\log_2 n$, así que 10+ caras seguidas son esperables con $n$ grande.

## Transferencia isomorfa

- **Ley de Little ($L=\lambda W$) ↔ throughput/latencia de sistemas:** "cuántos en vuelo $=$ tasa $\times$ tiempo" gobierna colas de servidores, pipelines y SLAs (conecta con [[arena-sre4]]).
- **Martingala $E[\text{pérdida}]=\infty$ ↔ San Petersburgo / media divergente:** doblar es primo de la paradoja de San Petersburgo; cola pesada que rompe "media = típico" (conecta con [[arena-q8]]).
- **Ruina del jugador / duración $k(N-k)$ ↔ parada óptima por martingala:** la probabilidad de absorción lineal y la duración cuadrática salen del muestreo opcional (conecta con [[arena-q11]]).
- **Problema del ascensor $k(1-(1-1/k)^m)$ ↔ ocupación y hashing:** cuántos contenedores se usan es el mismo conteo que cajas/bolas y colisiones (conecta con [[arena-fc1]]).

Moraleja de la arista: *la Ley de Little ata cola y espera en cualquier sistema estable, y la latencia se dispara cerca de $\rho=1$; ninguna martingala vence una esperanza negativa, solo esconde el riesgo en la cola.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "$E[\text{Chuck-a-luck}]$" | $-17/216\approx-7.9\%$ |
| "$p<0.5$, ¿tímido o audaz?" | Audaz siempre domina |
| "¿Martingala garantiza ganar?" | $E[\text{pérdida}]$ no es positiva con capital finito |
| "Racha más larga en $n$ lanzamientos" | $\approx\log_2 n$ |
| "$E[T_0]$ caminata aleatoria" | $\infty$ (recurrente nula) |
| "M/M/1 estable con $\rho=\lambda/\mu$" | $L=\rho/(1-\rho)$, $W=1/(\mu-\lambda)$ |
| "$E[\text{ascensores usados}]$" | $k(1-(1-1/k)^m)$ |
| "$E[\text{duración ruina}]$, $p=\tfrac12$, inicio $k$" | $k(N-k)$ |

---

> **Síntesis:** Las apuestas y colas revelan la asimetría entre probabilidad y esperanza: $P=1$ de volver al origen, pero $E[T]=\infty$. Con desventaja, el juego audaz domina al tímido. La martingala no crea valor: redistribuye riesgo hacia la cola. En colas M/M/1, la Ley de Little ($L=\lambda W$) conecta todas las métricas; $\rho<1$ es condición de estabilidad.

---

*Retrieval: cierra y responde: (1) la esperanza de Chuck-a-luck por apuesta de \$1; (2) $E[L]$ para M/M/1 con $\lambda=3$, $\mu=4$; (3) racha máxima esperada en $n=2^{16}$ tiros; (4) por qué $E[T_0]=\infty$ pero el retorno es seguro.*
