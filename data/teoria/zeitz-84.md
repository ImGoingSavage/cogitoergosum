# El poder de la geometría elemental

*Lección redactada para CogitoErgoSum a partir de la sección 8.4 de Zeitz (The Power of Elementary Geometry). Cubre el contenido completo de la unidad.*

## La checklist del solucionista geométrico

Los ocho puntos de Zeitz, en orden de trabajo:

1. **Dibuja un diagrama cuidadoso** (regla y compás mentales: proporciones honestas).
2. **Traza auxiliares — con moderación** (el penúltimo paso dicta cuáles, §8.2).
3. **Empieza cazando ángulos** (angle chasing), sin depender SOLO de eso.
4. **Busca a tus mejores amigos: triángulos rectángulos, paralelas y puntos concíclicos.**
5. **Compara áreas** (la lente multiplicativa de §8.3).
6. **Explota los semejantes sin piedad.**
7. **Usa la simetría y los puntos distinguidos** (centros, puntos medios, pies de altura).
8. **Puntos fantasma** cuando haya que probar que algo pasa por algún lugar (§8.2).

Los «tres mejores amigos» del punto 4 no son decorativos: cada uno es un generador de información — el rectángulo trae Pitágoras y la configuración de la altura; las paralelas traen ángulos iguales y semejantes; los concíclicos traen el ángulo inscrito y la potencia del punto.

## Un diagrama cuidadoso ES una herramienta de descubrimiento

En el USAMO 1990 (abajo), un dibujo honesto **revela** que los pies de las alturas caen sobre ciertos círculos — el regalo lo da Tales (§8.2): un ángulo recto que subtiende un diámetro delata el círculo. Un dibujo chueco esconde exactamente esos regalos: las coincidencias visuales (tres puntos alineados, cuatro en un círculo, dos segmentos iguales) son **conjeturas gratis** que el dibujo descuidado jamás te susurrará. Dibujar bien es ensuciarse las manos (§2.2) en versión geométrica.

## El menú de penúltimos pasos para «4 puntos concíclicos»

Para demostrar que M, N, P, Q comparten círculo, hay un MENÚ — listar los candidatos y **elegir el barato** es la estrategia (USAMO 1990):

1. **Encontrar el centro:** exhibe un punto equidistante de los cuatro.
2. **Cuadrilátero cíclico:** ángulos opuestos suplementarios (suman 180°).
3. **Mismo segmento, mismo lado:** dos ángulos iguales que subtienden el mismo segmento desde el mismo lado (recíproco del ángulo inscrito).
4. **Recíproco de la potencia del punto** (abajo).
5. **Recíproco de Ptolomeo** (en cíclicos, AC·BD = AB·CD + AD·BC).

**En el USAMO 1990** (cuatro puntos marcados sobre las alturas de un triángulo), el dibujo cuidadoso hace saltar al candidato 1: **el vértice A resulta equidistante de los cuatro puntos** — los segmentos desde A son radios de círculos que el propio dibujo sugiere (los ángulos rectos de las alturas subtienden diámetros: Tales otra vez). Probar cuatro distancias iguales fue más barato que cualquier persecución de ángulos. Moraleja: el menú se recorre **comparando costos**, no en orden fijo.

## Potencia del punto (POP)

> **Teorema:** fija un punto P y un círculo. Para TODA recta por P que corte al círculo en X e Y, el producto **PX·PY es el mismo** (la «potencia» de P respecto al círculo — un invariante de P).
>
> **Caso límite:** si la recta es tangente en T, la potencia es **PT²**. Corolario querido: **las dos tangentes desde un punto exterior son iguales**.

(*De dónde sale:* dos cuerdas por P generan triángulos semejantes — ángulos inscritos sobre los mismos arcos — y la proporción cruza a PX·PY = PX′·PY′.)

> **El RECÍPROCO certifica concíclicos:** si dos rectas se cortan en X, con Q, P sobre una y M, N sobre la otra, y **QX·XP = MX·XN** (con la configuración de signos correcta), entonces Q, P, M, N están en un círculo.

POP convierte círculos en **álgebra de productos de segmentos** — y el recíproco convierte álgebra en círculos.

## Cevianas y áreas: razones sin coordenadas

Para razones sobre **cevianas que se cortan** (¿en qué proporción divide el punto de corte a cada ceviana?), la lente de §8.3: **compara áreas de triángulos con base común** (o altura común). Cada razón de segmentos sobre una ceviana es una razón de áreas de los triángulos que la flanquean; encadenando dos o tres de esas igualdades, las razones «mágicas» (como el 2:1 de las medianas en el centroide) caen **sin coordenadas ni trigonometría**. Protocolo: nombra las áreas de las piezas, escribe cada razón de segmentos como razón de áreas, resuelve el sistemita.

## El error conceptual del cuadrilátero cíclico

«∠QMP + ∠QNP = 180° **porque** MNPQ es cíclico, **por lo tanto** es cíclico» — además de circular, delata una confusión de fondo: el lema del cuadrilátero cíclico tiene **dos direcciones distintas**. *Directa:* cíclico ⇒ opuestos suplementarios. *Recíproca:* opuestos suplementarios ⇒ cíclico. Para DEMOSTRAR conciclicidad necesitas la **recíproca**, y su entrada (los 180°) debe venir de **otra fuente** (angle chasing independiente). Citar la dirección equivocada es el mismo error recíproca/implicación de §2.3, vestido de geometría.

## Disparadores

- **Tangentes desde un punto exterior** o **productos de segmentos sobre cuerdas que se cortan** → potencia del punto (igualdad de tangentes; PX·PY invariante); para concíclicos, su recíproco.
- «Demuestra que 4 puntos están en un círculo» → recorre el MENÚ y elige el penúltimo paso barato.
- Razones sobre cevianas → áreas con bases comunes.
- El dibujo sugiere una coincidencia → trátala como conjetura y busca qué amigo (rectángulo/paralela/concíclicos) la explica.

## Síntesis

> **Chunk mínimo:** Checklist: diagrama honesto (es herramienta de descubrimiento: las coincidencias visuales son conjeturas gratis) → auxiliares con moderación → angle chasing → los tres amigos (rectángulos, paralelas, concíclicos) → áreas → semejantes → simetría → fantasmas. Para «4 concíclicos», un MENÚ que se recorre por costo: centro equidistante (lo barato en el USAMO 1990, vía Tales), opuestos suplementarios (¡dirección recíproca, con los 180° de otra fuente!), mismo segmento mismo lado, recíproco de POP, Ptolomeo. POP: PX·PY constante para toda recta por P (tangente: PT²; corolario: tangentes desde un punto son iguales); su recíproco certifica concíclicos. Razones sobre cevianas → sistema de áreas con bases comunes.

---

*Antes del quiz: reconstruye de memoria la checklist con los tres amigos, el enunciado de POP con tangente y recíproco, el menú de concíclicos con la elección del USAMO 1990 y las dos direcciones del lema cíclico.*
