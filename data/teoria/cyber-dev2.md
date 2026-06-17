# Dependencias y supply chain: SBOM, SCA y CI/CD seguro

> Recurso troncal: **OpenSSF / Wheeler, *Secure Software Development Fundamentals***. Continúa [[cyber-dev1]]: tu código puede ser impecable y aun así ser inseguro por lo que **importas**.

## De qué trata (y qué sabrás hacer al final)

Un proyecto de ciencia de datos moderno tiene 5 líneas tuyas y 500 000 de otros: NumPy, pandas, scikit-learn, y las cientos de dependencias *transitivas* que ellas arrastran. Cada una es código que corre con tus permisos. La **cadena de suministro de software** (supply chain) es hoy una de las superficies de ataque más explotadas: no te atacan a ti, atacan a una librería que tú usas.

La intuición: cocinas un platillo con ingredientes comprados. Tú puedes ser un chef impecable, pero si un proveedor adulteró la harina, tu pastel envenena igual. La seguridad de tu plato depende de la **procedencia** de cada ingrediente y de tu capacidad de saber **qué llevas dentro** cuando se descubre que un lote estaba malo.

Al terminar podrás: (1) explicar el **riesgo de dependencias y supply chain**; (2) entender **SBOM, SCA y SAST**; (3) reconocer ataques como *typosquatting* y paquetes maliciosos; y (4) razonar un **CI/CD seguro** con permisos mínimos.

## Por qué las dependencias son la superficie de ataque

- **Vulnerabilidades conocidas:** una versión de una librería con un CVE público corre en tu app hasta que la actualizas. (El caso Log4Shell mostró el alcance: una librería de logging comprometió a medio mundo.)
- **Paquetes maliciosos:** un atacante publica un paquete que parece útil, o **typosquatting** (`reqeusts` por `requests`), o secuestra un paquete legítimo abandonado e inyecta código.
- **Dependencias transitivas:** no eliges la mayoría de lo que corre; viene arrastrado. No puedes proteger lo que no sabes que tienes.

## SBOM, SCA, SAST: el instrumental

| Herramienta | Qué es | Para qué |
|---|---|---|
| **SBOM** (Software Bill of Materials) | Lista completa de todo lo que tu software incluye, incl. transitivas | Saber **qué llevas dentro** cuando sale un CVE |
| **SCA** (Software Composition Analysis) | Escanea tus dependencias contra bases de vulnerabilidades | Detectar dependencias vulnerables |
| **SAST** (Static Application Security Testing) | Analiza **tu** código fuente buscando patrones inseguros | Cazar bugs antes de ejecutar |
| **Fuzzing** | Lanza entradas aleatorias/malformadas para provocar fallos | Hallar fallos que las pruebas normales no |

La pareja clave para un DS: **SBOM + SCA**. Sin SBOM, cuando estalle el próximo Log4Shell no sabrás si te afecta. Con SCA en el CI, te enteras de una dependencia vulnerable antes de desplegarla.

## CI/CD seguro

El pipeline que construye y despliega tu software es, él mismo, un activo crítico: tiene acceso a secretos y a producción. Principios:

- **Permisos mínimos para el pipeline:** tokens de alcance estrecho, no credenciales de admin "por comodidad" (least privilege otra vez).
- **Fijar versiones (pinning) y verificar integridad:** instala versiones exactas con *hashes* verificados (ver [[cyber-sys2]]), no "la última" a ciegas.
- **Aislar la ejecución:** builds en entornos efímeros; no ejecutar scripts de instalación arbitrarios con permisos amplios.
- **Secretos del CI:** en el *secret store* del CI, nunca en el archivo de configuración del pipeline.

## Cuándo actualizar una dependencia vulnerable

No es automático "siempre actualiza ya". Razonas: ¿el CVE es **explotable en tu uso** (¿usas la función afectada?)? ¿el impacto sobre tus activos es alto? ¿la actualización rompe compatibilidad? La regla práctica: **parchea rápido lo crítico y explotable**; planifica lo demás; pero **nunca ignores** un CVE de severidad alta en una dependencia expuesta.

