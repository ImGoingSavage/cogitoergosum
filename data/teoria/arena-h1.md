# DAGs y adjustment sets

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

1. Dibuja el DAG con estas 4 variables (X, Y, ingreso, urbana, tos).
2. ¿Qué variables ajustas para estimar el efecto total de X sobre Y?

*Respuesta: Ajusta {ingreso, urbana} (confounders). No ajustes tos (es mediator del camino X → tos → diagnóstico → Y, y posiblemente collider en el diagnóstico). Efecto total: ajusta los confounders, no los mediators.*
