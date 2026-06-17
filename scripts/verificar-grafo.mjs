import { readFileSync, readdirSync } from 'node:fs';

const study = JSON.parse(readFileSync('data/study.json', 'utf8'));
const unitIds = new Set(study.unidades.map((u) => u.id));
const clusterUnits = {};

for (const t of ['entrevista', 'ciberseguridad', 'genai']) {
  const tax = JSON.parse(readFileSync(`data/${t}/_taxonomia.json`, 'utf8'));
  for (const c of tax.clusters || []) clusterUnits[c.id] = c.unidades || [];
}

const parent = {};
const find = (x) => (parent[x] === x ? x : (parent[x] = find(parent[x])));
const union = (a, b) => {
  parent[find(a)] = find(b);
};

for (const id of unitIds) parent[id] = id;
const deg = Object.fromEntries([...unitIds].map((id) => [id, 0]));

for (const id of unitIds) {
  const f = `data/teoria/${id}.md`;
  let txt = '';
  try {
    txt = readFileSync(f, 'utf8');
  } catch {
    continue;
  }
  for (const m of txt.matchAll(/\[\[([^\]]+)\]\]/g)) {
    const t = m[1].split('|')[0].trim();
    const targets = unitIds.has(t) ? [t] : clusterUnits[t] || [];
    for (const tt of targets) {
      if (tt !== id && unitIds.has(tt)) {
        union(id, tt);
        deg[id]++;
        deg[tt]++;
      }
    }
  }
}

const comps = new Set([...unitIds].map(find));
const aislados = [...unitIds].filter((id) => deg[id] === 0);
const sizes = {};
for (const id of unitIds) sizes[find(id)] = (sizes[find(id)] || 0) + 1;

console.log(`componentes: ${comps.size} | aislados: ${aislados.length} | mayor: ${Math.max(...Object.values(sizes))}/${unitIds.size}`);
if (aislados.length) console.log('aislados:', aislados.join(', '));
if (comps.size > 1 || aislados.length) {
  console.log('FALLA: el grafo no es conexo');
  process.exit(1);
}
console.log('OK: grafo conexo');
