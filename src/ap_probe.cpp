#include <Arduino.h>
#include <WiFi.h>

// Temporary radio diagnosis: no web server and no motor commands.
void setup() {
  digitalWrite(2, LOW);
  pinMode(2, OUTPUT);
  digitalWrite(3, LOW);
  pinMode(3, OUTPUT);
  Serial.begin(115200);

  WiFi.mode(WIFI_AP_STA);
  const bool configured = WiFi.softAP("Klipsch-C3-Test", nullptr, 1, 0);
  Serial.printf("Probe AP configured=%d, SSID=%s, channel=%ld, MAC=%s\n",
                configured, WiFi.softAPSSID().c_str(),
                static_cast<long>(WiFi.channel()), WiFi.softAPmacAddress().c_str());

  delay(1500);
  const int count = WiFi.scanNetworks(false, true);
  Serial.printf("Probe scan found %d networks\n", count);
  for (int i = 0; i < count; ++i) {
    Serial.printf("  %s (%d dBm, channel %ld)\n", WiFi.SSID(i).c_str(),
                  WiFi.RSSI(i), static_cast<long>(WiFi.channel(i)));
  }
}

void loop() {
  static uint32_t lastMs = 0;
  if (millis() - lastMs >= 5000) {
    lastMs = millis();
    Serial.printf("Probe alive: clients=%u, SSID=%s, channel=%ld\n",
                  WiFi.softAPgetStationNum(), WiFi.softAPSSID().c_str(),
                  static_cast<long>(WiFi.channel()));
  }
}
