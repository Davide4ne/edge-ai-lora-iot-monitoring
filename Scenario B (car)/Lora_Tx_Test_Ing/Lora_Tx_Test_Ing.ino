#include <SPI.h>
#include <LoRa.h>
#include "SSD1306Wire.h"

#define SS    18
#define RST   14
#define DIO0  26

SSD1306Wire display(0x3C, 21, 22);

unsigned long packetId = 0;
unsigned long txCount = 0;
unsigned long ackOk = 0;
unsigned long ackFail = 0;

int lastAckRssi = 0;
float lastAckSnr = 0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 10000;

void updateDisplay() {
  display.clear();

  display.drawString(0, 0, "LoRa TX TEST");

  display.drawString(0, 12,
    "TX:" + String(txCount));

  display.drawString(64, 12,
    "OK:" + String(ackOk));

  display.drawString(0, 24,
    "KO:" + String(ackFail));

  display.drawString(0, 36,
    "RSSI:" + String(lastAckRssi));

  display.drawString(0, 48,
    "SNR:" + String(lastAckSnr, 1));

  display.display();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);

  display.clear();
  display.drawString(0, 0, "Avvio TX...");
  display.display();

  SPI.begin(5, 19, 27, 18);

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(868E6)) {
    display.clear();
    display.drawString(0, 0, "LoRa FAIL");
    display.display();

    while (true);
  }

  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(62.5E3);
  LoRa.setCodingRate4(8);
  LoRa.setPreambleLength(16);
  LoRa.setSyncWord(0x12);
  LoRa.setTxPower(17);
  LoRa.enableCrc();

  Serial.println("LoRa TX OK");

  updateDisplay();
}

void loop() {

  if (millis() - lastSendTime >= sendInterval) {

    lastSendTime = millis();

    packetId++;

    String msg =
      "{\"id\":" +
      String(packetId) +
      ",\"test\":\"lora\"}";

    String expectedAck =
      "{\"ack\":" +
      String(packetId) +
      "}";

    LoRa.beginPacket();
    LoRa.print(msg);
    LoRa.endPacket();

    txCount++;

    bool ackRicevuto = false;

    unsigned long startTime = millis();

    while (millis() - startTime < 7000) {

      int packetSize = LoRa.parsePacket();

      if (packetSize) {

        String response = "";

        while (LoRa.available()) {
          response += (char)LoRa.read();
        }

        response.trim();

        lastAckRssi = LoRa.packetRssi();
        lastAckSnr = LoRa.packetSnr();

        if (response == expectedAck) {
          ackRicevuto = true;
          break;
        }
      }
    }

    if (ackRicevuto) {
      ackOk++;
    } else {
      ackFail++;
    }

    updateDisplay();
  }
}