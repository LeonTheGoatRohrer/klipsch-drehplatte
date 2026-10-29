# Konstruktionsplan Revision D – Ø250, 77 mm, Treiber lose darunter

Stand 06.10.2026. Die [vierblättrige A3-Zeichnung](Technische_Zeichnung_Standfuss_Rev_D_77mm_A3.pdf), der [parametrische CAD-Quelltext](standfuss_v4.py), das [STEP-Modell](standfuss_v4.step) und die [neue Test-STL für den Slicer](standfuss_v4_testfit.stl) definieren den Standfuß. Ein [separater Stahl-Gewindering](gewindering_v4.step) dient als Gegenstück für vier von unten betätigte Schrauben. Die alte `final/Unten.stl` wurde nicht verändert.

## 1. Bezug, Messwerte und Annahmen

Alle Maßangaben in mm. Ursprung `(0,0,0)` ist die Mitte der Unterseite von `Unten.stl`; +Z zeigt in diese Platte, der Fuß erstreckt sich in −Z. Die 77 mm werden wie zuvor besprochen als Abstand von der oberen Auflagefläche bis zum Boden **einschließlich 1 mm überstehendem Gummi** interpretiert. STL enthält keine eigene Einheit; Millimeter folgen aus Projekt und Motorzeichnung.

| Merkmal | Vom Nutzer am realen Aufbau angegeben | Aus `final/Unten.stl` gemessen |
|---|---:|---:|
| Oberer Auflagendurchmesser | 124 | 124,6 |
| Abstand gegenüberliegender Lochmitten | 113 | 115,6 |
| Durchmesser der vier Löcher | 4 | 4,5 |
| Motortasche, quadratisch | nicht separat gemessen | 42,6 × 42,6, Tiefe 4,95 |
| Standkreis unten | höchstens 250 | — |
| Gesamthöhe bis Boden | 77 | — |
| Treibergehäuse | 97 × 70 × 28 | nicht in STL enthalten |
| Platz für Treiberkabel | zusätzlich etwa 20 an einer Längsseite | nicht in STL enthalten |

