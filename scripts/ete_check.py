#!/usr/bin/env python3
"""Verificador del Español Técnico Controlado (ETC).

Dos usos:
  ete_check.py texto.md [--max-words 20]   Revisa un texto y lista avisos.
  ete_check.py --validate                  Valida el diccionario y sus ejemplos.

Es una ayuda heurística, no un analizador gramatical. Detecta:
  - palabras de la lista «evitar» del diccionario (con su alternativa aprobada),
  - frases demasiado largas,
  - gerundios.
Salida: 0 si no hay avisos o si no se usa --strict; 1 si hay avisos y se usa --strict.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "skills" / "espanol-tecnico-controlado" / "references" / "diccionario.psv"

GERUND_RE = re.compile(r"\b[a-záéíóúñü]+(?:ando|iendo|yendo|endo)\b", re.IGNORECASE)
GERUND_EXCEPTIONS = {
    "cuando", "comando", "mando", "blando", "demando", "quando",
    "estupendo", "tremendo", "horrendo", "dividendo", "reverendo",
    "fernando", "orlando", "bolando", "mendo", "agenda",
}
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü0-9]+(?:[-'][A-Za-zÁÉÍÓÚÑÜáéíóúñü0-9]+)*")

AR = ["ar", "as", "a", "amos", "an", "e", "es", "en", "ando", "ado", "ada", "ados", "adas",
      "aba", "aban", "aron", "ó", "é", "arse", "ándose"]
ER = ["er", "es", "e", "emos", "en", "iendo", "ido", "ida", "idos", "idas", "ía", "ían",
      "ió", "ieron", "a", "as", "an", "erse"]
IR = ["ir", "es", "e", "imos", "en", "iendo", "ido", "ida", "idos", "idas", "ía", "ían",
      "ió", "ieron", "a", "as", "an", "irse"]


class Entry:
    def __init__(self, word, cat, sense, avoid, example, line):
        self.word, self.cat, self.sense = word, cat, sense
        self.avoid_raw = avoid
        self.example = example
        self.line = line
        self.avoid = [a.strip() for a in avoid.split(";") if a.strip()]


def load_dictionary(path=DICT_PATH):
    entries = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) != 5:
            raise ValueError(f"{path.name}:{n}: se esperaban 5 columnas y hay {len(parts)}")
        entries.append(Entry(*parts, line=n))
    return entries


def verb_forms(infinitive):
    # Se omite la forma en «-o» (yo): casi siempre coincide con un nombre o un adjetivo.
    inf = infinitive.lower()
    if inf.endswith("ar"):
        endings, stem = AR, inf[:-2]
    elif inf.endswith("er"):
        endings, stem = ER, inf[:-2]
    elif inf.endswith("ir"):
        endings, stem = IR, inf[:-2]
    else:
        return {inf}
    return {stem + e for e in endings}


def build_patterns(entries):
    """Devuelve una lista de (regex, texto_evitado, palabra_aprobada)."""
    patterns = []
    for e in entries:
        for a in e.avoid:
            if a.endswith("(v)"):
                forms = verb_forms(a[:-3])
                rx = r"\b(?:" + "|".join(sorted(map(re.escape, forms), key=len, reverse=True)) + r")\b"
                patterns.append((re.compile(rx, re.IGNORECASE), a[:-3], e.word))
            elif a.endswith("*"):
                patterns.append((re.compile(r"\b" + re.escape(a[:-1]) + r"\w*", re.IGNORECASE), a, e.word))
            else:
                rx = r"\b" + r"\s+".join(re.escape(w) for w in a.split()) + r"\b"
                patterns.append((re.compile(rx, re.IGNORECASE), a, e.word))
    return patterns


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    return re.sub(r"`[^`]*`", " ", text)


def split_sentences(text):
    text = strip_code(text)
    parts = re.split(r"(?<=[.!?¿¡:;])\s+|\n+", text)
    return [p.strip() for p in parts if p.strip()]


def check_text(text, patterns, max_words=20):
    findings = []
    for s in split_sentences(text):
        words = WORD_RE.findall(s)
        if len(words) > max_words:
            findings.append(("longitud", f"{len(words)} palabras (máximo {max_words}): «{s[:70]}…»"))
        for rx, avoided, approved in patterns:
            if rx.search(s):
                findings.append(("evitar", f"«{avoided}» → usa «{approved}» en: «{s[:70]}»"))
        for m in GERUND_RE.finditer(s):
            if m.group(0).lower() not in GERUND_EXCEPTIONS:
                findings.append(("gerundio", f"«{m.group(0)}» en: «{s[:70]}»"))
    return findings


def validate(entries):
    errors = []
    seen = {}
    approved_words = {e.word.lower() for e in entries}
    patterns = build_patterns(entries)
    for e in entries:
        key = (e.word.lower(), e.cat)
        if e.word.lower() in seen:
            errors.append(f"línea {e.line}: palabra repetida «{e.word}» (también en línea {seen[e.word.lower()]})")
        seen[e.word.lower()] = e.line
        if e.cat not in {"V", "N", "ADJ", "ADV", "FUNC"}:
            errors.append(f"línea {e.line}: categoría no válida «{e.cat}»")
        if not e.sense:
            errors.append(f"línea {e.line}: «{e.word}» no tiene sentido definido")
        if not e.example:
            errors.append(f"línea {e.line}: «{e.word}» no tiene ejemplo")
        if not e.avoid:
            errors.append(f"línea {e.line}: «{e.word}» no tiene alternativas a evitar")
        # Una palabra aprobada no puede estar prohibida en otra entrada.
        for a in e.avoid:
            plain = a[:-3] if a.endswith("(v)") else a.rstrip("*")
            if plain.lower() in approved_words and plain.lower() != e.word.lower():
                errors.append(f"línea {e.line}: «{plain}» está en «evitar» pero es palabra aprobada")
        # El ejemplo debe cumplir las reglas del propio estándar.
        for kind, msg in check_text(e.example, patterns):
            errors.append(f"línea {e.line} (ejemplo de «{e.word}»): {kind}: {msg}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="texto a revisar (usa - para stdin)")
    ap.add_argument("--max-words", type=int, default=20)
    ap.add_argument("--validate", action="store_true", help="valida el diccionario y sus ejemplos")
    ap.add_argument("--strict", action="store_true", help="devuelve 1 si hay avisos")
    args = ap.parse_args()

    entries = load_dictionary()
    if args.validate:
        errs = validate(entries)
        for e in errs:
            print("ERROR", e)
        print(f"{len(entries)} entradas; {len(errs)} errores.")
        return 1 if errs else 0

    if not args.file:
        ap.error("indica un archivo o usa --validate")
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    findings = check_text(text, build_patterns(entries), args.max_words)
    for kind, msg in findings:
        print(f"[{kind}] {msg}")
    print(f"{len(findings)} avisos.")
    return 1 if (findings and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
