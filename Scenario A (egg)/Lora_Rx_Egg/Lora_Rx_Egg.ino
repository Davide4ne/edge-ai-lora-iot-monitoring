#include <SPI.h>
#include <LoRa.h>

#define SS    18
#define RST   14
#define DIO0  26

void setup() {
  Serial.begin(115200);

  SPI.begin(5, 19, 27, 18);
  LoRa.setPins(SS, RST, DIO0);

  Serial.println("Avvio LoRa RX...");

  if (!LoRa.begin(868E6)) {
    Serial.println("Errore inizializzazione LoRa");
    while (true);
  }

  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.setSyncWord(0x12);

  Serial.println("LoRa RX OK");
}
void loop() {
  int packetSize = LoRa.parsePacket();

  if (packetSize) {
    String msg = "";

    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }

    //Serial.print("Ricevuto: ");
    Serial.println(msg);

    // Estrazione del campo "id" dal JSON
    int idPos = msg.indexOf("\"id\":");

    if (idPos >= 0) {
      int start = idPos + 5;
      int end = msg.indexOf(",", start);

      if (end < 0) {
        end = msg.indexOf("}", start);
      }

      String packetId = msg.substring(start, end);

      String ack = "{\"ack\":" + packetId + "}";

      delay(100);

      LoRa.beginPacket();
      LoRa.print(ack);
      LoRa.endPacket();

      //Serial.print("ACK inviato: ");
      //Serial.println(ack);
    } 
    //else {
      //Serial.println("ID non trovato, ACK non inviato");
    //}
  }
}