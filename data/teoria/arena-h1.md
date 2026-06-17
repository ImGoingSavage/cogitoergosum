# DAGs y adjustment sets

## De qué trata esta lección (y qué sabrás hacer al final)

Antes de correr una regresión, hay una decisión que la mayoría toma a ciegas: **¿qué variables incluyo en el ajuste?** La respuesta intuitiva ("controla por todo lo disponible") puede *sesgar* tu estimación en vez de mejorarla. Esta lección construye, desde cero, la herramienta que decide bien: el **DAG** como mapa de tus supuestos, los tres roles de una variable (confounder, mediador, collider) y el **criterio de back-door** que te dice exactamente qué ajustar para estimar un efecto causal.

Al terminar podrás: (1) clasificar cada variable por su rol y saber si ajustarla; (2) reconocer por qué ajustar un collider es el error más costoso (paradoja de Berkson); (3) aplicar el criterio de back-door para elegir el conjunto de ajuste; y (4) evitar la trampa de las variables post-tratamiento. Es la versión operativa de las junciones de [[arena-h16]], orientada a "qué meto en el modelo".

## Por qué importa el DAG antes de la regresión

Un Directed Acyclic Graph (DAG) causal es un mapa de tus supuestos sobre el proceso que generó los datos. Si lo dibujas antes de construir tu modelo, te dice exactamente qué variables incluir en el ajuste — y cuáles dejarías fuera aunque parezca contraintuitivo.

Sin el DAG, "controlar por todas las variables disponibles" puede sesgar tu estimado en lugar de mejorarlo.

---

## Los tres tipos de variables en un DAG

### Confounder (variable de confusión)

```
C
├── → X (causa la exposición)
└── → Y (causa el outcome)
```

Un confounder crea un camino no causal entre X e Y (camino "de puerta trasera"). **Ajustar lo cierra.**

Ejemplo: la edad (C) causa tanto el ejercicio (X) como la salud cardiovascular (Y). Sin ajustar por edad, la asociación ejercicio-salud mezcla el efecto causal con el efecto espurio vía edad.

### Mediator (mediador)

```
X → M → Y
```

Un mediator está en el camino causal de X a Y. **Ajustar estima el efecto directo** (X → Y) pero cierra el indirecto (X → M → Y).

Ejemplo: un medicamento (X) reduce el colesterol (M), que reduce el riesgo cardíaco (Y). Ajustar por colesterol estima el efecto del medicamento que no pasa por la reducción de colesterol.

### Collider

```
X → C ← Y
```

Ambas flechas apuntan al collider. **No ajustar.** Ajustar un collider **abre** una asociación espuria entre X e Y que no existe en la población no condicionada.

---

## El error más costoso: ajustar un collider

La paradoja de Berkson: en un hospital, los pacientes con la enfermedad A parecen tener menos probabilidad de tener la enfermedad B, aunque en la población general no hay relación.

DAG: 
```
Enfermedad A → Hospitalizado ← Enfermedad B
```

Al estudiar solo pacientes hospitalizados, condicionas en el collider "Hospitalizado". Esto abre el camino A ↔ B y crea una correlación espuria negativa: entre los hospitalizados, si no tienes A, es más probable que tengas B (y viceversa).

**Señal del collider:** las flechas llegan al nodo, no salen.

---

## El criterio de backdoor

Un conjunto de variables Z satisface el criterio de backdoor para estimar el efecto de X sobre Y si:
1. Z no contiene descendientes de X
2. Z bloquea todos los caminos "de puerta trasera" (que empiezan con una flecha que entra a X)

Un camino está bloqueado si:
- Contiene un no-collider que está en Z (el confounder es ajustado), o
- Contiene un collider que **no** está en Z (y ninguno de sus descendientes está en Z)

---

## Ejemplo práctico: ¿qué ajustar?

DAG hipotético para el efecto de una intervención educativa (X) sobre el ingreso (Y):

```
Nivel socioeconómico familiar (C) → X
C → Y
X → Habilidades cognitivas (M) → Y
X → Y (efecto directo)
X → Primer empleo (Co) ← Y
```

- C es confounder: ajustar
- M es mediator: ajustar estima el efecto directo solamente
- Co es collider: NO ajustar

Si quieres el efecto total de X sobre Y: ajusta {C}, no ajustes M ni Co.

---

## Variables post-tratamiento: la regla práctica

Nunca incluyas en un modelo de regresión variables que son causadas por la exposición X, a menos que quieras estimar el efecto directo específicamente. Estas variables son mediators (o colliders si también causan Y por otra vía).

Preguntas a hacerse antes de incluir una variable:
1. ¿Esta variable causa X, o X la causa?
2. ¿Podría ser un collider (causada tanto por X como por Y)?
3. Si la incluyo, ¿qué pregunta causal estoy respondiendo?

---

## Herramientas formales

