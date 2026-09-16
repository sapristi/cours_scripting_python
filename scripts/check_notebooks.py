#!/usr/bin/env python3
"""Exécute les notebooks du vault pour vérifier que solutions + tests passent.

Les notebooks source (dans source/) contiennent les solutions entre marqueurs
"#BEGIN" / "#END" ; ce script les exécute de haut en bas avec le noyau Python
local et échoue dès qu'une cellule lève (assert, exception...). À lancer après
toute modification d'un notebook, avant de considérer un module comme terminé.
La version déployée (content/, cf. scripts/collect_lite_content.py) a les
solutions retirées : elle n'est PAS exécutable, c'est normal.

Usage :
    uv run scripts/check_notebooks.py [CHEMIN ...]
    uv run scripts/check_notebooks.py "source/2. Intro python/exercices.ipynb"
    uv run scripts/check_notebooks.py source      # tout le vault (défaut)

Sortie : 0 si tous les notebooks s'exécutent sans erreur, 1 sinon.
"""

import argparse
import sys
import traceback
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
EXCLUS = (".git", "dist", "content", "node_modules", ".venv", ".obsidian", ".ipynb_checkpoints")


def est_exclu(chemin: Path) -> bool:
    return any(part in EXCLUS for part in chemin.parts)


def collecter_notebooks(cibles: list[str]) -> list[Path]:
    trouves: list[Path] = []
    for cible in cibles:
        p = Path(cible)
        if not p.is_absolute():
            p = RACINE / p
        if p.is_dir():
            trouves.extend(sorted(p.rglob("*.ipynb")))
        elif p.is_file():
            trouves.append(p)
        else:
            print(f"cible introuvable : {cible}", file=sys.stderr)
    return sorted(
        p
        for p in trouves
        if p.suffix == ".ipynb"
        and "checkpoint" not in p.name
        and not est_exclu(p.relative_to(RACINE) if p.is_relative_to(RACINE) else p)
    )


def executer(notebook: Path, timeout: int, kernel: str) -> tuple[bool, str]:
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        return False, "nbclient/nbformat manquant (uv sync requis)"
    try:
        nb = nbformat.read(str(notebook), as_version=4)
        client = NotebookClient(nb, timeout=timeout, kernel_name=kernel)
        client.execute()
    except Exception as e:  # noqa: BLE001 — on veut le message, pas le type
        details = "".join(traceback.format_exception_only(e))[:2000]
        return False, details.strip()
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chemins", nargs="*", default=["source"], help="fichiers ou dossiers à exécuter")
    parser.add_argument("--timeout", type=int, default=120, help="timeout par cellule (s)")
    parser.add_argument("--kernel", default="python3", help="noyau Jupyter à utiliser")
    args = parser.parse_args()

    notebooks = collecter_notebooks(args.chemins)
    if not notebooks:
        print("aucun notebook trouvé.")
        return 1

    echecs = 0
    for nb in notebooks:
        try:
            rel = nb.relative_to(RACINE)
        except ValueError:
            rel = nb
        print(f"exécution {rel} ...", flush=True)
        ok, details = executer(nb, args.timeout, args.kernel)
        if ok:
            print(f"  OK : {rel}")
        else:
            echecs += 1
            print(f"  ÉCHEC : {rel}\n{details}")

    print(f"{len(notebooks)} notebook(s) vérifié(s), {echecs} échec(s).")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
