# Anatomía de un ataque de red: DNS, MITM y por qué TLS importa

> Recurso troncal: **UC Berkeley CS 161 — *Computer Security***. Capstone del cluster de sistemas: integra red ([[cyber-sys1]]), cripto/TLS ([[cyber-sys2]]), identidad ([[cyber-sys3]]) y aislamiento ([[cyber-sys4]]) en el modelo de amenaza de red.

## De qué trata (y qué sabrás hacer al final)

Tus datos casi nunca están quietos: viajan entre tu laptop, el repositorio, la nube y los servicios. Cada salto es una oportunidad para un atacante **de red** que observa o manipula el tráfico. Esta lección arma el modelo de amenaza de red de extremo a extremo y muestra por qué TLS no es opcional para datos que importan.

La intuición: enviar datos por la red sin protección es como mandar postales —cualquiera en el camino las lee y podría reescribirlas antes de reenviarlas—. TLS convierte la postal en un sobre lacrado y verificado: nadie en el medio lo lee ni lo altera sin que se note, y sabes que llegó al destinatario correcto.

Al terminar podrás: (1) describir un ataque **man-in-the-middle (MITM)**; (2) entender el **envenenamiento de DNS** y por qué redirige al impostor; (3) explicar cómo **TLS** frustra ambos; y (4) modelar la amenaza de red de un entorno de datos.

## El atacante de red y el MITM

Define el adversario ([[cyber-sys1]]): un atacante **de red** puede estar en el camino del tráfico (un Wi-Fi público, un router comprometido, un proveedor). Sus capacidades:

- **Espiar (pasivo):** leer todo lo que va en claro → rompe **confidencialidad**.
- **Alterar/inyectar (activo):** modificar mensajes o insertarlos → rompe **integridad**.
- **MITM:** colocarse entre cliente y servidor, hablando con ambos como si fuera el otro. Sin protección, captura credenciales, tokens ([[cyber-sys3]]) y datos, y puede manipular respuestas.

## DNS: el directorio que te puede engañar

Antes de conectarte, **DNS** traduce `api.midominio.com` a una IP. Si un atacante **envenena** esa traducción (responde antes/falso), te conectas a **su** servidor creyendo que es el tuyo. Es la puerta de entrada clásica al MITM: no necesita romper tu conexión, solo convencerte de a quién te conectas. Lo mismo logran un Wi-Fi malicioso o un router comprometido.

## Por qué TLS lo frustra

TLS ([[cyber-sys2]]) responde a las tres amenazas a la vez:

- **Confidencialidad (cifrado):** el espía pasivo solo ve ruido.
- **Integridad (MAC):** una alteración activa se detecta y la conexión se corta.
- **Autenticación del servidor (certificado firmado):** aunque el DNS te mande al impostor, su certificado **no** será válido para ese dominio → el cliente lo rechaza. Aquí está la clave: el certificado convierte el envenenamiento de DNS en un error visible, no en una trampa silenciosa.

Por eso los avisos de "certificado inválido" **importan**: a menudo son exactamente la señal de un MITM. Saltárselos anula la protección.

## Mini-ejemplo trabajado

Un analista trabaja desde un café y su script sube un dataset a `http://datos.interno/ingest` (sin TLS) usando una API key en la cabecera. Modelo de amenaza:

- **Atacante de red** en el Wi-Fi del café: ve la **API key** y el **dataset** en claro (confidencialidad rota), y podría alterar el dataset en tránsito (integridad rota) o redirigir vía DNS a su servidor (MITM).
- **Corrección:** usar `https://` (TLS) de extremo a extremo; rechazar conexiones sin certificado válido; rotar la key si pudo viajar en claro alguna vez ([[cyber-secure-dev]]); idealmente, no exponer el endpoint de ingest a redes no confiables (VPN/allow-list).
- **Lección transversal:** "es interno" no protege si el camino pasa por una red hostil ([[cyber-sys1]]).

## Señales de reconocimiento

| Señal | Riesgo de red |
|---|---|
| Datos sensibles o keys sobre `http://` | Espionaje/alteración en tránsito |
| "Ignora el aviso de certificado para que funcione" | Posible MITM enmascarado |
| Trabajo con datos en Wi-Fi público sin VPN | Atacante de red en el camino |
| Confiar en la IP/host sin verificar certificado | Envenenamiento de DNS → impostor |

## Errores típicos

- **Creer que `http` interno es seguro:** la red interna o el tramo público también tienen atacantes.
- **Saltarse avisos de certificado:** es desactivar justo la defensa contra MITM.
- **Proteger el login con TLS pero no el resto:** si el token viaja luego en claro, se roba igual ([[cyber-sys3]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un MITM envenena el DNS para redirigirte a un impostor; TLS (cifrado + MAC + certificado) frustra el espionaje, la alteración y el DNS envenenado.
- **Contraejemplo:** TLS de extremo a extremo con verificación estricta de certificado y keys que nunca viajan en claro: el atacante del café solo ve ruido y el impostor de DNS es rechazado. La postal se volvió sobre lacrado.
- **Caso borde:** TLS protege el **tránsito**, no los **extremos**: si tu laptop o el servidor están comprometidos ([[cyber-sys4]]), el dato se lee antes de cifrarse o después de descifrarse. TLS no sustituye la seguridad de los endpoints.

## Transferencia a ciencia de datos e IA

Todo pipeline de datos (ingesta, descarga de datasets/modelos, llamadas a APIs de inferencia) cruza la red: exige TLS y verificación de integridad de lo que descargas (provenance, [[cyber-ml-security]]). Un agente LLM que hace *fetch* de URLs ([[cyber-llm-rag-agents]]) enfrenta MITM y debe validar destinos y certificados. Este es el modelo de amenaza de red que sostiene al resto.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el mini-ejemplo, lista qué ve y qué puede alterar el atacante de red, y cómo lo frustra cada garantía de TLS.
- **Misión externa (lab vivo):** en **picoCTF Practice** (https://play.picoctf.org/practice), resuelve un reto de la categoría *Networking/Forensics* introductorio (leer tráfico). **Criterio de cierre:** explicar qué información viaja en claro y qué la habría protegido. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable (mini-proyecto del cluster):** un **checklist de seguridad del entorno personal de un científico de datos** (laptop, GitHub, notebooks, llaves API, entornos Python y nube): para cada uno, su amenaza principal, el control (TLS, aislamiento, secretos, MFA) y cómo verificarlo. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** un atacante **de red** puede espiar (rompe C) y alterar/inyectar (rompe I), y con **envenenamiento de DNS** te redirige a un impostor (**MITM**). **TLS** frustra las tres amenazas a la vez —cifrado, MAC y certificado del servidor—, por lo que datos y credenciales nunca deben viajar por `http://` y los avisos de certificado no se ignoran. TLS protege el **tránsito**, no los **extremos**: la seguridad de la red complementa, no sustituye, la de los hosts.

---

**Referencias**

- Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security* (CS 161). University of California, Berkeley.
- picoCTF. (n.d.). *Practice*. https://play.picoctf.org/practice

*Retrieval: (1) ¿qué puede hacer un atacante de red pasivo vs activo?; (2) ¿cómo redirige el envenenamiento de DNS y a qué lleva?; (3) ¿cómo frustra TLS el MITM, incluido el DNS envenenado?; (4) ¿por qué TLS no basta si el endpoint está comprometido?*
