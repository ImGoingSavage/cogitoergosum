import { readFileSync, readdirSync } from 'node:fs';

const study = JSON.parse(readFileSync('data/study.json', 'utf8'));
const valid = new Set(study.unidades.map((u) => u.id));

for (const t of ['entrevista', 'ciberseguridad', 'genai']) {
  const tax = JSON.parse(readFileSync(`data/${t}/_taxonomia.json`, 'utf8'));
  for (const c of tax.clusters || []) valid.add(c.id);
}

let rotos = 0;
for (const f of readdirSync('data/teoria').filter((file) => file.endsWith('.md'))) {
  const txt = readFileSync(`data/teoria/${f}`, 'utf8');
  for (const m of txt.matchAll(/\[\[([^\]]+)\]\]/g)) {
    const target = m[1].split('|')[0].trim();
    if (!valid.has(target)) {
      console.log(`ROTO: ${f} -> [[${target}]]`);
      rotos++;
    }
  }
}

console.log(rotos ? `FALLA: ${rotos} enlaces rotos` : 'OK: 0 enlaces rotos');
if (rotos) process.exit(1);
