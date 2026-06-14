# Inferencia causal II: confundimiento, selección y medición (estructura)

> El enfoque **estructural**: cada sesgo es una estructura de caminos en el DAG. El lenguaje de **d-separación** dice qué ajustar y qué NO. Complementa [[arena-h1]] (definiciones básicas confundidor/mediador/collider).

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
