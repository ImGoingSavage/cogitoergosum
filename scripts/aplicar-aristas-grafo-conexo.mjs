import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const START = '<!-- GRAFO_CONEXO_OLEADA3_START -->';
const END = '<!-- GRAFO_CONEXO_OLEADA3_END -->';

const study = JSON.parse(readFileSync('data/study.json', 'utf8'));
const valid = new Set(study.unidades.map((u) => u.id));
for (const dir of ['entrevista', 'ciberseguridad', 'genai']) {
  const tax = JSON.parse(readFileSync(`data/${dir}/_taxonomia.json`, 'utf8'));
  for (const c of tax.clusters || []) valid.add(c.id);
}

const blocks = {
  'polya-cuatro-pasos': `## Puente de transferencia

Las cuatro fases de Polya son el protocolo general que vuelve operables los problemas de [[zeitz-1]] (diferenciar ejercicio de problema): entender, planear, ejecutar y revisar. En trabajo aplicado, la misma disciplina aparece en [[arena-c4]] (stakeholders y carrera) cuando conviertes ambiguedad en un plan verificable, y en [[gen-resp4]] cuando eliges la pieza GenAI mas simple que resuelve el caso antes de construir.`,

  'polya-diccionario': `## Puente de transferencia

El diccionario de heuristicas funciona como indice mental para elegir movimientos: ensuciarse las manos en [[zeitz-2b]], buscar invariantes o simetrias en [[arena-q12]], y reconocer el tipo de acertijo en [[arena-p1]]. No es una lista para memorizar; es un sistema de routing cognitivo que decide que herramienta probar segun la forma del bloqueo.`,

  'zeitz-1': `## Puente de transferencia

La diferencia entre ejercicio y problema prepara todo el modo Estudio: en [[polya-cuatro-pasos]] aparece como ciclo de ataque, y en [[arena-p1]] como razonamiento rapido que exige reconocer estructura bajo presion. Cuando el problema pide prueba o estrategia, [[arena-q13]] retoma la misma frontera entre aplicar una receta y construir una idea.`,

  'zeitz-2a': `## Puente de transferencia

La psicologia del resolvedor explica por que [[polya-cuatro-pasos]] empieza con entender y no con calcular. La tolerancia a fallar, pedir feedback y sostener ambiguedad conecta con [[arena-c2]], mientras que el bucle estado-accion-observacion de [[gen-ag1]] formaliza esa adaptacion como decisiones con retroalimentacion.`,

  'zeitz-2b': `## Puente de transferencia

Manos sucias, penultimo paso y pensamiento ilusorio son tacticas para romper bloqueo: [[polya-diccionario]] las organiza como heuristicas, [[arena-p1]] las ejercita en acertijos, y [[gen-eval4]] las traduce al ciclo moderno de probar prompts, medir errores y reformular con datos held-out.`,

  'zeitz-23': `## Puente de transferencia

Contradiccion e induccion son motores de prueba que reaparecen en [[engel-ind]] como induccion fuerte y descenso, y en [[arena-cc3]] como razonamiento recursivo sobre subproblemas. En entrevistas, [[arena-q13]] usa la misma estructura cuando un juego o una logica solo cede al fortalecer la hipotesis.`,

  'zeitz-24': `## Puente de transferencia

Reformular un problema es cambiar su representacion: dibujar, traducir o mirar desde otro punto de vista. Esa idea conecta con [[arena-h1]] cuando un DAG vuelve visible un sesgo causal, con [[arena-q12]] cuando un invariante sustituye fuerza bruta, y con [[gen-rag4]] cuando el diagnostico separa recuperacion, generacion y evaluacion.`,

  'zeitz-31': `## Puente de transferencia

La simetria reduce casos porque identifica lo que realmente cambia y lo que no. Esa misma compresion aparece en [[arena-q12]] al buscar invariantes, en [[aime-geo]] al elegir coordenadas o reflejos, y en [[zeitz-85a]] cuando una transformacion rigida conserva distancias y angulos.`,

  'zeitz-32': `## Puente de transferencia

El principio extremo convierte una coleccion desordenada en un punto de ataque: toma el menor, mayor o mas saturado y fuerzalo. [[engel-extremo]] profundiza esa cantera, [[arena-q13]] lo usa en pruebas de logica e induccion, y [[arena-sre4]] lo refleja en produccion cuando buscas el cuello de botella o el modo de fallo limite antes de generalizar.`,

  'zeitz-33': `## Puente de transferencia

El palomar es conteo con tension: demasiados objetos para pocas cajas. Su hogar natural esta en [[arena-b1]] (conteo y probabilidad), se vuelve tecnica de competencia en [[aime-cnt]], y aparece como criterio de imposibilidad junto a biyecciones y particiones en [[zeitz-62]].`,

  'zeitz-34': `## Puente de transferencia

Invariantes y monovariantes son memoria estructural de un proceso: que no cambia y que avanza en una sola direccion. [[engel-inv]] lo desarrolla como principio de imposibilidad, [[arena-q12]] lo usa en brainteasers de conteo y juegos, y [[arena-cc3]] lo convierte en argumento de terminacion para recursion y programacion dinamica.`,

  'zeitz-41': `## Puente de transferencia

Los grafos recodifican relaciones para que caminos, componentes y grados hagan visible lo oculto. [[arena-cc2]] enseña busqueda en arboles y grafos, [[arena-h1]] usa DAGs para razonar causalidad y adjustment sets, y [[gen-ma2]] lleva la misma idea a orquestacion: agentes como nodos y mensajes como aristas con fallos posibles.`,

  'zeitz-61': `## Puente de transferencia

Sumar, multiplicar y dividir son la gramatica basica del conteo. [[arena-b1]] los convierte en probabilidad operativa, [[arena-p2]] los usa en combinatoria discreta, y [[aime-cnt]] los entrena bajo presion con casos, complemento y control de doble conteo.`,

  'zeitz-62': `## Puente de transferencia

Particiones y biyecciones muestran que contar es elegir una representacion donde los objetos se vuelven comparables. [[arena-b1]] da el lenguaje probabilistico, [[arena-p2]] lo extiende a estructuras discretas, y [[aime-cnt]] lo exige cuando una cuenta directa es torpe pero una correspondencia limpia resuelve el problema.`,

  'zeitz-63': `## Puente de transferencia

Complemento e inclusion-exclusion son antidotos contra contar mal por solapes. [[arena-b1]] introduce el principio en conteo basico, [[arena-fc1]] lo aplica a urnas y emparejamientos, y [[aime-cnt]] lo vuelve una decision tactica: contar lo prohibido puede ser mas barato que contar lo permitido.`,

  'engel-comb': `## Puente de transferencia

La cantera combinatoria de Engel funciona como gimnasio para las tecnicas de [[zeitz-61]], [[zeitz-62]] y [[zeitz-63]]. En la Arena, [[arena-p2]] organiza esas mismas ideas como probabilidad discreta, mientras [[aime-cnt]] las prueba en problemas donde elegir casos correctos importa mas que expandir formulas.`,

  'zeitz-71': `## Puente de transferencia

Primos y divisibilidad son restricciones estructurales: factorizan el universo antes de calcular. [[engel-nt]] ofrece mas cantera de teoria de numeros, [[zeitz-72]] transforma divisibilidad en congruencias manejables, y [[arena-q13]] reutiliza esa mentalidad cuando una prueba necesita filtrar casos imposibles.`,

  'zeitz-72': `## Puente de transferencia

Las congruencias convierten una pregunta infinita en un mundo finito donde los residuos importan. Se apoyan en [[zeitz-71]] para factorizacion y divisibilidad, alimentan problemas diofanticos en [[zeitz-74]], y conectan con [[arena-q12]] porque un residuo modulo m suele ser el invariante que no cambia.`,

  'zeitz-64': `## Puente de transferencia

Las recurrencias convierten una historia en estado y transicion: Fibonacci, Catalan y DP comparten esa forma. [[arena-cc3]] la implementa como recursion y programacion dinamica, [[engel-suc]] la entrena como sucesiones, y [[arena-p2]] muestra cuando la recurrencia cuenta objetos combinatorios.`,

  'zeitz-43': `## Puente de transferencia

Las funciones generatrices codifican conteos como algebra para que coeficientes revelen estructura. Nacen de recurrencias como [[zeitz-64]], conectan con la combinatoria de [[arena-p2]], y regresan a [[arena-b1]] cuando una distribucion o suma se entiende mejor mediante una funcion que empaqueta casos.`,

  'zeitz-73': `## Puente de transferencia

Las funciones aritmeticas d, sigma y phi cuentan estructura interna de los enteros. Dependen de la factorizacion de [[zeitz-71]], se simplifican con congruencias de [[zeitz-72]], y conectan con [[arena-b1]] porque muchas identidades son conteos de divisores vistos desde dos perspectivas.`,

  'zeitz-74': `## Puente de transferencia

Las diofanticas se resuelven filtrando: factorizacion, paridad, modulo y acotacion. [[zeitz-71]] aporta primos y divisibilidad, [[zeitz-72]] aporta congruencias, y [[arena-q13]] retoma el habito de convertir una busqueda infinita en una prueba por casos imposibles.`,

  'zeitz-75': `## Puente de transferencia

Los ejemplos de primos, polinomios y collares son mapas de transferencia: [[zeitz-71]] explica las restricciones aritmeticas, [[zeitz-43]] muestra como empaquetar conteos, y [[arena-q12]] recuerda que simetrias e invariantes suelen ser el atajo que evita enumerar todo.`,

  'engel-nt': `## Puente de transferencia

La cantera de teoria de numeros de Engel profundiza los filtros de [[zeitz-71]] y las congruencias de [[zeitz-72]]. En entrevistas, [[arena-q13]] usa la misma caja de herramientas para pruebas cortas donde modularidad, paridad y descenso eliminan familias completas de candidatos.`,

  'zeitz-52': `## Puente de transferencia

Factorizar sin piedad es convertir expresiones opacas en estructura. [[arena-p4]] lo conecta con algebra lineal y calculo para quant, [[aime-alg]] lo practica en sustituciones y sucesiones, y [[engel-pol]] lo extiende a polinomios donde ceros y coeficientes revelan la solucion.`,

  'zeitz-53': `## Puente de transferencia

El telescopio muestra que una suma puede colapsar si eliges la forma correcta. [[arena-p4]] usa esa manipulacion en calculo y finanzas, [[aime-alg]] la entrena como algebra de competencia, y [[zeitz-9]] la lleva a series y convergencia cuando el patron se vuelve infinito.`,

  'zeitz-54': `## Puente de transferencia

Polinomios, ceros y Vieta convierten raices en coeficientes y viceversa. [[engel-pol]] amplifica esa cantera, [[aime-alg]] la aplica bajo restricciones de examen, y [[arena-p4]] muestra por que la misma estructura algebraica importa en modelos y calculo financiero.`,

  'zeitz-55': `## Puente de transferencia

Las desigualdades son control de forma: AM-GM, Cauchy y massage dicen que expresiones pueden dominar a otras. [[engel-ineq]] profundiza tecnicas de competencia, [[arena-p4]] las conecta con optimizacion y calculo, y [[arena-q5]] las usa cuando derivadas y convexidad explican mercados y riesgo.`,

  'engel-ineq': `## Puente de transferencia

La cantera de desigualdades de Engel es la version intensiva de [[zeitz-55]]. Sus tecnicas se apoyan en la intuicion de optimizacion de [[arena-p4]] y reaparecen en [[arena-q5]] cuando una cota, una derivada o una convexidad decide que extremo financiero es posible.`,

  'zeitz-42': `## Puente de transferencia

Los numeros complejos permiten cruzar algebra y geometria sin cambiar de problema. [[engel-geo2]] usa complejos, vectores y trigonometria como lenguaje geometrico, [[aime-geo]] los traduce a problemas de examen, y [[arena-p4]] conserva la estructura algebraica que hace utiles esas transformaciones.`,

  'zeitz-82': `## Puente de transferencia

Angulos y fantasmas geometricos son una forma de crear informacion que el diagrama oculta. [[aime-geo]] practica esa lectura en examenes, [[engel-geo2]] aporta vectores y trigonometria, y [[arena-p4]] recuerda que elegir coordenadas o algebraizar puede volver calculable la configuracion.`,

  'zeitz-83': `## Puente de transferencia

Area y semejanza convierten una figura en relaciones de escala. [[aime-geo]] las usa con Heron, potencia y coordenadas, [[engel-geo2]] aporta herramientas avanzadas, y [[zeitz-85b]] muestra como homotecia y semejanza espiral explican por que ciertas longitudes cambian juntas.`,

  'zeitz-84': `## Puente de transferencia

El poder de la geometria elemental esta en elegir el lenguaje adecuado antes de calcular. [[aime-geo]] entrena esa eleccion en problemas cerrados, [[engel-geo2]] da tecnicas avanzadas, y [[zeitz-83]] muestra que area y semejanza suelen ser el puente mas barato hacia la solucion.`,

  'zeitz-9': `## Puente de transferencia

El calculo de competencia une convergencia, series y manipulacion euleriana. [[arena-p4]] ofrece el marco de calculo para finanzas cuantitativas, [[arena-q5]] conecta derivadas con mercados, y [[zeitz-53]] muestra que muchas series primero se vuelven manejables por telescopio.`,

  'engel-inv': `## Puente de transferencia

El principio de invariancia de Engel profundiza [[zeitz-34]]: si algo no cambia, restringe todo el proceso. [[arena-q12]] lo usa para brainteasers de conteo, y [[arena-cc3]] lo convierte en argumento de terminacion o correccion cuando un algoritmo recursivo debe conservar una propiedad.`,

  'engel-color': `## Puente de transferencia

Las coloraciones son invariantes visuales: colorear crea una cantidad conservada que vuelve imposible una configuracion. Conecta con [[zeitz-34]] y [[arena-q12]], y tambien con [[arena-b1]] cuando el argumento depende de contar clases de color en lugar de piezas individuales.`,

  'engel-extremo': `## Puente de transferencia

El principio extremal de Engel es el compañero directo de [[zeitz-32]]. En [[arena-q13]] aparece cuando eliges el objeto minimo o maximo para forzar una contradiccion, y en [[arena-sre4]] se reconoce como buscar el caso limite que dispara cascada, sobrecarga o fallo de simplicidad.`,

  'engel-juegos': `## Puente de transferencia

Juegos de posiciones perdedoras y pareo combinan invariantes con decision secuencial. [[arena-q13]] trabaja esos argumentos en entrevistas, [[zeitz-34]] aporta propiedades que no cambian, y [[arena-q8]] conecta juegos con esperanza, parada optima y valor de actuar en el tiempo.`,

  'zeitz-85a': `## Puente de transferencia

Reflexion, rotacion y traslacion conservan estructura; por eso una figura dificil puede moverse sin cambiar el problema. [[aime-geo]] usa esas transformaciones bajo presion, [[engel-geo2]] las combina con vectores, y [[zeitz-31]] explica la simetria que hace legitimo el movimiento.`,

  'zeitz-85b': `## Puente de transferencia

Homotecia y semejanza espiral son transformaciones donde escala y giro explican relaciones escondidas. [[aime-geo]] las necesita para reconocer semejanza, [[engel-geo2]] aporta herramientas avanzadas, y [[zeitz-42]] muestra por que los complejos son un lenguaje natural para rotar y escalar.`,

  'engel-ind': `## Puente de transferencia

Induccion fuerte, fortalecida y descenso son refinamientos de [[zeitz-23]]. [[arena-cc3]] los vuelve algoritmo en recursion y DP, mientras [[arena-q13]] los usa como estrategia de prueba cuando el enunciado original debe fortalecerse para que el paso inductivo cierre.`,

  'engel-suc': `## Puente de transferencia

Sucesiones y recurrencias comparten estado, transicion y condicion inicial. [[zeitz-64]] da Fibonacci y Catalan como patrones, [[arena-cc3]] los implementa en programacion dinamica, y [[arena-p2]] muestra cuando una sucesion realmente cuenta configuraciones combinatorias.`,

  'engel-pol': `## Puente de transferencia

Polinomios en Engel retoman [[zeitz-54]] con factor, Vieta y valores especiales. [[aime-alg]] los convierte en tecnica de examen, y [[arena-p4]] muestra que la misma manipulacion algebraica sostiene modelos, optimizacion y calculo aplicado.`,

  'engel-fun': `## Puente de transferencia

Las ecuaciones funcionales exigen tratar una regla como objeto de prueba: probar valores, forzar simetrias y usar invariantes. [[arena-q13]] aporta el marco de logica y juegos de estrategia, [[zeitz-54]] recuerda el papel de identidades polinomiales, y [[aime-alg]] practica sustituciones controladas.`,

  'engel-geo2': `## Puente de transferencia

Geometria avanzada con vectores, complejos y trigonometria es el puente entre configuraciones visuales y calculo. [[aime-geo]] lo aplica en problemas cerrados, [[zeitz-42]] explica el lenguaje complejo, y [[arena-p4]] da la base algebraica para mover entre representaciones.`,

  'aime-alg': `## Puente de transferencia

El algebra AIME concentra sucesiones, Vieta y sustitucion en problemas con respuesta exacta. [[zeitz-52]] aporta factorizacion, [[zeitz-54]] aporta polinomios y Vieta, y [[arena-p4]] conecta esas tecnicas con calculo y algebra lineal de uso profesional.`,

  'aime-geo': `## Puente de transferencia

La geometria AIME exige elegir rapido entre Heron, potencia, coordenadas y semejanza. [[zeitz-82]] y [[zeitz-83]] construyen los fundamentos, mientras [[engel-geo2]] ofrece herramientas avanzadas para convertir el diagrama en relaciones calculables.`,

  'aime-cnt': `## Puente de transferencia

Conteo y probabilidad AIME vuelven tacticas a las tecnicas de [[zeitz-61]], [[zeitz-62]] y [[zeitz-63]]. [[arena-b1]] da el hogar conceptual: suma, producto, complemento y casos son el mismo lenguaje que luego se mide como probabilidad.`,

  'arena-b1': `## Puentes de regreso

El hogar de conteo y probabilidad se vuelve mas transferible cuando enlaza con sus canteras olimpicas: [[zeitz-61]] formaliza suma/producto/division, [[zeitz-62]] entrena particiones y biyecciones, [[zeitz-63]] controla solapes con inclusion-exclusion, [[engel-comb]] aporta practica intensa y [[aime-cnt]] muestra la version de examen bajo presion.`,

  'arena-p2': `## Puentes de regreso

La combinatoria discreta de la Arena no vive aislada: [[zeitz-43]] empaqueta conteos en funciones generatrices, [[zeitz-64]] convierte estructuras en recurrencias, y [[engel-suc]] entrena sucesiones donde el estado correcto decide si la cuenta cierra.`,

  'arena-q12': `## Puentes de regreso

Los brainteasers de invariantes y conteo se conectan hacia atras con [[zeitz-34]] y [[engel-inv]], donde se aprende a nombrar lo que no cambia. [[engel-color]] muestra invariantes visuales por coloracion, y [[zeitz-31]] agrega simetria como compresion de casos antes de contar.`,

  'arena-q13': `## Puentes de regreso

La logica de entrevistas recupera tecnicas de prueba clasicas: [[zeitz-23]] para contradiccion e induccion, [[engel-ind]] para fortalecer la hipotesis, [[engel-extremo]] para elegir un objeto limite, [[engel-juegos]] para posiciones ganadoras y [[engel-fun]] para reglas que se prueban por sustitucion.`,

  'arena-cc2': `## Puentes de regreso

Arboles, grafos y busqueda tienen una raiz olimpica en [[zeitz-41]]: recodificar relaciones como nodos y aristas. Ese mismo gesto reaparece en causalidad con [[arena-h1]] y en agentes con [[gen-ma2]], donde la estructura del grafo decide rutas, dependencias y fallos.`,

  'arena-h1': `## Puentes de regreso

Los DAGs causales de esta unidad son grafos con semantica: heredan la intuicion de [[zeitz-41]] sobre relaciones y caminos, pero agregan direccion causal y adjustment sets. Esa diferencia prepara el salto a [[gen-ma2]], donde el grafo de agentes tambien exige controlar que informacion cruza cada arista.`,

  'arena-p4': `## Puentes de regreso

Calculo y algebra lineal para finanzas se apoyan en una base olimpica amplia: [[zeitz-52]] para factorizacion, [[zeitz-54]] para polinomios y Vieta, [[zeitz-55]] para desigualdades, [[zeitz-42]] para complejos, [[aime-alg]] para manipulacion exacta y [[aime-geo]] cuando una representacion geometrica simplifica el calculo.`,

  'arena-fc1': `## Puentes de regreso

Coincidencias, urnas y emparejamientos son terreno natural para complemento e inclusion-exclusion. [[zeitz-63]] aporta el lenguaje de solapes, y [[aime-cnt]] muestra por que contar lo que no ocurre suele ser mas estable que enumerar directamente lo que si ocurre.`,

  'arena-dmls4': `## Puente inter-fase

Cambios de distribucion, monitoreo y pruebas en produccion conectan directamente con [[gen-resp3]]: en GenAI, cada cambio de prompt, modelo, corpus o herramienta dispara reevaluacion continua. La misma disciplina se cruza con [[cyber-mls5]], donde supply chain de modelos y AI RMF convierten drift y versionado en riesgo gobernado.`,

  'gen-resp3': `## Puente inter-fase

La operacion de GenAI no empieza de cero: [[arena-dmls4]] ya enseña distribution shift, monitoreo y pruebas en produccion, y [[arena-rml3]] profundiza serving y observabilidad de modelos. En seguridad, [[cyber-blue1]] aporta la mentalidad de logs y deteccion que aqui se vuelve tracing, alertas de calidad y respuesta a regresiones.`,
};

