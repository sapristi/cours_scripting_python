# AGENTS.md — scripting_python (cours)

Contenu pédagogique en français : scripting Python pour la cybersécurité (3e année). 
Obsidian vault, pas un projet code.

## Structure

- `source/` = vault Obsidian (à ouvrir comme vault ; workspace dans `source/.obsidian/`).
- `source/Entrypoint.md` : objectifs + plan.
- `source/N. <Titre>.md` = un module de cours. Frontmatter requis : `durée (h)` (nombre) + `Contexte` (texte, source du plan).
- `source/N. <Titre>/` (même nom que le `.md`) = assets du module (slides, images, notebooks `.ipynb`, futurs énoncés/TP).
- `source/Cours.base` = config Bases/Dataview du tableau de bord (`file.folder == "/"`, `file.ext == "md"`, `/` = racine du vault `source/`). Ne pas éditer comme du contenu.
- Images : `![[Pasted image ....png|largeur]]` (embed Obsidian + resize). Stocker dans chaque dossier correspondant.
- Slides : source `.typ` (Typst), compilée en `.pdf` à côté. Éditer le `.typ`, jamais le `.pdf` directement ; recompiler : `typst compile "<fichier>.typ"`.

## Conventions Obsidian

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Ne pas toucher à `source/.obsidian/` (workspace, `graph.json`, `types.json`, plugins : `auto-numbered-headings`, `floating-headings`, `heading-level-indent`).
- Rédiger en français. Vocabulaire suggéré du module 1 : CIA, AAA, vulnérabilité/exploit/payload/IOC/TTP, Kill Chain, Red/Blue team.

## Garde-fou contenu

- Tout exemple offensif (scan `socket`, brute-force `requests`/`paramiko`, injection) doit rappeler : **labo isolé uniquement, autorisation écrite, art. 323-1 Code pénal**. Ne jamais proposer de cible réelle.
- Libs de référence du cours : `socket`, `requests`, `hashlib`, `re`, `paramiko`, `pandas` (module 7).

## Scripts

- `scripts/check_snippets.py` : syntaxe des snippets Python des `.md` (`ast.parse`, REPL `>>>` ignorés). Usage : `python3 scripts/check_snippets.py [CHEMIN ...]` (défaut : `source/`). À lancer avant de considérer un module comme terminé.
- `scripts/collect_lite_content.py` : copie les notebooks de `source/` vers `content/` (staging gitignoré pour `jupyter lite build`, CI + `scripts/preview_lite.py`). Ne jamais éditer les copies dans `content/`.
