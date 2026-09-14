# AGENTS.md — scripting_python (cours)

Contenu pédagogique en français : scripting Python pour la cybersécurité (3e année). 
Obsidian vault, pas un projet code.

## Structure

- `Général.md` : objectifs + plan.
- `N. <Titre>.md` à la racine = un module de cours. Frontmatter requis : `durée (h)` (nombre) + `Contexte` (texte, source du plan).
- `N. <Titre>/` (même nom que le `.md`) = assets du module (slides, images, futurs énoncés/TP). 
- `Cours.base` = config Bases/Dataview du tableau de bord (`file.folder == "/"`, `file.ext == "md"`). Ne pas éditer comme du contenu.
- Images : `![[Pasted image ....png|largeur]]` (embed Obsidian + resize). Stocker dans chaque dossier correspondant.
- Slides : source `.typ` (Typst), compilée en `.pdf` à côté. Éditer le `.typ`, jamais le `.pdf` directement ; recompiler : `typst compile "<fichier>.typ"`.

## Conventions Obsidian

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Ne pas toucher à `.obsidian/` (workspace, `graph.json`, `types.json`, plugins : `auto-numbered-headings`, `floating-headings`, `heading-level-indent`).
- Rédiger en français. Vocabulaire suggéré du module 1 : CIA, AAA, vulnérabilité/exploit/payload/IOC/TTP, Kill Chain, Red/Blue team.

## Garde-fou contenu

- Tout exemple offensif (scan `socket`, brute-force `requests`/`paramiko`, injection) doit rappeler : **labo isolé uniquement, autorisation écrite, art. 323-1 Code pénal**. Ne jamais proposer de cible réelle.
- Libs de référence du cours : `socket`, `requests`, `hashlib`, `re`, `paramiko`, `pandas` (module 7).

## Scripts

- `scripts/check_snippets.py` : vérifie la syntaxe des snippets Python dans les `.md` (blocs ` ```python ` via `ast.parse`, blocs REPL `>>>` ignorés). Usage : `python3 scripts/check_snippets.py [CHEMIN ...]` (défaut : tout le vault). À lancer avant de considérer un module comme terminé.
