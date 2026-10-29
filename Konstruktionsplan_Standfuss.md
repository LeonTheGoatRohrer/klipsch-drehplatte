# Konstruktionsplan: zusätzlicher Standfuß für `final/Unten.stl` (überholt)

**Aktueller Stand:** [Revision D – Ø250 mm, 77 mm Gesamthöhe, Treiber lose darunter](Konstruktion/Revision_D_77mm/Konstruktionsplan_Rev_D_77mm.md). Die Angaben und Zeichnung in dieser Datei gehören zum älteren 90-mm-Entwurf und sollen nicht für den aktuellen Druck verwendet werden.

Stand: 06.10.2026. **Planungsstand, kein freigegebenes Druckteil.** Die STL wurde nur gelesen. Für die nun vollständig festgelegte **Modellgeometrie** ist die dreiblättrige [technische Zeichnung](Konstruktion/Technische_Zeichnung_Standfuss_A3.pdf) maßgeblich; ihre Maße konkretisieren die vorläufigen Angaben unten. Koordinatensystem: Mittelpunkt der vorhandenen Scheibe `(x,y)=(0,0)`, ihre Unterseite `z=0`; der neue Fuß reicht in negative z-Richtung. Alle folgenden Maße sind Millimeter. STL speichert selbst keine Einheit; Millimeter folgen aus Projektkontext und Motorzeichnung.

## 1. Aus der STL gemessen

Quelle: `final/Unten.stl`, SHA-256 `b657eb9beee4e406524f1b351296753bde1b388ae7aaf2460a3f7643e8865692`. Binäres Dreiecksnetz mit 4.832 Dreiecken; bei der Netzprüfung hatten alle Kanten zwei Dreiecke, keine Dreiecke Nullfläche. CAD-Sichtprüfung in Drauf-, Unter- und Schrägansicht. Die Zahlen sind **Sollgeometrie der Datei**, keine Messung des gedruckten Teils.

| Merkmal | Aus der STL gemessener Wert | Lage / Bedeutung |
|---|---:|---|
| Gesamthöhe | 30,00 | `z=0 … 30` |
| Äußerer Befestigungsflansch | Ø124,60; Dicke 6,00 | `z=0 … 6` |
| Oberer zylindrischer Körper | Außen-Ø99,60 | `z=6 … 30` |
| Obere runde Ausnehmung | Innen-Ø85,60; Tiefe 12,00 | offen von `z=30` bis Boden `z=18`; Ringwand radial 7,00 |
| Zentraler Durchlass | Ø30,00; Länge 13,05 | von `z=4,95` bis `z=18` |
| Motortasche auf der Unterseite | **quadratisch 42,60 × 42,60; Tiefe 4,95** | offen bei `z=0`, Taschenboden bei `z=4,95`; ebene, scharfe Ecken in der STL |
| Flanschbohrungen | **4 × Ø4,50**, durchgehend 6,00 | Mittelpunkte `(57,80;0)`, `(0;57,80)`, `(−57,80;0)`, `(0;−57,80)` |
| Lochkreis / Lochabstände | Ø115,60; gegenüber 115,60; benachbart 81,74 | gleiche Achse wie Körper und Motortasche |
| Randabstand der Bohrung | 2,25 Material zur äußeren Flanschkante; 5,75 zur Außenwand Ø99,60 | gemessen ab Bohrungsrand, radial |

In der STL sind **keine** vier Motor-M3-Bohrungen, Gewinde, Kabelschlitze, Schraubenkopfsenkungen oder Muttern erkennbar. Die vorhandene Motorbefestigung ist daher aus dieser Datei nicht rekonstruierbar.

## 2. Vorgeschlagene Geometrie des neuen Fußes

Dies sind **Entwurfswerte**, noch keine Messwerte oder Freigabe für den Druck:

