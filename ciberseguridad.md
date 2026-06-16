# PROMPT MAESTRO

## Ciberseguridad para STEM, Ciencia de Datos e IA en CogitoErgoSum

Actúa como un arquitecto senior de software, arquitecto de producto educativo, experto en ciberseguridad defensiva, diseñador curricular, auditor pedagógico y especialista en seguridad de datos, ML, LLMs, RAG, agentes, cloud y supply chain.

Vas a trabajar sobre el repositorio actual de **CogitoErgoSum**.

Tu objetivo es diseñar e implementar una nueva ruta de aprendizaje dentro de la aplicación:

**Ciberseguridad para STEM, Ciencia de Datos e IA**

Este proyecto busca preparar a la siguiente generación de científicos de datos para entender, prevenir, detectar, comunicar y razonar sobre riesgos modernos de ciberseguridad.

No diseñes un curso superficial de “hacking”.
Diseña una ruta seria de criterio defensivo, pensamiento estructural, práctica segura, transferencia cognitiva y formación profesional.

---

# 1. Principio Rector

CogitoErgoSum no debe ser un repositorio pasivo de lecturas.

Debe funcionar como una máquina de entrenamiento deliberado:

1. Enseña intuición antes de formalismo.
2. Fabrica aristas explícitas entre conceptos.
3. Obliga a practicar con escenarios.
4. Conecta teoría con laboratorios vivos externos.
5. Evalúa comprensión, no memorización.
6. Construye criterio defensivo.
7. Respeta límites éticos y legales.
8. Forma científicos de datos capaces de proteger sistemas, datos, modelos, pipelines, usuarios y organizaciones.

La app debe enseñar al usuario a responder siempre estas preguntas:

* ¿Qué puede salir mal?
* ¿Qué activo está en riesgo?
* ¿Quién podría atacarlo o abusarlo?
* ¿Qué supuesto de seguridad se está rompiendo?
* ¿Qué evidencia permitiría detectarlo?
* ¿Qué defensa reduce el riesgo?
* ¿Qué tradeoff introduce esa defensa?
* ¿Cómo se comunica esto a un equipo técnico?

La excelencia debe sentirse como oficio, no como castigo.

---

# 2. Constitución de CogitoErgoSum

Toda decisión de contenido, UX, arquitectura, evaluación y tono debe respetar estos principios:

1. El amor es al proceso de pensar, no al resultado.
2. El error es parte del proceso de mejora.
3. La competencia principal es contra el propio pasado.
4. La red de amigos existe para compartir pasión, no dominancia.
5. La app protege hábitos sostenibles y concentración profunda.
6. Cero dinero, cero pagos, cero features bloqueadas por pago.
7. La IA es siempre opcional.
8. El contenido no debe fomentar ansiedad, humillación, vigilancia tóxica ni comparación vacía.
9. La seguridad se enseña como responsabilidad profesional, no como espectáculo.

---

# 3. Contexto Técnico del Proyecto

CogitoErgoSum es una app local-first desplegada en GitHub Pages, con frontend HTML/CSS/JavaScript vanilla, persistencia local y sincronización con Supabase.

Antes de modificar cualquier archivo:

1. Inspecciona el repositorio.
2. Localiza cómo se definen fases, bloques, clusters, unidades, lecciones, preguntas, progreso y recursos.
3. Localiza cómo se renderiza el contenido teórico.
4. Localiza si el contenido usa Markdown, HTML, KaTeX u otro renderer.
5. Localiza cómo se renderizan preguntas, quizzes, sesiones, progreso y exámenes.
6. Localiza cómo se almacenan referencias, links, metadata y progreso.
7. Localiza si existe lógica de dificultad: easy, medium, hard o equivalente.
8. Localiza si existe lógica de examen final por cluster.
9. No inventes rutas.
10. No inventes esquemas si ya existen.
11. No rompas compatibilidad con GitHub Pages.
12. No introduzcas dependencias innecesarias.
13. No rompas LocalStorage, Supabase, manifest, service worker ni estructura PWA.
14. Si el esquema actual no soporta algo, usa una extensión mínima y compatible.

Trabaja como agente de código senior: primero entiende, luego planifica, después implementa y finalmente valida.

