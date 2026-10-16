#!/usr/bin/env python3

import subprocess
import sys
import os
from datetime import datetime

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CAPTURE_SCRIPT = BASE_DIR / "capture_cam.py"
PREDICT_SCRIPT = BASE_DIR / "predict_lora.py"

def run_step(name, command):
    print(f"\n=== {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {name} ===")

    result = subprocess.run(
        command,
        cwd=str(BASE_DIR),
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0:
        print(f"ERRORE: step '{name}' fallito")
        sys.exit(result.returncode)

    print(f"OK: {name} completato")

def main():
    run_step("Cattura immagine", [sys.executable, str(CAPTURE_SCRIPT)])
    run_step("Inferenza + invio LoRa", [sys.executable, str(PREDICT_SCRIPT)])
    print("\n=== Rilevazione completata ===")

if __name__ == "__main__":
    main()