| Maß / Stelle | Vorläufiger Sollwert | Begründung |
|---|---:|---|
| Oberer Außendurchmesser | Ø132 (`R=66`) bei `z=0` | 3,70 radial über dem vorhandenen Flansch; Platz für vier Schraubkanäle |
| Unterer Außendurchmesser | Ø300 (`R=150`) bei `z=−90` | breite, kegelförmige Standbasis; Größe noch anhand Kippnachweis festlegen |
| Fußhöhe | 90 | Motor und Kabelraum; flache, druckbare Kegelneigungen |
| Innerer freier Öffnungsradius | `R=36` oben, linear auf `R=125` unten erweitert | oben Ø72: 5,88 radialer Abstand zur Ecke der quadratischen Motortasche |
| Radiale Materialzone | 30 oben, 25 unten | als tragender Ring mit Rippen/geeignetem Infill; um Schrauben lokale massive Bosse |
| Kontaktfläche zu `Unten.stl` | Fußoberseite eben `R=36 … 66` bei `z=0`; tatsächliche Flanschberührung `R=36 … 62,3` | breite Auflage auf der vorhandenen Flanschunterseite |
| Untere Auflage | Ring `R=125 … 150`, mit rutschfestem Gummiring etwa `R=130 … 145` | offener Boden für Motor- und Schraubenzugang; konservativer Kipphebel `r_eff=130` |
| Kegelwinkel zur Vertikalen | außen 43,03°, innen 44,68° | bei Druck mit Anschlussfläche auf dem Bett nominell unter 45° |

Der Fuß trägt die Vertikallast über die breite ringförmige Kontaktfläche. Die vier Schrauben halten die Teile zusammen und nehmen Zug bei Kippmoment auf; die schmalen 2,25-mm-Randstege des **vorhandenen** Flanschs bleiben eine zu prüfende Schwachstelle. Rundungen `R≥3` an Übergängen des neuen Fußes und `R≥2` am Kabelkanal vermeiden Kerben. Keine scharfe Innenkante in der Kabelroute.

### Kippstabilität

Ø300 ist ein **Startwert**, keine nachgewiesen ausreichende Größe. Mit einem durchgehend aufliegenden Gummiring wird für die Vorrechnung nur `r_eff=130` angesetzt. Für Masse `m`, Schwerpunktversatz `e`, Schwerpunktshöhe `H_S`, Bodenneigung `θ`, seitliche Prüfkraft `F` in Höhe `H_F` gilt näherungsweise:

`e + H_S·tan(θ) + F·H_F/(m·g) < r_eff`.

Für Sicherheitsfaktor 1,5 soll die linke Seite höchstens `r_eff/1,5` sein. Beispiel **nur zur Einordnung**: Bei `m=20 kg`, `H_F=1000`, ohne Versatz/Neigung, läge die rechnerische Kippschwelle schon bei etwa 25,5 N; mit Faktor 1,5 bei etwa 17 N. Wenn die tatsächliche Box so hoch und leicht ist, reicht Ø300 möglicherweise nicht: Basis verbreitern, Masse tief anbringen oder am Boden sichern. Die tatsächliche Boxmasse, Fußabmessung, Schwerpunkthöhe und -versatz, zu erwartende seitliche Kraft, Bodenbeschaffenheit sowie Beschleunigung beim Drehen fehlen. Das Gewicht des Druckteils allein ersetzt keinen Kippnachweis.

## 3. Verschraubung vollständig von unten

Vier vertikale Achsen übernehmen **exakt** die aus der STL gemessenen Mittelpunkte. Der Fuß erhält Ø5,2-Durchgänge für M4; die unveränderten Ø4,5-Löcher in `Unten.stl` bleiben die engste Passage. Für den Anfang wird je eine M4×25-Innensechskantschraube mit Kopf-Ø **höchstens 8** vorgesehen. Schraubentyp, Kopf-Ø, Kopfhöhe und tatsächlicher Schraubendreher sind vor Fertigung zu messen.