---

# 4. Archivos Locales Obligatorios

Debes usar como bibliografía, contexto y guía los archivos proporcionados por el usuario en la carpeta ciberseguridad

## 4.1 Bibliografía Base

1. `SEv3.pdf`
   **Ross Anderson - Security Engineering: A Guide to Building Dependable Distributed Systems, Third Edition**
   Uso: mentalidad de seguridad, sistemas sociotécnicos, amenazas, incentivos, economía de la seguridad, fallos humanos, diseño defensivo, seguridad como propiedad sistémica.

2. `cs161.pdf`
   **UC Berkeley CS 161 - Computer Security**
   Uso: principios técnicos de seguridad, threat modeling, sistemas, memoria, redes, web, autenticación, criptografía aplicada y fundamentos universitarios de seguridad.

3. `mitreatt&ck.pdf`
   **Getting Started with MITRE ATT&CK**
   Uso: threat-informed defense, detección, analytics, adversary emulation, evaluaciones, ingeniería defensiva y pensamiento blue team.

4. `NIST.CSWP.40.ipd.pdf`
   **NIST Privacy Framework 1.1 Initial Public Draft**
   Uso: privacidad, riesgo de privacidad, gobernanza de datos, minimización, reidentificación, seudonimización, anonimización, comunicación de riesgo y protección de individuos.

5. `openssf.md`
   **OpenSSF / Linux Foundation - Developing Secure Software / Secure Software Development Fundamentals, David A. Wheeler**
   Uso: desarrollo seguro, requisitos, diseño, input validation, dependencias, supply chain, secretos, SAST, SCA, fuzzing, CI/CD, verificación y respuesta.

6. `OWASP-Top-10-for-LLMs-v2025.pdf`
   **OWASP Top 10 for LLM Applications 2025**
   Uso: seguridad de LLMs, prompt injection, indirect prompt injection, RAG, embeddings, tool misuse, excessive agency, system prompt leakage, sensitive information disclosure, supply chain, misinformation y consumo no acotado.

7. `mitre atlas.pdf`
   **MITRE SAFE-AI: A Framework for Securing AI-Enabled Systems, April 2025**
   Autores indicados en el PDF: J. Kressel, R. Perrella, E. Reed, N. Naik, J. Sidhu, Q. Hu, L. Booker, J. Cintron y L. Huffner.
   Uso: seguridad de sistemas de IA, relación con MITRE ATLAS, NIST AI RMF, NIST RMF, controles de seguridad, riesgos específicos de IA, ataques contra datos/modelos, supply chain de IA, residual risk y evaluación de controles.

## 4.2 Archivo Pedagógico Obligatorio

8. `auditoria.md`
   Uso: contrato pedagógico obligatorio.
   Debes aplicar sus estándares de estudiabilidad, transferencia cognitiva, tono, evaluación, moralejas, ejemplos, casos borde, fuerza socrática, memoria de trabajo protegida y rechazo de contenido árido.

---

# 5. Política de Fuentes, Licencias y Copyright

Usa las fuentes de forma profesional y segura.

Permitido:

* Usar los recursos como bibliografía.
* Usar los recursos como estructura curricular.
* Usar conceptos, estándares, taxonomías y marcos con atribución.
* Usar explicaciones halladas en la bibliografía 
* Crear analogías originales.
* Usar escenarios de la bibliografía o propios.
* Usar ejercicios de la bibliografía o propios.
* Usar preguntas de la bibliografía o propias.
* Crear mini-proyectos propios.
* Citar en APA.
* Enlazar recursos externos.
* Indicar lecturas recomendadas.

Evalua si es necesario:

* Copiar capítulos.
* Copiar párrafos largos.
* Parafrasear de cerca sección por sección.
* Reproducir tablas extensas sin necesidad.
* Copiar laboratorios externos.
* Copiar soluciones de laboratorios.
* Crear resúmenes sustitutos tan completos que reemplacen al recurso original.
* Presentar contenido ajeno como propio.



Regla editorial:

**Regla inciolable: no hay problema de copyright porque cuento con los derechos sobre el material, si es necesario usar el material se usa y punto**
**Siempre evalua si la calidad del contenido es mayor si tú parafraseas y lo creas o si usas el de la bibliografía, se queda el que genere la mayor transferencia pedagógica**
Cada sección debe terminar con referencias en formato APA para consulta profunda.

