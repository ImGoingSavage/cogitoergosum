# Cálculo y álgebra lineal para finanzas cuantitativas

## De qué trata (y qué sabrás hacer)

Detrás de casi toda fórmula financiera hay una idea sencilla del cálculo o del álgebra lineal: una **derivada** que mide sensibilidad, una **serie de Taylor** que aproxima lo no lineal, o una **descomposición de matriz** que encuentra los ejes del riesgo. Esta lección reúne ese kit, pero construyendo cada herramienta desde su intuición antes de la fórmula, y mostrando que delta/gamma de una opción son literalmente la primera y segunda derivada.

Al terminar sabrás aproximar funciones con Taylor (y leer los Greeks como sus términos), resolver integrales clave, y entender qué hacen los valores propios (traza, determinante, PCA). Cada idea se ancla en un ejemplo.

---

## Series de Taylor esenciales

Una serie de Taylor aproxima una función cerca de un punto con un polinomio: el valor, más la pendiente, más la curvatura, etc. Las que más aparecen (alrededor de 0):

| Función | Expansión | Converge si |
|---------|-----------|-------------|
| $e^x$ | $1+x+\tfrac{x^2}{2!}+\tfrac{x^3}{3!}+\cdots$ | todo $x$ |
| $\sin x$ | $x-\tfrac{x^3}{6}+\tfrac{x^5}{120}-\cdots$ | todo $x$ |
| $\ln(1+x)$ | $x-\tfrac{x^2}{2}+\tfrac{x^3}{3}-\cdots$ | $\lvert x\rvert<1$ |
| $(1+x)^\alpha$ | $1+\alpha x+\tfrac{\alpha(\alpha-1)}{2}x^2+\cdots$ | $\lvert x\rvert<1$ |

Para $e^{0.1}$: $1+0.1+0.005+0.000167\approx1.10517$ (error $\approx4\times10^{-6}$). Truncar en pocos términos basta cuando $x$ es pequeño.

---

## Taylor aplicado a opciones — los Greeks como derivadas

¿Cómo cambia el precio $C(S)$ de una opción ante un movimiento $\Delta S$ del subyacente? Expande en Taylor:

$$C(S+\Delta S)\approx C(S)+\underbrace{\Delta}_{\partial C/\partial S}\cdot\Delta S+\tfrac12\underbrace{\Gamma}_{\partial^2 C/\partial S^2}(\Delta S)^2.$$

**Delta** es la sensibilidad lineal; **gamma** es la curvatura. Un portafolio delta-neutral (long call, short $\Delta$ acciones) borra el término lineal y deja $\Delta\text{P\&L}\approx\tfrac12\Gamma(\Delta S)^2+\Theta\,dt$: con $\Gamma>0$ ganas con movimientos grandes en cualquier dirección, pero pagas $\Theta<0$ (el tiempo corroe). Toda la "magia" de los Greeks es Taylor truncado en el segundo término (conecta con la duración/convexidad de [[arena-q7]]).

---

## Integral gaussiana

La integral que normaliza la campana de Gauss:

$$\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt\pi.$$

El truco es elevarla al cuadrado y pasar a coordenadas polares: $I^2=\iint e^{-(x^2+y^2)}\,dx\,dy=\int_0^{2\pi}\!\int_0^\infty e^{-r^2}r\,dr\,d\theta=\pi$, de donde $I=\sqrt\pi$. Consecuencia directa: $\int_{-\infty}^\infty e^{-x^2/2}\,dx=\sqrt{2\pi}$, la constante de normalización de $N(0,1)$.

---

## Álgebra lineal — valores propios

Un **valor propio** $\lambda$ de una matriz $A$ es un factor de estiramiento a lo largo de una dirección especial (su vector propio): $Av=\lambda v$. Dos identidades que conviene saber de memoria:

$$\det(A)=\prod_i\lambda_i, \qquad \operatorname{tr}(A)=\sum_i\lambda_i.$$

El determinante es el producto de los estiramientos (volumen); la traza, su suma. Para una matriz **simétrica** (como toda covarianza), los valores propios son reales y los vectores propios ortogonales.

---

## Matrices semidefinidas positivas y PCA

Una matriz $A$ es **semidefinida positiva** si $x^\top A x\ge0$ para todo $x$ (equivalente: todos sus valores propios $\ge0$). Toda **matriz de covarianza** $\Sigma$ lo es, porque $x^\top\Sigma x=\text{Var}(x^\top X)\ge0$ — la varianza de cualquier combinación lineal no puede ser negativa (por eso no puedes inventar correlaciones, conecta con [[arena-q9]]).

El **PCA** (análisis de componentes principales) es la descomposición espectral de $\Sigma$: $\Sigma=P\Lambda P^\top$. Los vectores propios son las direcciones de máxima varianza (componentes principales) y los valores propios $\lambda_i$ son la varianza explicada por cada una. Ejemplo: la curva de tasas de interés tiene 3 componentes (nivel, pendiente, curvatura) que explican $>95\%$ del movimiento.

---

## Newton–Raphson

Para resolver $f(x)=0$, iteras siguiendo la tangente:

$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.$$

La convergencia es **cuadrática**: el número de dígitos correctos se duplica en cada paso. Para $f(x)=x^2-2$ (hallar $\sqrt2$), partiendo de $1.5$: $1.41667\to1.41422\to1.41421356\ldots$ en tres pasos. Es el mismo método que ajusta una regresión logística o maximiza una log-verosimilitud (conecta con [[arena-dg2]]).

---

## Función generatriz de momentos