Jeder Kopf sitzt auf einer **ebenen Schulter bei `z=−15`**. Ab dort führt ein Ø10-Werkzeugkanal abwärts und mündet etwa bei `z=−29` in den offenen Innenraum. Benötigt wird ein gerader Inbusschlüssel oder Bitverlängerer mit Außendurchmesser **≤10** und mindestens 75 mm nutzbarer Reichweite von der Fußunterseite. Der Kanal liegt am Lochkreis `R=57,8`; die anderen Fußteile dürfen seinen Zugriff nicht verstellen. Um die Schulter und den Kanal einen lokalen, massiven Boss vorsehen, der die Innenwand bei `z≈−15` um mindestens 5 mm nach innen verstärkt. Rechnerisch verbleiben dort ohne Boss innen nur 1,97 mm; mit 5-mm-Boss etwa 6,97 mm. Außen bleiben 17,2 mm. Die Bosse laufen bis `z≈−29` aus, damit der Werkzeugkanal in den Innenraum öffnet.

Oberhalb des vorhandenen Flanschs liegt ein **separater, verdrehsicher zu führender Stahl-Gewindering**, Außen-Ø132, Innen-Ø100,4, Dicke 4, vier M4-Gewinde auf Lochkreis Ø115,6. Sein Innen-Ø hat zur idealen STL-Außenwand Ø99,6 radial 0,4 mm Luft; die reale Passung ist zu prüfen. Der Ring liegt bei `z=6 … 10`; die vier M4×25-Schrauben reichen von der Kopfauflage `z=−15` bis nominell `z=10`, also durch **4 mm Stahlgewinde = 1×D**. Keine Gewindetragfähigkeit in gedrucktem Kunststoff voraussetzen. Gewindering und gedruckte Flanschkante für die tatsächliche Boxlast und das Kippmoment separat prüfen. Der Ring darf obere bewegte Teile nicht berühren; sein Platz bei `z=6 … 10` ist mangels Baugruppenlage **noch nicht freigegeben**.

Der offene Unterboden (Ø250) hält auch den Motor für Werkzeug und Wartung zugänglich, sobald die Einheit angehoben ist. Ob **seine bereits vorhandenen Befestigungsschrauben** tatsächlich alle von unten erreichbar sind, zeigt die STL nicht; deren Köpfe und Werkzeugbahnen am realen Aufbau prüfen. Gegebenenfalls im neuen Fuß zusätzliche Servicefenster vorsehen. Eine verdeckte Motorschraube wäre vor Druckfreigabe zu lösen; die nachgewiesene Unterseitenmontage gilt derzeit nur für die vier neu geplanten Standfußschrauben.

Montage: Gewindering oben auflegen, mit zwei M4-Führungsstiften durch die vorhandenen Löcher von unten ausrichten, Fuß unten ansetzen und alle vier Schrauben **von unten** einsetzen und gleichmäßig anziehen. Führungsstifte nacheinander durch Schrauben ersetzen. Zum späteren Lösen ebenfalls von unten arbeiten; vor der letzten Schraube einen Führungsstift in ein zweites Loch drehen, damit der Gewindering nicht mitdreht oder verrutscht. Führungsstifte sind Montagewerkzeuge, keine zusätzlichen Befestigungsschrauben. Falls der obere Ring in der realen Baugruppe nicht zugänglich oder der Platz zu klein ist, muss vor dem Druck eine andere von unten bedienbare, formschlüssig gesicherte Mutterlösung konstruiert und geprüft werden.

## 4. Motor-, Wellen- und Kabelraum

