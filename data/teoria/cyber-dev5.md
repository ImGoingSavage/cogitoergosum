# CI/CD seguro, contenedores y respuesta a vulnerabilidades

> Recurso troncal: **OpenSSF / Wheeler, *Secure Software Development Fundamentals***. Capstone del cluster: del código verificado al despliegue seguro y a qué hacer cuando aparece un fallo. Integra [[cyber-dev1]]–[[cyber-dev4]] y prepara el mini-proyecto.

## De qué trata (y qué sabrás hacer al final)

El software no es seguro hasta que **se despliega** seguro y se **mantiene** seguro. El pipeline que construye y libera tu código (CI/CD) es un activo crítico —tiene secretos y acceso a producción—, y las vulnerabilidades aparecerán **después** de liberar, así que necesitas un proceso para divulgarlas y parchearlas rápido. Esta lección cierra el ciclo de vida del desarrollo seguro.

La intuición: construiste y revisaste un buen producto; ahora la fábrica que lo empaqueta y envía (CI/CD) también puede ser saboteada, y tras la venta aparecerán defectos que hay que poder **retirar y reparar** rápido. Seguridad no termina en "compila"; termina (y reempieza) en "se desplegó y se mantiene".

Al terminar podrás: (1) asegurar un **pipeline CI/CD** con permisos mínimos e integridad; (2) endurecer **contenedores** en el despliegue ([[cyber-sys4]]); (3) diseñar **divulgación de vulnerabilidades y parcheo rápido**; y (4) ejecutar el mini-proyecto del pipeline ML seguro.

## El CI/CD como activo crítico

El pipeline tiene las llaves del reino: credenciales de despliegue, secretos, acceso a producción. Comprometerlo es comprometer **todo** lo que despliega (ataques de supply chain famosos atacaron justo aquí). Principios:

- **Permisos mínimos:** tokens de alcance estrecho por job, no credenciales de admin "por comodidad" ([[cyber-ms2]]).
- **Integridad de lo que entra:** fijar versiones (pinning) y verificar hashes/firmas de dependencias y artefactos ([[cyber-sys2]], [[cyber-dev2]]).
- **Aislar la ejecución:** builds en entornos efímeros; no ejecutar scripts arbitrarios con permisos amplios.
- **Secretos en el store del CI**, nunca en el archivo de configuración del pipeline ni en logs ([[cyber-dev1]]).
- **Procedencia del artefacto:** poder demostrar que lo que se despliega salió de tu pipeline y no fue alterado.

## Contenedores en despliegue (repaso aplicado)

De [[cyber-sys4]]: contenedores **no-root**, sin `--privileged`, **sin secretos en la imagen** (quedan en las capas), imágenes base actualizadas (heredan CVEs, [[cyber-dev2]]) y montando solo lo necesario. El contenedor empaqueta y reproduce, pero comparte el kernel: su config decide si aísla o solo aparenta.

## Divulgación y parcheo rápido

Las vulnerabilidades aparecerán tras liberar; lo que distingue a un equipo maduro es el **proceso**:

- **Recibir reportes:** una vía clara para que alguien (interno o externo) reporte un fallo (política de divulgación / `security.txt`), sin castigar al mensajero.
- **Priorizar:** por explotabilidad e impacto ([[cyber-dev2]]), no por orden de llegada.
- **Parchear rápido lo crítico:** y poder **desplegar** el parche con confianza (gracias al CI/CD seguro).
- **Comunicar:** avisar a quien usa lo afectado.

Sin proceso de respuesta, un fallo conocido sigue explotable durante meses; con él, se cierra en horas o días.

## Mini-ejemplo trabajado

Tu equipo despliega un modelo con un pipeline que usa una credencial de admin, instala dependencias "a la última", mete la API key en el YAML del pipeline y corre el contenedor como root. Y no hay forma de reportar fallos. Endurecimiento:

