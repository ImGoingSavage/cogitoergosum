# Geometría de supervivencia I: ángulos, auxiliares y fantasmas

*Lección redactada para CogitoErgoSum a partir de la sección 8.2 de Zeitz (Survival Geometry I). Cubre el contenido completo de la unidad.*

## Congruencia: las condiciones válidas

Dos triángulos son congruentes si coinciden en:

- **SAS** (lado-ángulo-lado, con el ángulo ENTRE los lados),
- **ASA** (ángulo-lado-ángulo),
- **SSS** (tres lados),
- **AAS** (dos ángulos y un lado no comprendido — funciona porque dos ángulos determinan el tercero, y se reduce a ASA).

**Por qué ASS falla:** con un ángulo, un lado adyacente y el lado OPUESTO dados, el lado opuesto puede «caer» en dos posiciones — el compás que lo traza corta a la recta base en **dos puntos**, produciendo dos triángulos distintos con los mismos datos (el caso ambiguo de la ley de senos). **Cuándo SÍ vale ASS:** si el ángulo dado es **≥ 90°** (o el lado opuesto es mayor que el adyacente): el círculo solo corta una vez del lado relevante — en particular el caso hipotenusa-cateto de triángulos rectángulos.

**AAA** nunca da congruencia: da **semejanza** (forma sin tamaño, §8.3).

## Paralelas: el hecho motor

> Una transversal corta dos paralelas formando **ángulos alternos internos iguales** (y correspondientes iguales).

De ese único hecho salen en cascada los dos básicos: **la suma de los ángulos de un triángulo es 180°** (traza por un vértice la paralela al lado opuesto: los tres ángulos se alinean sobre ella) y **el ángulo exterior = suma de los dos interiores no adyacentes**.

## Objetos auxiliares: con tacto

La técnica más productiva de la geometría elemental: **dibujar algo que no estaba** — una paralela, un radio, una prolongación, un punto medio. Pero con tacto: demasiados auxiliares ensucian la figura y esconden lo que importaba. **La guía: deja que el penúltimo paso te diga qué entidad «natural» falta.** ¿Quieres ángulos iguales? Quizá falta un triángulo isósceles o una paralela. ¿Segmentos iguales? Quizá un círculo (todos los radios son iguales) o una congruencia. ¿Una razón? Una paralela que fabrique semejantes (§8.3). El auxiliar correcto es el que materializa tu penúltimo paso.

## El método del punto fantasma

**El problema tipo (8.2.12):** quieres probar que la recta por F paralela a BC **pasa por el punto medio E** de cierto segmento. La tentación: dibujar la paralela «por F y E» y razonar — pero eso **asume lo que quieres probar**.

**El método:** define **E′** como la intersección de la paralela por F con el segmento — un punto «fantasma» con la propiedad que controla la paralela — y **demuestra que E′ = E** (típicamente: demuestra que E′ es punto medio, y como el punto medio es único, E′ = E).

**A qué se parece:** a la **suposición contraria de una reducción al absurdo** — te da *algo concreto con qué trabajar*, que se retira al terminar. El fantasma convierte «probar que X tiene la propiedad P» en «construir el objeto con la propiedad P y probar que coincide con X»: a menudo la dirección fácil.

**El error emparentado (banco):** para probar que la recta entre dos puntos medios D, E es paralela a BC, decir «como DE es paralela a BC por el teorema del punto medio…» es **usar la conclusión como premisa** (petición de principio) — exactamente lo que el fantasma evita: define la paralela por D, llama E′ a su corte, prueba E′ = E.

## Círculos y ángulos: el teorema del ángulo inscrito

Vocabulario: el **ángulo central** mide lo mismo que su arco. El teorema estrella:

> **Ángulo inscrito = la MITAD del arco que subtiende** (la mitad del ángulo central del mismo arco).

**Esquema de la demostración — el prototipo del angle chasing:** UNA sola línea auxiliar: **el radio al vértice** del ángulo inscrito (conectar el centro O con el vértice V). Aparecen **triángulos isósceles** (¡dos lados son radios!): en cada uno, los ángulos de la base son iguales, y el ángulo exterior en O es la suma de los dos. Recolectando esa información angular caso por caso (centro dentro del ángulo, fuera, sobre un lado), el ángulo central termina siendo el doble del inscrito. ∎ La lección de método: una auxiliar natural + isósceles por radios + contabilidad paciente de ángulos = la mayoría de los lemas de círculos.

**Corolarios de oro:**

- **Todos los ángulos inscritos que subtienden el mismo arco son iguales** (cada uno es la mitad del mismo arco) — la fuente n.º 1 de ángulos iguales en figuras con círculos.
- **Todo ángulo inscrito en una semicircunferencia es recto** (Tales): subtiende un diámetro = arco de 180°.

**El reflejo de doble vía:** «ángulo recto» y «diámetro» **se delatan mutuamente**. ¿Ves un ángulo recto inscrito? El lado que subtiende es diámetro (y conoces el centro: su punto medio). ¿Ves un diámetro y un punto del círculo? Hay un ángulo recto esperándote. Este reflejo destapa el USAMO 1990 en §8.4.

## Disparadores

- Probar igualdad de segmentos/ángulos → busca congruencias (SAS/ASA/SSS/AAS) o isósceles; desconfía de ASS.
- «Demuestra que la recta pasa por el punto X» → punto fantasma: corta, nombra E′, demuestra E′ = X.
- Figura con círculo → caza ángulos inscritos: mismos arcos = mismos ángulos.
- Ángulo recto o diámetro a la vista → Tales en ambas direcciones.
- ¿Qué auxiliar trazar? → el que materializa tu penúltimo paso (radio, paralela, prolongación).

## Síntesis

> **Chunk mínimo:** Congruencia: SAS, ASA, SSS, AAS; ASS falla por el caso ambiguo (el compás corta dos veces) salvo ángulo ≥ 90° o hipotenusa-cateto; AAA da semejanza. De «alternos internos iguales» caen los 180° del triángulo y el ángulo exterior. Auxiliares con tacto: el penúltimo paso dicta cuál (¿ángulos iguales? isósceles/paralela; ¿segmentos? radios/congruencia). Punto fantasma: para «la recta pasa por E», define E′ = el corte y demuestra E′ = E — jamás asumas la conclusión (petición de principio). Ángulo inscrito = mitad del arco (prueba: radio al vértice → isósceles → contabilidad); corolarios: mismo arco = mismos ángulos, y Tales: recto ⟺ subtiende diámetro (reflejo de doble vía).

---

*Antes del quiz: reconstruye de memoria las cuatro condiciones con el porqué del fallo de ASS, el método del fantasma y su pariente lógico, y el esquema completo de la prueba del ángulo inscrito.*
