import serial
import time
from pathlib import Path
from datetime import datetime
import shutil

import os

PORT = os.getenv("CAM_SERIAL_PORT", "/dev/ttyUSB0")
BAUD = 115200

# CAMBIA QUESTO: "Egg" oppure "NoEgg"
LABEL = "NoEgg"

BASE_DIR = Path("dataset_esp32")
OUT_DIR = BASE_DIR / LABEL
OUT_DIR.mkdir(parents=True, exist_ok=True)

def capture_image(out_file):
    ser = serial.Serial(PORT, BAUD, timeout=2)
    ser.setDTR(False)
    ser.setRTS(False)
    time.sleep(3)

    ser.write(b"CAPTURE\n")
    ser.flush()

    length = None

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line.startswith("IMG_START:"):
            length = int(line.split(":")[1])
            break

    img = ser.read(length)

    with open(out_file, "wb") as f:
        f.write(img)

    ser.close()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = OUT_DIR / f"{LABEL.lower()}_{timestamp}.jpg"

capture_image(filename)

# Copia sempre l'ultima immagine qui, così la vedi dal browser
shutil.copy(filename, "last_capture.jpg")

print("Salvata:", filename)
print("Anteprima browser: last_capture.jpg")
