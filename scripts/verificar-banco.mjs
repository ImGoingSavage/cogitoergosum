import { readFileSync } from 'node:fs';

const us = JSON.parse(readFileSync('data/genai/_unidades.json', 'utf8')).unidades;
let mcMal = 0, dup = 0, larga = 0, trunc = 0, plantilla = 0;
const ids = new Set();
const susp = (s) => {
  s = String(s).trim();
  const o = (s.match(/\(/g) || []).length;
  const c = (s.match(/\)/g) || []).length;
  return o > c || (!/[.!?:)\]"»]$/.test(s) && s.length > 40);
};

for (const u of us) {
  for (const b of u.banco || []) {
    if (ids.has(b.id)) dup++;
    ids.add(b.id);
    if (b?.metadata?.generated_by) plantilla++;
    if (b.tipo === 'concepto') {
      const ok = Array.isArray(b.options) && b.options.length === 4 && b.options.includes(b.answer);
      if (!ok) mcMal++;
      for (const o of b.options || []) {
        if (o.length >= 180) larga++;
        if (susp(o)) trunc++;
      }
    }
  }
}

const total = us.reduce((a, u) => a + (u.banco?.length || 0), 0);
console.log(`fase-9: ${us.length} unidades, ${total} preguntas`);
console.log(`MC mal:${mcMal} dupIds:${dup} opcion>=180:${larga} truncadas:${trunc} plantilla:${plantilla}`);
if (mcMal || dup || larga || trunc || plantilla) {
  console.log('FALLA: corrige antes de commitear');
  process.exit(1);
}
console.log('OK');