- **Permisos:** token de despliegue de alcance mínimo, no admin.
- **Integridad:** fijar versiones con hashes; SCA en el pipeline ([[cyber-dev2]]).
- **Secretos:** mover la key al store del CI; rotarla (estuvo en el YAML → comprometida, [[cyber-dev1]]).
- **Contenedor:** no-root, sin secretos en imagen, base actualizada.
- **Respuesta:** publicar una vía de reporte y un criterio de parcheo por severidad.
- **Resultado:** el pipeline deja de ser el eslabón débil y los fallos futuros tienen camino de reparación.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| El pipeline corre con credenciales de admin | Compromiso del CI = compromiso total |
| Secretos en el YAML del pipeline o en logs | Fuga de credenciales |
| "Instala la última versión" en el build | Build no reproducible ni verificado |
| Contenedor como root / con secretos en la imagen | Aislamiento anulado, secretos recuperables |
| Sin vía para reportar vulnerabilidades | Fallos conocidos sin cerrar |

## Errores típicos

- **Tratar el CI/CD como infraestructura "interna" inofensiva:** es de los blancos de mayor valor.
- **No tener proceso de respuesta:** descubrir el fallo y no saber cómo priorizar ni desplegar el parche.
- **Castigar a quien reporta:** desincentiva la divulgación responsable y empuja los hallazgos al mercado negro.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** endureces el pipeline con token de despliegue mínimo, versiones fijadas por hash, key en el store del CI y contenedor no-root sin secretos en la imagen.
- **Contraejemplo:** pipeline con permisos mínimos, dependencias fijadas y verificadas, secretos en el store, contenedores no-root y una política de divulgación con parcheo por severidad: la supply chain está endurecida de extremo a extremo y los fallos se cierran rápido.
- **Caso borde:** un parche **apresurado** sin verificación ([[cyber-dev4]]) puede introducir un bug nuevo o romper producción; "rápido" no significa "sin pruebas". El equilibrio es un canal de despliegue confiable que permita parchear **rápido y seguro**, no rápido y a ciegas.

## Transferencia a ciencia de datos e IA

Este es literalmente el **mini-proyecto del cluster** y el puente con [[cyber-ml-security]]: un pipeline ML seguro maneja secretos, fija y escanea dependencias (incluidos modelos y datasets, su supply chain), corre en contenedores endurecidos y tiene un criterio de parcheo. La integridad del artefacto es la **provenance** del modelo que despliegas.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** endurece el pipeline del mini-ejemplo punto por punto, justificando cada cambio con un principio.
- **Misión externa (lab vivo):** revisa material de **OpenSSF Training** (https://openssf.org/training/courses/) sobre CI/CD seguro y divulgación de vulnerabilidades. **Criterio de cierre:** describir tu política de respuesta a un CVE crítico.
- **Mini-entregable (mini-proyecto del cluster):** un **plan de pipeline ML seguro**: manejo de secretos, SBOM + SCA, permisos del CI/CD, control de las fuentes de datos/modelos, contenedores endurecidos y criterio de actualización ante dependencias vulnerables. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** el software no es seguro hasta que se **despliega** y se **mantiene** seguro. El **CI/CD** es un activo crítico: permisos mínimos, integridad de dependencias/artefactos (pinning + verificación), ejecución aislada y secretos en su store. Los **contenedores** se endurecen (no-root, sin secretos en imagen, base actualizada). Y como las vulnerabilidades aparecen tras liberar, hace falta un **proceso de divulgación y parcheo rápido** —pero rápido y **verificado**, no a ciegas—.

---

**Referencias**

- Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure software development fundamentals*. Open Source Security Foundation. https://openssf.org/training/courses/
- Open Source Security Foundation. (n.d.). *OpenSSF training courses*. https://openssf.org/training/courses/

*Retrieval: (1) ¿por qué el CI/CD es un activo crítico y cómo se endurece?; (2) ¿qué config endurece un contenedor en despliegue?; (3) ¿qué elementos tiene un proceso de divulgación y parcheo?; (4) ¿por qué 'parchear rápido' no es 'parchear sin verificar'?*
