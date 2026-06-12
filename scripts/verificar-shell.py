#!/usr/bin/env python3
"""
verificar-shell.py — Verifica la integridad del shell de CogitoErgoSum.

Comprueba:
  1. Todos los archivos del array SHELL de sw.js existen en disco.
  2. Todos los archivos .json del SHELL son JSON válido.
  3. Los IDs de elementos HTML en index.html son únicos.

Uso:
  python3 scripts/verificar-shell.py

Salida: "OK — N archivos" si todo está bien; lista de errores y exit 1 si no.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def verificar_shell():
    sw_path = os.path.join(ROOT, 'sw.js')
    with open(sw_path, encoding='utf-8') as f:
        sw = f.read()

    m = re.search(r'const SHELL\s*=\s*\[(.*?)\];', sw, re.DOTALL)
    if not m:
        return ["ERROR: no se encontró el array SHELL en sw.js"]

    archivos = re.findall(r"'([^']+)'", m.group(1))
    errores = []

    for ruta in archivos:
        full = os.path.join(ROOT, ruta.lstrip('./'))
        if not os.path.exists(full):
            errores.append(f"FALTA:        {ruta}")
            continue
        if ruta.endswith('.json'):
            try:
                with open(full, encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                errores.append(f"JSON inválido: {ruta}  →  {e}")

    return errores, len(archivos)


def verificar_ids_html():
    html_path = os.path.join(ROOT, 'index.html')
    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
    vistos = {}
    duplicados = []
    for id_ in ids:
        vistos[id_] = vistos.get(id_, 0) + 1
    for id_, n in vistos.items():
        if n > 1:
            duplicados.append(f"ID duplicado ({n}×): #{id_}")

    return duplicados


def main():
    resultado = verificar_shell()
    if isinstance(resultado, list):
        # Sólo errores, sin cuenta
        errores_shell = resultado
        n_shell = 0
    else:
        errores_shell, n_shell = resultado

    errores_html = verificar_ids_html()
    todos = errores_shell + errores_html

    if todos:
        print('\n'.join(todos))
        sys.exit(1)
    else:
        print(f"OK — {n_shell} archivos del shell verificados, sin IDs duplicados en index.html.")


if __name__ == '__main__':
    main()
