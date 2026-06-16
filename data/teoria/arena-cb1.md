# Suficiencia, estadísticos completos y el principio de verosimilitud

## De qué trata esta lección (y qué sabrás hacer al final)

Cuando estimas un parámetro, no todos los detalles de tus datos importan: parte es señal sobre $\theta$ y parte es ruido. Esta lección construye, desde cero, la teoría que separa una cosa de la otra: la **suficiencia** (qué resumen de los datos contiene toda la información sobre $\theta$), la **completitud** (cuándo ese resumen es además único) y el **teorema de Basu** (cómo la completitud regala independencias gratis). Es la maquinaria fina detrás de "el mejor estimador insesgado".

Al terminar podrás: (1) usar el criterio de factorización para detectar un estadístico suficiente; (2) reconocer la familia exponencial como el lugar donde la suficiencia se comprime a dimensión fija; (3) distinguir suficiente de completo y entender por qué hace falta lo segundo para el UMVUE; y (4) aplicar Basu para deducir independencias sin integrar. Cada concepto entra por un ejemplo. Los teoremas duros (completitud, Basu) van en `[CAJA NEGRA OK]`: la intuición es obligatoria; la prueba, opcional.

> Esta lección es la capa profunda de la suficiencia que [[arena-dg1]] introdujo y que [[arena-cb2]] usará para construir UMVUEs.

---

## Estadístico suficiente

Vuelve al ejemplo raíz: lanzas una moneda 5 veces y sale $(1,0,1,1,0)$. Para estimar $p$, ¿importa el **orden**? No: basta saber que hubo **3 éxitos**. El total $\sum X_i$ ya contiene toda la información sobre $p$; las posiciones son ruido. Eso es la **suficiencia**: $T(X)$ es suficiente para $\theta$ si, sabiendo $T$, los datos crudos no añaden nada más sobre $\theta$ (la distribución de $X$ dado $T=t$ no depende de $\theta$).

Detectarlo con la definición es engorroso; el atajo es el **criterio de factorización (Fisher-Neyman):**

$$f(x\mid\theta) = g(T(x),\theta)\cdot h(x).$$

$T$ es suficiente si y solo si la densidad se parte así, con toda la dependencia de $\theta$ encerrada en $g$ (a través de $T$) y un factor $h(x)$ libre de $\theta$. Dicho de otro modo: **la verosimilitud solo toca los datos a través de $T(x)$**.

| Distribución | Estadístico suficiente |
|-------------|----------------------|
| Bernoulli$(p)$ | $T=\sum X_i$ |
| Normal $N(\mu,\sigma^2)$ — ambos desconocidos | $T=(\sum X_i,\ \sum X_i^2)$ |
| Poisson$(\lambda)$ | $T=\sum X_i$ |
| Uniforme$[0,\theta]$ | $T=X_{(n)}=\max X_i$ |
| Gamma$(\alpha,\beta)$ — $\alpha$ conocida | $T=\sum X_i$ |

---

## Familias exponenciales

La razón de que tantos suficientes sean sumas: pertenecen a la **familia exponencial**

$$f(x\mid\theta)=h(x)\,c(\theta)\,\exp\!\Big(\sum_k w_k(\theta)\,t_k(x)\Big),$$

cuyos estadísticos suficientes son $T=\big(\sum t_1(X_i),\dots,\sum t_k(X_i)\big)$ — sumas de las funciones $t_k$. Toda la tabla anterior es familia exponencial **salvo la uniforme** (cuyo soporte depende de $\theta$, lo que la deja fuera). Esta es la clave de por qué la uniforme se comporta distinto en casi todos los teoremas.

---

## Estadístico minimal suficiente

Puede haber muchos estadísticos suficientes (los datos completos lo son, trivialmente). El **minimal suficiente** es la **compresión máxima**: es función de cualquier otro suficiente, así que no se puede comprimir más sin perder información sobre $\theta$.

`[CAJA NEGRA OK]` — asume el criterio; su prueba no aporta a usarlo. **Criterio de Lehmann-Scheffé:** $T(x)$ es minimal suficiente cuando el cociente de verosimilitudes $L(\theta\mid x)/L(\theta\mid y)$ **no depende de $\theta$** exactamente si $T(x)=T(y)$. Intuición: dos muestras son "equivalentes para $\theta$" precisamente cuando tienen el mismo $T$.