- **dagitty.net**: herramienta online para dibujar DAGs e identificar adjustment sets automáticamente
- **DoWhy** (Python): implementación del framework causal de Pearl con DAGs
- **ggdag** (R): visualización de DAGs con tidyverse

---

## Mini-ejemplo trabajado: la paradoja de Berkson con números

En la población general, tener gripe (A) y tener una fractura (B) son **independientes**. Inventemos 100 personas: 10 con gripe, 10 con fractura, y por independencia 1 con ambas. Ahora estudias solo a los **hospitalizados** (collider), y supón que se hospitaliza a quien tiene A *o* B:

- Hospitalizados: 10 (gripe) + 10 (fractura) − 1 (ambas) = 19.
- Entre ellos, de los 10 con gripe, solo 1 tiene fractura → 10%.
- Entre los hospitalizados **sin** gripe (9), todos están por su fractura → 100% tiene fractura.

Condicionar en "hospitalizado" creó una correlación **negativa** espuria entre gripe y fractura que no existe en la población. Las flechas A→Hosp←B se "abrieron" al filtrar por el collider.

**Predicción antes de seguir:** tu instinto dice "controla por más variables para reducir sesgo". ¿Siempre ayuda? Respuesta: **no** — ajustar por un confounder cierra un camino espurio (bien), pero ajustar por un *collider* lo **abre** (mal). "Controlar por todo" no es prudencia: puede fabricar el sesgo que creías evitar. El grafo, no la disponibilidad de datos, decide qué ajustar.

## Prototipo, contraejemplo y caso borde

- **Prototipo (confounder):** C→X y C→Y → ajustar cierra el back-door y desconfunde.
- **Contraejemplo (collider):** X→C←Y → NO ajustar; condicionar abre una asociación falsa (Berkson).
- **Caso borde (mediador):** X→M→Y → ajustar estima el efecto *directo* pero borra el indirecto; si querías el efecto total, no lo ajustes. El mismo nodo puede pedir ajuste o no según la pregunta causal.

## Errores típicos

- **Conceptual:** "ajustar por todo reduce ruido" — ajustar un collider o un mediador introduce sesgo, no lo elimina.
- **Técnico:** incluir variables post-tratamiento (causadas por X) en la regresión sin querer el efecto directo.
- **De supuestos:** elegir el conjunto de ajuste por disponibilidad de datos en vez de por el DAG.

## Transferencia isomorfa

- **Ajustar un collider ↔ data leakage y sesgo de selección:** condicionar en una variable posterior (hospitalización, una feature filtrada) abre asociaciones espurias igual que el leakage infla el desempeño (conecta con [[arena-h17]] y [[arena-cds1]]).
- **Confounder no ajustado ↔ variable omitida en regresión:** el coeficiente con signo absurdo nace de no cerrar el back-door (conecta con [[arena-pst4]]).
- **Selección por outcome ↔ efectos de red / muestreo sesgado:** filtrar la cohorte por algo que X e Y causan reaparece como contaminación de control en A/B tests (conecta con [[arena-ads4]]).
- **do(x) ↔ borrar las flechas hacia X:** el back-door es la receta observacional cuando no puedes intervenir (conecta con [[arena-h17]]).

Moraleja de la arista: *el grafo decide qué ajustar: cierra confounders, nunca toques colliders; "controlar por todo" puede fabricar el sesgo que querías evitar.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "¿Qué variables incluyo en el modelo?" | Dibuja el DAG primero. Luego decide. |
| "Colega quiere controlar por variable post-tratamiento" | ¿Es mediator o collider? Pregunta qué quiere estimar |
| "Correlación espuria entre dos variables independientes" | Busca un collider compartido en el que estés condicionando |
| "Selección de muestra basada en outcome o exposición" | Posible collider vía la variable de selección |
| "Ajusta todo para reducir ruido" | No: ajustar un collider introduce sesgo, no lo elimina |

---

## Ejercicio de consolidación

Un estudio analiza el efecto de fumar (X) sobre el cáncer de pulmón (Y). Las variables disponibles son: ingreso (causa fumar, no causa directamente el cáncer), residencia en zona urbana (causa fumar y también causa el cáncer por contaminación), y tos crónica (causada por fumar, también causa la visita al médico donde se detecta el cáncer).

1. Dibuja el DAG con estas 5 variables (X, Y, ingreso, urbana, tos).
2. ¿Qué variables ajustas para estimar el efecto total de X sobre Y?

*Respuesta: Ajusta {ingreso, urbana} (confounders). No ajustes tos (es mediator del camino X → tos → diagnóstico → Y, y posiblemente collider en el diagnóstico). Efecto total: ajusta los confounders, no los mediators.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

Los DAGs causales de esta unidad son grafos con semantica: heredan la intuicion de [[zeitz-41]] sobre relaciones y caminos, pero agregan direccion causal y adjustment sets. Esa diferencia prepara el salto a [[gen-ma2]], donde el grafo de agentes tambien exige controlar que informacion cruza cada arista.
<!-- GRAFO_CONEXO_OLEADA3_END -->
