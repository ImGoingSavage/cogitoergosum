# Positional encoding y Vision Transformers (ViT)

> Recurso troncal: [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) §3.5 + [An Image is Worth 16x16 Words (Dosovitskiy et al., 2021)](https://arxiv.org/abs/2010.11929). Capstone del cluster: resuelve la tensión "paralelismo vs orden" de [[gen-tf1]] y extiende el Transformer a imágenes.

## De qué trata (y qué sabrás hacer al final)

En [[gen-tf1]] quedó pendiente una tensión: el Transformer procesa todas las palabras **en paralelo**, lo que le da velocidad, pero **pierde el orden** —y "el gato mordió al perro" no es lo mismo que "el perro mordió al gato"—. La **codificación posicional** (positional encoding, PE) devuelve esa información. Luego damos el salto que demostró la generalidad del Transformer: aplicarlo a **imágenes** (Vision Transformers), tratando trozos de imagen como si fueran palabras.

La intuición del PE: la self-attention es como una **bolsa de palabras conectadas** — sabe qué palabras hay y cómo se relacionan, pero no en qué **posición** está cada una (es *permutation-invariant*: si barajas la entrada, la atención da lo mismo). Es como tener todas las palabras de una frase escritas en fichas sueltas sobre una mesa: ves las palabras, pero no el orden. El PE es **escribir un número de posición en cada ficha** antes de mezclarlas, para que el modelo pueda recuperar "esta iba primero, esta segunda".

Al terminar podrás: (1) explicar por qué la self-attention es **ciega al orden** y por qué eso es un problema; (2) entender el **positional encoding** (sinusoidal y aprendido); (3) explicar cómo un **Vision Transformer** convierte una imagen en "palabras"; y (4) conectar todo esto con LLMs, RAG y multimodalidad.

## Por qué la atención es ciega al orden

La self-attention calcula relaciones entre pares de tokens por su **contenido** (Q·K), no por su **posición**. Matemáticamente es **invariante a permutaciones**: si reordenas los tokens de entrada, las salidas se reordenan igual, pero las relaciones calculadas son las mismas. Sin información de orden, "Juan ama a María" y "María ama a Juan" serían **idénticas** para el modelo — un desastre para el lenguaje, donde el orden carga significado. Las RNN no tenían este problema (procesaban en orden por construcción); el Transformer lo ganó como **efecto colateral** del paralelismo, y hay que repararlo explícitamente.

## Positional encoding: devolver el orden

La solución: **sumar a cada embedding de token un vector que codifica su posición.** Así el vector de entrada de la posición 3 lleva, mezclada, la información "soy la posición 3". Dos enfoques:

- **Sinusoidal (original):** el [paper §3.5](https://arxiv.org/abs/1706.03762) usa funciones seno y coseno de distintas frecuencias:
  $$PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right),\quad PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)$$
  Cada dimensión oscila a una frecuencia distinta (como las manecillas de un reloj: segundos, minutos, horas). La ventaja: las posiciones relativas se vuelven combinaciones lineales fáciles de aprender, y **generaliza a longitudes no vistas** en entrenamiento (no requiere aprender un vector por posición).
- **Aprendido:** simplemente una tabla de vectores de posición que el modelo entrena (lo usa BERT). Más simple, pero limitado a la longitud máxima vista.