| Distribución | Minimal suficiente |
|-------------|-------------------------------|
| Normal $N(\mu,\sigma^2)$ | $(\bar X,\ S^2)$ |
| Cauchy$(\theta,1)$ | estadísticos de orden $(X_{(1)},\dots,X_{(n)})$ |
| Uniforme $U(\theta,\theta+1)$ | $(X_{(1)},\ X_{(n)})$ |

Observa el caso Cauchy: **no hay compresión**. Hay que retener *todos* los datos ordenados. Fuera de la familia exponencial, la naturaleza no siempre te deja resumir.

---

## Completitud

Suficiente no es suficiente (valga el juego) para garantizar **unicidad**. Para eso está la **completitud**, una condición técnica con una lectura simple: el estadístico $T$ es completo si **ningún cambio de variable no trivial de $T$ tiene esperanza cero para todo $\theta$**. Formalmente:

$$E[g(T)]=0\ \text{ para todo }\theta\ \Longrightarrow\ g(T)=0\ \text{(casi seguramente)}.$$

`[CAJA NEGRA OK]` — *Qué asumir:* que la completitud convierte "una función insesgada de $T$" en "**la única** función insesgada de $T$". *Por qué importa:* sin unicidad no hay "mejor estimador" bien definido. *Regla práctica:* las **familias exponenciales de rango completo** tienen estadístico suficiente **completo** — así que en la práctica casi siempre lo tienes.

- **Ejemplo:** $N(\mu,\sigma^2)$ con ambos desconocidos: $T=(\sum X_i,\sum X_i^2)$ es suficiente **y completo**.
- **Contraejemplo:** $N(\theta,a\theta^2)$ con $a$ conocido: $(\sum X_i,\sum X_i^2)$ es suficiente pero **no completo**, porque el espacio de parámetros es una curva (no un abierto): existe una combinación de $T$ con esperanza cero. Suficiente sin completo no basta para el UMVUE.

---

## Estadístico ancilario

El opuesto de un suficiente: un estadístico $V(X)$ es **ancilario** para $\theta$ si su distribución **no depende de $\theta$** — es ciego al parámetro. Ejemplos:

- $X_1-X_2$ en una familia de **localización** (un corrimiento de $\theta$ cancela en la diferencia).
- $S^2$ en $N(\mu,\sigma^2)$ cuando estimas $\mu$ con $\sigma^2$ conocida (la dispersión no informa de la media).
- $(X_i-\bar X)/S$ en cualquier familia de localización-escala.

¿Para qué sirve algo que ignora $\theta$? Para construir **pivotes** (intervalos de confianza, ver [[arena-cb4]]) y, vía Basu, para deducir independencias.

---

## Teorema de Basu

`[CAJA NEGRA OK]` — un resultado tan útil como su prueba es prescindible para usarlo.

**Si $T$ es completo y suficiente, y $V$ es ancilario, entonces $T$ y $V$ son independientes.** La intuición: $T$ contiene toda la información de $\theta$ y $V$ no contiene ninguna; siendo $T$ además *completo* (no le sobra estructura), no queda nada que los ligue. Aplicaciones clásicas que de otro modo requerirían integrales feas:

- $\bar X \perp S^2$ en la normal (la media muestral y la varianza muestral son independientes — un hecho central en la construcción de la $t$-Student).

---

## Principio de suficiencia y de verosimilitud

Dos principios que cierran la lógica del capítulo:

- **Principio de suficiencia:** si $T(x)=T(y)$, cualquier inferencia sobre $\theta$ **debe ser la misma** para $x$ que para $y$. Lo que el suficiente borra es, por definición, irrelevante.
- **Principio de verosimilitud (Birnbaum):** toda la información de los datos sobre $\theta$ está en la **función de verosimilitud** $L(\theta\mid x)\propto f(x\mid\theta)$. Dos datasets con la misma $L$ (salvo constante) deben dar la misma inferencia.

Consecuencia: en familias regulares, la verosimilitud es uno-a-uno con el minimal suficiente. Es el fundamento de comparar modelos por razón de verosimilitudes ([[arena-cb3]]).

---

## Mini-ejemplo trabajado: por qué ΣXᵢ basta (factorización)

n monedas Bernoulli(p), datos x=(1,0,1,1,0). La verosimilitud es:

> L(p|x) = ∏ p^{xᵢ}(1−p)^{1−xᵢ} = p^{Σxᵢ}(1−p)^{n−Σxᵢ}

