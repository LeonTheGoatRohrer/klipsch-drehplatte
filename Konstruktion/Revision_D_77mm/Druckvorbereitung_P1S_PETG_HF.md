# Druckvorbereitung – P1S / PETG HF Schwarz

Stand: 7. Oktober 2026. Status: digital vorbereitet; Rolle noch nicht kalibriert.
Kein Druck und kein Kalibrierdruck wurde gestartet.

## Aktuelle, korrigierte Vorbereitung

**Aktives Projekt: `Standfuss_P1S_PETG_HF_Spar_020_3W_6P.3mf`.**
Berechnete Druckbahnen: `Standfuss_P1S_PETG_HF_Spar_020_3W_6P_sliced.3mf`.

Bambu Studio berechnet **237,53 g einschließlich Brim und Stützen**, **6 h 31 min 52 s reine
Modelldruckzeit** und **6 h 38 min 08 s einschließlich Startablauf**. Dies sind Schätzungen;
die noch ausstehende Rollenkalibrierung kann Verbrauch und Zeit ändern.

Die frühere Vorbereitung mit 491,18 g und 27 h 32 min ist verworfen. Die Dateien mit dem
Namen `Standfuss_P1S_PETG_HF_230C_8mm_Innenbrim` dokumentieren diesen alten Stand.

## Vor dem nächsten Druck

1. Textured PEI Plate mit warmem Wasser und Spülmittel reinigen, gut abspülen und trocknen.
2. Die gereinigte Druckfläche anschließend nicht mehr berühren.
3. Festgeklebtes PETG von der Düse entfernen; dabei die Wartungsanleitung und die heiße Düse beachten.
4. Bei Verdacht auf Feuchtigkeit PETG HF ungefähr acht Stunden bei 65 °C in einem geeigneten Filamenttrockner trocknen.

## Profil und Schichten

- Drucker: Bambu Lab P1S, serienmäßige 0,4-mm-Düse.
- Platte: Textured PEI Plate.
- Originales Filamentprofil: Bambu PETG HF @BBL X1C, unterstützt den P1S.
- Separate Kopie: Bambu PETG HF Schwarz – Standfuss 230C @P1S.
- Druckschichten: 230 °C; Bett: 70 °C.
- Erste Kontur: 20 mm/s; erste Füllung: 30 mm/s, unter der Grenze von 40 mm/s.
- Erste Schicht und folgende Schichten jeweils 0,20 mm, 380 Druckschichten.
- Bauteillüfter während der ersten drei Druckschichten aus.
- Hilfslüfter P2 vollständig aus, einschließlich der zwei Einschaltbefehle im serienmäßigen Startablauf.
- Innenbrim 8 mm; kein Außenbrim, da Ø250 + 2 × 8 mm nicht auf das 256-mm-Bett passt.
- Drei Wandlinien, 6 % adaptiv kubische Innenfüllung, oben/unten jeweils 0,8 mm und vier Schichten.
- Linienbreite außen 0,42 mm, innen 0,45 mm: nominell ca. 1,32 mm radial je Konturpaket; tatsächliche Stärke hängt von Überlappung und Flächenschräge ab. Innen- und Außenkontur werden jeweils gedruckt.
- Vier lokale Schraubensitz-Modifikatoren Ø20 × 10 mm: 100 % Füllung und sechs Wandlinien.
- Zusätzliche massive Füllung an Schrägen: vertikale Schalendicke auf „Teilweise“; Erkennung freischwebender Schalen bleibt aktiviert. Dadurch bleiben drei Konturlinien erhalten, während unnötig große massive Innenbereiche entfallen.
- Normale automatische Stützen; Schwellwinkel 30°, Abstand oben/unten 0,20 mm, Grundmusterabstand 3 mm, unabhängige Stützschichthöhe aus.
- Sollgeschwindigkeiten: Außenwände 140 mm/s und 2.500 mm/s²; Innenwände und Innenfüllung 250 mm/s, massive Füllung 180 mm/s, Deckflächen 50 mm/s. Überhänge, erste Schichten und volumetrische Begrenzung reduzieren diese Werte bei Bedarf.
- Maximale volumetrische Geschwindigkeit unverändert 21 mm³/s.
- Flussverhältnis vorläufig unverändert 0,95. Dies ist kein gemessenes Ergebnis dieser Rolle.
- Die serienmäßige Reinigung/Spülung vor der ersten Schicht verwendet teilweise andere Temperaturen. Die Druckschichten verwenden 230 °C.

0,20 mm ist der Kompromiss für das Zeitlimit. Sichtbare Schichtstufen an der Kegelfläche
bleiben möglich; eine spiegelglatte Oberfläche ist damit nicht zugesichert. Die schnelle
Innenfüllung und 230 °C müssen mit der noch unkalibrierten Rolle zuerst geprüft werden.

## Platzierung und Montage