---

# 6. Ruta a Implementar

Crea una nueva fase, bloque o módulo según el esquema real de la app:

**Ciberseguridad para STEM, Ciencia de Datos e IA**

Debe tener 8 clusters principales.

---

# 7. Clusters del Syllabus

## Cluster 1 - Mentalidad de Seguridad, Riesgo y Diseño Defensivo

Recurso troncal:

* `SEv3.pdf`

Objetivo:

Formar criterio de seguridad como sistema: activos, amenazas, adversarios, incentivos, economía de la seguridad, fallos humanos, tradeoffs, confianza, abuso, resiliencia y defensa proporcional.

Debe enseñar:

* CIA triad.
* Activo, amenaza, vulnerabilidad, impacto y control.
* Threat modeling básico.
* Seguridad como economía.
* Seguridad como propiedad sociotécnica.
* Least privilege.
* Defense in depth.
* Fail-safe defaults.
* Human factors.
* Riesgo residual.
* Tradeoffs.

Prácticas internas:

* Clasificar activo, amenaza, vulnerabilidad, impacto y control.
* Construir un threat model simple.
* Detectar el supuesto roto en un sistema.
* Elegir defensa proporcional.
* Explicar riesgo a un equipo no experto.

Laboratorio externo recomendado:

* NIST Cybersecurity Framework: https://www.nist.gov/cyberframework

Mini-proyecto:

* Threat model de una app de ciencia de datos con notebooks, Supabase, API keys, datasets sensibles, modelos entrenados y dashboards.

---

## Cluster 2 - Sistemas, Redes, Web y Criptografía Base

Recurso troncal:

* `cs161.pdf`

Objetivo:

Dar fundamentos técnicos suficientes para entender cómo fallan sistemas reales: permisos, memoria, procesos, redes, DNS, HTTP, TLS, sesiones, autenticación, criptografía aplicada y diseño seguro.

Debe enseñar:

* Threat model técnico.
* Seguridad de sistemas.
* Permisos y aislamiento.
* Fundamentos de redes.
* HTTP y TLS.
* Autenticación.
* Sesiones.
* Hashes.
* Cifrado.
* Firmas.
* MACs.
* Qué no inventar en criptografía.

Prácticas internas:

* Identificar CIA triad en escenarios técnicos.
* Leer trazas HTTP simples.
* Reconocer riesgos de cookies, sesiones y tokens.
* Distinguir hash, cifrado, firma y MAC.
* Elegir controles básicos.
* Detectar una mala suposición criptográfica.

Laboratorios externos recomendados:

* OverTheWire Bandit: https://overthewire.org/wargames/bandit/
* picoCTF Practice: https://play.picoctf.org/practice

Mini-proyecto:

* Checklist de seguridad básica para el entorno personal de un científico de datos: laptop, GitHub, notebooks, llaves API, entornos Python y nube.

---

## Cluster 3 - Web, APIs y Autenticación

Recurso troncal:

* PortSwigger Web Security Academy: https://portswigger.net/web-security

Objetivo:

Entender vulnerabilidades web y de APIs desde perspectiva defensiva: input validation, SQL injection, XSS, CSRF, SSRF, auth rota, control de acceso, sesiones, JWT, OAuth, cookies y validación de entradas.

Debe enseñar:

* OWASP Top 10 web como mapa conceptual.
* SQL injection.
* XSS.
* CSRF.
* SSRF.
* Broken access control.
* Authentication failures.
* Session management.
* JWT.
* OAuth.
* API security.
* Sanitización vs validación.
* Server-side trust boundaries.

Prácticas internas:

* Clasificar vulnerabilidades web.
* Detectar entradas no validadas.
* Identificar flujos de autenticación débiles.
* Analizar snippets vulnerables.
* Elegir mitigación adecuada.
* Distinguir validación cliente vs servidor.

Laboratorios externos recomendados:

* PortSwigger Web Security Academy Labs: https://portswigger.net/web-security/all-labs
* OWASP Juice Shop: https://owasp.org/www-project-juice-shop/