**[CAJA NEGRA OK]** No necesitas memorizar la fórmula sinusoidal; sí la intuición: *cada posición recibe una "firma" única y suave que el modelo puede leer para recuperar el orden y las distancias relativas.* Los LLMs modernos usan variantes más potentes —**RoPE** (rotary, [Su et al., 2021](https://arxiv.org/abs/2104.09864)) y **ALiBi** ([Press et al., 2021](https://arxiv.org/abs/2108.12409))— que codifican posiciones **relativas** y extrapolan mejor a contextos largos. Es área activa: la "ventana de contexto" gigante de los LLMs de hoy depende en parte de mejores PE.

## Vision Transformers: una imagen es 16×16 palabras

Aquí el Transformer demostró que no era solo para texto. La idea de [Dosovitskiy et al. (2021)](https://arxiv.org/abs/2010.11929), elegante por lo simple:

1. **Corta la imagen en parches** (p. ej. cuadros de 16×16 píxeles).
2. **Aplana cada parche** y lo proyecta a un vector → ahora cada parche es un "token", como una palabra.
3. **Suma positional encoding** (¿en qué posición de la cuadrícula va el parche? — mismo problema de orden, ahora en 2D).
4. **Pásalos por un Transformer estándar** (encoder), con un token especial `[CLS]` cuya salida se usa para clasificar.

El hallazgo: con **suficientes datos**, un Transformer puro **iguala o supera** a las redes convolucionales (CNN) en visión, **sin** los sesgos de diseño de las CNN (localidad, invariancia a traslación). La lección profunda: el Transformer es un **aprendiz de relaciones de propósito general**; dale cualquier cosa que puedas trocear en tokens (texto, imagen, audio, código) y aprenderá sus relaciones. Esa generalidad es la base de los modelos **multimodales** actuales.

## Mini-ejemplo trabajado: barajar la entrada

Toma "el perro mordió al cartero". Sin PE, si el modelo procesara los tokens en cualquier orden, "el cartero mordió al perro" produciría las mismas representaciones internas — no podría distinguir quién mordió a quién. Con PE, el token "perro" en posición 2 (sujeto) lleva una firma distinta del "perro" en posición 5 (objeto), y la atención puede aprender el rol según la posición. Predicción antes de seguir: en un ViT, ¿qué pasaría si **no** sumamos positional encoding a los parches? → el modelo perdería la **disposición espacial**: una cara con los ojos y la boca intercambiados se vería igual que una normal (bolsa de parches sin geometría). El orden/posición es tan esencial en imágenes como en texto.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El modelo no distingue el orden de las palabras" | Falta o falla el positional encoding |
| "Necesito contextos muy largos / extrapolar longitud" | PE relativo (RoPE, ALiBi) > sinusoidal/aprendido fijo |
| "Quiero aplicar Transformers a imágenes" | ViT: parches como tokens + PE 2D |
| "Tengo texto + imagen + audio juntos" | Tokeniza cada modalidad → Transformer multimodal |

## Errores típicos

- **Olvidar que la atención es permutation-invariant:** sin PE, el orden se pierde por completo.
- **Creer que el PE "ordena" los tokens:** no los reordena; les **añade** una firma de posición que el modelo aprende a usar.
- **Pensar que ViT necesita pocos datos:** sin grandes datasets (o pre-entrenamiento), las CNN ganan; el ViT brilla a escala.

## Contraejemplo y caso borde

- **Contraejemplo:** para datasets de imágenes **pequeños**, una CNN suele superar a un ViT entrenado desde cero — los sesgos inductivos de la convolución (localidad) son una ventaja cuando faltan datos. La generalidad del Transformer cuesta datos.
- **Caso borde:** un modelo entrenado con PE para longitud máxima $L$ puede **degradarse abruptamente** más allá de $L$ (no "vio" esas posiciones). Resolverlo —extrapolación de longitud— es justo lo que motivó RoPE/ALiBi; es el límite de los contextos "infinitos".

## Transferencia isomorfa

- **PE ↔ timestamps en eventos:** añadir la posición a un token es como añadir la **marca de tiempo** a un evento clínico o una transacción: sin ella, tienes un conjunto; con ella, una secuencia ordenada (conecta con el manejo de ventanas temporales).
- **ViT (parches como tokens) ↔ "todo es secuencia":** trocear cualquier dato en unidades y dejar que la atención aprenda sus relaciones es el mismo patrón que aplicarás a audio, código o grafos. La estructura del dato se vuelve "una lista de tokens + sus posiciones".
- **Multimodalidad ↔ embeddings compartidos:** texto e imagen proyectados al mismo espacio de tokens es la base de modelos como [CLIP](https://arxiv.org/abs/2103.00020), puente con la búsqueda semántica del RAG.

Moraleja de la arista: *el Transformer aprende relaciones entre tokens; conviértelo en universal dándole tokens (de lo que sea) + sus posiciones.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** explica, con la analogía de las fichas sobre la mesa, por qué sin PE "Juan ama a María" = "María ama a Juan" para el modelo.
- **Misión externa (lab vivo):** hojea el paper [ViT (Dosovitskiy et al., 2021)](https://arxiv.org/abs/2010.11929), Figura 1 (el pipeline de parches). **Criterio de cierre:** explicar los 4 pasos que convierten una imagen en tokens para el Transformer.
- **Mini-entregable:** un esquema que muestre, en paralelo, cómo texto e imagen se convierten ambos en "tokens + positional encoding" para el mismo tipo de Transformer.

## Reconstrucción mínima en código

Dos piezas: el positional encoding sinusoidal que se **suma** al embedding, y la conversión de una imagen en "tokens" que demuestra que ViT es el mismo Transformer en otro dominio.

```python
import torch, math

def positional_encoding(T, d):
    pos = torch.arange(T).unsqueeze(1)                 # (T, 1)
    i   = torch.arange(0, d, 2)                        # dimensiones pares
    div = torch.exp(-math.log(10000.0) * i / d)
    pe = torch.zeros(T, d)
    pe[:, 0::2] = torch.sin(pos * div)                 # seno en pares
    pe[:, 1::2] = torch.cos(pos * div)                 # coseno en impares
    return pe                                          # se SUMA al embedding

# La atención es invariante a permutaciones: sin PE, "Juan ama a María"
# y "María ama a Juan" producen lo mismo. La posición rompe esa simetría.

# ViT: una imagen es una secuencia de parches, cada uno con su posición.
img = torch.randn(3, 32, 32)                           # C, H, W
P = 8                                                  # parche 8x8 -> 16 parches
patches = img.unfold(1, P, P).unfold(2, P, P)          # (3, 4, 4, 8, 8)
tokens  = patches.reshape(3, 16, P * P).permute(1, 0, 2).reshape(16, 3 * P * P)
print(tokens.shape)                                    # (16, 192): 16 "palabras" visuales
```

**Qué observar:** las filas de `positional_encoding` son únicas por posición pero suaves entre vecinas, así el modelo puede *interpolar* a longitudes nuevas. Y el bloque de ViT no cambia la arquitectura: cambiar texto por parches es **transferencia estructural**, el cierre del recorrido que abrió [[gen-tf1]].

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (positional encoding, embeddings y extensión Transformer a visión) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** anadir embeddings posicionales y comparar texto causal contra patches de imagen.
2. **Baseline obligatorio:** tokens sin codificacion de posición.
3. **Versión mejorada:** positional embeddings aprendidos o sinusoidales.
4. **Evaluación:** accuracy en pares permutados y comparación con/sin positional encoding.
5. **Fallo que debes explicar:** el modelo no distingue secuencias con los mismos tokens en otro orden.
6. **Transferencia:** visión: tratar imágenes como secuencias de patches con posición.

**Laboratorio externo principal:** [Stanford CS25: Transformers United](https://web.stanford.edu/class/cs25/).
**Laboratorio alternativo:** [Stanford CS224N: NLP with Deep Learning](https://web.stanford.edu/class/cs224n/).
**Ruta de cluster:** proyecto final tipo GPT-2: tokenizador simple, decoder causal, entrenamiento, generación y evaluación.

**Entregable:** experimento con permutaciones, positional embeddings y reporte de errores. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** la self-attention es **invariante a permutaciones** (ciega al orden), lo que para el lenguaje y las imágenes es fatal. El **positional encoding** lo arregla **sumando** a cada token una firma de su posición —**sinusoidal** (generaliza a longitudes nuevas), **aprendido** (BERT) o **relativo moderno** (RoPE, ALiBi, clave para contextos largos)—. Los **Vision Transformers** muestran la generalidad del modelo: cortan la imagen en **parches que se tratan como palabras** (+ PE 2D) y, **a escala de datos**, igualan a las CNN. Lección de fondo: el Transformer aprende **relaciones entre tokens**; dale tokens de cualquier modalidad + sus posiciones y se vuelve universal (multimodalidad).

---

**Referencias**

- Vaswani, A., et al. (2017). Attention is all you need (§3.5 Positional Encoding). *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Dosovitskiy, A., et al. (2021). An image is worth 16x16 words: Transformers for image recognition at scale. *ICLR*. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
- Su, J., et al. (2021). RoFormer: Enhanced transformer with rotary position embedding (RoPE). [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
- Press, O., Smith, N. A., & Lewis, M. (2021). Train short, test long: Attention with linear biases (ALiBi). [arXiv:2108.12409](https://arxiv.org/abs/2108.12409)
- Radford, A., et al. (2021). Learning transferable visual models from natural language supervision (CLIP). [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)

*Retrieval: (1) ¿por qué la self-attention es ciega al orden?; (2) ¿qué hace el positional encoding y qué aporta el sinusoidal frente al aprendido?; (3) ¿cómo convierte un ViT una imagen en tokens?; (4) ¿por qué el ViT necesita muchos datos para ganar a una CNN?*
