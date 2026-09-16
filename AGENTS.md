# AGENTS.md — scripting_python (cours)

Contenu pédagogique en français : scripting Python pour la cybersécurité (3e année). 
Obsidian vault, pas un projet code.

## Structure

- `cours scripting python/` = vault Obsidian (à ouvrir comme vault ; workspace dans `cours scripting python/.obsidian/`).
- `cours scripting python/Entrypoint.md` : objectifs + plan.
- `cours scripting python/N. <Titre>.md` = un module de cours. Frontmatter requis : `durée (h)` (nombre) + `Contexte` (texte, source du plan).
- `cours scripting python/N. <Titre>/` (même nom que le `.md`) = assets du module (slides, images, notebooks `.ipynb`, futurs énoncés/TP).
- `cours scripting python/Cours.base` = config Bases/Dataview du tableau de bord (`file.folder == "/"`, `file.ext == "md"`, `/` = racine du vault `cours scripting python/`). Ne pas éditer comme du contenu.
- Images : `![[Pasted image ....png|largeur]]` (embed Obsidian + resize). Stocker dans chaque dossier correspondant.
- Slides : source `.typ` (Typst), compilée en `.pdf` à côté. Éditer le `.typ`, jamais le `.pdf` directement ; recompiler : `typst compile "<fichier>.typ"`.

## Conventions Obsidian

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Ne pas toucher à `cours scripting python/.obsidian/` (workspace, `graph.json`, `types.json`, plugins : `auto-numbered-headings`, `floating-headings`, `heading-level-indent`).
- Rédiger en français. Vocabulaire suggéré du module 1 : CIA, AAA, vulnérabilité/exploit/payload/IOC/TTP, Kill Chain, Red/Blue team.

## Garde-fou contenu

- Tout exemple offensif (scan `socket`, brute-force `requests`/`paramiko`, injection) doit rappeler : **labo isolé uniquement, autorisation écrite, art. 323-1 Code pénal**. Ne jamais proposer de cible réelle.
- Libs de référence du cours : `socket`, `requests`, `hashlib`, `re`, `paramiko`, `pandas` (module 7).

## Scripts

- `scripts/check_snippets.py` : syntaxe des snippets Python des `.md` (`ast.parse`, REPL `>>>` ignorés). Usage : `python3 scripts/check_snippets.py [CHEMIN ...]` (défaut : `cours scripting python/`). À lancer avant de considérer un module comme terminé.
- `scripts/check_notebooks.py` : exécute les notebooks de `cours scripting python/` avec le noyau local (`uv run scripts/check_notebooks.py [CHEMIN ...]`, défaut : `cours scripting python/`). Les notebooks source contiennent les solutions ; sortie 0 si tout passe. À lancer après toute modification d'un notebook.
- `scripts/collect_lite_content.py` : copie les notebooks de `cours scripting python/` vers `content/` (staging gitignoré pour `jupyter lite build`, CI + `scripts/preview_lite.py`). Ne jamais éditer les copies dans `content/`. À la copie : retire les solutions entre `#BEGIN` / `#END` (`#BEGIN` → `# TODO: Votre solution`, sorties vidées) et injecte la cellule "Clear notebook" en première position.