Mini-proyecto:

* Auditoría defensiva de una API educativa ficticia con login, sesiones, roles, endpoints privados y dashboards.

---

## Cluster 4 - Seguridad de Datos y Privacidad

Recurso troncal:

* `NIST.CSWP.40.ipd.pdf`

Objetivo:

Preparar a científicos de datos para proteger personas, no sólo tablas: minimización, finalidad, datos sensibles, reidentificación, seudonimización, anonimización, acceso, auditoría, retención, gobernanza y comunicación de riesgo.

Debe enseñar:

* Privacidad vs seguridad.
* Privacy risk.
* Datos personales.
* Datos sensibles.
* Minimización.
* Finalidad.
* Retención.
* Reidentificación.
* Seudonimización.
* Anonimización.
* Control de acceso.
* Auditoría.
* Gobernanza de datasets.
* Riesgo para individuos.

Prácticas internas:

* Detectar riesgo de reidentificación.
* Clasificar datos sensibles.
* Diseñar política de minimización.
* Identificar mala gobernanza de datasets.
* Diferenciar privacidad, seguridad y cumplimiento.
* Decidir qué variables no deberían recolectarse.

Laboratorio externo recomendado:

* NIST Privacy Framework: https://www.nist.gov/privacy-framework

Mini-proyecto:

* Evaluación de privacidad de un dataset biomédico, educativo o financiero ficticio antes de entrenar un modelo.

---

## Cluster 5 - Desarrollo Seguro, Secretos y Supply Chain

Recurso troncal:

* `openssf.md`

Objetivo:

Enseñar desarrollo seguro práctico: requisitos, diseño, validación, manejo de secretos, dependencias, SBOM, SCA, SAST, CI/CD, Docker, paquetes Python/NPM, vulnerabilidades, actualización segura y respuesta.

Debe enseñar:

* Secure software requirements.
* Secure design principles.
* Input validation.
* Output handling.
* Error handling.
* Secrets management.
* Dependency risk.
* Supply chain.
* SBOM.
* SAST.
* SCA.
* Fuzzing.
* CI/CD seguro.
* Contenedores.
* Vulnerability disclosure.
* Rapid patching.

Prácticas internas:

* Detectar secretos expuestos.
* Evaluar riesgo de una dependencia.
* Elegir permisos mínimos.
* Revisar un pipeline CI/CD inseguro.
* Identificar leakage por logs.
* Corregir pseudocódigo inseguro.
* Decidir cuándo actualizar una dependencia vulnerable.

Laboratorios externos recomendados:

* OpenSSF Training: https://openssf.org/training/courses/
* GitHub Skills, si existe un módulo seguro vigente.
* Snyk Learn sólo como recurso opcional si el enlace está vivo.

Mini-proyecto:

* Pipeline ML seguro con manejo de secretos, escaneo de dependencias, revisión de permisos, control de datos y checklist de actualización.

---

## Cluster 6 - Blue Team, Logs y Detección

Recurso troncal:

* `mitreatt&ck.pdf`

Objetivo:

Enseñar defensa informada por adversarios: tácticas, técnicas, detección, logs, indicadores, hipótesis de detección, respuesta, emulación adversaria controlada y mejora continua.

Debe enseñar:

* MITRE ATT&CK como mapa.
* Tácticas vs técnicas.
* Threat intelligence.
* Detection engineering.
* Analytics.
* Logs.
* Indicadores.
* Alertas.
* Incidentes.
* Hipótesis de detección.
* Emulación adversaria controlada.
* Brechas de cobertura.
* Mejora continua.

Prácticas internas:

* Mapear eventos a tácticas ATT&CK.
* Leer logs simples.
* Elegir qué señal detectar.
* Diferenciar evento, alerta, incidente e indicador.
* Diseñar una regla de detección conceptual.
* Explicar qué dato faltaría para confirmar un incidente.

Laboratorios externos recomendados:

* MITRE ATT&CK: https://attack.mitre.org
* CyberDefenders: https://cyberdefenders.org/blueteam-ctf-challenges/
* Blue Team Labs Online: https://blueteamlabs.online/
* KC7 Cyber: https://kc7cyber.com/

