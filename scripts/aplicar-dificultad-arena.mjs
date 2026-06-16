#!/usr/bin/env node
// Inyecta "difficulty" en cada pregunta del banco de Fase 7 Arena.
// Fuente: data/arena-dificultades.json (clasificación manual del arquitecto).
// Idempotente: correrlo dos veces deja data/study.json igual.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const studyPath = join(ROOT, 'data', 'study.json');
const difPath   = join(ROOT, 'data', 'arena-dificultades.json');

const study = JSON.parse(readFileSync(studyPath, 'utf8'));
const { dificultades } = JSON.parse(readFileSync(difPath, 'utf8'));

let modificadas = 0;
const faltantes = [];

for (const unidad of study.unidades) {
  if (unidad.bloque !== 'fase-7') continue;
  for (const q of (unidad.banco ?? [])) {
    if (!(q.id in dificultades)) {
      faltantes.push(q.id);
      continue;
    }
    const nueva = dificultades[q.id];
    if (q.difficulty !== nueva) {
      q.difficulty = nueva;
      modificadas++;
    }
  }
}

if (faltantes.length) {
  console.error(`\nERROR: ${faltantes.length} pregunta(s) de fase-7 sin clasificar:`);
  faltantes.forEach((id) => console.error(`  - ${id}`));
  process.exit(1);
}

writeFileSync(studyPath, JSON.stringify(study, null, 1), 'utf8');
console.log(`OK: difficulty inyectada. Campos actualizados: ${modificadas} (0 = ya estaba al día).`);
