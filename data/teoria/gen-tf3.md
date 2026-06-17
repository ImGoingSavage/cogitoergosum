# Multi-head, masking y la arquitectura Transformer completa

> Recurso troncal: [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) §3.1–3.3. Ensambla la self-attention de [[gen-tf2]] en el bloque Transformer completo. Prepara [[gen-tf4]] (positional encoding y ViT).

## De qué trata (y qué sabrás hacer al final)

Ya tienes la pieza central (scaled dot-product attention). Esta lección la ensambla en el **bloque Transformer** real: por qué se usan **varias cabezas** de atención (multi-head), cómo el **masking** controla qué puede ver cada palabra, y cómo se apilan atención + **residuales** + **LayerNorm** + **red feed-forward** para formar las capas que, repetidas decenas de veces, son un LLM.

La intuición: una sola cabeza de atención es como leer una frase prestando atención a **un** tipo de relación (digamos, sujeto-verbo). Pero el lenguaje tiene muchas relaciones simultáneas: gramaticales, de correferencia ("él" → "Juan"), semánticas, de posición. **Multi-head** es tener **varios lectores en paralelo**, cada uno especializado en un tipo de relación, y luego combinar sus hallazgos. El **masking** es taparle los ojos al lector para que no haga trampa (no mire el futuro que debe predecir). Y los **residuales + LayerNorm** son los andamios que permiten apilar muchas capas sin que el entrenamiento colapse.

Al terminar podrás: (1) explicar **por qué multi-head** supera a una sola cabeza; (2) distinguir **masking causal** (no ver el futuro) de **padding mask**; (3) nombrar los componentes de un **bloque Transformer** y qué hace cada uno; y (4) entender encoder vs decoder.

## Multi-head attention: varios lectores en paralelo

En vez de una atención sobre vectores de dimensión $d_{\text{model}}$, se hacen $h$ atenciones en paralelo (las **cabezas**), cada una sobre proyecciones más pequeñas (dimensión $d_k = d_{\text{model}}/h$):

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)\,W^O$$
$$\text{donde } \text{head}_i = \text{Attention}(QW_i^Q,\, KW_i^K,\, VW_i^V)$$