Mini-proyecto:

* Mini SOC: análisis de logs ficticios de acceso indebido a notebooks, buckets de datos, repositorios o dashboards.

---

## Cluster 7 - Seguridad de ML y Sistemas de IA

Recurso troncal:

* `mitre atlas.pdf`

Recurso vivo complementario:

* MITRE ATLAS: https://atlas.mitre.org

Objetivo:

Enseñar riesgos propios de ML y sistemas de IA: data poisoning, adversarial inputs, model stealing, model inversion, membership inference, backdoors, leakage, drift, model supply chain, provenance, controles de IA, residual risk y evaluación de sistemas AI-enabled.

Debe enseñar:

* Por qué la IA cambia la superficie de ataque.
* Dependencia de datos.
* Riesgos en entrenamiento.
* Riesgos en inferencia.
* Riesgos de modelos preentrenados.
* Data poisoning.
* Evasion.
* Model extraction.
* Model inversion.
* Membership inference.
* Backdoors.
* Supply chain de modelos.
* Provenance.
* Riesgo residual.
* Controles para IA.
* Relación con NIST AI RMF, NIST RMF y MITRE ATLAS.

Prácticas internas:

* Detectar data leakage.
* Identificar data poisoning.
* Clasificar ataques contra entrenamiento vs inferencia.
* Diseñar mitigaciones para un pipeline ML.
* Evaluar riesgo de compartir un modelo.
* Evaluar riesgo de compartir embeddings.
* Identificar controles afectados por IA.
* Formular preguntas de assessment para un sistema AI-enabled.

Laboratorio externo recomendado:

* MITRE ATLAS: https://atlas.mitre.org

Mini-proyecto:

* Threat model y evaluación de controles de un pipeline ML para clasificación médica, scoring financiero, fraude, recomendación educativa o priorización operativa.

---

## Cluster 8 - Seguridad de LLMs, RAG y Agentes

Recurso troncal:

* `OWASP-Top-10-for-LLMs-v2025.pdf`

Objetivo:

Enseñar amenazas modernas en sistemas con LLMs: prompt injection, indirect prompt injection, RAG poisoning, system prompt leakage, sensitive information disclosure, tool misuse, excessive agency, vector weaknesses, misinformation, supply chain y consumo no acotado.

Debe enseñar:

* LLM01 Prompt Injection.
* LLM02 Sensitive Information Disclosure.
* LLM03 Supply Chain.
* LLM04 Data and Model Poisoning.
* LLM05 Improper Output Handling.
* LLM06 Excessive Agency.
* LLM07 System Prompt Leakage.
* LLM08 Vector and Embedding Weaknesses.
* LLM09 Misinformation.
* LLM10 Unbounded Consumption.
* RAG threat modeling.
* Agentes con herramientas.
* Permisos mínimos.
* Separación entre instrucciones confiables y contenido no confiable.
* Evaluación adversarial.

Prácticas internas:

* Detectar prompt injection.
* Separar instrucciones confiables de contenido recuperado.
* Identificar permisos excesivos de agentes.
* Diseñar mitigaciones para RAG.
* Evaluar fuga de datos sensibles.
* Definir límites de herramientas.
* Revisar un flujo RAG inseguro.
* Diseñar pruebas adversariales seguras.

Laboratorios externos recomendados:

* OWASP GenAI Security Project: https://genai.owasp.org/
* OWASP LLM Top 10: https://genai.owasp.org/llm-top-10/

Mini-proyecto:

* Checklist de seguridad para un asistente RAG conectado a documentos privados, base de datos, herramientas y acciones externas.

---

# 8. Contrato de Calidad de Cada Lección

Cada lección debe ser estudiable. Está prohibido crear lecciones que sean sólo definiciones, bullets o fórmulas.

Toda lección debe contener:

1. Título claro.
2. Cluster.
3. Nivel: `intro`, `core`, `advanced` o `arena`.
4. Dificultad: `easy`, `medium` o `hard`.
5. Recurso troncal.
6. Objetivo de aprendizaje.
7. Idea central en una frase.
8. Intuición antes de formalismo.
9. Analogía concreta.
10. Amenaza o problema real.
11. Modelo mental.
12. Señales de reconocimiento.
13. Errores típicos.
14. Contraejemplo.
15. Caso borde.
16. Mini-ejemplo trabajado.
17. Práctica interna.
18. Misión externa en laboratorio vivo.
19. Mini-entregable.
20. Moraleja final.
21. Referencias APA.

