import json
import time
import serial

import os

SERIAL_PORT = os.getenv("LORA_SERIAL_PORT", "/dev/ttyACM0")
BAUD_RATE = 115200


def send_lora_count(count):
    packet_id = int(time.time())

    payload = {
        "id": packet_id,
        "cars": int(count)
    }

    msg = json.dumps(payload)

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        ser.write((msg + "\n").encode("utf-8"))
        ser.flush()

        print("Inviato al modulo LoRa:", msg)

        start = time.time()
        while time.time() - start < 60:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if line:
                print("Seriale LoRa:", line)

                if "ACK ricevuto correttamente" in line:
                    return True

        return False
