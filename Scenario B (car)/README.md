# 🚗 Scenario B - Parking Vehicle Counting using Edge AI, Telegram and LoRa

## Overview

This project implements an Internet of Things (IoT) system capable of automatically estimating the number of vehicles parked inside an outdoor parking area through Edge Artificial Intelligence.

Unlike traditional parking monitoring systems based on fixed surveillance cameras, this scenario simulates the acquisition process through a drone. Once the image has been captured, it is transmitted to a Raspberry Pi through a Telegram Bot, where a TensorFlow Lite model performs local inference to detect and count the parked vehicles.

The estimated number of vehicles is then transmitted through a LoRa Point-to-Point communication towards a remote monitoring station.

The received data are visualized on a Node-RED dashboard, stored inside a SQLite database and can be used for further processing or visualization.

The project has been developed as part of the Master's Degree course in Internet of Things.

---

# System Architecture

```
                 PARKING AREA

                +----------------+
                |     Drone      |
                +--------+-------+
                         |
                         |
                  Captured Image
                         |
                         |
                  Smartphone App
                         |
                         |
                   Telegram Bot
                         |
                         |
               Internet Connection
                         |
                         |
                 +-------v-------+
                 | Raspberry Pi3 |
                 +-------+-------+
                         |
                  AI Inference
                         |
                 Vehicle Counting
                         |
                         |
                  +------v------+
                  | LoRa TTGO TX|
                  +------+------+

                 LoRa Point-to-Point

                  +------+------+
                  | LoRa TTGO RX|
                  +------+------+
                         |
                         |
                    USB Serial
                         |
                    +----v-----+
                    |    PC    |
                    | Node-RED |
                    +----+-----+
                         |
           +-------------+--------------+
           |             |              |
       Dashboard      SQLite         MQTT
```

---

# Project Workflow

The complete workflow consists of the following phases:

1. Image acquisition through the drone.
2. Image transmission to the Telegram Bot.
3. Automatic download on Raspberry Pi.
4. Vehicle detection using TensorFlow Lite.
5. Vehicle counting.
6. JSON payload generation.
7. LoRa transmission.
8. ACK reception.
9. Node-RED processing.
10. Dashboard update.
11. SQLite logging.

---

# Repository Structure

```text
Scenario B (car)/
├── Lora_Tx_Car_Arch/
├── Lora_Rx_Car_Arch/
├── Lora_Tx_Car_Ing/
├── Lora_Rx_Car_Ing/
├── Lora_Tx_Test_Arch/
├── Lora_Rx_Test_Arch/
├── Lora_Tx_Test_Ing/
├── Lora_Rx_Test_Ing/
├── flow_car.json
├── model_visdrone_yolov8n_car.tflite
├── bot.py
├── vehicle_detector.py
├── lora_send.py
├── database/schema.sql
├── requirements.txt
├── Dataset_visdrone.txt
├── HOW TO.pdf
└── README.md
```

---

# Hardware

The system has been developed using the following hardware:

- DJI Drone
- Smartphone
- Raspberry Pi 3
- 2 × LilyGO TTGO LoRa 868 MHz
- Personal Computer
- USB cables

---

# Software

- Raspberry Pi OS
- Python 3
- Arduino IDE
- Google Colab
- YOLOv8
- TensorFlow Lite
- Node-RED
- SQLite
- Telegram Bot API

---

# AI Model

Vehicle detection has been performed through YOLOv8.

The model has been trained on the VisDrone dataset and subsequently converted into TensorFlow Lite format to allow inference directly on the Raspberry Pi.

The trained model performs object detection and returns the number of detected vehicles inside the acquired image.

Model file:

```
model_visdrone_yolov8n_car.tflite
```

---

# Image Acquisition

Unlike conventional smart parking systems based on fixed cameras, this scenario simulates image acquisition through a drone.

The captured image is automatically sent to a dedicated Telegram Bot.

The Raspberry Pi continuously monitors the Telegram Bot and automatically downloads every newly received image.

---

# Inference Pipeline

The complete execution flow is coordinated by

```
bot.py
```

which performs the following operations:

```
Receive Telegram Image

↓

Download Image

↓

Run AI Inference

↓

Vehicle Counting

↓

Generate JSON

↓

LoRa Transmission
```

---

# Python Scripts

### bot.py

Main application coordinating the complete pipeline.

Responsibilities include:

- Telegram Bot polling
- Image download
- AI inference execution
- LoRa transmission

---

### vehicle_detector.py

Loads the TensorFlow Lite model and performs vehicle detection.

The script returns:

- detected vehicles
- annotated output image

---

### lora_send.py

Generates the JSON payload and sends it through the LoRa transmitter.