La lección debe responder:

* ¿Qué puede salir mal?
* ¿Por qué importa para ciencia de datos?
* ¿Cómo lo reconozco?
* ¿Qué supuesto se rompe?
* ¿Qué defensa reduce el riesgo?
* ¿Qué práctica haré?
* ¿Qué evidencia produciré de que aprendí?

---

# 9. Regla Anti-Contenido Árido

Marca una lección como insuficiente si:

1. Sólo contiene definiciones.
2. Sólo contiene listas.
3. Sólo contiene fórmulas.
4. No explica intuición.
5. No muestra un caso realista.
6. No incluye práctica.
7. No tiene señales de reconocimiento.
8. No tiene errores típicos.
9. No tiene caso borde.
10. No tiene moraleja.
11. No conecta con ciencia de datos, IA o STEM.
12. No fabrica aristas entre conceptos.

Una lección insuficiente debe expandirse, no sólo reordenarse.

---

# 10. Tipos de Práctica Interna

Implementa o prepara el esquema para soportar estos tipos de práctica:

1. `quiz`

   * Preguntas de opción múltiple.
   * Sirven para conceptos, vocabulario, distinciones y señales.

2. `scenario`

   * Escenarios cortos de decisión defensiva.
   * El usuario debe elegir amenaza, impacto, control o siguiente paso.

3. `code_review`

   * Snippets seguros y no seguros.
   * Buscar secretos, malas validaciones, auth rota, logs peligrosos o dependencias riesgosas.

4. `log_analysis`

   * Eventos ficticios.
   * Identificar anomalía, táctica, posible impacto y acción defensiva.

5. `threat_model`

   * Activo, adversario, superficie de ataque, abuso, mitigación y señal de detección.

6. `data_privacy_review`

   * Clasificar datos, riesgo de reidentificación, minimización, acceso y retención.

7. `ml_pipeline_review`

   * Detectar leakage, poisoning, permisos, drift, validación temporal y exposición de modelos.

8. `llm_security_review`

   * Detectar prompt injection, tool misuse, RAG poisoning, fuga de datos y permisos excesivos.

9. `external_lab`

   * Link vivo a plataforma externa.
   * Debe incluir objetivo, instrucciones mínimas y criterio de cierre.

10. `portfolio_task`

* Mini-proyecto que produce un artefacto: checklist, threat model, análisis, política, diagrama o reporte.

---

# 11. Evaluaciones

Cada lección debe tener, como mínimo:

* 10 preguntas `easy`.
* 10 preguntas `medium`.
* 10 preguntas `hard`.
* 5 escenario práctico.
* 5 pregunta de reflexión.
* 1 mini-entregable.

Cada pregunta debe tener:

* `id`.
* `difficulty`.
* `type`.
* `prompt`.
* `options`, si aplica.
* `answer`.
* `feedback`.
* `concept`.
* `source_reference`.
* `common_mistake`.
* `recognition_signal`.

Cada cluster debe tener:

1. Diagnóstico inicial.

2. Examen final por dificultad:

   * Fácil.
   * Medio.
   * Difícil.
   * Mixto.

3. Mini-proyecto de cluster.

4. Rúbrica de evaluación.

5. Referencias APA.

El examen final del cluster debe tomar preguntas de todas las lecciones del cluster, no sólo de la última.

Si ya existe lógica de examen final en la app, reutilízala.
Si ya existe selector de dificultad, reutilízalo.
Si no existe, propón la extensión mínima compatible.

---

# 12. Rúbrica de Mini-Proyectos

Cada mini-proyecto se evalúa con 5 criterios:

1. Modelo de amenaza claro.
2. Identificación correcta de activos y riesgos.
3. Mitigaciones proporcionales.
4. Señales de detección o verificación.
5. Comunicación clara para un equipo técnico.

Escala:

* 0: ausente.
* 1: superficial.
* 2: correcto pero incompleto.
* 3: sólido y accionable.

