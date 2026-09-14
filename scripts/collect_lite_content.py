#!/usr/bin/env python3
"""Rassemble les notebooks du vault dans content/ pour `jupyter lite build`.

Les notebooks vivent dans les dossiers de modules ("source/N. <Titre>/...ipynb",
source de vérité, jamais modifiés ici) ; ce script les copie dans content/
en conservant l'arborescence relative à source/ (ex. "source/2. Intro
python/exercices.ipynb" devient "content/2. Intro python/exercices.ipynb"),
pour les retrouver sous leur dossier dans JupyterLite.

À la copie, chaque notebook reçoit en première cellule un bouton "Clear
notebook ..." qui efface son état du stockage local du navigateur
(toutes les bases IndexedDB dont le nom contient "JupyterLite Storage",
tables "checkpoints" et "files") : sans
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
SOURCE = RACINE / "source"
CONTENT = RACINE / "content"

EXCLUS = (".git", "dist", "content", "node_modules", ".venv", ".obsidian", ".ipynb_checkpoints")

MARQUEUR = "indexedDB"


def est_exclu(chemin: Path) -> bool:
    return any(part in EXCLUS for part in chemin.parts)


def trouver_notebooks() -> list[Path]:
    return sorted(
        p
        for p in SOURCE.rglob("*.ipynb")
        if not est_exclu(p.relative_to(SOURCE))
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
        "        function clearFrom(dbName) {"
        "            let req;"
        "            try { req = window.indexedDB.open(dbName); }"
        '            catch (err) { console.warn("Skipping " + dbName + ": " + err); return; }'
        "            req.onerror = function(ev) {"
        '                console.warn("Cannot open " + dbName + ": " + (ev.target.error || ev));'
        "            };"
        "            req.onsuccess = function(e) {"
        "                let db = e.target.result;"
        '                for (let tablename of ["checkpoints", "files"]) {'
        "                    try {"
        "                        if (!db.objectStoreNames.contains(tablename)) continue;"
        '                        let t = db.transaction(tablename, "readwrite");'
        "                        t.onerror = function(ev) {};"
        f"                    let del; try {{ del = t.objectStore(tablename).delete('{jk}'); }} catch (err) {{ continue; }}"
        "                        del.onerror = function(ev) {};"
        "                        del.onsuccess = function(ev) {"
        f'                            console.log("Deleted {jk} state in " + dbName + "/" + tablename + " (" + ev.target.result + ")");'
        "                        };"
        "                    }"
        '                    catch (err) { console.warn("Skipping " + dbName + "/" + tablename + ": " + err); }'
        "                }"
        "            };"
        "        };"
        "        if (window.indexedDB.databases) {"
        "            window.indexedDB.databases().then(dbs => {"
        "                let names = dbs.map(d => d.name).filter(n => n && n.includes('JupyterLite Storage'));"
        "                if (!names.length) names = ['JupyterLite Storage'];"
        "                names.forEach(clearFrom);"
        "            });"
        "        } else {"
        "            clearFrom('JupyterLite Storage');"
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
        rel = src.relative_to(SOURCE)
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
