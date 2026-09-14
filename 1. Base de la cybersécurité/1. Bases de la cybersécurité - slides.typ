#import "@preview/touying:0.6.1": *
#import themes.university: *

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Bases de la cybersécurité],
    subtitle: [Scripting Python — Module 1 · Durée : 1h],
    author: [Cours Scripting Python],
    date: datetime.today(),
  ),
  config-methods(
    init: (self: none, body) => {
      set text(size: 20pt)
      show heading.where(level: 3): set text(fill: self.colors.primary)
      show heading.where(level: 4): set text(fill: self.colors.primary)
      body
    },
    alert: utils.alert-with-primary-color,
  ),
  // le titre est déjà affiché dans le corps de chaque slide :
  // on désactive son rappel dans l'en-tête pour éviter le doublon
  config-store(
    header: none,
    header-right: none,
  ),
)

#set text(lang: "fr")
#show raw.where(block: true): set text(size: 0.55em)
#show table: set text(size: 0.75em)

#title-slide()

#slide[
  == Plan

    - #strong[1.] Qu'est-ce que la cybersécurité ? — #strong[10 min]
    - #strong[2.] Le vocabulaire minimum — #strong[10 min]
    - #strong[3.] Les 5 menaces à connaître — #strong[15 min]
    - #strong[4.] Les 3 défenses à coder — #strong[10 min]
    - #strong[5.] Cadre légal / éthique (FR) — #strong[5 min]
    - #strong[6.] Pourquoi Python en cyber — #strong[5 min]

]

#slide[
  == 1. La cybersécurité, c'est quoi ?

  #block(fill: blue.lighten(90%), inset: 0.7em, radius: 0.5em)[
    Protéger les systèmes, réseaux et données contre les attaques, les vols et les interruptions.
  ]
  #v(0.3em)
  #grid(columns: (1fr, 1fr), gutter: 1em)[
    - Tout est connecté : hôpitaux, banques, usines, téléphones
    - Une panne = vies, argent, confiance en jeu
  ][
    - #strong[Ransomware :] hôpital paralysé, rançon exigée
    - #strong[Phishing :] un simple clic vole un accès
    - #strong[Fuite :] millions de mots de passe revendus
  ]
]

#slide[
  == 1. Qui attaque, qui défend ?

  #grid(columns: (1fr, 1fr), gutter: 1.2em)[
    #block(fill: red.lighten(85%), inset: 0.7em, radius: 0.5em)[
      #strong[⚔️ Les attaquants]
      - Cybercriminels (ransomware, arnaques)
      - États (espionnage, sabotage)
      - Hacktivistes, insiders
    ]
  ][
    #block(fill: blue.lighten(85%), inset: 0.7em, radius: 0.5em)[
      #strong[🛡️ Les défenseurs]
      - SOC / CERT : surveillent, répondent
      - RSSI, pentesters, devs
      - …et bientôt vos scripts !
    ]
  ]
  #v(0.5em)
  #align(center)[Domaines : réseau · web · système · crypto · gouvernance — on les croisera tous.]
]

#slide[
  == 2. Vocabulaire (1/3) — CIA + AAA

  #grid(columns: (1fr, 1fr), gutter: 1em)[
    #block(fill: gray.lighten(90%), inset: 0.8em, radius: 0.5em)[
      #strong[CIA — ce qu'on protège]
      - #strong[C]onfidentialité : l'accès est restreint
      - #strong[I]ntégrité : les données n'ont pas été modifiées
      - #strong[D]isponibilité : le service est opérationnel
    ]
  ][
    #block(fill: gray.lighten(90%), inset: 0.8em, radius: 0.5em)[
      #strong[AAA — comment on contrôle]
      - #strong[A]uthentification : qui es-tu ? (login, MFA)
      - #strong[A]utorisation : droit de faire quoi ?
      - #strong[T]raçabilité (accounting) : qui a fait quoi ? (logs)
    ]
  ]
  #v(0.5em)
  Exemple : login cassé = _Authentification_ HS, log altéré = _Intégrité + Traçabilité_ HS.
]

#slide[
  == 2. Vocabulaire (2/3) — les 5 mots à ne plus confondre

  #table(
    columns: (auto, 1fr, 1fr),
    inset: 0.5em,
    [*Terme*], [*Définition courte*], [*Exemple*],
    [Vulnérabilité], [Faille exploitable], [SQLi non filtrée, SSH mdp faible],
    [Exploit], [Code qui utilise la faille], [Script brute-force SSH],
    [Payload], [Ce que l'exploit exécute], [`id; whoami`, reverse-shell],
    [IOC], [Indice de compromission], [IP, hash SHA256, domaine],
    [TTP], [Tactiques, Techniques, Procédures], [Brute-force puis exfil DNS],
  )
]

