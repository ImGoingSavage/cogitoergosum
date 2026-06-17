// smoke-teoria.mjs — Validación rápida del render de TODAS las lecciones de
// teoría tras editar data/teoria/*.md o js/markdown.js.
//
// Uso:  node scripts/smoke-teoria.mjs
// Espera: threw=0 rawDisplayMath=0 undefined=0 rawFence=0  (rawLinks puede ser >0: son
//         literales de matriz [[1,3],[2,6]] que se dejan crudos A PROPÓSITO).
//
// Rutas relativas a este archivo → funciona en cualquier cuenta/máquina.
import { renderMarkdown } from '../js/markdown.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(here, '..', 'data', 'teoria');
// Escanea TODOS los .md (arena-*, zeitz-*, engel-*, aime-*, polya-*)
const files = fs.readdirSync(dir).filter((f) => f.endsWith('.md'));

let bad = 0, rawmath = 0, rawlink = 0, undefs = 0, rawFence = 0;
for (const f of files) {
  const md = fs.readFileSync(path.join(dir, f), 'utf8');
  let html;
  try { html = renderMarkdown(md); }
  catch (e) { console.log('THREW', f, e.message); bad++; continue; }
  if (/\$\$/.test(html)) { console.log('RAW $$ in', f); rawmath++; }   // display math sin renderizar
  if (/\[\[/.test(html)) { console.log('RAW [[ in', f); rawlink++; }   // wiki-link sin convertir (o literal de matriz)
  // Detecta la cadena literal "undefined" en el HTML renderizado
  const n = (html.match(/undefined/g) ?? []).length;
  if (n > 0) { console.log(`UNDEF(${n}) in`, f); undefs += n; }
  const fences = (html.match(/```/g) ?? []).length;
  if (fences > 0) { console.log(`RAW FENCE(${fences}) in`, f); rawFence += fences; }
}
console.log(`\nfiles=${files.length} threw=${bad} rawDisplayMath=${rawmath} rawLinks=${rawlink} undefined=${undefs} rawFence=${rawFence}`);
if (undefs > 0 || rawFence > 0) {
  if (undefs > 0) {
    console.error(`\nERROR: ${undefs} ocurrencia(s) de "undefined" en el HTML renderizado. Corrige js/markdown.js.`);
  }
  if (rawFence > 0) {
    console.error(`\nERROR: ${rawFence} fence(s) sin renderizar en el HTML. Corrige el render de bloques de código.`);
  }
  process.exitCode = 1;
}

// Comprobación por-lección de las secciones del contrato (opcional, informativa):
// pásale ids como argumentos:  node scripts/smoke-teoria.mjs arena-q2 arena-b1
for (const id of process.argv.slice(2)) {
  const md = fs.readFileSync(path.join(dir, `${id}.md`), 'utf8');
  const has = (s) => md.includes(s);
  console.log(`${id.padEnd(12)} Transfer:${has('Transferencia isomorfa')} Errores:${has('Errores típicos')}`
    + ` Mini:${has('Mini-ejemplo')} closers:${has('## Disparadores') && /[Ss]íntesis/.test(md) && /[Rr]etrieval/.test(md)}`);
}
