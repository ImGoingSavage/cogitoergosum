# Cómo fallan los sistemas: permisos, memoria, redes y la web

> Recurso troncal: **UC Berkeley CS 161 — *Computer Security***. Da los fundamentos técnicos para entender por qué fallan sistemas reales. Conecta con [[cyber-ms2]] (diseño defensivo) y prepara [[cyber-sys2]] (criptografía) y [[cyber-web-api]].

## De qué trata (y qué sabrás hacer al final)

Un científico de datos vive sobre capas que rara vez mira: el sistema operativo que aísla procesos, la red que mueve los datos, el navegador que renderiza el dashboard. Cuando algo se rompe, casi siempre es porque **una frontera de confianza fue cruzada**: datos no confiables se trataron como confiables. Esta lección te da el mapa de esas fronteras.

La intuición: piensa en un edificio de oficinas. Hay **puertas con llave** (permisos), **paredes** entre oficinas (aislamiento de procesos/memoria), **mensajería** entre pisos (la red), y una **recepción** que decide quién entra (autenticación). Los robos ocurren en las costuras: una puerta mal cerrada, un mensajero suplantado, una pared con un hueco.

Al terminar podrás: (1) explicar el **modelo de amenaza técnico** (qué controla el atacante); (2) entender **permisos, aislamiento y el peligro de la memoria**; (3) leer una **traza HTTP** básica; y (4) reconocer dónde una frontera de confianza puede romperse.

## El modelo de amenaza técnico

Antes de defender, define **qué puede hacer el atacante**: ¿puede leer la red? ¿ejecutar código en la máquina? ¿solo enviar peticiones a tu API? Sin eso, "es seguro" no significa nada. Un cifrado que resiste a quien espía la red (atacante *de red*) puede ser irrelevante si el atacante ya **ejecuta código** en el servidor (atacante *local*). El mismo sistema es seguro contra un modelo e inseguro contra otro.

## Permisos, aislamiento y memoria

- **Permisos:** el SO decide qué puede leer/escribir/ejecutar cada usuario y proceso. Un proceso que corre como *root* (todo permitido) convierte cualquier bug en catástrofe → aquí reaparece **least privilege**.
- **Aislamiento:** cada proceso cree tener su propia memoria; el SO los separa. Cuando ese aislamiento se rompe, un proceso lee o altera a otro.
- **Memoria insegura:** en lenguajes como C, escribir más allá de un buffer (*buffer overflow*) puede sobreescribir datos o control del programa y permitir ejecutar código del atacante. Python te protege de mucho de esto, pero tus dependencias nativas (NumPy, drivers, librerías C) **no siempre**.

La moraleja transversal: **toda entrada es potencialmente hostil hasta que se valida**, sea un argumento de función, un archivo subido o un paquete de red.

## Redes, DNS y HTTP

Los datos viajan en **paquetes** por capas. Tres piezas que un DS debe reconocer:

- **DNS** traduce `api.midominio.com` a una dirección IP. Si alguien lo envenena, te conectas al servidor del atacante creyendo que es el tuyo.
- **HTTP** es el lenguaje de la web: una petición (`GET /datos`, cabeceras, cuerpo) y una respuesta (código `200`/`404`/`500`, cabeceras, cuerpo). Es **texto plano** salvo que lo envuelva TLS (próxima lección).
- **Cookies y tokens** viajan en cabeceras para mantener la sesión; quien los robe **es** tú ante el servidor.

## Mini-ejemplo trabajado: leer una traza HTTP

```
GET /api/v1/pacientes?id=42 HTTP/1.1
Host: datos.hospital.local
Authorization: Bearer eyJhbGciOi...
Cookie: session=9f3a...
```

Léelo como defensor: el cliente pide el paciente 42; se autentica con un **Bearer token** y una **cookie de sesión**. Preguntas inmediatas: ¿esto va por **HTTPS** (si no, el token viaja a la vista de cualquiera en la red)? ¿el servidor verifica que *este* usuario puede ver al paciente 42, o confía en el `id` del cliente (broken access control, ver [[cyber-web-api]])? La traza no es decorativa: cada campo es una frontera de confianza.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| El proceso corre como root/admin "para que jale" | Violación de least privilege; un bug = todo |
| Tráfico en `http://` con datos sensibles | Confidencialidad nula en la red |
| El servidor confía en un `id` o precio que manda el cliente | Frontera de confianza cruzada |
| Dependencia nativa sin actualizar | Posible memoria insegura heredada |

## Errores típicos

- **Creer que el cliente es confiable:** todo lo que llega del navegador o de otra máquina puede ser manipulado.
- **Confundir "interno" con "seguro":** la red interna también tiene atacantes (un equipo comprometido, un insider).
- **Ignorar las dependencias:** tu código Python puede ser seguro y aun así heredar un fallo de memoria de una librería C.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** una entrada no confiable tratada como confiable en una frontera (un parámetro del usuario usado sin validar) abre la falla; validar y aislar contiene el daño.
- **Contraejemplo:** "usamos tokens, estamos seguros" — pero sobre `http://`, el token viaja en claro y se roba. El control correcto contra el modelo equivocado.
- **Caso borde:** un servicio solo accesible desde `localhost` parece a salvo de la red; deja de estarlo si otro proceso del mismo host está comprometido, o si un SSRF (ver [[cyber-web-api]]) lo alcanza desde dentro.

## Transferencia a ciencia de datos e IA

Tus notebooks, tus endpoints de inferencia y tus jobs de entrenamiento son **procesos con permisos** que hablan por **la red** usando **HTTP**. Entender estas fronteras es lo que te deja razonar la seguridad de un servidor de modelos ([[cyber-ml-security]]) o de un asistente RAG que hace llamadas HTTP a herramientas ([[cyber-llm-rag-agents]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** dada la traza HTTP de arriba, lista 3 fronteras de confianza y qué supuesto rompe cada una.
- **Misión externa (lab vivo):** resuelve los primeros niveles de **OverTheWire: Bandit** (https://overthewire.org/wargames/bandit/), que enseñan permisos y manejo seguro de archivos en Linux. **Criterio de cierre:** llegar al nivel 5 entendiendo *por qué* cada paso funciona. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** un párrafo explicando, con tus palabras, qué significa "toda entrada es hostil hasta validarse".

---

> **Síntesis:** los sistemas fallan en las **fronteras de confianza**, cuando datos no confiables se tratan como confiables. Define siempre el **modelo de amenaza** (qué controla el atacante). **Permisos** y **aislamiento** contienen el daño; la **memoria insegura** y las **dependencias nativas** lo propagan; **DNS/HTTP/cookies** mueven y autentican, y cada campo es una frontera que un defensor debe revisar.

---

**Referencias**

- Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security* (CS 161). University of California, Berkeley.
- OverTheWire. (n.d.). *Bandit wargame*. https://overthewire.org/wargames/bandit/

*Retrieval: (1) ¿por qué "es seguro" no significa nada sin modelo de amenaza?; (2) ¿qué contienen permisos y aislamiento?; (3) nombra 3 campos de una petición HTTP y su riesgo; (4) ¿qué frontera de confianza rompe confiar en un `id` del cliente?*
