# Interpretabilidad I: conceptos, taxonomía y buenas explicaciones

## ¿Qué es la interpretabilidad y por qué importa?

**Interpretabilidad** = el grado en que un humano puede **entender la causa de una decisión** (o predecir de forma consistente el resultado del modelo). Cuanto más alta, más fácil es comprender por qué el modelo decidió algo. Sirve para satisfacer la **curiosidad y el aprendizaje**, dar **seguridad** (depurar, auditar), detectar **sesgo/injusticia**, generar **confianza**, cumplir requisitos legales (**derecho a explicación**) y permitir **acción** (recurso).

**No siempre hace falta:** cuando el problema está bien estudiado y de bajo impacto (no hay consecuencias graves de errores), o cuando exponer el mecanismo permite **gaming** del sistema. El criterio es el **gap de mundo real**: la métrica offline no captura todo lo que importa.

## Taxonomía (los ejes que debes nombrar)

- **Intrínseca vs post-hoc:** un modelo **simple** (árbol corto, lineal) es interpretable por su estructura (intrínseca); o explicas un modelo complejo **después** de entrenarlo (post-hoc, p. ej. permutación, SHAP).
- **Específico del modelo vs agnóstico:** específico usa la estructura interna (pesos lineales). **Agnóstico** trata el modelo como **caja negra** (solo input→output) → flexible, comparable entre modelos. Ventaja clave de lo agnóstico: **flexibilidad de modelo, de explicación y de representación**.
- **Global vs local:** global = cómo se comporta el modelo **en promedio** (qué features importan en general); local = por qué **esta predicción** concreta.
- **Resultado de la explicación:** estadístico de resumen por feature (importancias), visualización (PDP), internos del modelo (pesos), **data points** (contrafactuales, prototipos) o un **modelo sustituto** intrínsecamente interpretable.

## Alcance: del modelo a una instancia

Global holístico (todo el modelo a la vez, casi imposible si hay muchas features) → global modular (parte del modelo, p. ej. un peso) → **local para una predicción** (a menudo la explicación local es más fiel y más simple, porque localmente la superficie puede ser casi lineal) → local para un grupo.

## Qué hace BUENA a una explicación (lección de las ciencias sociales)

- **Contrastiva:** la gente no pregunta "¿por qué?" sino "¿por qué **esto y no aquello**?". Explica frente a un **caso de referencia** (por eso los contrafactuales convencen).
- **Selectiva:** 1-3 causas, no la lista completa (efecto Rashomon: varias explicaciones válidas; elige pocas).
- **Social:** depende de la audiencia y su conocimiento previo.
- **Se enfoca en lo anormal:** causas raras pero presentes pesan más.
- **Veraz (truthful), general y probable:** debe generalizar; pero la verdad por sí sola no basta si no es contrastiva/selectiva.

## Propiedades para evaluar métodos y explicaciones

De los **métodos**: expressive power, translucency (cuánto miran dentro del modelo), portability, complejidad algorítmica. De las **explicaciones**: accuracy, **fidelity** (¿aproxima bien al modelo?), consistency, **stability** (instancias similares → explicaciones similares), comprehensibility, certainty, degree of importance, novelty, representativeness.

**Niveles de evaluación (Doshi-Velez & Kim):** *application-grounded* (experto, tarea real) > *human-grounded* (lego, tarea simplificada) > *functionally-grounded* (proxy formal, sin humanos).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «¿Necesito interpretar este modelo?» | Sí si hay impacto/auditoría/ley/acción; no si es trivial o invita a gaming |
| Quiero comparar explicaciones entre modelos distintos | Usa métodos **agnósticos** (caja negra) |
| «¿Por qué predijo X?» de UNA instancia | Explicación **local** (suele ser más fiel y simple) |
| La explicación no convence a la gente | Hazla **contrastiva** (vs un caso de referencia) y **selectiva** (pocas causas) |
| ¿Es buena esta explicación? | Mide fidelity y stability; evalúa application/human/functionally-grounded |

---

> **Síntesis:** interpretabilidad = entender la causa de una decisión. Clasifícala por **intrínseca/post-hoc**, **específica/agnóstica**, **global/local** y por el **tipo de resultado**. Los métodos **agnósticos** ganan flexibilidad tratando al modelo como caja negra. Una buena explicación es **contrastiva, selectiva y social** (ciencias sociales), no una lista exhaustiva de causas. Evalúa con **fidelity/stability** y en los tres niveles application/human/functionally-grounded.

---

*Retrieval: (1) define interpretabilidad y da 2 razones para necesitarla y 1 para NO; (2) nombra los 4 ejes de la taxonomía; (3) ¿qué tres propiedades hacen humana a una explicación?; (4) ¿qué es fidelity vs stability?*