let avisos = 0;
let enlaces = 0;
for (const [id, body] of Object.entries(blocks)) {
  const file = `data/teoria/${id}.md`;
  if (!valid.has(id)) {
    console.log(`AVISO: unidad inexistente para bloque ${id}`);
    avisos++;
    continue;
  }
  if (!existsSync(file)) {
    console.log(`AVISO: falta archivo ${file}`);
    avisos++;
    continue;
  }
  for (const m of body.matchAll(/\[\[([^\]]+)\]\]/g)) {
    const target = m[1].split('|')[0].trim();
    enlaces++;
    if (!valid.has(target)) {
      console.log(`AVISO: target inexistente ${id} -> [[${target}]]`);
      avisos++;
    }
  }
  upsert(file, body);
}

console.log(`OK: aristas aplicadas archivos=${Object.keys(blocks).length} enlaces=${enlaces} avisos=${avisos}`);
if (avisos) process.exit(1);

function upsert(file, body) {
  const original = readFileSync(file, 'utf8').replace(/\s*$/u, '\n');
  const block = `\n${START}\n${body}\n${END}\n`;
  const start = original.indexOf(START);
  const end = original.indexOf(END);
  let next;
  if (start >= 0 && end > start) {
    next = `${original.slice(0, start).replace(/\s*$/u, '\n')}${block}${original.slice(end + END.length).replace(/^\s*/u, '')}`;
  } else {
    next = `${original}${block}`;
  }
  writeFileSync(file, next.endsWith('\n') ? next : `${next}\n`, 'utf8');
}
