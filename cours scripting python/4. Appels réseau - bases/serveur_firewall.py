#!/usr/bin/env python3
"""Serveur TP séance 4 + firewall local (LABO ISOLÉ UNIQUEMENT).

Usage:
    sudo python3 serveur_firewall.py --port 1500 --nom TP4

1. Applique iptables : DROP tout TCP sur 1000-10000 sauf --port.
2. Lance un serveur socket simple (COUCOU/NAME/BYE).
3. Ctrl+C -> serveur arrêté + règles nettoyées.

Cadre légal : labo isolé uniquement, autorisation écrite hors labo.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""
import argparse
import os
import socket
import subprocess
import sys

DEBUT_PLAGE = 1000
FIN_PLAGE = 10000
HOST = "0.0.0.0"  # joignable par les camarades en labo ; sinon 127.0.0.1


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def appliquer_firewall(port: int) -> None:
    # L'ordre compte : la 1re règle qui matche gagne.
    run(["iptables", "-I", "INPUT", "1", "-p", "tcp",
         "--dport", str(port), "-j", "ACCEPT"])
    run(["iptables", "-A", "INPUT", "-p", "tcp",
         "--dport", f"{DEBUT_PLAGE}:{FIN_PLAGE}", "-j", "DROP"])
    print(f"[fw] DROP tcp {DEBUT_PLAGE}-{FIN_PLAGE}, sauf {port}")


def nettoyer_firewall(port: int) -> None:
    for spec in (
        ["-D", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"],
        ["-D", "INPUT", "-p", "tcp",
         "--dport", f"{DEBUT_PLAGE}:{FIN_PLAGE}", "-j", "DROP"],
    ):
        try:
            run(["iptables", *spec])
        except subprocess.CalledProcessError:
            pass
    print("[fw] règles nettoyées")


def gerer_client(conn: socket.socket, nom: str) -> None:
    with conn:
        conn.sendall(f"COUCOU serveur {nom}\r\n".encode())
        f = conn.makefile("r", encoding="utf-8", errors="replace")
        for ligne in f:
            cmd = ligne.strip().split(maxsplit=1)
            if not cmd:
                continue
            ordre = cmd[0].upper()
            if ordre == "COUCOU":
                conn.sendall(f"COUCOU serveur {nom}\r\n".encode())
            elif ordre == "NAME":
                conn.sendall(f"{nom}\r\n".encode())
            elif ordre == "BYE":
                conn.sendall(b"BYE\r\n")
                break
            else:
                conn.sendall(b"ERREUR commande inconnue\r\n")


def lancer_serveur(port: int, nom: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, port))
        srv.listen(5)
        print(f"Ecoute sur {HOST}:{port} (Ctrl+C pour arreter)...")
        while True:
            conn, addr = srv.accept()
            print(f"Connexion de {addr}")
            gerer_client(conn, nom)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--nom", required=True)
    args = p.parse_args()

    if not (DEBUT_PLAGE <= args.port <= FIN_PLAGE):
        sys.exit(f"port hors plage {DEBUT_PLAGE}-{FIN_PLAGE}")
    if os.geteuid() != 0:
        sys.exit("relance avec sudo : les règles iptables l'exigent")

    appliquer_firewall(args.port)
    try:
        lancer_serveur(args.port, args.nom)
    except KeyboardInterrupt:
        print("\nArret demandé.")
    finally:
        nettoyer_firewall(args.port)


if __name__ == "__main__":
    main()