---

# LoRa Communication

The project adopts a Point-to-Point LoRa communication.

Communication parameters are related to the case study. In case of "Arch", they are:

| Parameter | Value |
|------------|------:|
| Frequency | 868 MHz |
| Spreading Factor | 12 |
| Bandwidth | 125 kHz |
| Coding Rate | 4/8 |
| Sync Word | 0x12 |
| CRC | Enabled |

while in case of "Ing", the difference is about the Bandwidth:
| Bandwidth | 62.5 kHz |
---

# Payload Format

After inference, Raspberry Pi generates a JSON message containing the vehicle count.

Example:

```json
{
    "id":1718708423,
    "count":32
}
```

Where:

- **id** → unique packet identifier
- **count** → detected number of vehicles

---

# ACK Mechanism

Communication reliability is improved through an acknowledgment mechanism.

After successfully receiving a packet, the receiver sends:

```json
{
    "ack":1718708423
}
```

The transmitter compares the ACK identifier with the transmitted packet identifier.

If both identifiers match, the transmission is considered successful.

---

# Node-RED

Node-RED acts as the backend of the application.

Its responsibilities include:

- receiving LoRa packets;
- parsing JSON messages;
- updating the dashboard;
- storing measurements inside SQLite.

---

# Dashboard

The dashboard displays:

- Number of detected vehicles
- Last acquisition timestamp

allowing remote monitoring of the parking area.

---

# Database

Each acquisition is permanently stored inside a local SQLite database.

Stored information includes:

- Timestamp
- Vehicle count

allowing historical analysis of parking occupancy.

---

# Telegram Bot

Telegram has been adopted as the communication interface between the drone operator and the Raspberry Pi.

The Raspberry Pi continuously polls the Telegram Bot searching for newly uploaded images.

Whenever a new image is received, the complete inference pipeline is automatically executed.

---

# Telegram Service

The Raspberry Pi continuously executes a Python service (`bot.py`) that performs polling on a dedicated Telegram Bot using the Telegram Bot API.

Whenever a new image is received, the bot automatically:

1. downloads the image;
2. stores it locally;
3. executes the AI inference pipeline;
4. counts the detected vehicles;
5. generates the JSON payload;
6. sends the result through the LoRa transmitter.

This approach allows the Raspberry Pi to autonomously react to every incoming image without requiring manual intervention.

---

# Python Dependencies

All Python dependencies are listed inside:

```
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

---

# Arduino sketches explaination

| Folder            | Purpose                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| LoRa_TX_Car_Arch  | Final transmitter used during the Architecture Tower experiments.                                            |
| LoRa_RX_Car_Arch  | Final receiver used during the Architecture Tower experiments.                                               |
| LoRa_TX_Car_Ing   | Final transmitter used during the Engineering Building experiments.                                          |
| LoRa_RX_Car_Ing   | Final receiver used during the Engineering Building experiments.                                             |
| LoRa_TX_Test_Arch | Connectivity tests performed before the complete parking monitoring experiments at the Architecture Tower.   |
| LoRa_RX_Test_Arch | Connectivity receiver used during Architecture Tower link validation.                                        |
| LoRa_TX_Test_Ing  | Connectivity tests performed before the complete parking monitoring experiments at the Engineering Building. |
| LoRa_RX_Test_Ing  | Connectivity receiver used during Engineering Building link validation.                                      |

---

# Arduino Libraries required

- ESP32 board package by Espressif Systems
- LoRa by Sandeep Mistry
- SPI, inclusa nel core Arduino/ESP32
 
In order to use the led of your LilyGOs:
- Adafruit BusIO
- Adafruit GFX Library
- Adafruit SSD1306
- Adafruit SSD1305/SSD1306
---

# Environment Variables

Sensitive information, such as the Telegram Bot Token, is stored inside a `.env` file.

Example:

```
TELEGRAM_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
```

The `.env` file is intentionally excluded from the repository. Node-RED also requires `TELEGRAM_CHAT_ID` to be configured in its environment for `flow_car.json`. See the repository-root `.env.example`.

---

# Dataset

The model has been trained using the VisDrone dataset.

Due to its size and licensing constraints, the complete dataset is not included inside this repository.

Further information can be found inside:

```
Dataset_visdrone.txt
```

---

# Future Improvements

Possible future developments include:

- fixed camera with antenna at an appropriate height
- LoRa multi-hop communication;
- payload optimization for reduced Time-on-Air;
- adaptive communication parameters.

---

# Authors

- Gabriele Postorino
- Davide Maria Quattrone

Master's Degree in Computer Engineering and Telecommunications

University Mediterranea of Reggio Calabria