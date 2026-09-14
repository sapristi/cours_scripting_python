#!/usr/bin/env python3
"""Aperçu local du site JupyterLite : collecte les notebooks, build, puis sert dist/.

Usage :
    uv run scripts/preview_lite.py [--port 8000]

Ouvrir ensuite http://127.0.0.1:8000/lab (ou le port choisi).
Arrêter avec Ctrl+C.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def lancer(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(list(cmd), cwd=RACINE, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prévisualiser le site JupyterLite en local.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    lancer(sys.executable, "scripts/collect_lite_content.py")
    lancer("jupyter", "lite", "build")

    cmd = ["jupyter", "lite", "serve", "--port", str(args.port)]
    print(f"$ {' '.join(cmd)}", flush=True)
    os.execvp("jupyter", cmd)


if __name__ == "__main__":
    sys.exit(main())
