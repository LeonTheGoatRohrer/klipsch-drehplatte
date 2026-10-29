// Small standalone reference for the wiring tested on 06.10.2026.
// This file is outside src/ and is not part of the Wi-Fi firmware build.
// At startup the motor stays still. In a 115200-baud serial monitor send
// 'a' for the tested DIR LOW direction or 'b' for DIR HIGH.
#include <Arduino.h>

constexpr uint8_t STEP_PIN = 2;  // PUL+
constexpr uint8_t DIR_PIN = 3;   // DIR+
constexpr uint16_t PULSES = 100;

void turnOnce(uint8_t direction) {
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, direction);
  delay(10);  // Let DIR settle before the first STEP pulse.

  for (uint16_t i = 0; i < PULSES; ++i) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(20);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(9980);  // Approximately 100 pulses per second.
  }
  Serial.println("100 pulses complete");
}

void setup() {
  digitalWrite(STEP_PIN, LOW);
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(DIR_PIN, LOW);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(115200);
  Serial.println("Ready: a = DIR LOW (right), b = DIR HIGH (left)");
}

void loop() {
  if (Serial.available() == 0) return;
  const char command = static_cast<char>(Serial.read());
  if (command == 'a') turnOnce(LOW);
  if (command == 'b') turnOnce(HIGH);
}
