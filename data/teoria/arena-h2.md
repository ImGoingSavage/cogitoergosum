# Target trial emulation e immortal time bias

## El ensayo objetivo: la pregunta que ordena todo

El "target trial" (ensayo objetivo) es el experimento aleatorizado hipotético que un estudio observacional intenta emular. Formularlo explícitamente es el paso que diferencia el análisis causal riguroso del análisis descriptivo.

La pregunta no es "¿qué asociación existe en los datos?" sino "¿qué ensayo clínico randomizado hubiéramos necesario para responder esta pregunta, y cómo lo emulamos con datos observacionales?"

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
