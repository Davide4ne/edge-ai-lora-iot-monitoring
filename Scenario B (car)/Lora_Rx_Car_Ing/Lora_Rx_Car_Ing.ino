#include <SPI.h>
#include <LoRa.h>

#define SS    18
#define RST   14
#define DIO0  26

String lastForwardedId = "";

void setup() {
  Serial.begin(115200);

  SPI.begin(5, 19, 27, 18);
  LoRa.setPins(SS, RST, DIO0);

  //Serial.println("Avvio LoRa RX...");

  if (!LoRa.begin(868E6)) {
    //Serial.println("Errore inizializzazione LoRa");
    while (true);
  }

  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(62.5E3);
  LoRa.setCodingRate4(8);
  LoRa.setSyncWord(0x12);
  LoRa.setTxPower(17);
  LoRa.setPreambleLength(16);
  LoRa.enableCrc();

  LoRa.receive();
  //Serial.println("LoRa RX OK");
}
void loop() {
  int packetSize = LoRa.parsePacket();

  if (packetSize) {
    String msg = "";

    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }

    //Serial.print("Ricevuto: ");
    //Serial.println(msg);

    // Estrazione del campo "id" dal JSON
    int idPos = msg.indexOf("\"id\":");

    if (idPos >= 0) {
      int start = idPos + 5;
      int end = msg.indexOf(",", start);

      if (end < 0) {
        end = msg.indexOf("}", start);
      }

      String packetId = msg.substring(start, end);
      packetId.trim();
      if (packetId != lastForwardedId) {
        Serial.println(msg);
        lastForwardedId = packetId;
      }

      String ack = "{\"ack\":" + packetId + "}";

      delay(100);

     for (int i = 0; i < 3; i++) {
        LoRa.beginPacket();
        LoRa.print(ack);
        LoRa.endPacket();
        delay(300);
      }

      LoRa.receive();

      //Serial.print("ACK inviato: ");
      //Serial.println(ack);
    } 
    //else {
      //Serial.println("ID non trovato, ACK non inviato");
    //}
  }
}