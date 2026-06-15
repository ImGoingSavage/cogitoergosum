# PROMPT para el siguiente agente (pégalo tal cual al iniciar la nueva cuenta)

---

Vas a continuar una **auditoría pedagógica de la Fase 7** (Arena de Entrevistas)
del proyecto CogitoErgoSum. El trabajo y su estado exacto están documentados en
el repo. **Antes de tocar nada, lee, en este orden:**

1. `HANDOFF-AUDITORIA-FASE7.md` (estado exacto, qué falta, cómo hacerlo, reglas).
2. `auditoria.md` (la especificación pedagógica original / contrato de calidad).
3. Como ejemplares del tono y profundidad esperados, lee estas lecciones ya
   enriquecidas: `data/teoria/arena-h17.md`, `data/teoria/arena-cc3.md`,
   `data/teoria/arena-sre4.md`.

**Contexto en una frase:** convertir las lecciones `data/teoria/arena-*.md` de
fichas densas de repaso en material estudiable que fabrique aristas conceptuales
entre dominios, **insertando** (nunca borrando) las secciones del contrato.

**Estado:** 63/118 lecciones hechas. Clusters completos: Health AI/causal
(h3-h22), ML Systems (rom/rml/dmls/htd/sre/mldp/obs/iml ×4), MAANG (cc1-4,
sd1-4, m1-2). **Faltan 55**, listadas en §3 del HANDOFF. El render de
matemáticas (`$…$`, `$$…$$`) y de enlaces `[[...]]` ya está arreglado en
`js/markdown.js` — NO lo rehagas.

**Tu tarea ahora:** continúa la Oleada 2 por **lotes de 5-8 lecciones** siguiendo
el orden sugerido en §6 del HANDOFF (empieza por el cluster **Quant/estadística**:
`arena-q2`, luego `arena-b1..b4`, etc.). Para cada lección, inserta justo antes
del closer `## Disparadores` las secciones de la **plantilla del §4 del HANDOFF**:
*Mini-ejemplo trabajado (con números + predicción socrática), Prototipo/
Contraejemplo/Caso-borde, Errores típicos, Transferencia isomorfa (obligatoria,
con aristas `[[arena-xxx]]` a otros clusters), y una Moraleja de la arista.*

**Reglas innegociables** (detalle en §4 del HANDOFF):
- Solo inserciones: el `git diff` de cada `.md` debe ser `+N, -0`. Conserva
  intactos los closers Disparadores/Síntesis/Retrieval.
- Anti-relleno: cada párrafo fabrica una arista. Intuición/ejemplo antes que
  fórmula. Números simples.
- Puedes citar libremente los libros de `Arena/` y `Biblioteca/` (comprados, sin
  problema de copyright).
- Nada de información clínica/diagnóstica en el contenido.

**Workflow por lote (detalle en §5 del HANDOFF):**
1. Lee los archivos del lote con la tool Read (un `cat` por Bash no habilita
   editar).
2. Enriquece con la plantilla.
3. Valida: `node scripts/smoke-teoria.mjs` → debe dar `threw=0
   rawDisplayMath=0` (rawLinks>0 es normal: literales de matriz).
4. Comprueba inserciones: `git diff --stat <archivos> | tail -1` → `+N, -0`.
5. Sube `const VERSION` en `sw.js` (incrementa `cogitoergosum-vNN`; iba en v63)
   y `node --check sw.js`.
6. Commit + push directo a `main` (mensaje en español, estilo del repo, con
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`).
7. Actualiza §3 del `HANDOFF-AUDITORIA-FASE7.md` marcando el lote como hecho y
   commitéalo.

Trabaja con criterio de arquitecto-integrador, prioriza calidad sobre cantidad,
valida y pushea cada lote antes de seguir, y mantén vivo el registro del HANDOFF.
Empieza ahora leyendo el HANDOFF y, cuando lo tengas claro, arranca con el primer
lote de Quant.