Cada cabeza tiene **sus propias** matrices $W_i^Q, W_i^K, W_i^V$, así que aprende a fijarse en un tipo distinto de relación. Sus salidas se **concatenan** y se mezclan con una matriz final $W^O$. Visualizaciones del Transformer entrenado ([BertViz](https://github.com/jessevig/bertviz), análisis de [Clark et al., 2019](https://arxiv.org/abs/1906.04341)) muestran cabezas que se especializan: unas siguen al siguiente token, otras a la correferencia, otras al objeto del verbo. **Por qué importa:** una sola cabeza promedia todo en un espacio; varias cabezas capturan **múltiples relaciones a la vez** sin que se estorben. El costo es ~el mismo que una atención grande, porque cada cabeza es más pequeña.

## Masking: controlar qué puede ver cada palabra

La atención, por defecto, deja que cada palabra mire a **todas**. A veces eso es trampa o error:

- **Masking causal (look-ahead mask):** en un **decoder** que genera texto palabra por palabra, al predecir la palabra $t$ el modelo **no debe ver** las palabras $t+1, t+2, \dots$ (el futuro que aún no existe). Se impone poniendo los puntajes de esas posiciones futuras en $-\infty$ **antes** del softmax, de modo que su peso quede en 0. Esto es lo que hace "autoregresivo" a un GPT: cada token solo atiende a los anteriores. Es la diferencia entre un modelo que **genera** y uno que solo **lee**.
- **Padding mask:** cuando se procesan frases de distinta longitud en un lote, las cortas se rellenan ("padding") hasta igualar la más larga. El padding mask evita que las palabras reales atiendan a ese relleno vacío.

Misma mecánica (poner $-\infty$ donde no se debe mirar), distintos propósitos. El masking causal es la pieza que distingue a los modelos **generativos** (GPT, decoder-only) de los puramente **comprensivos** (BERT, encoder-only, que sí ven todo el contexto — [Devlin et al., 2019](https://arxiv.org/abs/1810.04805)).

## El bloque Transformer completo

Un bloque (capa) del Transformer apila, en este orden:

1. **Multi-head self-attention** — mezcla contexto entre tokens.
2. **Conexión residual + LayerNorm** — se suma la entrada a la salida de la atención ($x + \text{Attn}(x)$) y se normaliza. La **residual** ([He et al., 2016](https://arxiv.org/abs/1512.03385)) permite que el gradiente fluya por atajos, haciendo entrenable apilar **muchas** capas. **LayerNorm** ([Ba et al., 2016](https://arxiv.org/abs/1607.06450)) estabiliza las activaciones.
3. **Red feed-forward (FFN)** — dos capas lineales con una no-linealidad, aplicadas a **cada posición por separado**. Es donde el modelo "procesa" lo que la atención reunió (gran parte de la capacidad/parámetros vive aquí).
4. **Residual + LayerNorm** otra vez.

Apila $N$ de estos bloques (en GPT-3, 96 capas) y tienes la columna vertebral. La atención **mueve información entre posiciones**; la FFN **transforma** cada posición. Esa alternancia, repetida, es lo que hace tan capaces a los LLMs.

## Encoder, decoder, o ambos

El Transformer original era **encoder-decoder** (para traducción): el encoder lee la entrada (atención sin máscara causal), el decoder genera la salida (con máscara causal) consultando al encoder vía **cross-attention** ([[gen-tf2]]). De ahí salieron tres familias:
- **Encoder-only (BERT):** ve todo el contexto; ideal para **entender** (clasificar, extraer).
- **Decoder-only (GPT, Claude, Llama):** masking causal; ideal para **generar**. Es la arquitectura dominante de los LLMs actuales.
- **Encoder-decoder (T5, traducción):** entrada→salida estructurada.

## Mini-ejemplo trabajado: ¿por qué la máscara causal y no entrenar "a ver el futuro"?

Entrenas un modelo para completar texto. Si durante el entrenamiento dejaras que, al predecir la palabra 5, el modelo viera la palabra 5 real (y las siguientes), aprendería a **copiarla** en vez de **predecirla** — y en producción, donde el futuro no existe, fallaría por completo. La máscara causal fuerza al modelo a predecir cada palabra **solo con el pasado**, que es la única situación realista al generar. Predicción antes de seguir: un modelo **encoder-only** (BERT) **sí** ve todo el contexto. ¿Sirve para generar texto fluido palabra por palabra? → No directamente; está optimizado para *entender* (con tokens enmascarados al azar), no para generar autoregresivamente. Arquitectura sigue a la tarea.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El lenguaje tiene muchas relaciones a la vez" | Multi-head (cabezas especializadas) |
| "El modelo genera palabra por palabra" | Decoder-only + masking causal |
| "Solo necesito entender/clasificar texto" | Encoder-only (BERT) |
| "Apilo muchas capas y no entrena" | Faltan residuales / LayerNorm |
| "Frases de distinta longitud en un lote" | Padding mask |

## Errores típicos

- **Creer que multi-head es 'más atención de lo mismo':** no; cada cabeza aprende relaciones distintas, esa es la ganancia.
- **Olvidar la máscara causal en generación:** el modelo "haría trampa" viendo el futuro y fallaría en producción.
- **Subestimar la FFN:** gran parte de la capacidad del modelo vive en las feed-forward, no solo en la atención.
- **Confundir LayerNorm con BatchNorm:** LayerNorm normaliza por muestra (no por lote), clave para secuencias.

## Contraejemplo y caso borde

- **Contraejemplo:** más cabezas no es siempre mejor; estudios ([Michel et al., 2019](https://arxiv.org/abs/1905.10650)) muestran que muchas cabezas son **podables** sin perder desempeño — su valor es la diversidad, no la cantidad bruta.
- **Caso borde:** el orden de la LayerNorm importa: "post-norm" (original) vs "pre-norm" (común hoy en LLMs grandes) cambia la estabilidad del entrenamiento a gran profundidad ([Xiong et al., 2020](https://arxiv.org/abs/2002.04745)). Un detalle de andamiaje con efecto real.

## Transferencia isomorfa

- **Multi-head ↔ ensembles/comités:** varios "expertos" con vistas distintas que se combinan, como un ensemble de modelos o un panel de revisores (la idea de paneles de jueces que usamos en evaluación).
- **Residual ↔ "no empieces de cero":** la capa aprende un **ajuste** sobre la entrada ($x + f(x)$), no a reconstruirla — como un control de versiones que guarda *diffs*, no copias completas.
- **Masking causal ↔ validación temporal:** no usar información del futuro para predecir el presente es exactamente la regla de oro contra el *data leakage* temporal en series de tiempo y backtesting.

Moraleja de la arista: *atención = mover información; FFN = transformarla; residual+norm = poder apilar; máscara = qué se permite ver.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** explica por qué poner $-\infty$ en los puntajes (antes del softmax) equivale a "prohibir mirar" esa posición.
- **Misión externa (lab vivo):** explora [BertViz](https://github.com/jessevig/bertviz) (visualizador de cabezas de atención) o las figuras de [Clark et al., 2019](https://arxiv.org/abs/1906.04341). **Criterio de cierre:** describir una relación lingüística que una cabeza concreta parece capturar.
- **Mini-entregable (mini-proyecto del cluster):** un **diagrama anotado de un bloque Transformer** (atención → residual+norm → FFN → residual+norm, con dónde entra el masking), explicando cada pieza con tus palabras. Evalúalo con la rúbrica de 5 criterios del cluster.

## Reconstrucción mínima en código

Un bloque GPT real, estilo nanoGPT: multi-head causal + MLP con residuales. Apilar `N` de estos **es** un GPT. La máscara triangular es la que garantiza que el token `t` solo use `1..t` (sin fuga del futuro).

```python
import torch, torch.nn as nn

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.n_heads, self.d_head = n_heads, d_model // n_heads
        self.qkv  = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
    def forward(self, x):                                  # x: (B, T, d_model)
        B, T, C = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        # parte en cabezas: (B, n_heads, T, d_head)
        q, k, v = [t.view(B, T, self.n_heads, self.d_head).transpose(1, 2) for t in (q, k, v)]
        att  = q @ k.transpose(-2, -1) / self.d_head ** 0.5
        mask = torch.tril(torch.ones(T, T))               # nadie mira al futuro
        att  = att.masked_fill(mask == 0, float('-inf')).softmax(-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, C)     # vuelve a juntar cabezas
        return self.proj(y)

class Block(nn.Module):                                    # el ladrillo de GPT
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d_model), nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads)
        self.mlp  = nn.Sequential(nn.Linear(d_model, 4*d_model), nn.GELU(),
                                  nn.Linear(4*d_model, d_model))
    def forward(self, x):
        x = x + self.attn(self.ln1(x))                     # residual: aprende un ajuste
        x = x + self.mlp(self.ln2(x))
        return x
```

**Qué observar:** corre `Block(8, 2)(torch.randn(1, 4, 8))` y revisa la matriz de atención: la fila 0 solo tiene peso en la columna 0. Si vieras peso a la derecha de la diagonal, la máscara causal estaría rota y el modelo haría *leakage* del futuro durante el entrenamiento. [[gen-tf4]] añade la pieza que falta: la posición.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (multi-head attention, masking causal y bloques decoder) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** construir multi-head attention con máscara causal, residual, LayerNorm y MLP.
2. **Baseline obligatorio:** una sola cabeza sin máscara causal.
3. **Versión mejorada:** multi-head causal attention con residual y LayerNorm.
4. **Evaluación:** perplexity de validación, prueba de fuga causal y diversidad entre heads.
5. **Fallo que debes explicar:** el modelo hace leakage mirando tokens futuros durante entrenamiento.
6. **Transferencia:** agentes: separar subproblemas como heads especializadas, pero medir redundancia.

**Laboratorio externo principal:** [nanoGPT](https://github.com/karpathy/nanoGPT).
**Laboratorio alternativo:** [Karpathy Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html).
**Ruta de cluster:** proyecto final tipo GPT-2: tokenizador simple, decoder causal, entrenamiento, generación y evaluación.

**Entregable:** bloque decoder entrenable con tests de causalidad y ablation de heads. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** **multi-head** corre varias atenciones en paralelo, cada una con sus matrices, para capturar **relaciones distintas a la vez** (y se concatenan con $W^O$). El **masking** pone $-\infty$ antes del softmax: **causal** (un decoder no ve el futuro → modelos generativos como GPT) o **padding** (ignorar relleno). El **bloque Transformer** apila *atención → residual+LayerNorm → FFN → residual+LayerNorm*; la atención **mueve** información entre posiciones y la FFN la **transforma**, y los residuales+norm permiten apilar decenas de capas. De ahí las familias **encoder-only** (BERT, entender), **decoder-only** (GPT/Claude, generar) y **encoder-decoder** (T5).

---

**Referencias**

- Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers. *NAACL*. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- He, K., et al. (2016). Deep residual learning for image recognition. *CVPR*. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)
- Ba, J. L., Kiros, J. R., & Hinton, G. E. (2016). Layer normalization. [arXiv:1607.06450](https://arxiv.org/abs/1607.06450)
- Clark, K., et al. (2019). What does BERT look at? An analysis of BERT's attention. [arXiv:1906.04341](https://arxiv.org/abs/1906.04341)
- Vig, J. (2019). BertViz: A tool for visualizing attention. [GitHub](https://github.com/jessevig/bertviz)

*Retrieval: (1) ¿por qué multi-head supera a una sola cabeza?; (2) ¿qué hace la máscara causal y a qué familia de modelos define?; (3) nombra los 4 componentes de un bloque Transformer y su rol; (4) encoder-only vs decoder-only.*