Das Bauteil bleibt Ø250 × 76 mm, montiert mit vorgesehenem Gummi 77 mm.
Die 3MF-Instanz liegt bei X128/Y130. Der im P1S-Profil enthaltene Y-Düsenversatz von 2 mm
wird damit ausgeglichen: tatsächliche Druckbahnen werden um X128/Y128 zentriert und bleiben
von den serienmäßigen vorderen Spüllinien getrennt. Eine spätere automatische Neuanordnung
kann diesen Abstand ändern; dann erneut die erste Schicht prüfen.

Brim und Stützen vollständig entfernen, insbesondere aus der Gummiringnut und aus den
Schrauben-/Werkzeugzugängen. Kabelkanten wie im Konstruktionsplan glätten und schützen.

## Kalibrierung und Freigabe

Die verwendete Rolle wurde laut Nutzer noch nicht kalibriert. Der P1S hat keine automatische
Flow-Dynamics-Messung mit Lidar. Deshalb kann die angeforderte automatische dynamische
Flusskalibrierung nicht aktiviert werden.

Nach ausdrücklicher Druckfreigabe die integrierten manuellen Tests in Bambu Studio verwenden:

1. Kopiertes Filamentprofil auswählen und bei 230 °C / 70 °C mit Textured PEI Plate kalibrieren.
2. Flow Dynamics: Kalibriermuster drucken, beste Linie auswählen, K-Wert für diese Rolle speichern.
3. Flow Rate: Grob- und anschließend Feinkalibrierung auswerten; resultierendes Flussverhältnis in der Kopie speichern.
4. Werte dem Projekt zuordnen und den Fuß mit den gemessenen Werten erneut slicen.
5. Beim Senden des Drucks automatische Bettnivellierung aktivieren.
6. Erst nach Bestätigung des Nutzers drucken. Die erste Schicht beobachten; bei erneut ablösenden Bahnen den Druck stoppen.

Der MCP ist für lokale Vorbereitung installiert; es wurden keine Zugangsdaten zum P1S
hinterlegt und keine Druckerbefehle gesendet. Bettnivellierung wird beim Druckstart gewählt,
nicht allein durch das Speichern einer 3MF-Datei aktiviert.

## Dateien und digitale Prüfung

- `Standfuss_P1S_PETG_HF_Spar_020_3W_6P.3mf`: aktuelles bearbeitbares Projekt.
- `Standfuss_P1S_PETG_HF_Spar_020_3W_6P_sliced.3mf`: aktuelle berechnete, noch unkalibrierte Druckvorbereitung.
- `Bambu_PETG_HF_Schwarz_Standfuss_230C.json`: separate Filamentprofil-Kopie.
- `Erste_Schicht_230C_Innenbrim8_Spar.png`: vollständige erste Schicht aus den aktuellen tatsächlichen G-Code-Druckbahnen.
- `Erste_Schicht_Pruefung_Spar.json`: prüfbare Werte, Geschwindigkeiten, Lüfter- und Temperaturkontrollen.
- `Sparprofil_Vergleich.json`: tatsächliche Ergebnisse aller vier neuen Slices und Vergleich der unveränderten Bauteilgeometrie.

Die erste Schicht wird vollständig einschließlich Brim und Stützen kontrolliert. Die digitale
Prüfung beweist keine reale Plattenhaftung, Materialqualität, Dauertraglast oder Kippstabilität.
Die angestrebten 15 kg bleiben durch einen realen Belastungs- und Wärmeversuch nachzuweisen.

Bambu Studio meldet bei 70 °C Bett eine Warnung, dass die Betttemperatur über der hinterlegten
Filament-Erweichungsschwelle liegt. Die 70 °C stammen aus dem Originalprofil und wurden vom
Nutzer ausdrücklich vorgegeben. Diese Warnung bleibt sichtbar; sie wird nicht unterdrückt.

## Abschließendes Slicing-Ergebnis

Berechnet: 237,53 g einschließlich Brim und Stützen; insgesamt 6 h 38 min. Noch ohne die ausstehenden Messwerte der Rollenkalibrierung.

Erste Schicht vollständig aus dem G-Code geprüft und visuell kontrolliert: geschlossene Ringkonturen, Innenbrim, Stützbasen, Druckbettgrenzen und Abstand zur vorderen Spüllinie. Die vorgesehenen Lüfter- und Temperaturwerte wurden geprüft.

Die Bauteilnetz-Geometrie im neuen Projekt und im geslicten Projekt ist identisch mit der
vorherigen Vorbereitung. Alle vier Modifikatoren für die Schraubensitze sind mit 100 %
Füllung und sechs Wänden vorhanden. ZIP-Datei und G-Code-Prüfsumme sind geprüft.

Die 15-kg-Tragfähigkeit ist **noch nicht nachgewiesen**. Vor dem dauerhaften Einsatz einen
stufenweisen Belastungsversuch am fertig montierten Fuß ohne Lautsprecher durchführen,
einschließlich längerem Halten der Last bei eingeschaltetem Motor. Verformung, Risse,
Schraubensitze und Kippverhalten kontrollieren. Schwerpunktlage und Langzeitverhalten bei
Motorwärme bleiben offene reale Prüfungen; ein Slicer kann sie nicht bestätigen.

Referenz zur Funktion der zusätzlichen Schrägenfüllung:
[Bambu Studio, PrintConfig.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp).