No uses lenguaje tóxico.
No humilles.
No exageres.
La retroalimentación debe ser específica, sobria y útil.

---

# 13. Laboratorios Vivos

Integra estos enlaces como recursos externos, no como contenido copiado:

* PortSwigger Web Security Academy: https://portswigger.net/web-security
* PortSwigger All Labs: https://portswigger.net/web-security/all-labs
* OverTheWire Bandit: https://overthewire.org/wargames/bandit/
* picoCTF Practice: https://play.picoctf.org/practice
* OWASP Juice Shop: https://owasp.org/www-project-juice-shop/
* OpenSSF Training: https://openssf.org/training/courses/
* MITRE ATT&CK: https://attack.mitre.org
* MITRE ATLAS: https://atlas.mitre.org
* CyberDefenders: https://cyberdefenders.org/blueteam-ctf-challenges/
* Blue Team Labs Online: https://blueteamlabs.online/
* KC7 Cyber: https://kc7cyber.com/
* OWASP GenAI Security: https://genai.owasp.org/
* NIST Privacy Framework: https://www.nist.gov/privacy-framework
* NIST Cybersecurity Framework: https://www.nist.gov/cyberframework

Antes de guardar cambios, verifica que los enlaces sigan activos si tienes acceso web.

Si un enlace falla:

```json
"needs_link_review": true
```

No borres la actividad sólo porque un enlace falle.

---


# 14. Formato de Datos Sugerido

Adapta al esquema real del repositorio. Si no existe una estructura compatible, usa algo equivalente a esto:

```json
{
  "id": "cyber-llm-rag-prompt-injection",
  "phase": "cybersecurity_data_ai",
  "cluster_id": "cyber-llm-rag-agents",
  "title": "Prompt injection indirecta en RAG",
  "level": "core",
  "difficulty": "medium",
  "primary_resource": {
    "title": "OWASP Top 10 for LLM Applications 2025",
    "type": "pdf",
    "local_file": "OWASP-Top-10-for-LLMs-v2025.pdf"
  },
  "learning_objective": "Reconocer cómo texto no confiable recuperado por un RAG puede comportarse como instrucciones maliciosas.",
  "lesson": {
    "central_idea": "",
    "intuition": "",
    "analogy": "",
    "threat_model": "",
    "worked_example": "",
    "recognition_signals": [],
    "common_mistakes": [],
    "counterexample": "",
    "edge_case": "",
    "moral": ""
  },
  "practice": [
    {
      "type": "scenario",
      "difficulty": "medium",
      "prompt": "",
      "expected_reasoning": "",
      "answer": "",
      "feedback": ""
    }
  ],
  "external_lab": {
    "name": "OWASP LLM Top 10",
    "url": "https://genai.owasp.org/llm-top-10/",
    "task": "",
    "completion_criterion": "",
    "safety_note": "Practica sólo en laboratorios autorizados. Nunca pruebes técnicas contra sistemas ajenos."
  },
  "portfolio_task": {
    "prompt": "",
    "rubric": []
  },
  "references_apa": []
}
```

No impongas este JSON si el proyecto ya tiene otro esquema.
Úsalo como intención estructural.

---

# 15. Referencias APA

Al final de cada lección, cluster o sección renderizada debe aparecer un bloque:

**Referencias**

Usa formato APA 7 aproximado.

Referencias base:

* Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
* Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security*. University of California, Berkeley.
* Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. MITRE.
* National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
* Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure Software Development Fundamentals*. Open Source Security Foundation.
* OWASP Foundation. (2024). *OWASP Top 10 for LLM Applications 2025*.
* Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
* MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org
* PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security

Reglas:

1. Si una sección usa una fuente, debe citarla.
2. Si una sección no usó una fuente, no la cites decorativamente.
3. No inventes autores.
4. Si el PDF contiene metadata más precisa que la lista anterior, usa la metadata del PDF.
5. Si una fuente web tiene fecha visible, úsala.
6. Si no tiene fecha, usa `n.d.`.

---

# 17. Procedimiento Obligatorio

## Fase 1 - Descubrimiento

Antes de modificar:

