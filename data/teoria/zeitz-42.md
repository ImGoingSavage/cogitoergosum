# Números complejos: el artista del cruce

*Lección redactada para CogitoErgoSum a partir de la sección 4.2 de Zeitz (Complex Numbers). Cubre el contenido completo de la unidad.*

## La triple identidad

Un complejo z = a + bi es, **a la vez**, tres cosas:

1. **Un PUNTO** (a, b) del plano de Argand (eje real horizontal, eje imaginario vertical).
2. **Un VECTOR** desde el origen hasta ese punto (con longitud |z| = √(a² + b²) y dirección arg z).
3. **Una TRANSFORMACIÓN**: «multiplicar por z» es una operación que rota el plano por arg z y lo estira por |z|.

La fluidez con complejos consiste en **saltar entre las tres lecturas según convenga**: los datos suelen entrar como puntos, las sumas se piensan como vectores, los giros como transformaciones.

## Por qué multiplicar rota y estira (sin trigonometría)

El argumento de Zeitz para (3 + 4i)·z:

(3 + 4i)z = 3z + 4iz

— es decir: **un estiramiento** de z (3z, misma dirección, triple longitud) **más una copia de z rotada 90° y estirada 4 veces** (porque **multiplicar por i es rotar π/2**: i·(a+bi) = −b + ai, el vector perpendicular). Sumar un vector con su perpendicular escalada produce un vector girado un ángulo fijo (arctan 4/3) y estirado por √(3²+4²) = 5 — **para cualquier z el mismo giro y el mismo estirón**, porque la construcción solo usó la forma de z, no su valor. Multiplicar por 3+4i = rotar arctan(4/3) y estirar ×5. Sin un solo seno.

## Forma polar y la aritmética de ángulos

z = r·Cis θ = r·e^{iθ}, con r = |z|, θ = arg z. Las reglas:

- **Multiplicar multiplica módulos y SUMA argumentos**; dividir resta.
- El **conjugado** z̄ = a − bi es la **reflexión en el eje real**; y **|z|² = z·z̄** — la identidad que convierte módulos en álgebra **sin raíces cuadradas** (para probar cosas sobre |w|, calcula w·w̄).
- **Suma = regla del paralelogramo** (vectores). Consecuencia visual: si z₁ + ⋯ + zₙ = 0, los vectores puestos **cabeza con cola cierran un polígono** — regresan al origen. *El acertijo del banco:* seis complejos que suman 0 forman un hexágono cerrado (quizá degenerado); por eso «fuerzas/desplazamientos que se cancelan» = «el polígono de vectores cierra», y problemas de equilibrio se vuelven geometría de polígonos de un golpe.

**El error clásico:** «|z₁ + z₂| = |z₁| + |z₂|». El módulo **sí es multiplicativo** (|zw| = |z||w| — y eso está bien), pero **NO es aditivo**: la suma obedece la **desigualdad del triángulo** |z₁ + z₂| ≤ |z₁| + |z₂|, con igualdad solo si apuntan en la misma dirección. (Dos lados de un triángulo no suman como uno recto salvo si el triángulo se aplasta.)

## De Moivre y las raíces de la unidad

> **De Moivre:** (cos θ + i sin θ)ⁿ = cos nθ + i sin nθ, para todo entero n.

(En forma exponencial es solo (e^{iθ})ⁿ = e^{inθ}: una ley de exponentes.) Es la máquina de dos fábricas:

1. **Trigonometría con potencias:** expande (cos θ + i sin θ)³ con el binomio, iguala partes reales con cos 3θ — las identidades de ángulo múltiple salen en una línea. Lo que en cartesianas es un mar de senos y cosenos, en e^{iθ} es álgebra de exponentes.
2. **Raíces n-ésimas de la unidad:** las soluciones de zⁿ = 1 son los n puntos ω_k = e^{2πik/n}, **igualmente espaciados en el círculo unitario** (vértices de un n-ágono regular con un vértice en 1). Regalan **simetría rotacional gratis**: suman 0 (¡polígono cerrado!), sus potencias permutan entre sí, y factorizan zⁿ − 1 = Π(z − ω_k). Para contar raíces con cierta propiedad o evaluar sumas trigonométricas cada 2π/n, son la herramienta canónica (incluido el truco de filtrar sumas «cada 3 términos» de §4.3 evaluando generatrices en raíces de la unidad).

## Disparadores

- **Rotaciones, polígonos regulares, ángulos que se suman** → tradúcelo a complejos en forma polar.
- **Potencias altas de expresiones trigonométricas** → De Moivre / forma exponencial.
- zⁿ = 1, vértices equiespaciados, sumas que «giran» → raíces de la unidad y su simetría.
- Módulos al cuadrado, distancias → |z|² = z·z̄ (álgebra sin raíces).
- Fuerzas/pasos que se cancelan → polígono de vectores cerrado.

## Síntesis

> **Chunk mínimo:** z es a la vez punto, vector y transformación (multiplicar por z = rotar arg z y estirar |z|; multiplicar por i = rotar 90°: el argumento 3z + 4iz da giro arctan 4/3 y estirón 5 sin trigonometría). Polar: multiplicar multiplica módulos y SUMA argumentos; |z|² = z·z̄ (módulos sin raíces); z₁+⋯+zₙ = 0 ⟺ el polígono de vectores cierra. Error clásico: el módulo es multiplicativo pero NO aditivo (desigualdad del triángulo). De Moivre ((e^{iθ})ⁿ = e^{inθ}) fabrica identidades de ángulo múltiple y las n raíces de zⁿ = 1: n-ágono regular en el círculo unitario que suma 0, con simetría rotacional gratis.

---

*Antes del quiz: reconstruye de memoria la triple identidad, el argumento 3z + 4iz completo, qué son las raíces n-ésimas en el plano y qué regalan, y el error del módulo «aditivo».*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Los numeros complejos permiten cruzar algebra y geometria sin cambiar de problema. [[engel-geo2]] usa complejos, vectores y trigonometria como lenguaje geometrico, [[aime-geo]] los traduce a problemas de examen, y [[arena-p4]] conserva la estructura algebraica que hace utiles esas transformaciones.
<!-- GRAFO_CONEXO_OLEADA3_END -->