## Mini-ejemplo trabajado

Tu repo de un modelo en producción tiene `requirements.txt` con `requests`, `pandas` y una librería de gráficas poco mantenida, todas sin versión fija. Un SCA reporta: la librería de gráficas tiene un CVE crítico explotable y no recibe mantenimiento. Decisión: como es explotable y de impacto alto, **reemplázala o fíjala a una versión parcheada** ya; fija (*pin*) todas las versiones con hashes; genera un **SBOM** para tener inventario; y añade **SCA al CI** para que el próximo CVE te avise solo. Lo barato (pinning + SBOM + SCA) previene la próxima crisis.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| `requirements.txt` sin versiones fijas | Instalas cualquier cosa, incl. una comprometida |
| Sin SBOM ni SCA | Ceguera ante CVEs en tus dependencias |
| Nombre de paquete raro/parecido al real | Posible typosquatting |
| El pipeline corre con credenciales de admin | Pipeline = blanco de alto valor |
| "Instala la última versión" en build | Build no reproducible ni verificado |

## Errores típicos

- **Confiar en un paquete por ser popular o "que ya usábamos":** la popularidad no es procedencia verificada; los secuestros existen.
- **Actualizar a ciegas o nunca actualizar:** ambos extremos fallan; se razona por explotabilidad e impacto.
- **Olvidar las transitivas:** el CVE casi siempre está en una dependencia que no instalaste tú directamente.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** generas un SBOM de tu app, SCA detecta una dependencia transitiva con CVE explotable y la actualizas fijando la versión por hash.
- **Contraejemplo:** un equipo con SAST impecable sobre **su** código pero sin SCA: pasan todas las revisiones y aun así despliegan una dependencia con un CVE crítico. Asegurar lo propio no asegura lo importado.
- **Caso borde:** una dependencia **sin CVE conocido** no es "segura", solo "sin fallos *publicados*"; un paquete abandonado es riesgo aunque su historial esté limpio.

## Transferencia a ciencia de datos e IA

La supply chain de software es la antesala de la **supply chain de modelos** ([[cyber-ml-security]]): un modelo preentrenado descargado de un repo público es una "dependencia" con su propia procedencia y riesgo de envenenamiento. Y la verificación de integridad por hash/firma de [[cyber-sys2]] es la herramienta concreta para confiar en lo que descargas, sea un paquete o un *checkpoint*.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** sobre un `requirements.txt` real, marca qué fijarías, qué auditarías con SCA y qué reemplazarías.
- **Misión externa (lab vivo):** explora un módulo de **OpenSSF Training** (https://openssf.org/training/courses/) sobre dependencias/supply chain. **Criterio de cierre:** explicar qué es un SBOM y por qué te salva ante el próximo CVE masivo.
- **Mini-entregable:** un plan de una carilla "supply chain segura para mi proyecto ML" (pinning, SBOM, SCA en CI, criterio de actualización).

---

> **Síntesis:** tu software incluye **muchísimo código ajeno** (incl. transitivo): la **supply chain** es superficie de ataque (CVEs, typosquatting, secuestros). Defiéndete con **SBOM** (saber qué llevas dentro), **SCA** (detectar dependencias vulnerables), **SAST/fuzzing** (tu propio código), **pinning + verificación de integridad**, y un **CI/CD con permisos mínimos**. Actualiza por **explotabilidad e impacto**, no a ciegas.

---

**Referencias**

- Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure software development fundamentals*. Open Source Security Foundation. https://openssf.org/training/courses/
- Open Source Security Foundation. (n.d.). *OpenSSF training courses*. https://openssf.org/training/courses/

*Retrieval: (1) ¿por qué las dependencias transitivas son peligrosas?; (2) define SBOM, SCA y SAST; (3) ¿qué es typosquatting?; (4) ¿cómo decides si actualizar una dependencia vulnerable?*
