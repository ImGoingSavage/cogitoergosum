# Linealidad de la esperanza bajo presión

## El teorema y su fuerza oculta

La linealidad de la esperanza dice algo que parece simple pero tiene una consecuencia extraordinaria:

$$E[X + Y] = E[X] + E[Y]$$

Para **cualquier** X e Y con esperanzas finitas. Sin condición de independencia.

Esto importa porque en casi todos los problemas de entrevista, las variables *no* son independientes. Pero la linealidad no lo necesita.

**Demostración (caso discreto):**

$$E[X+Y] = \sum_{x,y}(x+y)\cdot P(X=x, Y=y)$$
$$= \sum_{x,y} x \cdot P(X=x,Y=y) + \sum_{x,y} y \cdot P(X=x,Y=y)$$
$$= \sum_x x \sum_y P(X=x,Y=y) + \sum_y y \sum_x P(X=x,Y=y)$$
$$= \sum_x x \cdot P(X=x) + \sum_y y \cdot P(Y=y) = E[X] + E[Y]$$

No aparece ninguna asunción de independencia. Solo la linealidad de la suma y la marginación de la distribución conjunta.

---

## La técnica de las variables indicadoras

Es la aplicación más poderosa de la linealidad. La señal de reconocimiento:

> "¿Cuántos objetos de un conjunto cumplen una propiedad aleatoria?"

Si X = número de objetos que cumplen la propiedad, define **un indicador por objeto**:

$$I_k = \begin{cases} 1 & \text{si el objeto } k \text{ cumple la propiedad} \\ 0 & \text{en caso contrario} \end{cases}$$

Entonces:
$$X = I_1 + I_2 + \cdots + I_n$$
$$E[X] = E[I_1] + E[I_2] + \cdots + E[I_n] = P(I_1=1) + P(I_2=1) + \cdots + P(I_n=1)$$

---

## Ejemplo canónico: el problema del sombrero

*n* personas lanzan sus sombreros al centro. Cada persona toma uno al azar. ¿Cuántas personas esperan recuperar su propio sombrero?

**Señal detectada:** "¿cuántas de n personas recuperan su objeto?"

**Jugada:** indicador por persona.

$$I_k = 1 \text{ si la persona } k \text{ recupera su sombrero}$$
$$P(I_k = 1) = \frac{1}{n} \text{ (su sombrero está entre los } n \text{ disponibles)}$$
$$E[\text{total}] = n \cdot \frac{1}{n} = 1$$

Para cualquier *n*. La respuesta es siempre **1**.

Nota: los $I_k$ no son independientes (si todos recuperaron el suyo excepto uno, ese uno también lo recuperó). Pero la linealidad no lo necesita.

---

## Ejemplo: valor esperado del máximo de dos dados

Dos dados justos de 6 caras. Sea $M = \max(D_1, D_2)$.

**Método con indicadores:** definir $J_k = 1$ si $M \geq k$, para $k = 1,\ldots,6$.

$$M = J_1 + J_2 + J_3 + J_4 + J_5 + J_6$$
$$E[M] = \sum_{k=1}^{6} P(M \geq k) = \sum_{k=1}^{6} \left[1 - P(M < k)\right]$$
$$P(M < k) = P(D_1 < k) \cdot P(D_2 < k) = \left(\frac{k-1}{6}\right)^2$$

$$E[M] = 6 - \frac{1}{36}(0 + 1 + 4 + 9 + 16 + 25) = 6 - \frac{55}{36} = \frac{161}{36} \approx 4.47$$

---

## La trampa más frecuente en entrevistas

El entrevistador te da un problema con variables que claramente dependen entre sí. Muchos candidatos dicen:

*"No puedo calcular E[X] porque X e Y no son independientes."*

**Eso es incorrecto.** La independencia afecta la **varianza**, no la **media**.

$$\text{Var}(X+Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X,Y)$$

Aquí sí aparece la covarianza. Si te piden varianza, sí necesitas información sobre la dependencia. Si te piden media, no.

### [CAJA NEGRA OK] Ley de varianza total (Eve's law)

- **Qué puedes asumir:** Var[X] = E[Var(X|K)] + Var(E[X|K]) para cualquier variable condicionante K aleatoria.
- **Por qué se permite asumirlo:** la demostración es un ejercicio de esperanzas iteradas que no necesitas reproducir para usarla bien en entrevista.
- **Qué sí debes razonar:** cuál es la K natural del problema (el nivel extra de aleatoriedad) y cómo la varianza total se descompone en dos sumandos: ruido promedio dentro de cada escenario + variación entre escenarios.
- **Intuición mínima:** varianza total = varianza «dentro» + varianza «entre».
- **Cuándo reabrir la caja:** al estudiar esperanza condicional formal (es la descomposición de la varianza): Casella & Berger o Gut.

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "¿Cuántos objetos de n cumplen X?" | Indicador por objeto, suma de probabilidades |
| "Esperanza de una suma larga" | Linealidad directa, no calcules la distribución conjunta |
| "Variables claramente dependientes, piden media" | Aplica linealidad: la independencia no importa para E |
| "Problema de coincidencias / coincidencias aleatorias" | Indicadores de coincidencia, cada uno con P = 1/n |

---

## Ejercicio de consolidación

Un archivo tiene n líneas. Se leen en orden aleatorio (permutación aleatoria). Define "éxito" en la posición i si la línea leída está en su posición original. ¿Cuántos éxitos esperas?

Responde antes de leer: ¿es 1, n, o depende de n?

*Respuesta: 1, independientemente de n. Es el mismo argumento del sombrero.*
