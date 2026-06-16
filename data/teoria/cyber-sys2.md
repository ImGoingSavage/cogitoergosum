# Criptografía aplicada: hash, cifrado, firma, MAC y TLS

> Recurso troncal: **UC Berkeley CS 161 — *Computer Security***. Sigue a [[cyber-sys1]]: ahora que entiendes la red y sus fronteras, aprende las herramientas que protegen C e I sobre ella. **Regla de oro: nunca inventes criptografía.**

## De qué trata (y qué sabrás hacer al final)

La criptografía intimida porque suena a matemáticas pesadas, pero como **usuario defensivo** no necesitas demostrar teoremas: necesitas elegir la herramienta correcta para cada garantía y **no usar la herramienta equivocada**. El error catastrófico casi nunca es "el algoritmo es débil"; es "usé un hash donde necesitaba un MAC" o "inventé mi propio esquema".

La intuición con cuatro objetos cotidianos:
- **Hash** = una huella digital del documento (resumen fijo, irreversible).
- **Cifrado** = una caja fuerte (vuelve el dato ilegible sin la llave).
- **Firma** = una rúbrica verificable (prueba quién lo emitió y que no cambió).
- **MAC** = un sello de "intacto y de quien comparte el secreto".

Al terminar podrás: (1) **distinguir hash, cifrado, firma y MAC** y cuándo usar cada uno; (2) entender qué garantiza **TLS**; (3) reconocer una **mala suposición criptográfica**; y (4) recitar y aplicar la regla de no inventar cripto.

## Los cuatro objetos, sin confundirlos

| Herramienta | Garantiza | Reversible | Necesita | Ejemplo correcto |
|---|---|---|---|---|
| **Hash** (SHA-256) | Integridad / huella | No | nada | Verificar que un archivo no cambió |
| **Cifrado** (AES) | Confidencialidad | Sí, con llave | llave secreta/pública | Guardar datos cifrados en disco |
| **MAC** (HMAC) | Integridad + autenticidad | No | **secreto compartido** | Verificar que un mensaje viene del par confiable |
| **Firma** (RSA/Ed25519) | Integridad + autenticidad + **no repudio** | No | par de llaves pública/privada | Firmar un release de software |

Distinción clave que casi todos fallan: un **hash** detecta cambios *accidentales*, pero **no** maliciosos —el atacante recalcula el hash del dato alterado—. Para detectar alteración *maliciosa* necesitas un **MAC** (con secreto compartido) o una **firma** (con llave privada). Hash ≠ integridad contra un adversario.

Otra: contraseñas **nunca** se cifran (reversible = robable); se guardan como **hash lento y salado** (bcrypt, Argon2). Y para "¿este mensaje vino de mi servidor?" usas MAC/firma, no cifrado.

## TLS: el sobre cifrado de la web

`https://` = HTTP dentro de **TLS**. TLS combina las cuatro piezas para darte, sobre una red hostil: **confidencialidad** (cifrado), **integridad** (MAC), y **autenticación del servidor** (firma vía su certificado). Por eso [[cyber-sys1]] insistía: datos sensibles sobre `http://` viajan desnudos; sobre `https://` van en un sobre verificado. El certificado es la pieza que evita que te conectes al impostor del envenenamiento de DNS.

## Mini-ejemplo trabajado

Un equipo quiere "asegurar" los webhooks que su API recibe de un proveedor. Proponen: *"hasheamos el cuerpo con SHA-256 y comparamos"*. ¿Funciona?

No. Cualquiera que envíe un webhook falso puede hashear **su** cuerpo falso y mandar ese hash: el SHA-256 no prueba **quién** lo envió. La solución correcta es un **HMAC** con un **secreto compartido** entre proveedor y receptor: solo quien conoce el secreto produce un sello válido. Cambiamos *hash* por *MAC* y el problema (autenticidad) queda resuelto. Mismo "se ve cripto", garantía completamente distinta.

## Señales de reconocimiento

| Señal | Diagnóstico |
|---|---|
| "Guardamos las contraseñas cifradas" | Mal: deben ser hash lento + salt, no cifrado |
| "Usamos un hash para verificar el origen" | Falta autenticidad → necesitas MAC o firma |
| "Hicimos nuestro propio cifrado" | 🚩 Regla de oro rota |
| "MD5/SHA-1 nos sirve" | Algoritmos rotos para integridad adversaria |
| Datos sensibles sobre `http://` | Sin C ni I en tránsito → TLS |

## Errores típicos

- **Hash como prueba de origen:** confundir integridad accidental con autenticidad.
- **Cifrar lo que se debe hashear** (contraseñas) o **hashear lo que se debe cifrar** (un secreto que necesitas recuperar).
- **Inventar o "mejorar" un algoritmo:** la cripto casera falla de formas invisibles; usa librerías auditadas y modos estándar.

## Contraejemplo y caso borde

- **Contraejemplo:** "está cifrado, está seguro" — pero la llave está hardcodeada en el repo (ver [[cyber-secure-dev]]). El cifrado más fuerte es inútil si la llave es pública. **La seguridad se muda al manejo de llaves.**
- **Caso borde:** cifrar un dato garantiza **C**, no **I**: un atacante puede no leerlo y aun así corromperlo. Para C *y* protección de manipulación se usan modos **autenticados** (AES-GCM), que combinan cifrado + integridad.

## Transferencia a ciencia de datos e IA

Verificarás integridad de **datasets** y **modelos** descargados con hashes/firmas (provenance, [[cyber-ml-security]]); protegerás *secretos* y llaves en [[cyber-secure-dev]]; y entenderás por qué un endpoint de inferencia debe ir sobre TLS. La regla de oro —no inventar cripto— se extiende a no inventar tampoco tus propios esquemas de "tokenización segura" caseros.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para cada caso elige hash, cifrado, MAC o firma: (a) guardar contraseñas; (b) verificar que un release de PyPI es del autor; (c) ocultar datos en disco; (d) validar que un webhook viene del proveedor.
- **Misión externa (lab vivo):** en **picoCTF Practice** (https://play.picoctf.org/practice) resuelve un reto de la categoría *Cryptography* de nivel introductorio. **Criterio de cierre:** explicar qué suposición criptográfica rompía el reto. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** una tabla propia "garantía → herramienta" con un ejemplo real por fila.

---

> **Síntesis:** elige la herramienta por la **garantía**: **hash** (integridad accidental/huella), **cifrado** (confidencialidad), **MAC** (integridad + autenticidad con secreto compartido), **firma** (además, no repudio). **TLS** envuelve la web con las tres garantías y autentica al servidor. La seguridad se muda casi siempre al **manejo de llaves**, y la regla inviolable es **no inventar criptografía**.

---

**Referencias**

- Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security* (CS 161). University of California, Berkeley.
- picoCTF. (n.d.). *Practice*. https://play.picoctf.org/practice

*Retrieval: (1) ¿por qué un hash no prueba el origen?; (2) ¿cómo se guardan contraseñas y por qué no cifradas?; (3) ¿qué tres garantías da TLS?; (4) ¿adónde se muda la seguridad cuando todo está cifrado?*
