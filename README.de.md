# Klipsch-Drehplatte: Steuerung vom Handy

Der ESP32-C3 stellt ein eigenes WLAN und eine lokale Bedienseite bereit. Es ist
keine Internetverbindung nötig. Die bestehende Verdrahtung bleibt erhalten:
GPIO2 → PUL+, GPIO3 → DIR+, PUL−/DIR− → GND; ENA ist nicht angeschlossen.
Die Richtung wurde am realen Aufbau bestätigt: DIR HIGH (B) dreht nach links,
DIR LOW (A) nach rechts.

## Verbinden und bedienen

1. Das Handy mit **Klipsch-Drehplatte** verbinden. Passwort:
   **<set locally in local_config.h>**. Wenn das Handy „kein Internet“ meldet, dieses WLAN
   trotzdem verwenden.
2. Im Browser **http://192.168.4.1** öffnen und auf „Verbunden“ sowie „Bereit“
   warten. Falls nötig, den ESP32 nach dem Upload einmal manuell zurücksetzen.
3. Die Links- oder Rechts-Taste gedrückt halten. Der Motor fährt langsam,
   solange die Taste gehalten wird. Beim Loslassen stoppt er. Wenn die
   WLAN-Verbindung abreißt oder die Seite geschlossen wird, stoppt die Firmware
   spätestens nach 700 ms ohne Lebenszeichen.
4. Solange die 12-V-Versorgung des Treibers eingeschaltet ist, kann der Motor
   im Stillstand Haltemoment erzeugen.

Die Bewegung läuft mit 50 Treiberimpulsen pro Sekunde. Der Plattenwinkel hängt
von Mikroschritten und mechanischer Übersetzung ab, die noch nicht vollständig
erfasst sind. Beim Start und beim Verbinden bewegt sich der Motor nicht
automatisch.

## Bauen und Laden

Im Projektordner `pio run` ausführen. Vor jedem Upload den seriellen Monitor
schließen und die 12-V-Treiberversorgung ausschalten. COM7 wurde zuletzt als
einziger Espressif-USB-Port erkannt; vor weiteren Uploads mit `pio device list`
erneut prüfen, statt den Port ungeprüft zu übernehmen. Danach mit
`pio run -t upload --upload-port COM7` laden und den Monitor mit 115200 Baud
öffnen. Wenn nach dem Laden keine regelmäßige `Alive`-Meldung erscheint, den
ESP32 bei ausgeschaltetem Treiber einmal manuell zurücksetzen.

Die Zugangsdaten, Pinbelegung und Bewegungsgeschwindigkeit stehen in
`src/settings.h`. Die Handy-Seite liegt in `src/web_page.h`. Der aktive Ablauf
liegt in `src/main.cpp`. Das kleine, getrennte Beispiel
`examples/motor_reference.cpp` zeigt die bereits getesteten seriellen
Richtungsbefehle `a` und `b`; es wird vom normalen Build nicht mitkompiliert.

Der vorhandene Motor drehte im kurzen Test ohne Lautsprecher in beide
Richtungen. Die Polung des umsteckbaren Netzteilsteckers und die Spannung unter
Last wurden mangels Multimeter nicht gemessen. Das bisherige 0,5-A-Netzteil
ist nur für den kurzen Test dokumentiert. Motorleitungen nur bei ausgeschaltetem
Treiber ändern und die Lautsprecherbox erst nach Prüfung von Versorgung,
Mechanik und Drehgrenzen aufsetzen.

## WLAN-Diagnose

Wenn der Zugangspunkt trotz der seriellen Meldung `radio=started` nicht in der
WLAN-Liste erscheint, kann mit `pio run -e esp32c3-probe` ein eigenständiges
Diagnoseprogramm gebaut werden. Es sendet testweise das offene Netz
`Klipsch-C3-Test`, scannt die umliegenden Netze und enthält keine Motorbefehle.
Beim Test am 6. Oktober 2026 empfing das Board sieben umliegende WLANs. Die
Motorsteuerung meldete den eigenen Zugangspunkt als gestartet, aber der PC und
das Handy sahen `Klipsch-Drehplatte` zunächst nicht. Ob die spätere Reduktion
der Sendeleistung auf 8,5 dBm die Sichtbarkeit verbessert, ist noch nicht
bestätigt.
Vor dem Laden den seriellen Monitor schließen und den 12-V-Treiber ausschalten.
Danach den ESP32-Port mit `pio device list` erneut prüfen und die Probe mit
`pio run -e esp32c3-probe -t upload --upload-port COM7` laden, sofern der ESP32
weiterhin COM7 verwendet. Anschließend die normale Firmware mit
`pio run -e esp32c3 -t upload --upload-port COM7` wiederherstellen. Das normale
`pio run` baut ausschließlich die Motorsteuerung.