La **mgf** $M_X(t)=E[e^{tX}]$ codifica todos los momentos ($E[X^n]=M_X^{(n)}(0)$) y convierte la suma de variables independientes en producto. Para la normal, $M_X(t)=e^{\mu t+\sigma^2 t^2/2}$, así que $E[e^X]=M_X(1)=e^{\mu+\sigma^2/2}$ — el puente directo a la valoración lognormal y a la prima de Jensen (conecta con [[arena-q7]]).

---

## Mini-ejemplo trabajado: Taylor convierte una opción en $\Delta$ y $\Gamma$

¿Cómo cambia el precio de una opción $C(S)$ ante un movimiento $\Delta S$ del subyacente? Expande en Taylor alrededor de $S$:

$$C(S+\Delta S)\approx C(S)+\Delta\cdot\Delta S+\tfrac12\Gamma(\Delta S)^2,$$

donde $\Delta=\partial C/\partial S$ y $\Gamma=\partial^2 C/\partial S^2$. La **primera derivada** (delta) es la sensibilidad lineal; la **segunda** (gamma) es la curvatura. Un portafolio delta-neutral (long call, short $\Delta$ acciones) borra el término lineal y deja:

$$\Delta\text{P\&L}\approx\tfrac12\Gamma(\Delta S)^2+\Theta\,dt.$$

Con $\Gamma>0$ (long gamma) ganas con movimientos grandes en cualquier dirección, pero pagas $\Theta<0$ (el tiempo corroe). Toda la "magia" de los Greeks es una serie de Taylor truncada en el segundo término.

**Predicción antes de seguir:** ¿reconoces $\Delta$ y $\Gamma$ de algún otro instrumento? Respuesta: son **exactamente** la duración y la convexidad de un bono — primera y segunda derivada del precio frente a su factor de riesgo. Delta↔duración, gamma↔convexidad, theta↔carry. Una vez ves "Taylor de primer y segundo orden", el bono y la opción son el mismo objeto.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sensibilidad de un precio a un factor → Taylor: primer orden ($\Delta$/duración) + segundo orden ($\Gamma$/convexidad).
- **Contraejemplo (PCA y escala):** la descomposición espectral de $\Sigma$ supone features comparables; sin estandarizar, la variable de unidades grandes domina las componentes. PCA "sin escalar" engaña.
- **Caso borde (covarianza singular):** si una variable es combinación lineal de otras (multicolinealidad perfecta), $\Sigma$ tiene un valor propio 0 (semidefinida, no definida) y no es invertible. El borde conecta álgebra lineal con colinealidad.

## Errores típicos

- **Conceptual:** confundir media y mediana de una lognormal: $E[e^X]=e^{\mu+\sigma^2/2}>e^\mu$ por la convexidad (Jensen).
- **Técnico:** usar L'Hôpital donde Taylor es inmediato ($\lim(e^x-1-x)/x^2=\tfrac12$ sale de $e^x-1-x\approx x^2/2$).
- **De supuestos:** aplicar Monte Carlo esperando convergencia rápida; el error cae como $1/\sqrt N$ (su ventaja es la dimensión, no la velocidad).

## Transferencia isomorfa

- **Taylor → $\Delta,\Gamma$ ↔ duración y convexidad:** primera y segunda derivada del precio son los mismos Greeks de un bono (conecta con [[arena-q7]]).
- **Descomposición espectral (PCA) ↔ matriz de covarianza PSD:** las componentes son vectores propios de $\Sigma$, semidefinida positiva porque $x^\top\Sigma x=\text{Var}(x^\top X)\ge0$ (conecta con [[arena-q9]] y [[arena-q6]]).
- **mgf gaussiana $e^{\mu t+\sigma^2 t^2/2}$ ↔ valoración lognormal:** evaluarla en $t=1$ da $E[e^X]$, el puente a la prima de Jensen (conecta con [[arena-q7]]).
- **Newton–Raphson ↔ optimización del MLE:** resolver $f'(\theta)=0$ con convergencia cuadrática es cómo se ajusta una logística o se maximiza una log-verosimilitud (conecta con [[arena-dg2]]).

Moraleja de la arista: *casi todo es una derivada: delta/gamma son duración/convexidad, PCA son los ejes de la covarianza, y el segundo orden de Taylor es donde vive la convexidad.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Aproximar $e^x$ cerca de 0" | $1+x+\tfrac{x^2}{2}+\tfrac{x^3}{6}$ |
| "P&L de portafolio con opción" | $\tfrac12\Gamma(\Delta S)^2+\Theta\,dt$ |
| "$\int e^{-x^2}dx$ completo" | $\sqrt\pi$ (truco 2D polar) |
| "det y tr de $A$" | $\prod\lambda_i$ y $\sum\lambda_i$ |
| "Raíz de $f(x)=0$" | Newton–Raphson: convergencia cuadrática |
| "$E[e^X]$ para $X\sim N(\mu,\sigma^2)$" | $e^{\mu+\sigma^2/2}$ (desde mgf) |
| "PCA de $\Sigma$" | Vectores propios de $\Sigma$; varianza = valor propio |

---

> **Síntesis:** El cálculo y el álgebra lineal son el lenguaje de las finanzas cuantitativas. Taylor traduce no-linealidades en $\Delta$ y $\Gamma$; el lema de Itô extiende Taylor al ruido estocástico; la descomposición espectral (PCA) reduce dimensión; la mgf codifica todos los momentos. La integral gaussiana ($\sqrt\pi$) conecta el análisis real con la normal — la base de todo.

---

*Retrieval: sin mirar: (1) Taylor de $e^x$ hasta el 3.er término; (2) $\operatorname{tr}(A)$ y $\det(A)$ para $A=\big(\begin{smallmatrix}2&1\\1&3\end{smallmatrix}\big)$; (3) $x_1$ de Newton–Raphson en $x^2-3=0$ desde $x_0=2$; (4) qué mide cada valor propio de $\Sigma$ en PCA.*