Toda la dependencia de x entra **solo a través de Σxᵢ = 3**: dos muestras distintas con el mismo total (p. ej. (1,1,1,0,0)) dan exactamente la misma verosimilitud. Por el criterio de factorización f(x|p)=g(T,p)·h(x) con g=p^T(1−p)^{n−T} y h(x)=1, T=ΣXᵢ es **suficiente**. El orden y las posiciones de los 1 son "ruido" irrelevante para p.

**Predicción antes de seguir:** ¿el suficiente es siempre una suma/promedio? Respuesta: **no**. Para Uniforme[0,θ] el suficiente es el **máximo** X₍ₙ₎, no la suma; para la Cauchy ningún resumen comprime y hay que retener *todos* los estadísticos de orden. La forma del suficiente la dicta la familia, y fuera de la exponencial puede no haber compresión. (Caja negra: que la familia exponencial sea la única con suficiente de dimensión fija —Pitman-Koopman-Darmois— asúmelo por ahora; lo que importa es la intuición "comprime sin perder θ".)

## Prototipo, contraejemplo y caso borde

- **Prototipo:** familia exponencial → T=(Σt₁(Xᵢ),…) suficiente y, si es de rango completo, **completo** → habilita Lehmann-Scheffé.
- **Contraejemplo (suficiente pero no completo):** N(θ, aθ²) con a fijo: (ΣXᵢ, ΣXᵢ²) es suficiente pero NO completo porque el espacio paramétrico es una curva, no un abierto. Suficiente no garantiza UMVUE único.
- **Caso borde (ancilario):** S²/σ² no informa de μ pero su distribución es libre de μ → es **ancilario**; por Basu, X̄ ⊥ S² en la normal. El borde muestra que un estadístico puede ignorar por completo el parámetro.

## Errores típicos

- **Conceptual:** confundir suficiente (captura θ) con completo (unicidad); se necesita completo *además* de suficiente para Lehmann-Scheffé.
- **Técnico:** olvidar el factor h(x) al factorizar, o intentar derivar el suficiente cuando el soporte depende de θ (Uniforme).
- **De supuestos:** aplicar Basu sin verificar que T sea completo *y* suficiente y V ancilario.

## Transferencia isomorfa

- **Estadístico suficiente ↔ estado mínimo / compresión de features:** T(X) resume los datos sin perder información sobre θ, igual que un estado markoviano resume la historia o un embedding resume una entrada (conecta con [[arena-b4]] y [[arena-dg1]]).
- **Ancilario ↔ pivote:** un estadístico cuya distribución no depende de θ es la materia prima de un pivote para construir intervalos de confianza (conecta con [[arena-cb4]]).
- **Familia exponencial ↔ GLM y conjugación:** la forma h(x)exp(η·T−A) es la misma que da suficientes compactos, priors conjugados y los modelos lineales generalizados (conecta con [[arena-b4]]).
- **Principio de verosimilitud ↔ "solo la verosimilitud importa":** dos datasets con la misma L dan la misma inferencia — el fundamento de comparar modelos por razón de verosimilitudes (conecta con [[arena-cb3]]).

Moraleja de la arista: *el suficiente comprime los datos a lo que importa de θ; la completitud lo vuelve único; y un ancilario —ciego a θ— es la semilla de un pivote.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Captura toda la info de θ?" | Estadístico suficiente (factorización) |
| "¿La densidad es de la familia exponencial?" | T = (Σt₁(Xᵢ),…,Σtₖ(Xᵢ)) es suficiente |
| "¿Compresión máxima sin pérdida?" | Minimal suficiente (criterio de cociente) |
| "E[g(T)]=0 para todo θ implica g=0" | Completo — habilita Lehmann-Scheffé |
| "Independencia entre estadísticos" | Basu: uno completo suficiente, otro ancilario |
| "La distribución de V no depende de θ" | V es ancilario |

---

> **Síntesis (Casella & Berger, Ch 6):** La suficiencia comprime; la completitud garantiza unicidad; Basu conecta completitud con independencia. La familia exponencial es el laboratorio donde todo esto funciona limpiamente. Para familias fuera de la exponencial (Cauchy, uniforme en intervalo desconocido) los estadísticos de orden son el refugio.

---

*Retrieval: cierra y responde: (1) ¿Cuál es el estadístico suficiente de una Poisson(λ) con n observaciones? (2) ¿Qué condición hace que T=(ΣXᵢ,ΣXᵢ²) NO sea completo en N(θ,aθ²)? (3) Enuncia el teorema de Basu y da un ejemplo. (4) ¿Por qué los estadísticos de orden son minimales suficientes para la Cauchy?*
