import json
import time
import serial
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from ai_edge_litert.interpreter import Interpreter
import os

MODEL_PATH = "modello_TRANSFER_ESP32CAM_egg.tflite"
IMAGE_PATH = "camera.jpg"

SERIAL_PORT = os.getenv("LORA_SERIAL_PORT", "/dev/ttyACM0")
BAUDRATE = 115200

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

img = Image.open(IMAGE_PATH).convert("RGB")

img = img.crop((70, 50, 250, 230))
img.save("crop_debug.jpg")

# Correzione immagine ESP32-CAM
img = ImageOps.autocontrast(img)
img = ImageEnhance.Color(img).enhance(1.6)
img = ImageEnhance.Contrast(img).enhance(1.25)
img = ImageEnhance.Sharpness(img).enhance(1.2)

img = img.resize((224, 224))
img_array = np.array(img, dtype=np.float32) / 255.0
img_array = np.expand_dims(img_array, axis=0)

interpreter.set_tensor(input_details[0]["index"], img_array)
interpreter.invoke()

prediction = float(interpreter.get_tensor(output_details[0]["index"])[0][0])

egg = 1 if prediction >= 0.5 else 0
label = "Egg" if egg == 1 else "NoEgg"

packet_id = int(time.time())

payload = {
    "id": packet_id,
    "egg": egg,
    "label": label,
    "prob": round(prediction, 4)
}

msg = json.dumps(payload, separators=(",", ":"))

payload_bytes = len(msg.encode("utf-8"))

print("Risultato:", payload)
print("Invio LoRa:", msg)
print("Dimensione payload:", payload_bytes, "byte")

if payload_bytes > 51:
    print("ATTENZIONE: payload > 51 byte")


ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
time.sleep(2)
ser.write((msg + "\n").encode())
ser.flush()

start = time.time()
while time.time() - start < 5:
    line = ser.readline().decode(errors="ignore").strip()
    if line:
        print("TX:", line)

ser.close()
