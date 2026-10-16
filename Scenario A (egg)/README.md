# 🥚 Scenario A - Autonomous Egg Presence Monitoring using Edge AI and LoRa

## Overview

This project implements an autonomous Internet of Things (IoT) system capable of detecting the presence of eggs inside a nest through Artificial Intelligence executed directly on an edge device.

The objective is to periodically monitor a nest located in an environment without electrical power or Wi-Fi connectivity. Images are acquired through an ESP32-CAM, processed locally on a Raspberry Pi 3 using a TensorFlow Lite model and the inference result is transmitted through a LoRa Point-to-Point communication towards a remote monitoring station.

The received data are visualized on a Node-RED dashboard, stored inside a SQLite database and used to generate automatic Telegram notifications.

The project has been developed as part of the Master's Degree course in Internet of Things.

---

# System Architecture

```
                     GARDEN

             +--------------------+
             |    Power Bank      |
             +---------+----------+
                       |
                       |
               +-------v-------+
               | Raspberry Pi3 |
               +-------+-------+
                       |
          +------------+------------+
          |                         |
          | USB                     | USB
          |                         |
    +-----v------+          +-------v------+
    | ESP32-CAM  |          | LoRa TTGO TX |
    +------------+          +--------------+

                 LoRa Point-to-Point

    +--------------+
    | LoRa TTGO RX |
    +-------+------+
            |
            | USB
            |
      +-----v------+
      |    PC      |
      | Node-RED   |
      +-----+------+
            |
      +-----+------------------------------+
      |            |              |         |
 Dashboard      SQLite        MQTT      Telegram
```

---

# Project Workflow

The complete workflow consists of the following phases:

1. Image acquisition through ESP32-CAM.
2. Image transfer to Raspberry Pi.
3. Local inference using TensorFlow Lite.
4. JSON payload generation.
5. LoRa transmission.
6. ACK reception.
7. Node-RED processing.
8. Dashboard update.
9. SQLite logging.
10. Telegram notification.

---

# Repository Structure

```text
Scenario A (egg)/
├── Esp32Cam/
├── Esp32Cam_low_power/
├── Lora_Tx_Egg/
├── Lora_Tx_Egg_low_power/
├── Lora_Rx_Egg/
├── flow_egg.json
├── modello_TRANSFER_ESP32CAM_egg.tflite
├── dataset_esp32_egg.zip
├── capture_cam.py
├── predict_lora.py
├── run_detection.py
├── scatta_dataset.py
├── crontab_egg.txt
├── database/schema.sql
├── requirements.txt
├── HOW TO.pdf
└── README.md
```

---

# Hardware

The system has been developed using the following hardware:

- Raspberry Pi 3
- ESP32-CAM
- 2 × LilyGO TTGO LoRa 868 MHz
- Power Bank (5V / 2.4A)
- 32 GB MicroSD
- USB cables

---

# Software

- Raspberry Pi OS
- Python 3
- Arduino IDE
- Google Colab
- TensorFlow
- TensorFlow Lite
- Node-RED
- SQLite
- MQTT Broker (Mosquitto)
- Telegram Bot API

---

# AI Model

The classification model has been developed through Transfer Learning using EfficientNetV2B0.

Considering the absence of a public dataset representative of the acquisition conditions, a custom dataset has been created from scratch.

The dataset consists of:

- 60 RGB images
- 30 Egg
- 30 NoEgg
- Three acquisition time slots:
  - 09:00
  - 11:00
  - 20:00

To improve generalization, the training pipeline includes:

- Data Augmentation
- Central Crop
- K-Fold Cross Validation

The trained model has then been converted into TensorFlow Lite format to allow execution directly on Raspberry Pi.

Model file:

```
modello_TRANSFER_ESP32CAM_egg.tflite
```

---

# Image Acquisition

Image acquisition is performed by the ESP32-CAM.

The Raspberry Pi communicates with the camera through the serial interface.

Whenever the Raspberry sends the command

```
CAPTURE
```

the ESP32-CAM captures a new image and stores it locally.

---

# Inference Pipeline

The main execution flow is implemented inside

```
run_detection.py
```

which coordinates the entire pipeline:

```
Capture Image

↓

Load TensorFlow Lite Model

↓

Run Inference

↓

Generate JSON

↓

LoRa Transmission
```

---

# LoRa Communication

The project adopts a Point-to-Point LoRa communication.

Communication parameters are:

| Parameter | Value |
|------------|------:|
| Frequency | 868 MHz |
| Spreading Factor | 7 |
| Bandwidth | 125 kHz |
| Coding Rate | 4/5 |
| Sync Word | 0x12 |

---

# Payload Format

After each inference, Raspberry Pi generates a JSON message containing the prediction result.

Example:

```json
{
    "id": 1718708423,
    "egg": 1,
    "label": "Egg",
    "prob": 97.3
}
```

Where:

- **id** → unique packet identifier
- **egg** → binary prediction
- **label** → textual prediction
- **prob** → confidence score

---

# ACK Mechanism

To improve communication reliability, an acknowledgment mechanism has been implemented.

After receiving a packet, the receiver generates the following response:

```json
{
    "ack":1718708423
}
```

The transmitter compares the received ACK with the transmitted packet ID.

If the IDs match, the transmission is considered successful.

---

# Node-RED

Node-RED acts as the backend of the application. The flow used is in the folder.

Its responsibilities include:

- receiving LoRa packets;
- parsing JSON messages;
- publishing data on MQTT;
- updating the dashboard;
- storing measurements into SQLite;
- sending Telegram notifications.

---

# Dashboard

The dashboard displays:

- Egg status
- Prediction confidence
- Last acquisition timestamp

allowing real-time monitoring of the nest.

---

# Database

Each inference result is permanently stored inside a local SQLite database.

Stored information includes:

- Timestamp
- Egg value
- Label
- Confidence

allowing historical analysis of all acquisitions.

---

# Telegram Notifications

The system automatically generates Telegram notifications through a dedicated bot.

Whenever a new inference is completed, the user receives the classification result directly on Telegram.

---

# Scheduled Execution

The Raspberry Pi automatically performs three acquisitions per day through Cron.

Acquisition times are:

- 08:00
- 11:00
- 15:00

This scheduling minimizes energy consumption while matching the typical egg-laying period.

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

# Environment Variables

Telegram notifications use the `TELEGRAM_CHAT_ID` environment variable in Node-RED. Configure it before deploying `flow_egg.json`.

Example:

```
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

The repository-root `.env.example` documents the configuration values. Configure Node-RED environment variables separately; do not commit actual credentials.

---

# Arduino Libraries required

- ESP32 board package by Espressif Systems
- LoRa by Sandeep Mistry
- SPI, inclusa nel core Arduino/ESP32

---

# Future Improvements

Possible future developments include:

- solar-powered autonomous operation;
- Li-Ion battery charging system;
- weatherproof outdoor enclosure;
- remote firmware updates;
- power optimization;
- multi-hop LoRa communication.

---

# Authors

- Gabriele Postorino
- Davide Maria Quattrone

Master's Degree in Computer Engineering and Telecommunications

University Mediterranea of Reggio Calabria