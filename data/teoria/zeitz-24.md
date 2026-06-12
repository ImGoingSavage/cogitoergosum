# Reformula: dibuja, traduce, cambia el punto de vista

*Lección redactada para CogitoErgoSum a partir de la sección 2.4 de Zeitz (Other Important Strategies). Cubre el contenido completo de la unidad.*

## La tesis de la sección

Si llevas rato sin avanzar, **el problema puede estar bien y tu representación mal**. Un problema no viene con su representación pegada: la prosa del enunciado es solo *una* manera de codificarlo, y rara vez la mejor. Cambiar de representación es, a menudo, **todo el trabajo**.

## 1. ¡Dibuja! (aunque «no sea de geometría»)

Un dibujo no es decoración: es una **representación que hace visibles relaciones que la prosa esconde**. El sistema visual humano detecta colinealidades, simetrías, cruces y tendencias sin esfuerzo consciente — pero solo si le das algo que mirar.

Para servir como herramienta de razonamiento, el dibujo debe:

- Ser **fiel a la estructura** (no necesariamente a la escala): que las relaciones del problema estén representadas, no solo los objetos.
- Estar **etiquetado**: nombres en los puntos, valores en los segmentos, flechas en los movimientos.
- **Rehacerse** cuando se ensucia: el tercer dibujo siempre es mejor que el primero.

Ejemplos de dibujos en problemas «no geométricos»: una recta numérica para desigualdades, un diagrama de estados para un proceso, una **gráfica posición-tiempo** para problemas de movimiento, un diagrama de Venn para conteos.

**El monje de la montaña:** un monje sube el lunes de la base a la cima (sale al alba, llega al ocaso) y baja el martes por el mismo sendero. ¿Hay un punto del camino por el que pasa exactamente a la misma hora ambos días? En prosa parece imposible de atacar. **Dibuja posición contra tiempo y superpón los dos días**: una curva sube, la otra baja, ambas continuas en el mismo rectángulo — se cruzan en algún punto, y ese cruce ES el lugar y la hora pedidos. Misma información, otra representación: el problema se volvió trivial. (Equivale a imaginar dos monjes el mismo día: uno sube, otro baja — en algún momento se encuentran.)

## 2. Traduce el problema a otro lenguaje (recast)

**Qué significa:** reescribir el problema en un dominio donde tus herramientas sean más fuertes. Traducciones típicas y sus señales:

| Traducción | Señal para usarla |
|---|---|
| Relaciones entre objetos → **grafo** (puntos y aristas) | «conocidos entre sí», «conectados», «rutas», parejas |
| Enunciado algebraico → **imagen geométrica** | x² + y² sugiere distancias; productos sugieren áreas |
| Figura geométrica → **coordenadas / álgebra** | la figura tiene ángulos rectos y medidas cómodas |
| Proceso en el tiempo → **gráfica o tabla de estados** | «en cada paso…», movimientos repetidos |
| Conteo enredado → **codificación** (secuencias de símbolos) | «¿de cuántas formas…?» con estructura de elecciones |

La traducción correcta no añade información — reorganiza la que hay para que tu maquinaria (álgebra, geometría, grafos) pueda morderla.

## 3. Cambia el punto de vista

Tres movimientos clásicos:

- **Cuenta el complemento:** en vez de contar lo que SÍ pasa, cuenta lo que NO pasa y resta del total. **Señal clásica:** las palabras «al menos uno…» en un conteo o probabilidad — «al menos un seis en cuatro tiradas» se calcula como 1 − P(ningún seis) = 1 − (5/6)⁴. Lo directo exigiría sumar casos con uno, dos, tres y cuatro seises; el complemento es una sola resta.
- **Mira el proceso desde el final:** ¿cómo se ve el último paso? (hermano del penúltimo paso de §2.2 y de trabajar hacia atrás).
- **Mírale desde otro participante:** cambiar de protagonista simplifica problemas enteros. **La mosca y los trenes:** dos trenes parten a la vez de ciudades opuestas por la misma vía; una mosca vuela de frente de uno a otro, ida y vuelta, a velocidad constante, hasta que chocan. ¿Qué distancia recorre? El punto de vista de la mosca lleva a sumar una serie infinita de trayectos (se puede, pero duele). El punto de vista del **tiempo total**: los trenes chocan en un tiempo T fácil de calcular; la mosca voló durante ese mismo T a velocidad constante v, así que recorrió v·T. Fin. Misma pregunta, otro protagonista, problema de primaria.

## El meta-disparador de la sección

Atascado un buen rato + ningún error a la vista = **sospecha de la representación, no del problema**. Pregúntate: ¿qué otra cara tiene esto? ¿Dibujo? ¿Grafo? ¿Complemento? ¿Otro protagonista? Cambiar de cara cuesta 2 minutos; insistir en la cara equivocada cuesta la tarde.

## Disparadores

- Problema con movimiento/encuentros → gráfica posición-tiempo superpuesta.
- «Al menos uno» en conteo/probabilidad → complemento.
- Relaciones por parejas («se conocen», «conectados») → grafo.
- Proceso iterado descrito en prosa → tabla de estados o dibujo del tablero.
- Suma infinita amenazante → busca el protagonista para el que la pregunta es directa.

## Síntesis

> **Chunk mínimo:** Atascado sin error a la vista = sospecha de la REPRESENTACIÓN, no del problema. Tres salidas: (1) **Dibuja** — fiel a la estructura, etiquetado, rehecho cuando se ensucia; el monje de la montaña se vuelve trivial superponiendo las dos curvas posición-tiempo (se cruzan). (2) **Traduce**: parejas/conexiones → grafo; álgebra → imagen geométrica (y viceversa); proceso → tabla de estados; conteo de elecciones → codificación. (3) **Cambia el punto de vista**: «al menos uno» → complemento (1 − P(ninguno)); mira desde el final; cambia de protagonista — la mosca de los trenes se desarma calculando el tiempo T del choque: recorrió v·T, sin series.

---

*Antes del quiz: reconstruye de memoria qué aporta un dibujo y qué debe tener para servir, dos traducciones típicas con su señal, la señal del complemento, y cómo se desarma la mosca de los trenes.*
