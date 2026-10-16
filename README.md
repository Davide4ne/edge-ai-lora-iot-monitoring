# Edge AI and LoRa-based IoT Monitoring Systems

## Overview

This repository collects the projects developed as part of the **Internet of Things** Master's Degree course at the **University Mediterranea of Reggio Calabria**.

The main objective is to investigate the integration of **Edge Artificial Intelligence**, **LoRa Point-to-Point communication**, and **Internet of Things technologies** to implement autonomous monitoring systems operating in environments with limited or no Internet connectivity.

Two different application scenarios have been developed, each addressing a specific real-world use case while sharing a common architectural philosophy based on local AI inference, low-power communication, and remote monitoring.

---

# Repository Structure

```text
.
├── Scenario A (egg)/
│   ├── README.md
│   ├── HOW TO.pdf
│   └── ...
└── Scenario B (car)/
    ├── README.md
    ├── HOW TO.pdf
    └── ...
```

Each scenario is completely independent and includes its own source code, Arduino sketches, AI models, documentation and installation guide.

---

# Scenario A – Autonomous Egg Presence Monitoring

Scenario A implements an autonomous monitoring system capable of detecting the presence of eggs inside a nest using **Edge Artificial Intelligence**.

Images are periodically acquired through an ESP32-CAM, processed locally on a Raspberry Pi 3 using a TensorFlow Lite model and the inference result is transmitted through a LoRa Point-to-Point communication to a remote monitoring station.

The received information is visualized on a Node-RED dashboard, stored inside a SQLite database and used to generate Telegram notifications.

📄 **Documentation:** `Scenario A (egg)/README.md`

⚙️ **Installation guide:** `Scenario A (egg)/HOW TO.pdf`

---

# Scenario B – Smart Parking Monitoring

Scenario B implements a smart parking monitoring system based on **drone image acquisition**.

Parking images are acquired through a drone and transmitted to a Raspberry Pi using a Telegram Bot. A YOLOv8 TensorFlow Lite model performs local inference to detect and count the parked vehicles.

The resulting vehicle count is transmitted through LoRa Point-to-Point communication towards a remote monitoring station, where it is visualized using Node-RED and stored for future analysis.

The repository also contains the Arduino sketches used during the experimental campaigns carried out at both the **Engineering Department** and the **Architecture Tower**, including connectivity validation tests and the final communication implementations.

📄 **Documentation:** `Scenario B (car)/README.md`

⚙️ **Installation guide:** `Scenario B (car)/HOW TO.pdf`

---

# Technologies

The projects integrate several hardware and software technologies:

| Category | Technologies |
|-----------|--------------|
| Artificial Intelligence | TensorFlow Lite, YOLOv8, Transfer Learning |
| Embedded Systems | Raspberry Pi 3, ESP32-CAM, LilyGO TTGO LoRa |
| Wireless Communication | LoRa Point-to-Point, Telegram Bot API |
| Backend | Node-RED, SQLite, MQTT |
| Programming Languages | Python, C++ (Arduino) |

---

# Repository Contents

Each scenario includes:

- Python source code;
- Arduino sketches;
- AI models;
- Node-RED flows;
- Dependency files (`requirements.txt`);
- Configuration examples (`.env.example`, at repository root);
- Project documentation (`README.md`);
- Installation guide (`HOW_TO.pdf`).

---

# Authors

- **Gabriele Postorino**
- **Davide Maria Quattrone**

Master's Degree in Computer Engineering and Telecommunications

University Mediterranea of Reggio Calabria