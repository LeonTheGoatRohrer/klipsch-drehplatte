#include "local_config.h"
#pragma once

#include <Arduino.h>

// Confirmed wiring: GPIO2 -> PUL+, GPIO3 -> DIR+, PUL-/DIR- -> GND.
// ENA is not connected. The driver remains energized while its 12 V supply is on.
constexpr uint8_t STEP_GPIO = 2;
constexpr uint8_t DIR_GPIO = 3;

// In the physical test, B (DIR HIGH) turned left and A (DIR LOW) turned right.
constexpr uint8_t LEFT_DIR_LEVEL = HIGH;

// Held movement is intentionally slow; the webpage refreshes a short lease.
constexpr uint32_t PULSE_FREQUENCY_HZ = 50;
constexpr uint32_t PULSE_HIGH_US = 20;
constexpr uint32_t DIRECTION_SETUP_US = 10000;
constexpr uint32_t PULSE_INTERVAL_US = 1000000UL / PULSE_FREQUENCY_HZ;
constexpr uint32_t HOLD_LEASE_MS = 700;

constexpr char WIFI_SSID[] = "Klipsch-Drehplatte";
constexpr char WIFI_PASSWORD[] = LOCAL_WIFI_PASSWORD;

static_assert(STEP_GPIO != DIR_GPIO, "STEP and DIR must use different pins");
static_assert(PULSE_FREQUENCY_HZ > 0, "Pulse frequency must be positive");
static_assert(PULSE_INTERVAL_US > PULSE_HIGH_US, "Pulse interval is too short");
static_assert(HOLD_LEASE_MS >= 500, "Hold lease is too short for mobile Wi-Fi");
static_assert(sizeof(WIFI_PASSWORD) - 1 >= 8, "Wi-Fi password is too short");
