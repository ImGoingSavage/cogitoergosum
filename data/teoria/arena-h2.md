# Target trial emulation e immortal time bias

## El ensayo objetivo: la pregunta que ordena todo

El "target trial" (ensayo objetivo) es el experimento aleatorizado hipotético que un estudio observacional intenta emular. Formularlo explícitamente es el paso que diferencia el análisis causal riguroso del análisis descriptivo.

La pregunta no es "¿qué asociación existe en los datos?" sino "¿qué ensayo clínico aleatorizado habríamos necesitado para responder esta pregunta, y cómo lo emulamos con datos observacionales?"

---

## Los 7 componentes del protocolo

Un target trial se especifica completamente con estos 7 elementos:

1. **Criterios de elegibilidad:** ¿Qué características debe tener un participante para entrar al estudio? (al inicio, en t=0)

2. **Estrategias de tratamiento:** Las opciones específicas que se comparan. No "fue tratado" vs "no fue tratado", sino descripciones precisas (dosis, duración, adherencia mínima).

3. **Asignación:** En el trial hipotético, aleatorización. En la emulación, el método para lograr comparabilidad (matching, IPW, etc.).

4. **Inicio del seguimiento (t=0):** El momento desde el que se mide el tiempo. Debe coincidir con: (a) momento de elegibilidad, (b) momento de "asignación" al tratamiento o control.

5. **Outcome:** La variable de resultado, con su definición precisa (cómo se mide, quién lo mide).

6. **Fin del seguimiento:** Cuándo y por qué razones termina el seguimiento de un participante (evento, muerte, pérdida, fecha límite).

7. **Estimando:** El parámetro que quieres estimar (diferencia de riesgos, razón de tasas, etc.) y si es efecto intención de tratar o per-protocol.

---

## Immortal time bias: el sesgo del tiempo invulnerable

### El escenario clásico

Un estudio quiere evaluar si los pacientes que reciben un trasplante de órgano viven más que los que están en lista de espera pero no reciben trasplante.

Si el seguimiento empieza cuando el paciente entra a la lista de espera, el grupo "trasplantado" tiene un período entre la entrada a la lista y la fecha del trasplante durante el cual:
- No pudo morir (o si murió, salió del grupo trasplantado)
- No pudo sufrir el outcome de ninguna otra forma que lo saque del denominador

Este período es "inmortal" para el grupo trasplantado. Si ese tiempo se cuenta como tiempo de seguimiento, el grupo trasplantado parece vivir más simplemente porque los muertos tempranos nunca llegaron a trasplantarse.

### La señal

> "El grupo tratado requiere sobrevivir (o permanecer en observación) un período antes de ser clasificado como tratado."

O en términos del DAG temporal:

```
t=0 (entrada a lista)  ...  t=trasplante  ...  t=death/censoring
        |___ tiempo inmortal ___|
```

### El rediseño que lo elimina

**Principio:** t=0 debe ser el mismo para todos los sujetos, y debe coincidir con el momento de "asignación".

Métodos de emulación:
1. **Clonación + censura + ponderación:** cada sujeto es "clonado" en t=0 y asignado a ambas estrategias. La censura artificial cuando alguien se desvía de la estrategia asignada se pondera con IPW.
2. **Sequential trials:** a cada semana/mes, se define una nueva cohorte de elegibles y se emula el trial desde ese punto.

### [CAJA NEGRA OK] Ponderación IPW

- **Qué puedes asumir:** existe un método estándar (inverse probability weighting) que re-pondera a los sujetos no censurados para compensar la censura artificial de la clonación.
- **Por qué se permite asumirlo:** su derivación formal exige teoría que no aporta al reconocimiento del sesgo ni a proponer el rediseño.
- **Qué sí debes razonar:** por qué la clonación necesita censura (un clon se desvía de su estrategia asignada) y por qué censurar sin re-ponderar introduce sesgo de selección.
- **Intuición mínima:** cada sujeto que sigue en observación «habla por» los censurados de su perfil de riesgo.
- **Cuándo reabrir la caja:** si vas a IMPLEMENTAR la emulación (no solo diseñarla): Hernán & Robins, cap. 12.

---

## Ejemplo: medicación antihipertensiva

**Estudio original:** "Los pacientes que tomaron el medicamento por >2 años tienen 30% menos infartos que los que lo tomaron <2 años."

**Problema:** para estar en el grupo ">2 años", un paciente debe haber sobrevivido 2 años sin infarto. Los pacientes que tuvieron un infarto en el primer año de tratamiento están automáticamente en el grupo "<2 años". El grupo ">2 años" está sesgado hacia supervivientes.

**Target trial correspondiente:**
1. Elegibilidad: pacientes nuevos en medicación antihipertensiva, sin infarto previo.
2. Estrategias: adherir ≥2 años vs menos.
3. Asignación: aleatorización hipotética en t=0 (inicio de la medicación).
4. t=0: fecha de la primera prescripción.
5. Outcome: infarto no fatal o muerte cardiovascular.
6. Fin: 3 años desde t=0 o primer evento.
7. Estimando: diferencia de riesgo per-protocol (ponderando la adherencia real).

---

## Prevalent user bias: el primo del immortal time bias

Un estudio incluye a pacientes que ya llevan tiempo en tratamiento (usuarios prevalentes) en vez de solo nuevos usuarios (incidentes). Los usuarios prevalentes son supervivientes del período inicial: los que tuvieron reacciones adversas o murieron ya salieron de la cohorte.