#slide[
  == 2. Vocabulaire (3/3) — Kill Chain + MITRE ATT\&CK

  #strong[Kill Chain simplifiée] (où se place votre script ?) :
  Reconnaissance → Accès initial → Exécution → Persistance → Exfiltration

  #v(0.5em)
  #grid(columns: (1fr, 1fr), gutter: 1em)[
    - `socket` scan → #strong[Reconnaissance]
    - brute-force `requests` → #strong[Accès initial]
    - injection → #strong[Exécution]
  ][
    - hash / logs → #strong[Détection]
    - requêtes DNS anormales → #strong[Exfiltration / C2]
  ]
  #v(0.5em)
  MITRE ATT\&CK = catalogue officiel des TTP. Retenez : #strong[chaque script = une case ATT\&CK].
]

#slide[
  == 3. Les 5 menaces — vue d'ensemble

  #grid(columns: (1fr, 1fr), gutter: 0.6em)[
    #block(fill: orange.lighten(85%), inset: 0.5em, radius: 0.5em)[#strong[1.] Brute-force / stuffing — SSH, web]
    #block(fill: orange.lighten(85%), inset: 0.5em, radius: 0.5em)[#strong[2.] Injection — SQLi, XSS, Commande]
    #block(fill: orange.lighten(85%), inset: 0.5em, radius: 0.5em)[#strong[3.] Malware / phishing — hash, URL]
  ][
    #block(fill: orange.lighten(85%), inset: 0.5em, radius: 0.5em)[#strong[4.] Scan / énumération — `socket`, ports]
    #block(fill: orange.lighten(85%), inset: 0.5em, radius: 0.5em)[#strong[5.] Exfiltration / C2 — DNS tunneling]
  ]
]

#slide[
  == Menace 1 — Brute-force / credential stuffing

  - #strong[Quoi :] deviner un mot de passe en testant systématiquement des milliers de combinaisons.
  - #strong[Brute-force :] on génère les essais (wordlist, dictionnaire). #strong[Stuffing :] on rejoue des logins/mdp volés dans des fuites — les gens réutilisent leurs mots de passe !
  - Cibles : SSH, RDP, formulaires web, API.
  - Pourquoi ça marche encore : mots de passe courts, prévisibles (`Azerty123`), jamais changés.
  - #strong[Défenses :] MFA, limiter les tentatives (rate-limit), bannir après N échecs (fail2ban), mots de passe longs.
  - 🔴 En TP (labo !) : automatiser les essais. 🔵 Côté Blue : repérer les vagues d'échecs dans les logs.
]

#slide[
  == Menace 2 — Injection

  - #strong[Quoi :] une entrée utilisateur est interprétée comme du code → l'attaquant exécute ses propres ordres.
  - #strong[SQLi :] taper `' OR '1'='1` dans le login contourne l'authentification en truquant la requête SQL.
  - #strong[Commande :] un `; id` glissé dans un champ s'exécute sur le serveur si l'entrée est concaténée dans un appel système.
  - #strong[XSS :] un script injecté dans une page vole le cookie de session des visiteurs.
  - #strong[Fix :] requêtes paramétrées, validation stricte des entrées, jamais de concaténation, messages d'erreur génériques (le détail aide l'attaquant).
  - 🔴 En TP (labo !) : tester une SQLi. 🔵 Côté Blue : chercher les caractères suspects (`'`, `;`, `<script>`) dans les logs.
]

#slide[
  == Menace 3 — Malware / phishing

  - #strong[Quoi :] le phishing (mail piégé) est le 1er vecteur d'accès initial : un clic suffit.
  - Indices : expéditeur imité, urgence artificielle (« compte bloqué »), pièce jointe ou lien inattendu, URL qui n'est pas le vrai domaine.
  - #strong[Malware :] ransomware (chiffre et rançonne), keylogger (vole la frappe), RAT (contrôle à distance).
  - #strong[Hash SHA256 = carte d'identité du fichier :] 1 bit change → hash totalement différent ; on compare aux bases d'IOC connus.
  - #strong[Défenses :] ne jamais ouvrir dans le doute, vérifier l'URL, antivirus, sauvegardes déconnectées.
  - 🔵 Côté Blue : extraire hash + URL de chaque alerte, comparer aux IOC.
]

#slide[
  == Menace 4 — Scan / énumération

  - #strong[Quoi :] cartographier une cible : quels ports sont ouverts, quels services et versions tournent.
  - Ports ouverts = portes d'entrée potentielles ; la version du service dit s'il est vulnérable.
  - Bannières et réponses verbeuses en révèlent trop : un serveur qui se présente aide l'attaquant.
  - Étape #strong[Reconnaissance] de la Kill Chain : tout commence par observer, bien avant d'attaquer.
  - Scan furtif (lent, discret) vs agressif (rapide, bruyant et loggé).
  - 🔴 En TP (labo uniquement !) : coder un scanner de ports. 🔵 Côté Blue : détecter les balayages dans les logs firewall.
]

