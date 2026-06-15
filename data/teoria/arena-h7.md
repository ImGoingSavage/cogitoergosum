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

## Mini-ejemplo trabajado: Kaplan-Meier a mano

Seis pacientes, tiempos en meses (`+` = censurado): **3, 5, 5, 7+, 9, 12+**. Construye Ŝ(t) producto-límite, que solo baja en los **eventos**:

- **t=3:** en riesgo n=6, eventos d=1 → factor (6−1)/6 = 5/6. Ŝ = **0.833**.
- **t=5:** en riesgo n=5, eventos d=2 → (5−2)/5 = 3/5. Ŝ = 0.833·0.6 = **0.500**.
- **t=7:** **censura**, no baja la curva, pero saca a ese paciente del risk set.
- **t=9:** en riesgo n=2 (quedan el de 9 y el de 12+), d=1 → (2−1)/2 = 1/2. Ŝ = 0.500·0.5 = **0.250**.
- **t=12:** censura → la curva se queda en 0.250.

**Mediana** = primer t con Ŝ≤0.5 → **5 meses**. Fíjate cómo el censurado en 7 **no** bajó la curva pero **agrandó el salto** posterior (en t=9 el risk set ya era pequeño, así que un evento pesó ½). Esa es toda la mecánica de KM.

**Predicción antes de seguir:** si el paciente censurado en 7+ hubiera abandonado *porque estaba grave* (censura informativa), ¿sobre o subestima Ŝ? La sobrestima: tratas como "podría sobrevivir" a alguien con peor pronóstico.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** estudio con fin de seguimiento administrativo → censura por "aún no ocurrió", independiente del pronóstico → KM insesgado.
- **Contraejemplo (censura informativa):** los pacientes graves se retiran; analizarlos como censura ordinaria sesga la curva. Parece censura inocente, no lo es.
- **Caso borde (cola censurada):** si el último tiempo es censurado, Ŝ no llega a 0 → la **media** es inestimable; reporta la **mediana**.

## Errores típicos

- **Conceptual:** usar regresión logística/lineal sobre "tuvo el evento sí/no", tirando la información del *tiempo* y de los censurados.
- **Técnico:** confundir hazard (tasa instantánea, puede ser >1) con probabilidad.
- **De interpretación:** leer un log-rank no significativo como "no hay diferencia" cuando faltan eventos (poca potencia), o usarlo cuando las curvas **se cruzan** (no-PH).

## Transferencia isomorfa

La supervivencia es la matemática de *cualquier* "tiempo hasta que pasa algo":

- **Retención/churn en producto ↔ S(t):** la curva de retención de una cohorte ES una curva de supervivencia; los usuarios aún activos al final del periodo son **censura por la derecha** (conecta con [[arena-ads2]]).
- **Hazard ↔ tasa instantánea de baja:** "de los que siguen en el mes t, ¿qué fracción se va?" es exactamente h(t).
- **Risk set que se encoge ↔ denominador decreciente:** cada cancelación reduce el "en riesgo", igual que d_j/n_j en KM — por eso las tasas tardías son ruidosas con pocos usuarios.

Moraleja de la arista: *tiempo-hasta-evento + censura = supervivencia; la retención de usuarios y la vida de un componente son el mismo objeto con otra etiqueta.*

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
