#!/usr/bin/env node
// Inyecta la Fase 9 (IA Generativa, Responsable y Agéntica) en data/study.json:
//   - añade/actualiza el bloque "fase-9" en study.bloques
//   - añade/actualiza las unidades de data/genai/_unidades.json en study.unidades
// Idempotente: correrlo dos veces deja data/study.json igual.
// Respeta el formato del original: indentación de 1 espacio, sin newline final.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const studyPath = join(ROOT, 'data', 'study.json');
const uniPath = join(ROOT, 'data', 'genai', '_unidades.json');
const taxPath = join(ROOT, 'data', 'genai', '_taxonomia.json');

const study = JSON.parse(readFileSync(studyPath, 'utf8'));
const { unidades: genaiUnidades } = JSON.parse(readFileSync(uniPath, 'utf8'));
const { clusters } = JSON.parse(readFileSync(taxPath, 'utf8'));

// El orden de unidades del bloque sigue el orden de los clusters de la taxonomía.
const ordenUnidades = clusters.flatMap((c) => c.unidades);
const idsUni = new Set(genaiUnidades.map((u) => u.id));
const faltan = ordenUnidades.filter((id) => !idsUni.has(id));
const sobran = genaiUnidades.map((u) => u.id).filter((id) => !ordenUnidades.includes(id));
if (faltan.length || sobran.length) {
  console.error('ERROR: taxonomía y unidades no coinciden.');
  if (faltan.length) console.error('  En taxonomía sin unidad:', faltan.join(', '));
  if (sobran.length) console.error('  Unidad sin lugar en taxonomía:', sobran.join(', '));
  process.exit(1);
}

// 1) Unidades: reemplaza las de fase-9 existentes, conserva el resto.
study.unidades = study.unidades.filter((u) => u.bloque !== 'fase-9');
study.unidades.push(...genaiUnidades);

// 2) Bloque fase-9: lo crea o actualiza (sin campo examen → evaluación por cluster).
const bloqueFase9 = {
  id: 'fase-9',
  titulo: 'Fase 9 · IA Generativa, Responsable y Agéntica',
  meta:
    'Dominio técnico de la IA generativa al estado del arte: transformers y atención, RAG sobre datos propios, evaluación rigurosa de salidas, agentes (RL + LLM) y sistemas multi-agente, con IA responsable y de producción. Basado en el programa del MIT (MIT-AI.md); cada lección cita el estado del arte con enlaces vivos. Se evalúa con el examen final de cada cluster.',
  unidades: ordenUnidades,
};
const iBloque = study.bloques.findIndex((b) => b.id === 'fase-9');
if (iBloque === -1) study.bloques.push(bloqueFase9);
else study.bloques[iBloque] = bloqueFase9;

writeFileSync(studyPath, JSON.stringify(study, null, 1), 'utf8');
console.log(
  `OK: fase-9 inyectada. Unidades genai: ${genaiUnidades.length}. Bloques: ${study.bloques.length}. Unidades totales: ${study.unidades.length}.`
);
