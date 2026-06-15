/**
 * markdown.js — Render mínimo de Markdown a HTML para las lecciones de
 * teoría del Modo Estudio (data/teoria/*.md). Sin librerías (convención
 * del proyecto): soporta lo que las lecciones usan y nada más.
 *
 * Soportado: #/##/### encabezados, párrafos, **negrita**, *cursiva*,
 * `código`, listas - y 1., > citas, --- separador y tablas con pipes.
 * Además: matemáticas $…$ (en línea) y $$…$$ (bloque), y enlaces [[slug]]:
 * los que apuntan a una unidad real (arena-xxx) se renderizan navegables
 * (.enlace-unidad, el click lo cablea js/study.js); el resto queda como chip
 * informativo (.enlace-concepto). El render de matemáticas es un traductor ligero LaTeX→Unicode
 * (sin librerías, convención del proyecto): legible, no tipográficamente
 * perfecto.
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

/* Símbolos LaTeX → Unicode usados por las lecciones (quant/estadística). */
const SIMBOLOS_TEX = {
  '\\cdot': '·', '\\times': '×', '\\div': '÷', '\\ast': '∗', '\\star': '⋆',
  '\\pm': '±', '\\mp': '∓', '\\leq': '≤', '\\le': '≤', '\\geq': '≥', '\\ge': '≥',
  '\\neq': '≠', '\\ne': '≠', '\\approx': '≈', '\\equiv': '≡', '\\cong': '≅',
  '\\sim': '∼', '\\propto': '∝', '\\infty': '∞', '\\to': '→', '\\rightarrow': '→',
  '\\leftarrow': '←', '\\Rightarrow': '⇒', '\\Leftarrow': '⇐', '\\Leftrightarrow': '⇔',
  '\\implies': '⟹', '\\iff': '⟺', '\\mapsto': '↦', '\\in': '∈', '\\notin': '∉',
  '\\ni': '∋', '\\subset': '⊂', '\\subseteq': '⊆', '\\supset': '⊃', '\\supseteq': '⊇',
  '\\cup': '∪', '\\cap': '∩', '\\setminus': '∖', '\\emptyset': '∅', '\\varnothing': '∅',
  '\\forall': '∀', '\\exists': '∃', '\\nexists': '∄', '\\neg': '¬', '\\land': '∧',
  '\\lor': '∨', '\\perp': '⊥', '\\parallel': '∥', '\\angle': '∠', '\\mid': '∣',
  '\\sum': '∑', '\\prod': '∏', '\\coprod': '∐', '\\int': '∫', '\\iint': '∬',
  '\\oint': '∮', '\\partial': '∂', '\\nabla': '∇', '\\Delta': 'Δ', '\\nabla': '∇',
  '\\cdots': '⋯', '\\ldots': '…', '\\dots': '…', '\\vdots': '⋮', '\\ddots': '⋱',
  '\\langle': '⟨', '\\rangle': '⟩', '\\lfloor': '⌊', '\\rfloor': '⌋',
  '\\lceil': '⌈', '\\rceil': '⌉', '\\prime': '′', '\\circ': '∘', '\\bullet': '•',
  '\\oplus': '⊕', '\\otimes': '⊗', '\\wedge': '∧', '\\vee': '∨', '\\top': '⊤', '\\bot': '⊥',
  // Letras griegas
  '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ', '\\epsilon': 'ε',
  '\\varepsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η', '\\theta': 'θ', '\\vartheta': 'ϑ',
  '\\iota': 'ι', '\\kappa': 'κ', '\\lambda': 'λ', '\\mu': 'μ', '\\nu': 'ν', '\\xi': 'ξ',
  '\\pi': 'π', '\\varpi': 'ϖ', '\\rho': 'ρ', '\\varrho': 'ϱ', '\\sigma': 'σ',
  '\\varsigma': 'ς', '\\tau': 'τ', '\\upsilon': 'υ', '\\phi': 'φ', '\\varphi': 'φ',
  '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
  '\\Gamma': 'Γ', '\\Theta': 'Θ', '\\Lambda': 'Λ', '\\Xi': 'Ξ', '\\Pi': 'Π',
  '\\Sigma': 'Σ', '\\Upsilon': 'Υ', '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω',
  // Espacios y adornos que se descartan
  '\\quad': ' ', '\\qquad': '  ', '\\,': ' ', '\\;': ' ', '\\:': ' ', '\\!': '',
};

/**
 * Traduce un fragmento LaTeX (ya escapado como HTML) a Unicode legible.
 * No pretende ser tipográficamente exacto: prioriza que la idea se lea sin
 * un libro al lado. El texto entra ya escapado, así que < > & son entidades
 * y se dejan intactas (se muestran correctamente).
 */
