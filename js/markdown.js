/**
 * markdown.js — Render mínimo de Markdown a HTML para las lecciones de
 * teoría del Modo Estudio (data/teoria/*.md). Sin librerías (convención
 * del proyecto): soporta lo que las lecciones usan y nada más.
 *
 * Soportado: #/##/### encabezados, párrafos, **negrita**, *cursiva*,
 * `código`, listas - y 1., > citas, --- separador y tablas con pipes.
 * Todo el texto se escapa ANTES de transformar: una lección jamás puede
 * inyectar HTML.
 */

function escapar(texto) {
  return texto
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

/** Transforma negrita/cursiva/código de una línea ya escapada. */
function inline(texto) {
  // Los spans de código se protegen primero para que * y _ internos no se toquen
  const codigos = [];
  let s = texto.replace(/`([^`]+)`/g, (_, c) => {
    codigos.push(c);
    return `\u0000${codigos.length - 1}\u0000`;
  });
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  s = s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codigos[Number(i)]}</code>`);
  return s;
}

function esFilaTabla(linea) {
  return /^\s*\|.*\|\s*$/.test(linea);
}

function celdas(linea) {
  return linea.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

/**
 * Convierte un texto Markdown en HTML seguro (string).
 * @param {string} md
 * @returns {string}
 */
export function renderMarkdown(md) {
  const lineas = escapar(md ?? '').split('\n');
  const html = [];
  let lista = null;       // 'ul' | 'ol' | null
  let enCita = false;

  const cerrarLista = () => {
    if (lista) {
      html.push(`</${lista}>`);
      lista = null;
    }
  };
  const cerrarCita = () => {
    if (enCita) {
      html.push('</blockquote>');
      enCita = false;
    }
  };

  for (let i = 0; i < lineas.length; i++) {
    const linea = lineas[i];
    const t = linea.trim();

    if (!t) {
      cerrarLista();
      cerrarCita();
      continue;
    }

    // Tabla: fila | celda | celda | seguida de la fila separadora |---|---|
    if (esFilaTabla(linea) && esFilaTabla(lineas[i + 1] ?? '') && /^[\s|:-]+$/.test(lineas[i + 1])) {
      cerrarLista();
      cerrarCita();
      const cab = celdas(linea);
      html.push('<table><thead><tr>');
      cab.forEach((c) => html.push(`<th>${inline(c)}</th>`));
      html.push('</tr></thead><tbody>');
      i += 1; // salta la fila separadora
      while (esFilaTabla(lineas[i + 1] ?? '')) {
        i += 1;
        html.push('<tr>');
        celdas(lineas[i]).forEach((c) => html.push(`<td>${inline(c)}</td>`));
        html.push('</tr>');
      }
      html.push('</tbody></table>');
      continue;
    }

    const h = /^(#{1,4})\s+(.*)$/.exec(t);
    if (h) {
      cerrarLista();
      cerrarCita();
      const nivel = h[1].length;
      html.push(`<h${nivel}>${inline(h[2])}</h${nivel}>`);
      continue;
    }

    if (/^---+$/.test(t)) {
      cerrarLista();
      cerrarCita();
      html.push('<hr />');
      continue;
    }

    if (t.startsWith('&gt;')) {
      cerrarLista();
      if (!enCita) {
        html.push('<blockquote>');
        enCita = true;
      }
      html.push(`<p>${inline(t.replace(/^&gt;\s?/, ''))}</p>`);
      continue;
    }

    const li = /^[-*]\s+(.*)$/.exec(t);
    const liNum = /^\d+[.)]\s+(.*)$/.exec(t);
    if (li || liNum) {
      cerrarCita();
      const tipo = li ? 'ul' : 'ol';
      if (lista !== tipo) {
        cerrarLista();
        html.push(`<${tipo}>`);
        lista = tipo;
      }
      html.push(`<li>${inline((li ?? liNum)[1])}</li>`);
      continue;
    }

    cerrarLista();
    cerrarCita();
    html.push(`<p>${inline(t)}</p>`);
  }
  cerrarLista();
  cerrarCita();
  return html.join('\n');
}