Die im Projekt dokumentierte Motorbezeichnung ist `STEPPERONLINE 17HE19-2004S`; das [Herstellerdatenblatt](https://files.omc-stepperonline.com/17HE19-2004S_Full_Datasheet.pdf) nennt ein 48 mm langes Gehäuse. Diese Angabe und die Motorposition sind im digitalen Freiraumtest Annahmen, bis die Einbaulage gemessen ist.

**Wichtige Maßabweichung:** Die Achsen der alten STL liegen radial 1,3 mm neben den neuen Nutzermaßen. In den Ø4- und Ø4,5-Bohrungen ergibt sich für einen M3-Schaft zusammen nur 1,25 mm radiale Bewegungsreserve. Der neue Fuß ist daher auf das **bestätigte reale Lochbild Ø113** ausgelegt; eine direkte Schraubpassung gegen ein Teil, das exakt der gespeicherten STL entspricht, ist nominell nicht gegeben. Der ursprüngliche STL-Dateihash blieb `b657eb9beee4e406524f1b351296753bde1b388ae7aaf2460a3f7643e8865692`.

## 2. Geometrie des gedruckten Standfußes

Der tragende Körper ist ein rotationssymmetrischer, unten offener Kegelring. Sein exakt zu modellierendes Profil ist `(Radius, z) = (36,0) → (62,0) → (125,−76) → (100,−76) → zurück`. Außen- und Innenmantel sind jeweils geradlinig. Damit gelten für `−76≤z≤0`:

- `R_außen(z)=62+63·(−z)/76`;
- `R_innen(z)=36+64·(−z)/76`.

Außendurchmesser oben **124**, unten **250**; Innendurchmesser oben 72, unten 200. Die radiale Wandstärke beträgt 26 oben und 25 unten. Der Außenmantel hat 50,35° zur horizontalen Standfläche. Die breite Basis bildet einen geschlossenen Stützring, die Mitte bleibt offen. Oben liegt der Fuß plan auf dem vorhandenen äußeren Befestigungsbereich auf; die Mitte lässt Motor und Welle frei.

| Detail | Konstruktionsmaß |
|---|---|
| Gedruckte Höhe | `z=0…−76` = 76 |
| Standhöhe mit Gummi | `z=0…−77` = 77 |
| Vier Fußlöcher | Ø4, Achsen `(±56,5;0)` und `(0;±56,5)`, `z=0…−4` |
| Vier ebene Schraubenkopfauflagen | bei `z=−4` |
| Vier gerade Werkzeugkanäle | Ø10, dieselben Achsen, `z=−4…−34`; unten offen zum Innenraum |
| Untere Ringnut | radial `r=105…120`, axial `z=−76…−74`, Tiefe 2 |
| Gummiring | EPDM 70A, radial `r=105…120`, axial `z=−77…−74`, 15 breit und 3 dick, geklebt |
| Kabeldurchführung | radial Ø20, Winkel +45° ab +X zu +Y, Achshöhe `z=−54`, Schneidachse `r=65…125` |
| Zugentlastungsösen | zwei Zylinder Ø22 bei Radius 88, Winkeln +20° und +70°, `z=−57…−49`, jeweils axiales Ø5-Loch |
| Lüftung | drei radiale Ø18-Bohrungen bei 135°, 225° und 315°, Achshöhe `z=−60`, Schneidachse `r=70…130` |

Die drei Lüftungsöffnungen liegen räumlich getrennt vom Kabeldurchlass. Ihre Funktion ist passive Querlüftung; ausreichende Treibertemperatur wird dadurch **nicht** garantiert. In der fertigen Druckgeometrie sind Kabel- und Lüftungskanten scharf; nacharbeiten und insbesondere an der Kabelöffnung mit mindestens R2 glätten. Ein geteilter weicher Kantenschutz umschließt die Leitung an der Ø20-Öffnung. Die beiden Ösen ermöglichen Kabelbinder so, dass Zug nicht direkt an den Treiberklemmen wirkt. Die Leitung muss als lose Schlaufe vom Motor zum Treiber und dann zur Austrittsöffnung geführt werden; die reale Stecker- und Kabelposition ist vor endgültigem Betrieb sichtbar zu prüfen.

## 3. Befestigung, Werkzeug und Gewindering

Vier M3×16-Innensechskantschrauben, Kopf-Ø maximal 6 und Kopfhöhe maximal 3, gehen **von unten** durch den Fuß und die vorhandene Platte in einen separaten Stahlring. Ø4 ist eine sinnvolle M3-Durchgangsbohrung; für M4 wäre Ø4 nicht ausreichend. Ein gerades Werkzeug mit Außen-Ø maximal 8 passt durch den Ø10-Kanal. Die Zugangsbohrungen laufen bis `z=−34`, damit ein Bit auf jeder Achse tatsächlich vom offenen Fußinneren bis zum Schraubenkopf geschoben werden kann. Der kleinste radiale Materialsteg oben außerhalb eines Ø4-Lochs beträgt 3,5 mm; die Hauptlast liegt flächig auf dem ringförmigen Kontakt, nicht auf vier Kunststoffgewinden.

Der Stahlring hat Außen-Ø124, Innen-Ø100,4 und Dicke 6 bei `z=6…12`. Vier M3×0,5-6H-Gewinde liegen auf Lochkreis Ø113; das STEP zeigt Kernlöcher Ø2,5, die echte Gewindehelix ist Fertigungssache. Die nominelle STL-Oberwand Ø99,6 hat zur Ringöffnung 0,4 mm radial Luft. Bei 6 mm Dicke greift ein M3×16-Schaft von der Kopfauflage `z=−4` bis Ringoberseite `z=12` nominell über die volle Ringdicke. Schraubenlänge und reale Flanschdicke bei der Montage kontrollieren.

Der Ring wird von oben aufgelegt; alle **dauerhaften** Schrauben werden ausschließlich von unten eingeschraubt, angezogen und später gelöst. Zwei eingeschraubte Führungsstifte in noch freien Löchern halten den Ring während Ein- und Ausbau gegen Verdrehen. Der Treiber liegt lose unter der offenen Mitte und kann für Service zur Seite genommen werden; seine Lage im Betrieb ist so gewählt, dass auch mit dem angenommenen 20-mm-Kabelraum keine der vier geraden Ø8-Werkzeugbahnen berührt wird. Der reale Kabelstrang darf diese Bahnen bei der späteren Demontage nicht blockieren. Ob die bereits existierenden Motorschrauben von unten erreichbar sind, zeigt `Unten.stl` nicht.

## 4. Platzprüfung für Motor, Treiber und Kabel

Der Motor wurde im Prüfhüllkörper mittig mit 42,3 × 42,3 × 48 angenommen. Wenn seine Front an der 4,95 mm tiefen Tasche sitzt, liegt das hintere Gehäuseende bei `z=−43,05`. Die Bodenebene liegt bei `z=−77`; darunter stehen nominell **33,95 mm** zur Verfügung. Der Treiber ist 28 mm hoch. Er ist bewusst **nicht befestigt** und ruht auf der ebenen Stellfläche unter der offenen Fußmitte. In dieser Nennlage liegt er axial von `z=−77…−49` und hat **5,95 mm Luft** zum Motorende.

Für die digitale Passprobe ist das 97×70-Gehäuse in `x=−48,5…48,5`, `y=−40…30`, `z=−77…−49` gelegt. Die zusätzliche, 20 mm breite Kabelzone an einer Längsseite belegt `x=−48,5…48,5`, `y=30…50` in derselben Höhe. Damit bleibt das Gesamtpaket innerhalb `x=±48,5`, `y=−40…50`, `z=−77…−49`. Diese Orientierung übersetzt die Nutzerangabe „links an der Länge“ in eine prüfbare Annahme; der lose Treiber kann beim echten Kabelverlauf gedreht oder verschoben werden.

Die **CAD-Schnittprüfung** ergab in dieser Nennlage keine Überschneidung zwischen Treiber/Kabel-Hüllkörper und Kegelwand, dem passend ausgerichteten vorhandenen `17HE19-2004S.STEP` des Motors oder einer der vier geraden Ø8-Werkzeugbahnen. Bei der obersten Treiberkante `z=−49` hat die Innenwand Radius 77,3 mm; die äußerste Ecke des 97×90-Hüllrechtecks liegt bei Radius 69,7 mm. Die kleinste rechnerische Luft zur Innenwand ist somit rund **7,6 mm**. Zu den Werkzeugachsen bleiben in Projektion auf X/Y mindestens 4 mm am +/−X-Kanal und 2,5 mm am +Y-Kanal, unter der Annahme exakt begrenzter Kabelzone. Ein loses Kabel außerhalb dieser Zone kann den Zugang trotzdem versperren.

Steht das reale Gerät auf einer 1-mm-Unterlage, verringert sich der Motorabstand auf 4,95 mm; bei 3 mm Unterlage auf 2,95 mm. Gummikompression, wackeliger Boden, überstehende Klemmen oder dicke Kabel verringern die Reserven weiter. Der reale Aufbau muss bei Bewegung und unter Last beobachtet werden. Der Treiber braucht nach dem tatsächlichen Datenblatt und seiner Wärmeabgabe genügend Kühlluft; die drei Ø18-Öffnungen sind lediglich ein konstruktiver Startwert. Leitungen dürfen weder zwischen Fuß und Boden eingeklemmt noch an der Motorwelle aufgerieben werden.

## 5. Standsicherheit und Fertigung

Der Fuß wird unten auf Ø250 begrenzt. Der Gummiring berührt den Boden von Radius 105 bis 120. Für eine konservative Kippvorrechnung wird nur `r_eff=105` benutzt. Mit Boxmasse `m`, horizontalem Schwerpunktversatz `e`, Schwerpunkthöhe `H_S`, Bodenneigung `θ`, Seitenkraft `F` in Höhe `H_F` und gewünschtem Sicherheitsfaktor `S` gilt als Vorprüfung:

`e + H_S·tan(θ) + F·H_F/(m·g) ≤ 105/S`.

Die tatsächliche Lautsprechermasse, Schwerpunkthöhe und -lage, Seitenkräfte sowie Bodenreibung sind nicht dokumentiert. Daher ist die Kippstabilität noch nicht nachgewiesen. Eine große Box kann trotz breitem Fuß zusätzliche Bodenverankerung oder tiefen Ballast benötigen. Die Kunststoffflanschstege und die M3-Stahlschrauben sind für die tatsächliche Last separat zu beurteilen.

Den Fuß mit der **breiten Standseite auf dem Druckbett** drucken. Das Bett muss eine effektive freie Kreisfläche von Ø250 ohne äußeren Brim bieten; Slicer-Rand, erste Schicht und Endmaß prüfen. Als Ausgangspunkt: ASA oder vergleichbar temperaturgeeignetes Material, 5–6 Perimeter, etwa 40 % tragendes Infill. Druckziel Außen-Ø höchstens 250,0; Höhe 76 ±0,3; Loch-Ø4 +0,2/0; Achslage ±0,2; Ebenheit der oberen Auflage ≤0,3. Diese Werte sind Herstellziele und mit Probestück zu kalibrieren. Die inneren Kegelwände und seitlichen Rundöffnungen können Stützmaterial benötigen; alle Kanäle danach frei machen. Kabelöffnung auf R2 glätten und einen weichen Kantenschutz einsetzen. Nut und Gummiring rundum verkleben; Überstand 1,0 messen.

## 6. Digital geprüft und am Aufbau noch zu prüfen

Die STEP-Fußgeometrie ist ein gültiger, zusammenhängender Körper mit Bounding-Box `250×250×76`; der Stahlring ist ebenfalls ein gültiger Einzelkörper `124×124×6`. Die vier Schraubkanäle öffnen sichtbar zur Fußunterseite. Das Treiber/Kabel-Rechteck wurde im CAD gegen Kegel, vier vertikale Werkzeugzylinder und die Kabel-/Lüftungsdurchbrüche geprüft. Das vorhandene Motor-STEP wurde mit Front bei `z=4,95` und Welle nach +Z ausgerichtet und schneidet weder Fuß noch Treiberhülle. Die Lage der Gewindering-Oberseite relativ zu übrigen bewegten Teilen bleibt separat zu prüfen. Das vorhandene STL-Maßabweichungsproblem bleibt bestehen; der Hash der Ursprungsdatei wurde erneut bestätigt.

Vor einem endgültigen Druck beziehungsweise dem Betrieb des Lautsprechers müssen am **realen** Aufbau kontrolliert werden: Lochbild und Ø4-Passung mit einer einfachen Lehre; tatsächliches Motorende ab Auflagefläche; Treiberhöhe einschließlich Schraubklemmen, Kühlrippen und Kabelsteckern; Kabelbreite/Abbiegerichtung innerhalb der angenommenen 20 mm; verfügbare Lüftung und gemessene Temperatur; Freigang bei voller Drehbewegung; Boxgewicht/Schwerpunkt und Kippverhalten. Die STL allein kann diese Punkte nicht belegen. Kein Bestandteil der alten STL wurde bearbeitet.
