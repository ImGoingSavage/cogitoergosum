#!/usr/bin/env node
// Inyecta la Fase 8 (Ciberseguridad) en data/study.json:
//   - añade/actualiza el bloque "fase-8" en study.bloques
//   - añade/actualiza las 40 unidades de data/ciberseguridad/_unidades.json en study.unidades
// Idempotente: correrlo dos veces deja data/study.json igual.
// Respeta el formato del original: indentación de 1 espacio, sin newline final.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const studyPath = join(ROOT, 'data', 'study.json');
const uniPath = join(ROOT, 'data', 'ciberseguridad', '_unidades.json');
const taxPath = join(ROOT, 'data', 'ciberseguridad', '_taxonomia.json');

const study = JSON.parse(readFileSync(studyPath, 'utf8'));
const { unidades: cyberUnidades } = JSON.parse(readFileSync(uniPath, 'utf8'));
const { clusters } = JSON.parse(readFileSync(taxPath, 'utf8'));

// El orden de unidades del bloque sigue el orden de los clusters de la taxonomía.
const ordenUnidades = clusters.flatMap((c) => c.unidades);
// Verifica que la taxonomía y las unidades coincidan exactamente.
const idsUni = new Set(cyberUnidades.map((u) => u.id));
const faltan = ordenUnidades.filter((id) => !idsUni.has(id));
const sobran = cyberUnidades.map((u) => u.id).filter((id) => !ordenUnidades.includes(id));
if (faltan.length || sobran.length) {
  console.error('ERROR: taxonomía y unidades no coinciden.');
  if (faltan.length) console.error('  En taxonomía sin unidad:', faltan.join(', '));
  if (sobran.length) console.error('  Unidad sin lugar en taxonomía:', sobran.join(', '));
  process.exit(1);
}

// 1) Unidades: reemplaza las cyber-* existentes, conserva el resto.
study.unidades = study.unidades.filter((u) => u.bloque !== 'fase-8');
study.unidades.push(...cyberUnidades);

// 2) Bloque fase-8: lo crea o actualiza (sin campo examen → evaluación por cluster).
const bloqueFase8 = {
  id: 'fase-8',
  titulo: 'Fase 8 · Ciberseguridad para STEM, Ciencia de Datos e IA',
  meta:
    'Criterio defensivo para científicos de datos: mentalidad de riesgo, sistemas y cripto, web/APIs, privacidad de datos, desarrollo seguro y supply chain, blue team, y seguridad de ML y de LLMs/RAG. Ruta defensiva, no de hacking; cada lección termina en práctica y referencias. Se evalúa con el examen final de cada cluster.',
  unidades: ordenUnidades,
};
const iBloque = study.bloques.findIndex((b) => b.id === 'fase-8');
if (iBloque === -1) study.bloques.push(bloqueFase8);
else study.bloques[iBloque] = bloqueFase8;

writeFileSync(studyPath, JSON.stringify(study, null, 1), 'utf8');
console.log(
  `OK: fase-8 inyectada. Unidades cyber: ${cyberUnidades.length}. Bloques: ${study.bloques.length}. Unidades totales: ${study.unidades.length}.`
);
