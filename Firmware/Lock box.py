#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 6
#define RST_PIN 1
#define LED_PIN 27
#define SERVO_PIN 26

MFRC522 rfid(SS_PIN, RST_PIN);
Servo lockServo;

bool locked = true;

byte allowedUID[4] = {x, x, x, x}; // use card UID

void setup() {

  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();

  pinMode(LED_PIN, OUTPUT);

  lockServo.attach(SERVO_PIN);

  //Start in locking state
  lockServo.write(180);
  digitalWrite(LED_PIN, HIGH);
}

void loop() {

  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  bool allowed = true;

  for (byte i = 0; i < 4; i++) {
    if (rfid.uid.uidByte[i] != allowedUID[i]) {
      allowed = false;
    }
  }

  if (allowed) {

    if (locked) {

      Serial.println("Unlocking");
      lockServo.write(0);
      digitalWrite(LED_PIN, LOW);
      locked = false;

    } else {

      Serial.println("Locking");
      lockServo.write(180);
      digitalWrite(LED_PIN, HIGH);
      locked = true;

    }

    delay(1000); // stop double reads
  }

  rfid.PICC_HaltA();
}