Laut [Hersteller-Produktseite](https://www.omc-stepperonline.com/e-series-nema-17-bipolar-55ncm-77-88oz-in-2a-42x48mm-4-wires-w-1m-cable-connector-17he19-2004s) und [Herstellerzeichnung](https://files.omc-stepperonline.com/17HE19-2004S_Full_Datasheet.pdf) hat das angegebene Modell 17HE19-2004S nominell 48 mm Gehäuselänge, 42,3 mm max. Gehäusebreite, Ø5×24 Welle, Ø22 Zentrierbund und vier M3-Gewinde auf 31×31 mm Lochbild (Gewindetiefe mindestens 4,5). **Das sind Fremddaten zum Modellnamen, keine Maße des eingebauten Exemplars.** Die vorhandene 42,6-mm-Tasche lässt gegenüber 42,3 mm maximal nur 0,15 mm je Seite; die Ist-Passung muss geprüft werden. Auch die tatsächliche Motorlage und Befestigung sind vor Ort zu dokumentieren.

Bei bündig an der Taschenoberseite sitzender Motorfront läge das nominale Gehäuseende bei `z≈−43,05`; zum geplanten Fußboden `z=−90` blieben etwa 46,95 mm. Der Zentrierbund Ø22 hätte im STL-Durchlass Ø30 radial 4 mm Luft. Diese Rechnungen setzen die Motorlage voraus und sichern die Wellenkupplung nicht ab. Um Motor, feste Schrauben, Kupplung und bewegte Welle ist ein **separat zu prüfender Freiraum** vorzusehen; die Motorverdrahtung darf nicht in den Schwenkbereich gelangen. Das vorhandene Motorbefestigungskonzept bleibt erhalten; es wird nicht durch die Standfußschrauben ersetzt.

Kabelabgang am neuen Fuß: **radiale Ø20-Bohrung bei +45° und `z=−50`**, Werkzeugachse radial `r=75 … 135`, exakt in der Zeichnung definiert. Dort ist die Kegelwand nominal 27,2 mm radial dick, der freie Innenradius etwa 85,4 mm. Ein geschlitzter Silikonschlauch ID8/OD12, Länge 50 mm, im Durchlass und verrundete Kabelkanten `R2` sind vorgesehen. Im Inneren liegen zwei integrierte Ösen Ø18 bei `r=84`, +30°/+60°, `z=−53 … −43`, mit axialen Ø5-Löchern für Kabelbinder als Zugentlastung, so dass Zug **nicht** an Motoranschluss oder Lötstelle ankommt. Vom Motoranschluss zuerst eine spannungsfreie Schlaufe führen; als vorläufige Mindestvorgabe Biegeradius ≥20 mm oder größer nach Kabeldatenblatt. Leitung nicht zwischen Flansch und Fuß einklemmen. Die Beweglichkeit der **Lautsprecherleitung** bei der Drehung ist separat zu planen; die STL zeigt weder Drehwinkel noch Schleifring.

## 5. Druck und Toleranzen

- Anschlussfläche `z=0` aufs Druckbett, breite Standbasis nach oben. Für ein einteiliges Teil mit Ø300 wird ein Druckraum mit praktischem Rand von etwa **≥310–320 mm** benötigt. Die Kegelwinkel liegen bei dieser Richtung nominell unter 45°; Werkzeugkanäle laufen in z-Richtung. Kabelöffnung als tropfenförmige Öffnung oder lokal abgestützt drucken.
- Radiale Wandzone **25–30 mm**; darin 5–6 Perimeter und etwa 35–50 % tragfähiges Infill als Startwert, an Schraubenbossen massiv. Lokale tragende Stege nirgends unter 6 mm auslegen. Perimeter/Infill und Material nach Probestück, realer Motortemperatur und Lastprüfung anpassen; keine temperaturkritische Materialentscheidung allein aus der STL ableiten.
- Fußbohrungen Ø5,2 als Druck-Sollwert, bei Bedarf mit Bohrlehre auf Endmaß nacharbeiten. Achslagen zum Lochkreis ≤±0,2 angestrebt; eine gedruckte Abweichung ist zu messen. Gewindering-Bohrbild aus den **Ist-Bohrungen** übertragen und M4-Gewinde sauber schneiden. Kontaktflächen auf Planlage prüfen und nur den neuen Fuß nacharbeiten; die vorhandene STL bleibt unverändert.
- Bewegliche/steckbare Kunststoffpassungen zunächst mit 0,3–0,5 mm **radialem** Spiel als Probewert konstruieren, abhängig von Drucker und Material. Die bestehende Motortasche hat dieses Spiel gerade **nicht**. Kleine Lehre mit Motortaschenprofil und Schraubkanal vor Gesamtdruck herstellen und am realen Motor/Werkzeug prüfen.
- Gummiring so wählen, dass er eben und rundum trägt; nach Montage auf dem echten Boden auf Wackeln, Rutschen und Torsion prüfen. Falls Ø300 wegen Druckraum nicht einteilig machbar ist, Aufteilung nur mit formschlüssigen Verbindungen und Metallverschraubungen, nicht als bloße Klebefuge im tragenden Fuß.

## 6. Digitaler Abgleich und noch nötige Messungen

| Digital geprüft | Ergebnis / Grenze |
|---|---|
| Geometrie und Bohrungen der Ziel-STL | vier koaxial zur geplanten Fußplatte übernommene Bohrungen; Ø4,5 und Lochkreis Ø115,6 verifiziert |
| Oberer Fußdurchlass Ø72 gegen quadratische Tasche | nominal 5,88 mm Luft zur Taschenecke; keine Überschneidung des neuen Fußes mit der STL-Tasche |
| Schraubkanal Ø10 bei `z=−15` | außen 17,2 mm Material; innen ohne Boss **zu wenig** (1,97 mm), daher 5-mm-Boss zwingend |
| Nominaler Motorraum | 46,95 mm axial bis zum Fußboden bei angenommener Motorlage; Stecker/Kabel und Kupplung nicht durch STL belegbar |
| Druckbare Kegelflanken | 43,03° außen / 44,68° innen zur Vertikalen in vorgesehener Orientierung; Slicerprüfung bleibt nötig |

Vor einem druckfertigen CAD-Modell werden nur diese **Ist-Daten** gebraucht:

1. Masse der Box samt Drehteller, Box-Fußabmessungen sowie Schwerpunktshöhe/-versatz oder ein belastbarer Kipptest; gewünschte seitliche Prüfkraft und Aufstellort/Boden.
2. Foto und Messung am **eingebauten** Motor: Gehäusebreite, Länge ab Frontfläche, Lage seiner Frontfläche relativ zu `Unten.stl`, vorhandene Halterung, Kupplung, Stecker- und Kabelaustrittsmaß. Insbesondere freie Luft in der 42,6-mm-Tasche.
3. Ist-Ø des oberen Körpers/Flansches, Loch-Ø und Lochabstände am gedruckten Teil; freier axialer und radialer Raum **oberhalb** des Flanschs für den 4-mm-Gewindering. Zusammenbauposition von `Oben.stl`/Lager prüfen.
4. Kopf-Ø/-höhe der vorgesehenen M4-Schraube und Außendurchmesser/Länge des Werkzeugs; reale Kabel-/Steckermaße und kleinster zulässiger Biegeradius.
5. Drucker-Bauraum, Material, Düse/Schichthöhe und gewünschte maximale Fußhöhe.

Danach: parametrisierte Fußgeometrie modellieren, gegen die unveränderte Ziel-STL überlagern und Schnitte bei `z=0`, `−15`, `−29`, `−43` und `−50` prüfen; Gewindering und Motor-Hüllkörper einblenden; Kopf/Werkzeug-Sweep und Kabelschlaufe prüfen; slicen; kleine Passlehren drucken; schließlich unbelastete Montage und stufenweise Belastungs-/Kipptest durchführen. **Die vorliegende STL allein belegt weder die Kippfestigkeit noch reale Motortemperatur, Gewindetragfähigkeit, Drucktoleranz, Kabelsicherheit oder störungsfreie Bewegung der Gesamtbaugruppe.**
