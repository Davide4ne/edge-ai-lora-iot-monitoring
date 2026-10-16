import serial
import time

import os

PORT = os.getenv("CAM_SERIAL_PORT", "/dev/ttyUSB0")
BAUD = 115200

OUT_FILE = "camera.jpg"

ser = serial.Serial(PORT, BAUD, timeout=2)
ser.setDTR(False)
ser.setRTS(False)

time.sleep(3)

ser.write(b"CAPTURE\n")
ser.flush()

# Cerca IMG_START
length = None

while True:
    line = ser.readline().decode(errors="ignore").strip()
    print("LINE:", line)

    if line.startswith("IMG_START:"):
        length = int(line.split(":")[1])
        break

if length is None:
    raise RuntimeError("IMG_START non trovato")

print("Lunghezza immagine:", length)

img = ser.read(length)

with open(OUT_FILE, "wb") as f:
    f.write(img)

print("Immagine salvata:", OUT_FILE, "byte:", len(img))

# Legge eventuale IMG_END
tail = ser.readline().decode(errors="ignore").strip()
print("TAIL:", tail)

ser.close()
