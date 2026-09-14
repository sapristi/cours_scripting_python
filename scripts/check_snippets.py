#!/usr/bin/env python3
"""Vérifie la syntaxe des snippets Python dans les fichiers Markdown du cours.

Extrait les blocs ```python et les valide avec ast.parse.
Les blocs REPL (contenant >>>) sont ignorés.

Usage :
    python3 scripts/check_snippets.py [CHEMIN ...]
    python3 scripts/check_snippets.py "2. Intro python.md"
    python3 scripts/check_snippets.py .          # tout le vault (défaut)

Sortie : 0 si tout est OK, 1 si au moins un bloc est en erreur.
"""

import argparse
import ast
import re
import sys
from pathlib import Path

# ```python ou ```py, éventuellement préfixé par "> " (callout Obsidian).
FENCE_RE = re.compile(r"^[ \t]*(?:>\s*)*```(python|py)\s*$", re.MULTILINE)


def extraire_blocs(texte: str) -> list[str]:
    """Renvoie le contenu brut de chaque bloc python du markdown."""
    blocs: list[str] = []
    lignes = texte.splitlines()
    dans_bloc = False
    courant: list[str] = []
    for ligne in lignes:
        if not dans_bloc and FENCE_RE.match(ligne):
            dans_bloc = True
            courant = []
        elif dans_bloc and ligne.strip().lstrip(">").strip() == "```":
            dans_bloc = False
            blocs.append("\n".join(courant))
        elif dans_bloc:
            # Retire le préfixe de callout "> " si présent.
            nettoyee = re.sub(r"^[ \t]*>[ \t]?", "", ligne)
            courant.append(nettoyee)
    return blocs


def est_repl(code: str) -> bool:
    """Détecte un exemple de session interactive (>>>)."""
    return any(l.strip().startswith(">>>") for l in code.splitlines())


def verifier_fichier(chemin: Path) -> list[str]:
    """Vérifie un fichier .md. Renvoie la liste des erreurs trouvées."""
    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as e:
        return [f"{chemin}: illisible ({e})"]
    erreurs: list[str] = []
    for i, bloc in enumerate(extraire_blocs(texte)):
        if est_repl(bloc):
            continue
        try:
            ast.parse(bloc)
        except SyntaxError as e:
            erreurs.append(f"{chemin} [bloc {i}] : SyntaxError ligne {e.lineno} : {e.msg}")
    return erreurs


def collecter_md(cibles: list[str]) -> list[Path]:
    """Résout les cibles (fichiers ou dossiers) en liste de .md."""
    fichiers: list[Path] = []
    for cible in cibles:
        p = Path(cible)
        if p.is_dir():
            fichiers.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            fichiers.append(p)
        else:
            print(f"cible introuvable : {cible}", file=sys.stderr)
    # Exclut le workspace Obsidian.
    return [f for f in fichiers if ".obsidian" not in f.parts]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chemins", nargs="*", default=["."], help="fichiers ou dossiers à vérifier")
    args = parser.parse_args()

    fichiers = collecter_md(args.chemins)
    if not fichiers:
        print("aucun fichier .md trouvé.")
        return 1

    total_blocs = 0
    erreurs: list[str] = []
    for f in fichiers:
        try:
            total_blocs += len(extraire_blocs(f.read_text(encoding="utf-8")))
        except OSError:
            pass
        erreurs.extend(verifier_fichier(f))

    print(f"{len(fichiers)} fichier(s), {total_blocs} bloc(s) python vérifié(s).")
    if erreurs:
        print(f"{len(erreurs)} erreur(s) :")
        for e in erreurs:
            print(f"  - {e}")
        return 1
    print("OK : aucune erreur de syntaxe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
