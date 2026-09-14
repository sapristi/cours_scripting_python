# Préambule

Installer VSCode et Python : suivre le guide https://code.visualstudio.com/docs/python/python-tutorial (ignorer à partir de la section *Configure and run the debugger*).

# Module `argparse`

`argparse` est un module inclus dans la lib standard de Python, qui permet de parser les arguments passés à un programme appelé depuis un terminal.

> [!example] Exemple d'utilisation du module `argparse`
> On définit un fichier `myscript.py` :
>
> ```python
> import argparse
>
> parser = argparse.ArgumentParser(description='Argparse demo')
> parser.add_argument("--name")
> parser.add_argument("--year", type=int)
> args = parser.parse_args()
>
> print(f"Bonjour {args.name}, bienvenue en {args.year} !")
> ```
>
> On peut alors exécuter le script avec la commande suivante :
>
> ```shell
> python myscript.py --name franck --year 2024
> ```

# Exercices
## [!note] Exercice 1 : répétition de mots
> Écrire un script Python `repeat_words.py` tel que :
>
> **Entrée :**
> - un mot `mot`
> - un nombre `n`
>
> **Sortie :**
> - affiche `n` fois le mot `mot` (séparés par une espace)


## [!note] Exercice 2 : affichage de formes
> Écrire un script Python `affiche_forme.py` tel que :
>
> **Entrée :**
> - un choix : `triangle` ou `carré`
> - un nombre `n`
>
> **Sortie :**
> - affiche un triangle ou un carré, de la taille demandée `n`

## [!note] Exercice 3 : calculatrice
> Écrire un script Python `calculator.py` tel que :
>
> **Entrée :**
> - un choix : `addition` ou `multiplication`
> - une liste de nombres (`float`)
>
> **Sortie :**
> - le résultat de l'opération donnée appliquée à l'ensemble des nombres donnés
