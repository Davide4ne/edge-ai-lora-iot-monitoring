  #include <SPI.h>
  #include <LoRa.h>

  #define SS    18
  #define RST   14
  #define DIO0  26
  
  int counter = 0;

  void setup() {
    Serial.begin(115200);

    SPI.begin(5, 19, 27, 18);
    LoRa.setPins(SS, RST, DIO0);

    Serial.println("Avvio LoRa TX...");

    if (!LoRa.begin(868E6)) {
      Serial.println("Errore inizializzazione LoRa");
      while (true);
    }
    LoRa.setSpreadingFactor(12);
    LoRa.setSignalBandwidth(62.5E3);
    LoRa.setCodingRate4(8);
    LoRa.setSyncWord(0x12);
    LoRa.setTxPower(17);
    LoRa.enableCrc();
    LoRa.setPreambleLength(16);
    Serial.println("LoRa TX OK");
  }
  void loop() {
    if (Serial.available()) {
      String msg = Serial.readStringUntil('\n');
      msg.trim();

      if (msg.length() > 0) {

        // Estrazione campo "id" dal JSON ricevuto dal Raspberry
        int idPos = msg.indexOf("\"id\":");

        if (idPos < 0) {
          Serial.println("ERRORE: id non trovato nel messaggio");
          return;
        }

        int start = idPos + 5;
        int end = msg.indexOf(",", start);

        if (end < 0) {
          end = msg.indexOf("}", start);
        }

        String packetId = msg.substring(start, end);
        packetId.trim();

        Serial.println("Invio LoRa: " + msg);
        Serial.println("ID pacchetto: " + packetId);

        const int maxRetries = 5;
        unsigned long timeout = 10000;

        bool ackRicevuto = false;

        String expectedAck = "{\"ack\":" + packetId + "}";

        for (int tentativo = 1; tentativo <= maxRetries; tentativo++) {

          LoRa.beginPacket();
          LoRa.print(msg);
          LoRa.endPacket();

          unsigned long startTime = millis();

          while (millis() - startTime < timeout) {
            int packetSize = LoRa.parsePacket();

            if (packetSize) {
              String response = "";

              while (LoRa.available()) {
                response += (char)LoRa.read();
              }

              response.trim();

              Serial.println("Risposta LoRa: " + response);

              if (response == expectedAck) {
                ackRicevuto = true;
                break;
              }
            }
          }

          if (ackRicevuto) {
            break;
          }

          delay(1000);
        }

            if (ackRicevuto) {
              Serial.println("ACK ricevuto correttamente");
        } else {
          Serial.println("ACK non ricevuto entro il timeout");
        }
      }
    }
  }