function texAUnicode(tex) {
  let r = tex;
  // Estructuras con argumentos {…} primero
  r = r.replace(/\\(?:text|mathrm|mathbf|mathbb|mathcal|operatorname|textbf|textit)\s*\{([^{}]*)\}/g, '$1');
  r = r.replace(/\\(?:hat|bar|overline|vec|tilde|widehat)\s*\{([^{}]*)\}/g, '$1');
  r = r.replace(/\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '($1)/($2)');
  r = r.replace(/\\sqrt\s*\{([^{}]*)\}/g, '√($1)');
  r = r.replace(/\\binom\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, 'C($1,$2)');
  r = r.replace(/\\left|\\right/g, '');
  // cases / matrices: quita solo los envoltorios, conserva el cuerpo.
  // \\ separa filas (→ ";"), & alinea (escapado como &amp; → espacio).
  r = r.replace(/\\begin\{array\}\s*\{[^{}]*\}/g, '');
  r = r.replace(/\\begin\{(?:cases|aligned|matrix|pmatrix|bmatrix|smallmatrix)\}/g, '');
  r = r.replace(/\\end\{(?:cases|array|aligned|matrix|pmatrix|bmatrix|smallmatrix)\}/g, '');
  r = r.replace(/\\\\/g, ';  ');
  r = r.replace(/&amp;/g, ' ');
  // Símbolos con nombre (más largos primero para evitar prefijos)
  Object.keys(SIMBOLOS_TEX)
    .sort((a, b) => b.length - a.length)
    .forEach((cmd) => { r = r.split(cmd).join(SIMBOLOS_TEX[cmd]); });
  // Superíndices y subíndices
  r = r.replace(/\^\{([^{}]*)\}/g, (_, g) => `<sup>${g}</sup>`);
  r = r.replace(/\^([A-Za-z0-9])/g, (_, g) => `<sup>${g}</sup>`);
  r = r.replace(/_\{([^{}]*)\}/g, (_, g) => `<sub>${g}</sub>`);
  r = r.replace(/_([A-Za-z0-9])/g, (_, g) => `<sub>${g}</sub>`);
  // Comandos restantes desconocidos: quita la barra, conserva el nombre
  r = r.replace(/\\([A-Za-z]+)/g, '$1');
  // Llaves sueltas de agrupación
  r = r.replace(/[{}]/g, '');
  return r;
}

/** Transforma negrita/cursiva/código/matemáticas/enlaces de una línea ya escapada. */
function inline(texto) {
  // Spans de código y matemáticas se protegen primero (token  i ) para que
  // sus * _ \ {} internos no los toque la negrita/cursiva. El token guarda el
  // HTML ya formado y se restaura verbatim al final.
  const tokens = [];
  const proteger = (html) => {
    tokens.push(html);
    return ` ${tokens.length - 1} `;
  };

  let s = texto.replace(/`([^`]+)`/g, (_, c) => proteger(`<code>${c}</code>`));
  // Matemáticas en bloque dentro de una línea: $$ … $$
  s = s.replace(/\$\$([^$]+)\$\$/g, (_, m) => proteger(`<span class="matematica">${texAUnicode(m)}</span>`));
  // Matemáticas en línea: $ … $ — el lookahead (?![0-9\s]) evita capturar
  // cantidades en dólares ($4M, $100), que el corpus usa con frecuencia.
  s = s.replace(/\$(?![0-9\s])([^$\n]+?)\$/g, (_, m) => proteger(`<span class="matematica">${texAUnicode(m)}</span>`));

  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  // Enlaces [[slug]] o [[slug|etiqueta]]. Los que apuntan a una unidad real
  // (arena-xxx) se vuelven navegables; el click lo cablea js/study.js. El resto
  // queda como chip informativo. Cuando no hay etiqueta explícita, data-auto="1"
  // pide a study.js que ponga el título real de la unidad como texto del enlace.
  s = s.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, slug, etq) => {
    const id = slug.trim();
    const label = (etq ?? slug).trim().replace(/-/g, ' ');
    if (/^arena-[a-z0-9]+$/i.test(id)) {
      const auto = etq ? '' : ' data-auto="1"';
      return `<a class="enlace-unidad" data-unidad="${id}"${auto} role="button" tabindex="0">${label}</a>`;
    }
    return `<span class="enlace-concepto" data-concepto="${id}">${label}</span>`;
  });

  s = s.replace(/ (\d+) /g, (_, i) => tokens[Number(i)]);
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

    // Ecuación en bloque: una línea que es solo $$ … $$ → centrada, sin <p>
    const eq = /^\$\$(.+)\$\$$/.exec(t);
    if (eq) {
      cerrarLista();
      cerrarCita();
      html.push(`<div class="ecuacion">${texAUnicode(eq[1])}</div>`);
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
