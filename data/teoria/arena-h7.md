# Análisis de supervivencia I: fundamentos, Kaplan-Meier y log-rank

> La **mecánica** biostadística del tiempo-hasta-evento. Complementa [[arena-h6]] (supervivencia *causal* / g-métodos).

## Datos de tiempo-hasta-evento

El outcome es el **tiempo** desde un origen bien definido (t=0) hasta un evento. Dos rasgos: tiempos **sesgados** (positivos, no normales) y **censura**. Por individuo: **tiempo de seguimiento** + **indicador** (evento=1 / censura=0) + covariables.

## Las dos funciones

- **Supervivencia** S(t)=P(T>t): probabilidad de no tener el evento más allá de t; cae de 1 a 0.
- **Hazard** h(t): tasa **instantánea** de fallo dado que se sobrevivió hasta t (una tasa, puede ser >1).
- Relaciones: h(t)=f(t)/S(t)=−d/dt ln S(t); hazard acumulado H(t)=∫h; **S(t)=exp(−H(t))**. Ver [[funcion-supervivencia-hazard]].

Hazard **constante** (exponencial), **creciente** (desgaste), **decreciente** (riesgo postoperatorio que baja).

## Censura

No se observa el tiempo exacto: **derecha** (la común: fin de estudio, pérdida, retiro), **izquierda**, **intervalo**. Los censurados aportan "sobrevivió ≥ su tiempo". Supuesto crítico: **censura no informativa** (independiente del pronóstico); si es informativa (los graves abandonan), sesga. Ver [[manejar-censura-supervivencia]].

## Kaplan-Meier

Estimador **product-limit** no paramétrico: **Ŝ(t)=∏(n_j−d_j)/n_j** sobre los tiempos de evento ≤ t (n_j = en riesgo justo antes, d_j = eventos). Curva **escalonada**: baja solo en **eventos**; la censura achica el **risk set** y agranda los saltos posteriores. **Mediana** = t donde Ŝ(t)=0.5 (la media no se reporta si la cola está censurada). Ver [[estimador-kaplan-meier]].

## Log-rank

Compara curvas de ≥2 grupos. H0: curvas **iguales**. Suma de **observado − esperado** por tiempo de evento → chi² (gl = grupos−1). Da igual peso a todos los tiempos → óptimo bajo **PH** y sensible a diferencias tardías. Variantes que pesan lo temprano: **Wilcoxon** (Breslow), Tarone-Ware, Peto. Es un test, no una magnitud (para eso, el HR del Cox). Ver [[prueba-log-rank]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Outcome = tiempo + algunos sin evento | Métodos de supervivencia (no logística/lineal) |
| Estimar/graficar S(t) sin modelar | Kaplan-Meier |
| ¿Difieren dos curvas? | Log-rank (Wilcoxon si la diferencia es temprana) |
| Abandono según gravedad | Censura informativa → sesgo |
| La cola está censurada | Reporta la mediana, no la media |

---

> **Síntesis:** los datos de supervivencia combinan **tiempo + censura**. **S(t)** (lo que queda) y **h(t)** (riesgo momentáneo) se determinan mutuamente vía S=exp(−∫h). **Kaplan-Meier** estima S(t) no paramétricamente (escalones en eventos), y el **log-rank** compara curvas (H0: iguales; óptimo bajo PH). Todo asume **censura no informativa**.

---

*Retrieval: (1) relación entre S(t), h(t) y H(t); (2) ¿cómo afecta la censura a la curva KM?; (3) H0 del log-rank y cuándo usar Wilcoxon; (4) ¿qué supuesto sobre la censura es crítico?*
