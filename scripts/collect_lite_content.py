#!/usr/bin/env python3
"""Rassemble les notebooks du vault dans content/ pour `jupyter lite build`.

Les notebooks vivent dans les dossiers de modules ("cours scripting python/N. <Titre>/...ipynb",
source de vérité, jamais modifiés ici) ; ce script les copie dans content/
en conservant l'arborescence relative à "cours scripting python/" (ex. "cours scripting python/2. Intro
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

Les solutions restent dans "cours scripting python/" entre marqueurs "#BEGIN" / "#END"
(exécutables et testées en local, cf. scripts/check_notebooks.py) ; à la
copie, le corps entre ces marqueurs est retiré et "#BEGIN" devient
"# TODO: Votre solution", et les sorties sont vidées. La version déployée
est donc un énoncé à trous.

Usage :
    uv run scripts/collect_lite_content.py
"""

import html
import json
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "cours scripting python"
CONTENT = RACINE / "content"

EXCLUS = (".git", "dist", "content", "node_modules", ".venv", ".obsidian", ".ipynb_checkpoints")

MARQUEUR = "indexedDB"

SOLUTION_DEBUT = "#BEGIN"
SOLUTION_FIN = "#END"
SOLUTION_TODO = "# TODO: Votre solution"


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


def retirer_solutions(nb: dict) -> bool:
    """Retire les corps entre "#BEGIN" / "#END" (cf. cours_algo/other/post_treatment.py).

    "#BEGIN" devient "# TODO: Votre solution", la ligne "#END" disparaît,
    les sorties sont vidées. Opère en place sur le dict notebook.
    Renvoie True si au moins une solution a été retirée.
    """
    retire = False
    for cellule in nb.get("cells", []):
        if cellule.get("cell_type") != "code":
            continue
        source = cellule.get("source", [])
        lignes = source if isinstance(source, list) else source.splitlines(keepends=True)
        traitees: list[str] = []
        dans_solution = False
        for ligne in lignes:
            if SOLUTION_DEBUT in ligne:
                dans_solution = True
                retire = True
                traitees.append(ligne.replace(SOLUTION_DEBUT, SOLUTION_TODO))
                continue
            if SOLUTION_FIN in ligne:
                dans_solution = False
                continue
            if not dans_solution:
                traitees.append(ligne)
        cellule["source"] = traitees
        cellule["outputs"] = []
        cellule["execution_count"] = None
    return retire


def collecter() -> None:
    for src in trouver_notebooks():
        rel = src.relative_to(SOURCE)
        dst = CONTENT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        cle = rel.as_posix()
        with open(dst, encoding="utf-8") as f:
            nb = json.load(f)
        sans_solutions = retirer_solutions(nb)
        nb["cells"] = [cellule_clear(cle)] + [
            c for c in nb.get("cells", []) if not est_cellule_clear(c)
        ]
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
        suffixe = " [+ clear cell]"
        if sans_solutions:
            suffixe += " [+ solutions retirées]"
        print(f"{rel} -> content/{rel}{suffixe}")


def main() -> int:
    if not SOURCE.is_dir():
        print(f"dossier source introuvable : {SOURCE}", file=sys.stderr)
        return 1
    shutil.rmtree(CONTENT, ignore_errors=True)
    CONTENT.mkdir(parents=True, exist_ok=True)
    collecter()
    return 0


if __name__ == "__main__":
    sys.exit(main())
