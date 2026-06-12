# Invariantes y monovariantes

*Lección redactada para CogitoErgoSum a partir de la sección 3.4 de Zeitz (Invariants). Cubre el contenido completo de la unidad: paridad, aritmética modular, coloración y monovariantes.*

## Las definiciones y qué demuestra cada uno

- **Invariante:** una cantidad (o propiedad) que **ninguna movida permitida cambia**. Conclusión que habilita: **imposibilidad**. Si el estado inicial y el estado final difieren en el invariante, **no hay secuencia de movidas que lleve de uno a otro** — sin importar cuán larga o ingeniosa.
- **Monovariante** (o semi-invariante): una cantidad que con cada movida **solo crece** (o solo decrece). Conclusiones que habilita: **terminación** (si es entera y acotada, el proceso se detiene: no se puede decrecer infinitamente en ℕ) y **localización** (a dónde puede llegar el proceso: nunca a estados con valor «del lado prohibido»).

La pregunta «¿es posible llegar de A a B con estas operaciones?» es **casi siempre un problema de invariante**: la respuesta «no» se demuestra exhibiendo la cantidad conservada que A y B no comparten.

## El catálogo: los cuatro invariantes que pruebas primero

| Invariante | Se lleva bien con… |
|---|---|
| **Paridad** (par/impar) | operaciones que suman/restan, intercambian, voltean de a dos |
| **Suma** (o suma con signos) | operaciones que redistribuyen sin crear ni destruir |
| **Producto** | operaciones multiplicativas, reemplazos tipo (a,b) → (a·b, …) |
| **Residuos módulo k** | operaciones que cambian las cantidades en múltiplos fijos; paridad es el caso k = 2 |
| **Coloración** | movimientos sobre tableros: fichas, dominós, saltos (es un «módulo» geométrico) |

(El quinto, coloración, es tan importante que Engel le dedica un capítulo entero — lo verás en la fase 5.)

## Cómo se encuentra un invariante

No por iluminación: **ensuciándose las manos**. Ejecuta movidas concretas en un caso pequeño y **tabula** qué cantidades cambian y cómo: ¿la suma subió o bajó? ¿la paridad del número de fichas? ¿la suma módulo 3? El que no cambia **salta a la vista en la tabla** — no en la contemplación del enunciado. Pista estructural: mira qué hace la movida «en neto» (¿quita 2 y pone 2? ¿reemplaza a+b por a·b?) y pregunta qué función de los datos es ciega a ese cambio.

## Ejemplo resuelto: el acertijo de las diferencias

**Problema:** en una pizarra están 1, 2, 3, …, 2026. Eliges dos números, los borras y escribes su diferencia (mayor menos menor). Repites hasta que quede un solo número. ¿Puede ser 0?

**Análisis:** la movida reemplaza {a, b} por a − b. Mira la **suma total S**: cambia de S a S − a − b + (a − b) = S − 2b — **cambia en un número par**. Luego la **paridad de S es invariante**. Al inicio S = 1 + 2 + ⋯ + 2026 = 2026·2027/2 = 1013·2027, **impar**. Al final, si quedara 0, la suma sería 0: **par**. Imposible: el número final jamás es 0 (siempre será impar). ∎

Nota el método: probé la suma (cambió), pero *cómo* cambió (en pasos pares) reveló el invariante fino: la paridad de la suma.

## Ejemplo de monovariante: el proceso termina

Tipo clásico: en cada paso, si hay un número negativo en cierta configuración, se le aplica una operación local (voltear signos vecinos, redistribuir fichas…). ¿Puede continuar para siempre? **Método:** busca una cantidad entera ≥ 0 que cada movida **decrezca estrictamente** (una «energía»: suma de valores absolutos, suma de cuadrados, número de inversiones…). Si existe, el proceso termina — no hay descenso infinito en los enteros no negativos. El reto creativo es diseñar la energía correcta; las candidatas estándar: sumas de |·|, de cuadrados, distancias totales, número de pares en mal orden.

Y la segunda lectura del monovariante: **a dónde llega**. Si la cantidad solo crece y el estado deseado exige que haya bajado, el estado es inalcanzable — el monovariante también demuestra imposibilidad.

## Estructura de una solución por invariante

1. Define con precisión la cantidad I (función del estado).
2. Verifica que **toda movida permitida** la conserva (todas, no la movida que te conviene).
3. Evalúa I(inicial) e I(final deseado).
4. Si difieren: imposible, ∎. Si coinciden: el invariante no obstruye (¡ojo!, eso **no** prueba que sí se pueda — solo que este invariante no lo impide).

El punto 4 es el error conceptual más común: un invariante coincidente no es una demostración de posibilidad. Posibilidad se demuestra **exhibiendo la secuencia de movidas**.

## Disparadores

- «¿Es posible llegar de A a B con estas operaciones?» → invariante (catálogo: paridad, suma, producto, módulo, coloración).
- «¿Puede el proceso continuar para siempre?» → monovariante acotado (busca la energía que siempre baja).
- Operación local repetida (voltear, intercambiar, reemplazar dos por uno) → tabula movidas concretas y caza lo que no cambia.
- Tablero + fichas/dominós/saltos → coloración.

## Síntesis

> **Chunk mínimo:** Invariante = cantidad que ninguna movida cambia ⇒ demuestra IMPOSIBILIDAD (I(A) ≠ I(B) ⇒ no hay camino de A a B). Monovariante = solo crece o solo decrece ⇒ demuestra TERMINACIÓN (entero acotado) y localización. Catálogo en orden: paridad, suma, producto, residuos mod k, coloración (el «módulo geométrico» de los tableros). Se encuentra tabulando movidas concretas, no contemplando. Acertijo 1…2026: reemplazar {a,b} por a−b cambia S en −2b (par) ⇒ paridad de S invariante; S inicial impar ⇒ el final jamás es 0. Y el punto 4: invariante coincidente NO prueba posibilidad — posibilidad se prueba exhibiendo la secuencia.

---

*Antes del quiz: reconstruye de memoria las dos definiciones con la conclusión que habilita cada una, el catálogo de invariantes con su tipo de operación, y el argumento completo del acertijo 1…2026.*
