#include <Arduino.h>
#include <WebServer.h>
#include <WiFi.h>

#include "settings.h"
#include "web_page.h"

namespace {
enum class MotionState { Idle, DirectionSetup, Running, Stopped };

WebServer server(80);
MotionState state = MotionState::Idle;
bool apReady = false;
volatile bool apStarted = false;
bool pulseHigh = false;
bool continuousHold = false;
bool movingLeft = false;
uint32_t pulsesSent = 0;
uint32_t directionChangedUs = 0;
uint32_t nextPulseUs = 0;
uint32_t pulseStartedUs = 0;
uint32_t lastHoldRefreshMs = 0;

bool due(uint32_t now, uint32_t deadline) {
  return static_cast<int32_t>(now - deadline) >= 0;
}

bool motionBusy() {
  return state == MotionState::DirectionSetup || state == MotionState::Running;
}

const char *stateName() {
  switch (state) {
    case MotionState::Idle: return "idle";
    case MotionState::DirectionSetup: return "starting";
    case MotionState::Running: return "running";
    case MotionState::Stopped: return "stopped";
  }
  return "unknown";
}

void stopMotion(const char *reason) {
  digitalWrite(STEP_GPIO, LOW);
  pulseHigh = false;
  continuousHold = false;
  state = MotionState::Stopped;
  Serial.printf("Motor stopped (%s), pulses=%lu. STEP is LOW.\n", reason,
                static_cast<unsigned long>(pulsesSent));
}

void startMotion(bool left) {
  digitalWrite(STEP_GPIO, LOW);
  pulseHigh = false;
  continuousHold = true;
  movingLeft = left;
  pulsesSent = 0;
  const uint8_t directionLevel = left ? LEFT_DIR_LEVEL
                                      : (LEFT_DIR_LEVEL == HIGH ? LOW : HIGH);
  digitalWrite(DIR_GPIO, directionLevel);
  directionChangedUs = micros();
  lastHoldRefreshMs = millis();
  state = MotionState::DirectionSetup;
  Serial.printf("Hold start: %s, %lu Hz.\n", left ? "left" : "right",
                static_cast<unsigned long>(PULSE_FREQUENCY_HZ));
}

void updateMotion(uint32_t nowUs) {
  if (continuousHold && static_cast<uint32_t>(millis() - lastHoldRefreshMs) > HOLD_LEASE_MS) {
    stopMotion("hold lease expired");
    return;
  }

  if (state == MotionState::DirectionSetup) {
    if (static_cast<uint32_t>(nowUs - directionChangedUs) < DIRECTION_SETUP_US) return;
    state = MotionState::Running;
    nextPulseUs = nowUs;
  }
  if (state != MotionState::Running) return;

  if (pulseHigh) {
    if (static_cast<uint32_t>(nowUs - pulseStartedUs) < PULSE_HIGH_US) return;
    digitalWrite(STEP_GPIO, LOW);
    pulseHigh = false;
  }

  if (!due(nowUs, nextPulseUs)) return;
  digitalWrite(STEP_GPIO, HIGH);
  pulseHigh = true;
  pulseStartedUs = nowUs;
  ++pulsesSent;
  nextPulseUs = nowUs + PULSE_INTERVAL_US;
}

void sendState(int httpCode = 200) {
  char json[176];
  snprintf(json, sizeof(json),
           "{\"state\":\"%s\",\"busy\":%s,\"continuous\":%s,\"direction\":\"%s\",\"sent\":%lu}",
           stateName(), motionBusy() ? "true" : "false",
           continuousHold ? "true" : "false", movingLeft ? "left" : "right",
           static_cast<unsigned long>(pulsesSent));
  server.sendHeader("Cache-Control", "no-store");
  server.send(httpCode, "application/json; charset=utf-8", json);
}

void handleHold() {
  if (!server.hasArg("direction")) {
    server.send(400, "application/json", "{\"error\":\"direction required\"}");
    return;
  }
  const String direction = server.arg("direction");
  if (direction != "left" && direction != "right") {
    server.send(400, "application/json", "{\"error\":\"invalid direction\"}");
    return;
  }
  if (motionBusy()) {
    server.send(409, "application/json", "{\"error\":\"motor busy\"}");
    return;
  }
  startMotion(direction == "left");
  sendState(202);
}

void handleKeepAlive() {
  if (!continuousHold || !motionBusy()) {
    server.send(409, "application/json", "{\"error\":\"no active hold\"}");
    return;
  }
  lastHoldRefreshMs = millis();
  sendState();
}

void handleStop() {
  stopMotion("released");
  sendState();
}

void setupWebServer() {
  server.on("/", HTTP_GET, [] {
    server.sendHeader("Cache-Control", "no-store");
    server.send_P(200, "text/html; charset=utf-8", WEB_PAGE);
  });
  server.on("/api/status", HTTP_GET, [] { sendState(); });
  server.on("/api/hold", HTTP_POST, handleHold);
  server.on("/api/keepalive", HTTP_POST, handleKeepAlive);
  server.on("/api/stop", HTTP_POST, handleStop);
  server.onNotFound([] { server.send(404, "text/plain", "Not found"); });
  server.begin();
}
}  // namespace

void setup() {
  digitalWrite(STEP_GPIO, LOW);
  pinMode(STEP_GPIO, OUTPUT);
  digitalWrite(DIR_GPIO, LOW);
  pinMode(DIR_GPIO, OUTPUT);
  Serial.begin(115200);

  WiFi.onEvent([](arduino_event_id_t event) {
    if (event == ARDUINO_EVENT_WIFI_AP_START) apStarted = true;
    if (event == ARDUINO_EVENT_WIFI_AP_STOP) apStarted = false;
  });
  WiFi.mode(WIFI_AP);
  const IPAddress apAddress(192, 168, 4, 1);
  if (!WiFi.softAPConfig(apAddress, apAddress, IPAddress(255, 255, 255, 0))) {
    Serial.println("AP address configuration failed.");
  }
  apReady = WiFi.softAP(WIFI_SSID, WIFI_PASSWORD, 6, 0);
  if (apReady) {
    Serial.printf("Wi-Fi transmit power limited: %s\n",
                  WiFi.setTxPower(WIFI_POWER_8_5dBm) ? "yes" : "no");
    setupWebServer();
    Serial.printf("Wi-Fi AP ready: %s at %s\n", WIFI_SSID,
                  WiFi.softAPIP().toString().c_str());
  } else {
    Serial.println("Wi-Fi AP could not start. Motor remains idle.");
  }
}

void loop() {
  updateMotion(micros());
  if (pulseHigh) return;
  if (apReady) server.handleClient();
  if (Serial.available() && Serial.read() == 's') stopMotion("serial");

  static uint32_t lastHeartbeatMs = 0;
  const uint32_t nowMs = millis();
  if (static_cast<uint32_t>(nowMs - lastHeartbeatMs) >= 5000) {
    lastHeartbeatMs = nowMs;
    Serial.printf("Alive: AP=%s, radio=%s, clients=%u, state=%s, direction=%s, pulses=%lu\n",
                  apReady ? "configured" : "off", apStarted ? "started" : "stopped",
                  WiFi.softAPgetStationNum(), stateName(), movingLeft ? "left" : "right",
                  static_cast<unsigned long>(pulsesSent));
  }
}
