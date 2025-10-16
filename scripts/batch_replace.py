#!/usr/bin/env python3
import argparse, re, sys, difflib
from pathlib import Path

rx_backslash_lt = re.compile(r'\\<')
rx_backslash_gt = re.compile(r'\\>')
rx_br = re.compile(r'<br\s*/?>', re.IGNORECASE)
rx_backslash_dot = re.compile(r'\\\.')  # correspond à "\."

def transform(text: str) -> str:
    text = rx_backslash_lt.sub('<', text)
    text = rx_backslash_gt.sub('>', text)
    text = rx_backslash_dot.sub('.', text) 
    text = rx_br.sub('', text)
    return text

def main():
    ap = argparse.ArgumentParser(description="Remplacements sur un seul fichier.")
    ap.add_argument("file", help="Chemin du fichier à traiter")
    ap.add_argument("--dry-run", action="store_true", help="N'écrit pas, affiche un diff")
    ap.add_argument("--backup", action="store_true", help="Crée une sauvegarde .bak avant écriture")
    args = ap.parse_args()

    p = Path(args.file)
    if not p.is_file():
        print(f"Erreur: fichier introuvable: {p}", file=sys.stderr)
        sys.exit(2)

    # Lecture UTF-8 (tolérante)
    try:
        original = p.read_text(encoding="utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        original = p.read_text(encoding="latin-1")
        encoding = "latin-1"

    updated = transform(original)

    if updated == original:
        print("Aucun changement.")
        return

    if args.dry_run:
        print(f"--- {p}")
        print(f"+++ {p} (après)")
        diff = difflib.unified_diff(
            original.splitlines(keepends=False),
            updated.splitlines(keepends=False),
            fromfile=str(p),
            tofile=str(p) + " (après)",
            lineterm=""
        )
        for line in diff:
            print(line)
        return

    if args.backup:
        p.with_suffix(p.suffix + ".bak").write_text(original, encoding=encoding)

    p.write_text(updated, encoding=encoding)
    print(f"OK: écrit {p} (encodage {encoding})")

if __name__ == "__main__":
    main()