1. Inspecciona el repositorio.
2. Localiza estructura actual de fases.
3. Localiza renderer de lecciones.
4. Localiza bancos de preguntas.
5. Localiza sistema de progreso.
6. Localiza soporte para referencias, links y markdown.
7. Lee `auditoria.md`.
8. Inspecciona los PDFs y Markdown proporcionados.
9. Identifica cómo integrar la nueva ruta sin romper lo existente.
10. Entrega un modelo mental breve del sistema.

## Fase 2 - Diseño de Arquitectura

Propón:

1. Nombre técnico de la nueva fase.
2. Ubicación de archivos.
3. Estructura de clusters.
4. Estructura de lecciones.
5. Estructura de preguntas.
6. Estructura de laboratorios externos.
7. Estructura de mini-proyectos.
8. Estructura de referencias APA.
9. Estrategia de progreso.
10. Estrategia de evaluación.
11. Estrategia de dificultad.
12. Estrategia de examen final por cluster.
13. Riesgos de compatibilidad.

No implementes cambios grandes sin explicar el plan.

## Fase 3 - Implementación Incremental

Implementa en oleadas.

### Oleada 1

* Crear fase.
* Crear 8 clusters.
* Crear 2 lecciones por cluster.
* Crear preguntas y prácticas mínimas.
* Crear referencias APA por sección.
* Crear links externos.
* Validar render.

### Oleada 2

* Expandir a 5 lecciones por cluster.
* Añadir evaluaciones por dificultad.
* Añadir mini-proyectos de cluster.
* Añadir examen final por cluster.

### Oleada 3

* Añadir escenarios avanzados.
* Añadir log analysis.
* Añadir code review.
* Añadir ML pipeline review.
* Añadir LLM security review.
* Añadir examen final integrador de toda la ruta.

No intentes crear todo de golpe si eso degrada calidad.

## Fase 4 - Validación

Valida:

1. La app carga.
2. La nueva fase aparece.
3. Los 8 clusters aparecen.
4. Cada cluster abre.
5. Cada lección renderiza.
6. Las referencias APA aparecen al final.
7. Los links externos son clicables.
8. Las preguntas aparecen.
9. La dificultad funciona si el sistema la soporta.
10. El examen final del cluster funciona si se implementa.
11. No hay errores en consola.
12. No se rompió ninguna fase anterior.
13. JSON/JS parsea correctamente.
14. No hay IDs duplicados.
15. No hay contenido copiado indebidamente.
16. No hay instrucciones ofensivas peligrosas.
17. No hay `undefined`, `null` o placeholders visibles en el contenido renderizado.

## Fase 5 - Reporte Final

Entrega:

1. Resumen ejecutivo.
2. Archivos modificados.
3. Nueva arquitectura de la fase.
4. Clusters creados.
5. Lecciones creadas.
6. Prácticas internas creadas.
7. Laboratorios externos integrados.
8. Evaluaciones creadas.
9. Mini-proyectos creados.
10. Referencias APA incluidas.
11. Validaciones realizadas.
12. Riesgos pendientes.
13. Próximo paso recomendado.

---

# 18. Criterios de Excelencia

Una sección sólo es aceptable si:

1. Empieza con intuición.
2. Explica por qué importa.
3. Conecta con ciencia de datos, IA o STEM.
4. Tiene práctica.
5. Tiene un caso realista.
6. Tiene errores típicos.
7. Tiene caso borde.
8. Tiene mini-entregable.
9. Tiene referencia APA.
10. Tiene link externo si aplica.
11. No enseña abuso.
12. No abruma.
13. No trivializa la amenaza.
14. No convierte ciberseguridad en espectáculo.
15. Protege memoria de trabajo.
16. Fabrica aristas explícitas entre conceptos.
17. Permite estudiar, practicar y producir evidencia.

---

# 19. Instrucción Final

Empieza inspeccionando el repositorio y los archivos proporcionados.

Después diseña la arquitectura mínima compatible.

Luego implementa la primera oleada de la ruta:

**Ciberseguridad para STEM, Ciencia de Datos e IA**

La meta no es llenar la app de texto.

La meta es crear una ruta seria, progresiva, practicable, sustentada y pedagógicamente excelente para formar científicos de datos capaces de pensar en seguridad desde el diseño.