**Solución:** active comparator new user design. Solo incluye usuarios que inician el tratamiento por primera vez, comparados con usuarios que inician un tratamiento alternativo al mismo tiempo.

---

## Plantilla de diseño (cópiala en la pizarra antes de proponer el análisis)

| Campo | Tu respuesta |
|---|---|
| Supuestos | |
| Métrica principal | |
| Métrica secundaria / guardrails | |
| Riesgos | |
| Tradeoffs | |
| Datos disponibles | |
| Datos NO disponibles | |
| Componentes del sistema | |
| Puntos de leakage | |
| Privacidad / PHI | |
| Monitoreo | |
| Rollback | |
| Casos borde | |

---

## Mini-ejemplo trabajado: el tiempo inmortal del trasplante, contado

100 pacientes entran a lista de espera. A los 30 trasplantados les cuentas el seguimiento **desde la entrada a la lista**. Pero para *llegar* al trasplante (digamos a los 6 meses) hubo que **sobrevivir** esos 6 meses: quien murió antes nunca fue trasplantado y cayó en el grupo "lista". Así, el grupo trasplantado acumula 6 meses "inmortales" de seguimiento donde, por construcción, nadie podía morir como trasplantado.

Resultado: el grupo trasplantado "vive más" aunque el trasplante no haga nada — el sesgo viene de regalarle tiempo durante el cual era invulnerable. La corrección: **t=0 igual para todos**, alineado con el momento de asignación (o clonar + censurar + ponderar, o sequential trials).

**Predicción antes de seguir:** ¿el immortal time bias infla o desinfla el beneficio del tratamiento? Respuesta: lo **infla** sistemáticamente — el grupo tratado se enriquece de supervivientes. Es el mismo mecanismo que el "prevalent user bias" (incluir usuarios que ya sobrevivieron al período de adversos) y, en ML, que evaluar con un split que mira el futuro. Quien define mal el tiempo cero, regala supervivencia.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** el grupo tratado se define por *completar* algo (N ciclos, ≥2 años) → sospecha tiempo inmortal; alinea t=0 con la asignación.
- **Contraejemplo (no es immortal time):** si la clasificación tratado/control se fija en t=0 sin requerir supervivencia previa, no hay tiempo inmortal aunque los grupos difieran.
- **Caso borde (retención de usuarios):** "los que usan más la app retienen mejor" puede ser que los heavy users simplemente sobrevivieron al onboarding — immortal time disfrazado de engagement.

## Errores típicos

- **Conceptual:** empezar el seguimiento en un evento (diagnóstico, entrada a lista) distinto del momento de asignación al tratamiento.
- **Técnico:** incluir usuarios prevalentes en vez de new users (active comparator new user design lo corrige).
- **De supuestos:** analizar datos observacionales sin escribir antes los 7 componentes del target trial.

## Transferencia isomorfa

- **Immortal time bias ↔ leakage temporal en ML:** contar tiempo que el sujeto debía sobrevivir es "ver el futuro", el mismo pecado que un split de evaluación que no respeta el tiempo (conecta con [[arena-s1]] y [[arena-cds1]]).
- **Prevalent user bias ↔ sesgo de supervivencia / selección:** estudiar a los que ya sobrevivieron sesga hacia los robustos, como condicionar en un collider (conecta con [[arena-h1]]).
- **Definir t=0 ↔ "definir tiempo cero" del arsenal:** alinear el origen del tiempo con la asignación es la heurística que ordena todo análisis longitudinal.
- **Target trial (7 componentes) ↔ plantilla de diseño de sistemas:** especificar elegibilidad, estrategia, outcome y estimando antes de analizar es la misma disciplina que la plantilla de diseño antes de proponer arquitectura (conecta con [[arena-s1]]).

Moraleja de la arista: *quien define mal el tiempo cero regala supervivencia al grupo tratado; alinea t=0 con la asignación, como en ML alineas el split con el tiempo.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "Grupo tratado definido por completar N ciclos" | Busca el período de N ciclos como tiempo inmortal |
| "Seguimiento empieza en diagnóstico, pero el tratamiento inicia después" | t=0 diferente entre grupos → immortal time |
| "Estudio de usuarios de una app en análisis de retención" | ¿Los usuarios que 'usan más' son los que sobrevivieron al período de onboarding? |
| "Empieza el análisis, ¿qué specifica el target trial?" | Lista los 7 componentes antes de escribir código |
| "¿Qué pacientes incluyes?" | New users vs prevalent users: prefiere new user design |

---

## Ejercicio de consolidación

Un análisis evalúa si los pacientes que completan un programa de rehabilitación cardíaca de 12 semanas tienen mejor calidad de vida al año que los que no completan. El seguimiento comienza cuando el paciente es dado de alta tras un infarto.

Identifica:
1. ¿Existe immortal time bias?
2. ¿Cuál es el período inmortal?
3. ¿Cómo rediseñarías el t=0?

*Respuesta: (1) Sí. (2) Las 12 semanas del programa: para estar en el grupo "completó", el paciente debe sobrevivir y permanecer elegible esas 12 semanas. Los que murieron o tuvieron eventos adversos en esas 12 semanas no pueden "completar". (3) Rediseño: t=0 = semana 12 para todos; comparar los que completaron las 12 semanas (tratados) con los que estaban disponibles en la semana 12 pero no completaron. O mejor: emular un trial de asignación al inicio del programa, usando ponderación para la adherencia real.*
