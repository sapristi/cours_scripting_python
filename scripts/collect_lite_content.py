#!/usr/bin/env python3
"""Rassemble les notebooks du vault dans content/ pour `jupyter lite build`.

Les notebooks vivent dans les dossiers de modules ("N. <Titre>/...ipynb",
source de vérité, jamais modifiés ici) ; ce script les copie dans content/
en conservant l'arborescence (ex. "2. Intro python/exercices.ipynb" reste
sous "2. Intro python/"), pour les retrouver sous leur dossier dans
JupyterLite.

À la copie, chaque notebook reçoit en première cellule un bouton "Clear
notebook ..." qui efface son état du stockage local du navigateur
(IndexedDB "JupyterLite Storage", tables "checkpoints" et "files") : sans
ça, un élève qui rouvre le site retrouve son ancienne version au lieu de
celle publiée. La clé effacée est le chemin du notebook dans le site
(ex. "2. Intro python/exercices.ipynb"). Si le notebook source contient
déjà une telle cellule (détectée via "indexedDB", ex. clé codée en dur
"ESGI_1A/..."), elle est remplacée par la version à la bonne clé.

Usage :
    uv run scripts/collect_lite_content.py
"""

import html
import json
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CONTENT = RACINE / "content"

EXCLUS = (".git", "dist", "content", "node_modules", ".venv", ".ipynb_checkpoints")

MARQUEUR = "indexedDB"


def est_exclu(chemin: Path) -> bool:
    return any(part in EXCLUS for part in chemin.parts)


def trouver_notebooks() -> list[Path]:
    return sorted(
        p
        for p in RACINE.rglob("*.ipynb")
        if not est_exclu(p.relative_to(RACINE))
        and "checkpoint" not in p.name
    )


def cle_js(cle: str) -> str:
    return cle.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')


def cellule_clear(cle: str) -> dict:
    """Première cellule : bouton qui purge l'état du notebook dans IndexedDB."""
    libelle = html.escape(f"Clear notebook {cle}")
    jk = cle_js(cle)
    source = (
        "from IPython.display import display, HTML\n"
        f'display(HTML("""<button type="button" id="button_for_indexeddb">{libelle}</button>'
        "    <script>"
        "    window.button_for_indexeddb.onclick = function(e) {"
        "        window.indexedDB.open('JupyterLite Storage').onsuccess = function(e) {"
        '            let tables = ["checkpoints", "files"];'
        '            let t = e.target.result.transaction(tables, "readwrite");'
        "            function clearNotenook(tablename) {"
        f"                t.objectStore(tablename).delete('{jk}').onsuccess = function(e) {{"
        f'                    console.log("Deleted {jk} state in " + tablename + " (" + e.target.result + ")");'
        "                }"
        "            }"
        "            for (let tablename of tables) {"
        "                clearNotenook(tablename);"
        "            }"
        "        }"
        "    };"
        '    </script>"""))'
    )
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "clear-local-storage",
        "metadata": {},
        "outputs": [],
        "source": [source],
    }


def est_cellule_clear(cellule: dict) -> bool:
    if cellule.get("cell_type") != "code":
        return False
    return MARQUEUR in "".join(cellule.get("source", []))


def collecter() -> None:
    for src in trouver_notebooks():
        rel = src.relative_to(RACINE)
        dst = CONTENT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        cle = rel.as_posix()
        with open(dst, encoding="utf-8") as f:
            nb = json.load(f)
        nb["cells"] = [cellule_clear(cle)] + [
            c for c in nb.get("cells", []) if not est_cellule_clear(c)
        ]
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"{rel} -> content/{rel} [+ clear cell]")


def main() -> int:
    shutil.rmtree(CONTENT, ignore_errors=True)
    CONTENT.mkdir(parents=True, exist_ok=True)
    collecter()
    return 0


if __name__ == "__main__":
    sys.exit(main())