#slide[
  == Menace 5 — Exfiltration / C2

  - #strong[Quoi :] une fois dedans, l'attaquant vole des données (exfiltration) et garde le contrôle via un canal de commande (C2).
  - #strong[Beaconing :] le poste compromis « appelle » le serveur de l'attaquant à intervalles réguliers — discret car sortant.
  - #strong[DNS tunneling :] des données cachées dans des requêtes DNS, un protocole que personne ne bloque.
  - #strong[HTTPS vers domaine rare :] noyé dans le trafic web normal, presque invisible.
  - Signaux Blue : volume anormal, domaines jamais vus, requêtes à heures fixes ou la nuit.
  - 🔵 En TP : compter les requêtes par domaine et alerter sur l'inconnu.
]

#slide[
  == 4. Défenses (1/3) — principes

  #grid(columns: (1fr, 1fr, 1fr), gutter: 0.8em)[
    #block(fill: green.lighten(85%), inset: 0.6em, radius: 0.5em)[#strong[Défense en profondeur] \ Firewall + auth + logs + patch.]
    #block(fill: green.lighten(85%), inset: 0.6em, radius: 0.5em)[#strong[Moindre privilège] \ Droits minimum. Pas de root pour un scan !]
    #block(fill: green.lighten(85%), inset: 0.6em, radius: 0.5em)[#strong[Zero Trust] \ Chaque requête vérifiée + loggée.]
  ]
]

#slide[
  == 4. Défenses (2/3) — Crypto utile + démo

  #grid(columns: (1fr, 1fr), gutter: 1em)[
    - #strong[Hash] (intégrité) : `SHA256` = empreinte. Vérifie mdp / logs. Irréversible.
    - #strong[Symétrique] : 1 clé (AES). Rapide, partage délicat.
    - #strong[Asymétrique] : publique/privée (RSA). Échange + signatures.
  ][
    ```python
    import hashlib
    # Démo 2 min : intégrité
    def sha256_texte(t: str) -> str:
        return hashlib.sha256(t.encode()).hexdigest()

    print(sha256_texte("motdepasse123"))
    # vérif log : recalculer et comparer
    ```
  ]
  Retenez : #strong[hash = détecter la modification, chiffrement = empêcher la lecture].
]

#slide[
  == 4. Défenses (3/3) — Hygiène

  #grid(columns: (1fr, 1fr), gutter: 1em)[
    - Mots de passe longs + uniques + gestionnaire
    - #strong[MFA] partout (même en labo)
    - Patching : OS + libs Python (`pip`)
  ][
    - Sauvegardes testées
    - Logs : qui, quoi, quand — et on les protège (hash !)
  ]
  #v(0.5em)
  #align(center)[#strong[Le script le plus sûr est inutile sans hygiène de base.]]
]

#slide[
  == 5. Cadre légal / éthique — obligatoire (FR)

  #block(fill: red.lighten(90%), inset: 0.8em, radius: 0.5em)[
    #strong[⛔ Pas de scan / test hors labo sans autorisation écrite.]
  ]
  - #strong[Art. 323-1 Code pénal :] accès frauduleux = délit (même « juste pour voir »).
  - #strong[Loi Informatique et Libertés + RGPD :] logs = données personnelles → minimiser, sécuriser, durées limitées.
  - En classe : labo isolé, cibles dédiées, autorisation écrite, traçabilité.
  #v(0.5em)
  _Ça vous protège, vous et l'enseignant. Hacker éthique = hacker autorisé._
]

#slide[
  == 6. Pourquoi Python en cyber — le couteau suisse

  #grid(columns: (1fr, 1fr), gutter: 1.2em)[
    #block(fill: red.lighten(85%), inset: 0.8em, radius: 0.5em)[
      #strong[🔴 Red Team — attaquer (en labo)]
      - Scan ports / énumération (`socket`)
      - Exploit / brute-force (`requests`, `paramiko`)
      - OSINT (collecte, parsing, API)
    ]
  ][
    #block(fill: blue.lighten(85%), inset: 0.8em, radius: 0.5em)[
      #strong[🔵 Blue Team — défendre / détecter]
      - Analyse de logs, détection d'IOC
      - Réponse incident, durcissement
      - Automatisation : hash, alertes, parsing
    ]
  ]
  #v(0.5em)
  #align(center)[Python = rapide, lisible, bibliothèques nombreuses : #strong[socket · requests · hashlib · re · paramiko]]
]

#slide[
  == Conclusion — et maintenant, on scripte !

  - Python Red : `socket` → scan, `requests` → brute-force/injection (labo !)
  - Python Blue : `hashlib` → intégrité, parsing logs → détection d'IOC
  - Chaque TP = 1 étape Kill Chain / 1 case ATT\&CK
  #v(0.5em)
  #align(center)[#strong[Prochain module : prise en main Python → premier scanner + premier hash.]]
  #v(0.5em)
  Règle d'or : #strong[labo uniquement, autorisation écrite, on log tout].
]
