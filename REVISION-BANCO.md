# Protocolo de revisión — banco de problemas (`data/problems.json`)

> Estado inicial: **716 problemas**, 686 con LaTeX, 30 sin.  
> El fix de `textContent → renderInline()` ya está en producción (commit `8d34067`).  
> Lo que queda: los datos tienen LaTeX malformado — el parser lo recibe pero no puede renderizarlo bien.

---

## Alcance

| Categoría | Cantidad | Prioridad |
|---|---|---|
| Trig/log **partido** (palabra fuera, argumento dentro de `$`) | ~43 | 🔴 Alta |
| Mezcla cruda (LaTeX dentro y fuera de `$` en la misma expresión) | ~52 | 🔴 Alta |
| Superíndice Unicode (`m²`, `x³`) fuera de math | ~5 | 🟡 Media |
| `\$` para cantidades monetarias (`\$100`) | 12 | ✅ Ya correcto — no tocar |

---

## Anti-patrones y su corrección

### 1. Trig partido — el más común

El nombre de la función está fuera del `$` y el argumento adentro.

```
❌  sen $\theta = 3/5$
❌  cos $\theta = 4/5$
❌  tan $\theta$

✅  $\text{sen}\,\theta = 3/5$
✅  $\cos \theta = 4/5$
✅  $\tan \theta$
```

**Regla:** todo el bloque `función + argumento` va dentro de un solo `$…$`.  
En español usamos `\text{sen}` (KaTeX no tiene `\sen` nativo).  
`cos`, `tan`, `log`, `ln` son comandos nativos de KaTeX → sin `\text{}`.

```
❌  log $n$           →  ✅  $\log n$
❌  ln $x$            →  ✅  $\ln x$
❌  cos $\alpha$      →  ✅  $\cos \alpha$
❌  sen $\theta$      →  ✅  $\text{sen}\,\theta$
```

---

### 2. Expresión cruda partida en varios bloques `$`

```
❌  sin$^2x +$ cos$^2x = 1$
❌  cos$^2\theta = 1 - (3/5)^2$
❌  $(1/2)\cdot 5\cdot 8\cdot$sen $\theta$

✅  $\sin^2 x + \cos^2 x = 1$
✅  $\cos^2\theta = 1 - (3/5)^2$
✅  $\tfrac{1}{2}\cdot 5\cdot 8\cdot\text{sen}\,\theta$
```

**Regla:** una expresión matemática = un solo bloque `$…$`.  
Nunca abrir y cerrar `$` en medio de una expresión para añadir texto.

---

### 3. Superíndices Unicode

```
❌  m²   →  ✅  $m^2$
❌  x³   →  ✅  $x^3$
❌  cm²  →  ✅  $\text{cm}^2$
```

---

### 4. `\$` para cantidades monetarias — **no tocar**

```
✅  \$100    →  se renderiza como "$100" (literal, no math)
✅  \$1,000
```

`renderInline` en `markdown.js` protege `\$` antes de parsear math.  
Cambiar esto a `$100` haría que KaTeX intente renderizarlo como LaTeX.

---

### 5. `|…|` valor absoluto / norma

```
❌  |sin $x_1|$     →  ✅  $|\text{sen}\,x_1|$
❌  $|$sin $x|$     →  ✅  $|\text{sen}\,x|$
```

Las barras de valor absoluto van **dentro** del bloque math.

---

### 6. Fracciones crudas en texto narrativo

Solo aplica si el fragmento es matemático puro (no una razón o precio):

```
❌  "la probabilidad es 3/5"   →  ✅  "la probabilidad es $3/5$"
⚠️  "página 3/5 del examen"   →  dejar como está (es texto)
```

---

## Workflow de revisión

### Orden recomendado

1. Empezar por los **43 trig partido** (IDs conocidos: ver lista abajo).
2. Luego los **~9 de mezcla cruda** restantes (IDs conocidos: ver lista).
3. Por último barrer los superíndices Unicode.

### Cómo revisar un problema

1. Buscar el ID en `data/problems.json`.
2. Leer `enunciado`, `solucion` y `explicacion`.
3. Identificar el anti-patrón (sección de arriba).
4. Corregir **en el JSON** directamente.
5. Verificar en la app local (`python3 -m http.server 8000`) que renderiza bien.
6. Continuar con el siguiente.

### Señal de que el problema está limpio

- Todo bloque matemático abre y cierra con `$…$` o `$$…$$`.
- Ningún nombre de función (`sen`, `cos`, `tan`, `log`, `ln`) aparece fuera de un bloque math.
- No hay Unicode matemático (`²`, `³`, `→`, `≤` etc.) mezclado con LaTeX — elegir uno u otro para toda la expresión.

---

## Lista de IDs con trig partido (prioridad 🔴)

```
217, 219, 305, 389, 629, 630, 633, 637, 651, 652, 653, 654, 655, 659,
660, 662, 663, 664, 671
```
*(más los que surjan al revisar — la lista no es exhaustiva)*

## Lista de IDs con mezcla cruda (prioridad 🔴)

```
115, 148, 204, 217, 218, 219, 299, 305
```

---

## Convenciones KaTeX — referencia rápida

| Quieres escribir | LaTeX correcto |
|---|---|
| seno (español) | `\text{sen}` |
| coseno | `\cos` |
| tangente | `\tan` |
| logaritmo | `\log` |
| logaritmo natural | `\ln` |
| fracción inline | `\tfrac{a}{b}` |
| fracción display | `\dfrac{a}{b}` |
| valor absoluto | `\lvert x \rvert` o `|x|` |
| norma | `\lVert x \rVert` |
| implica | `\Rightarrow` |
| si y solo si | `\Leftrightarrow` |
| pertenece | `\in` |
| ángulo | `\angle` o `^\circ` |
| grados | `90^\circ` |

---

## Criterio de calidad final

Un problema está **revisado** cuando:

- [ ] Abre la app en localhost y el enunciado renderiza con tipografía KaTeX limpia.
- [ ] La solución no tiene texto partido (`función`…`$argumento$`).
- [ ] La explicación tampoco.
- [ ] No hay `$` solitarios ni llaves sueltas visibles en pantalla.
