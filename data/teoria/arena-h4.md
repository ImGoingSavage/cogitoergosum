# Inferencia causal II: confundimiento, selección y medición (estructura)

> El enfoque **estructural**: cada sesgo es una estructura de caminos en el DAG. El lenguaje de **d-separación** dice qué ajustar y qué NO. Complementa [[arena-h1]] (definiciones básicas confundidor/mediador/collider).

## De qué trata esta lección (y qué sabrás hacer al final)

Los tres grandes sesgos de un estudio —confundimiento, selección y medición— suelen tratarse como un saco de "cosas que salen mal". Esta lección construye, desde cero, la idea que los unifica: **cada sesgo es una estructura concreta de caminos en el DAG**, y la **d-separación** es la regla mecánica que dice qué ajustar y qué no. Con ese lenguaje, "¿controlo por esta variable?" deja de ser intuición y pasa a ser una lectura del grafo.

Al terminar podrás: (1) cerrar un camino trasero con el criterio backdoor y reconocer la d-separación; (2) distinguir confundimiento (causa común anterior) de sesgo de selección (efecto común condicionado, incluida la censura informativa → IPCW); (3) saber por qué el error de medición no diferencial atenúa hacia el nulo y el diferencial no; y (4) evitar ajustar mediadores, colliders o instrumentos. Cada estructura entra por un ejemplo.

## Confundimiento y criterio de la puerta trasera

**Confundimiento** = A e Y comparten una **causa común**, abriendo un **camino trasero** A ← C → Y que transmite asociación no causal. Ver [[confundimiento-backdoor]].

**Criterio backdoor:** un conjunto L identifica el efecto si (i) **bloquea** todos los caminos traseros y (ii) **no** contiene descendientes de A. Cumplirlo = intercambiabilidad condicional dado L.

### d-separación
Un camino está **bloqueado** si: condicionas un **no-collider** (cadena A→B→C o bifurcación A←B→C), o **no** condicionas un **collider** (A→B←C, ni sus descendientes). Mnemónico: condicionar **cierra** cadenas/bifurcaciones pero **abre** colliders.

## Sesgo de selección (colliders)

Surge al **condicionar** (restringir, estratificar, seleccionar) un **efecto común** (collider) de A (o causa de A) e Y (o causa de Y) → abre asociación espuria. Se distingue del confundimiento: causa común **anterior** (confundimiento) vs efecto común **posterior** condicionado (selección).

**Censura informativa:** permanecer no censurado (C=0) es efecto de A y predictor de Y; analizar solo a los no censurados condiciona un collider → corrige con **IP weighting de censura (IPCW)**. Ver [[sesgo-de-seleccion-censura]].

## Sesgo de medición

De medir con error A, Y o L:
- **No diferencial** (error independiente del valor de la otra variable): suele **atenuar** hacia el nulo.
- **Diferencial** (error depende, p. ej. recall bias): sesga en **cualquier** dirección.
- **Confundidor mal medido** → **confundimiento residual** (ajuste incompleto). Ver [[sesgo-de-medicion-misclasificacion]].

Se modela con **diagramas no causales** (variable real → variable medida ← nodo de error).

## Qué NO ajustar + identificación vs estimación

- **Mediador** (A→M→Y): bloquearlo sesga el efecto **total**.
- **Collider/selección:** condicionarlo abre sesgo (**M-bias** con colliders pretratamiento).
- **Instrumento** (solo causa A): **amplifica** confundimiento residual y varianza (**Z-bias**).
- **Identificación** (¿estimable bajo supuestos, con datos infinitos?) vs **estimación** (con datos finitos: modelos, IC). Sin identificación, más datos no ayudan.

---

## Mini-ejemplo trabajado: el error no diferencial atenúa hacia el nulo

Verdad: el tratamiento dobla el riesgo. Entre expuestos reales el riesgo es 0.40; entre no expuestos, 0.20 → **razón de riesgos = 2.0**. Ahora mide la *exposición* con un sensor que se equivoca el 20% de las veces **en ambos sentidos por igual** (error no diferencial). El grupo "medido como expuesto" se contamina con verdaderos no-expuestos (riesgo 0.20) y viceversa, así que las tasas observadas se acercan: el expuesto-medido baja de 0.40 y el no-expuesto-medido sube de 0.20 → la RR observada cae hacia **~1.5**, nunca por debajo de 1. La señal **se diluye hacia el nulo**, no se invierte.

**Predicción antes de seguir:** ¿y si el error fuera *diferencial* (los enfermos recuerdan mejor su exposición, recall bias)? Entonces el sesgo puede ir en **cualquier** dirección, incluso inflar la RR por encima de 2 — por eso el tipo de error importa más que su tamaño.

## Prototipo, contraejemplo y caso borde

- **Prototipo (confundimiento):** A←C→Y con C medido → cierras el backdoor ajustando por C.
- **Contraejemplo (ajuste que **abre** sesgo):** condicionar un collider pretratamiento (M-bias) o un mediador "porque mejora el ajuste". El criterio es la d-separación, no el R².
- **Caso borde (censura informativa):** abandonar el estudio (C=0) es efecto del tratamiento y predictor del outcome → analizar solo a los no censurados condiciona un collider; se corrige con **IPCW**, no eliminando filas.

## Errores típicos

- **Conceptual:** tratar todo sesgo como "confundimiento"; selección y medición son estructuras distintas (efecto común condicionado vs error de medida).
- **Técnico:** "ajustar por todo lo disponible" → mete mediadores, colliders o instrumentos y empeora la estimación.
- **De interpretación:** asumir que un error de medición siempre atenúa — solo el **no diferencial** lo hace.

## Transferencia isomorfa

Estos sesgos estructurales reaparecen en datos y ML:

- **Error no diferencial ↔ ruido de etiquetas:** etiquetas con ruido aleatorio atenúan la señal aprendida hacia el azar, igual que la misclasificación atenúa la RR (conecta con [[arena-dmls2]]).
- **Censura informativa / IPCW ↔ sesgo de supervivencia en churn:** analizar solo usuarios que siguen activos condiciona un collider; reponderar por probabilidad de seguir es el IPCW del producto.
- **Z-bias del instrumento ↔ feature casi-colineal con el tratamiento:** meter una variable que solo predice la asignación amplifica varianza sin reducir sesgo.

Moraleja de la arista: *cada sesgo es un camino en el DAG; "qué ajustar" lo decide la d-separación, y el ruido de medida casi nunca es neutral.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Asociación no causal por causa común | Confundimiento: cierra el backdoor ajustando por C |
| Muestra restringida por efecto común | Sesgo de selección (collider): NO condicionar |
| Abandono según tratamiento y pronóstico | Censura informativa → IPCW |
| Variable medida con error | No diferencial atenúa; diferencial, impredecible |
| «Ajustemos por todo» | Error: mediador/collider/instrumento sesgan; decide con el DAG |

---

> **Síntesis:** los sesgos son **estructuras**: el **confundimiento** (causa común) se cierra con el **criterio backdoor**; el **sesgo de selección** (condicionar un collider, incluida la censura) se evita NO condicionando o con **IPCW**; el **sesgo de medición** depende de si la misclasificación es **diferencial**. La **d-separación** y el DAG —no la significancia— deciden qué ajustar; nunca mediadores, colliders ni instrumentos.

---

*Retrieval: (1) criterio de la puerta trasera; (2) ¿cuándo condicionar abre un camino?; (3) confundimiento vs selección estructuralmente; (4) ¿misclasificación no diferencial vs diferencial?*
