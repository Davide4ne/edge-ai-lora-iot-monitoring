#include <SPI.h>
#include <LoRa.h>
#include "SSD1306Wire.h"

#define SS    18
#define RST   14
#define DIO0  26

SSD1306Wire display(0x3C, 21, 22);

unsigned long rxCount = 0;
unsigned long ackCount = 0;

String lastId = "-";

int lastRssi = 0;
float lastSnr = 0;

void updateDisplay() {

  display.clear();

  display.drawString(0, 0, "LoRa RX TEST");

  display.drawString(0, 12,
    "RX:" + String(rxCount));

  display.drawString(64, 12,
    "ACK:" + String(ackCount));

  display.drawString(0, 24,
    "ID:" + lastId);

  display.drawString(0, 36,
    "RSSI:" + String(lastRssi));

  display.drawString(0, 48,
    "SNR:" + String(lastSnr, 1));

  display.display();
}

void setup() {

  Serial.begin(115200);
  delay(1000);

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);

  display.clear();
  display.drawString(0, 0, "Avvio RX...");
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
  LoRa.setPreambleLength(16);
  LoRa.setCodingRate4(8);
  LoRa.setSyncWord(0x12);
  LoRa.setTxPower(17);
  LoRa.enableCrc();

  Serial.println("LoRa RX OK");

  updateDisplay();
}

void loop() {

  int packetSize = LoRa.parsePacket();

  if (packetSize) {

    String msg = "";

    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }

    msg.trim();

    rxCount++;

    lastRssi = LoRa.packetRssi();
    lastSnr = LoRa.packetSnr();

    int idPos = msg.indexOf("\"id\":");

    if (idPos >= 0) {

      int start = idPos + 5;
      int end = msg.indexOf(",", start);

      if (end < 0) {
        end = msg.indexOf("}", start);
      }

      String packetId =
        msg.substring(start, end);

      packetId.trim();

      lastId = packetId;

      String ack =
        "{\"ack\":" +
        packetId +
        "}";

      delay(100);

      LoRa.beginPacket();
      LoRa.print(ack);
      LoRa.endPacket();

      ackCount++;
    }

    updateDisplay();
  }
}