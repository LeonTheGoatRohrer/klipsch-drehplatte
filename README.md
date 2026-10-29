# Klipsch Motorized Turntable

A local ESP32-C3 browser controller for a motorized speaker turntable with a STEP/DIR driver.

## Implemented features

- Hold-to-run left/right controls.
- Fixed 50 pulse/s movement and 700 ms command lease.
- Direction setup timing and no automatic motion at startup.
- Separate radio probe and serial motor reference.

## Technology

PlatformIO, ESP32-C3 Arduino framework, C++, local HTML/JavaScript.

## Installation and local use

1. Copy `src/local_config.example.h` to `src/local_config.h` and choose a unique Wi-Fi password.
2. Build the default controller using `pio run`.
3. With the motor driver supply off, identify the board port and upload.
4. Join `Klipsch-Drehplatte`, open `http://192.168.4.1` and hold a direction button.
5. `pio run -e esp32c3-probe` builds the separate radio diagnostic.

## Configuration and requirements

ESP32-C3; compatible STEP/DIR motor driver; stepper motor and suitable driver supply. Driver microstepping and gear ratio must be checked on the actual assembly. Credentials are local only.

## Development status and limitations

Prototype. DIR HIGH was recorded as left, LOW as right. The plate angle is not measured. Power polarity, loaded supply voltage and physical travel limits still require verification. Release stops motion, while the powered driver can retain holding torque. Historical radio visibility issues remain documented. No hardware movement is part of this publication.

## Contribution and attribution

Leon Rohrer: personal firmware and turntable-control project. Existing vendor and component attribution is retained.

## Wiring and files

| ESP32-C3 | Driver |
|---|---|
| GPIO2 | PUL+ / STEP |
| GPIO3 | DIR+ |
| GND | PUL− and DIR− |

ENA is not connected in the recorded setup. `src/main.cpp` contains the controller, `src/settings.h` the pins/timing and `src/web_page.h` the interface. `examples/motor_reference.cpp` is outside the default build. The existing `motor_gauge.stl` is retained as a project accessory; other CAD provenance is not inferred.

## Publication notes

This portfolio copy includes project source and relevant documentation. Local credentials, private datasets, dependencies and generated build files are excluded. No deployment or paid service is configured by this publication. Existing copyright and license notices remain applicable; this publication does not introduce a new license.
