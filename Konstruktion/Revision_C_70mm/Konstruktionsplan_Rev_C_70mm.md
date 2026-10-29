# Standfuß Revision C – 70 mm Gesamthöhe, Ø250 mm Standkreis (überholt)

**Aktueller Entwurf:** [Revision D mit 77 mm Gesamthöhe und losem Treiber](../Revision_D_77mm/Konstruktionsplan_Rev_D_77mm.md).

Stand: 06.10.2026. Maßgebliche Dateien: [A3-Zeichnung](Technische_Zeichnung_Standfuss_Rev_C_70mm_A3.pdf), [parametrischer Fuß](standfuss_v3.py), [Fuß als STEP](standfuss_v3.step), [Gewindering als STEP](gewindering_v3.step). Die STEP-Dateien bilden den **Fuß-Hüllkörper und den Gewindering** ab. Der Treiber ist nach Nutzermaß **100 × 75 × 40 mm, zuzüglich Kabel- und Lüftungsraum**. Eine flache direkte Stapelung unter dem dokumentierten Motor ist innerhalb von 70 mm unmöglich; der Fuß ist daher noch kein freigegebenes Druckteil. `final/Unten.stl` bleibt unverändert.

## Bezug und gesicherte Angaben

Alle Maße sind mm. Ursprung `(0,0,0)` ist die Mitte der Unterseite von `Unten.stl`; +Z zeigt in das vorhandene Teil, der Fuß liegt in −Z. STL selbst speichert keine Einheit; Millimeter folgen aus dem Projektkontext. Der Nutzer hat am realen Teil **Ø124 Auflage, 113 gegenüberliegender Lochmittenabstand und Ø4 Bohrungen** bestätigt. Er verlangt **maximal Ø250 unten** und nun **70 mm Gesamthöhe**; der Treiber soll **flach unter dem Motor** liegen. Wie bei der vorher bestätigten 44-mm-Angabe wird Gesamthöhe von der Auflagefläche bis zum Boden **einschließlich des überstehenden Gummis** verstanden.

Die unveränderte `final/Unten.stl` (SHA-256 `b657eb9beee4e406524f1b351296753bde1b388ae7aaf2460a3f7643e8865692`) liefert andere Befestigungsmaße:

| Merkmal | Vorhandene STL, digital gemessen | Neues Modell nach Nutzerangabe |
|---|---:|---:|
| Befestigungsflansch, Außen-Ø | 124,6 | 124,0 |
| Vier Durchgangslöcher | Ø4,5 | Ø4,0 |
| Gegenüberliegende Lochmitten / Lochkreis | 115,6 | 113,0 |
| Lochmittelpunkte auf X/Y | ±57,8 | ±56,5 |
| Motortasche | 42,6 × 42,6, Tiefe 4,95 | vorhandene Geometrie wird nicht geändert |

Die Lochachsen der gespeicherten STL liegen radial **1,3 mm** außerhalb der neuen Achsen. Die nominelle gemeinsame radiale Bewegungsreserve eines M3-Schaftes in Ø4 und Ø4,5 beträgt nur `0,5+0,75=1,25 mm`. **Eine Verschraubung des neuen Fußes mit einem Teil nach genau dieser STL ist geometrisch nicht gesichert.** Die real gemessenen Werte haben für das neue Modell Vorrang; eine Passprobe am realen Teil ist erforderlich. Die STL beweist weder die Form noch die Maßhaltigkeit eines bereits gedruckten Teils.

## Vollständig bemaßte Fuß-Außenform

Der Fußkörper ist ein offener Rotationskörper aus dem Polygon `(r,z) = (36,0), (62,0), (125,−69), (100,−69)`. Die Mantellinien sind gerade. Daraus folgen die exakten Funktionen `R_außen(z)=62+63·(−z)/69` und `R_innen(z)=36+64·(−z)/69` für `−69≤z≤0`. Die Außenwand steht 47,60° zur Standfläche. Die radiale Wandstärke beträgt oben 26, unten 25 mm. Die offene Mitte ist oben Ø72 und unten Ø200. Die Kontur hat weder Bodenplatte noch ungezeichnete Rippen.

| Stelle | Sollwert |
|---|---:|
| Obere Kontaktfläche | eben `z=0`, Ring `r=36…62`, Außen-Ø124 |
| Gedruckte Unterkante | `z=−69`, Außen-Ø250, Öffnung Ø200 |
| Standfläche mit Gummi | `z=−70`, Gesamthöhe 70 |
| Nut an der Unterseite | `r=105…120`, `z=−69…−67` |
| Gummiring | EPDM 70A, innen Ø210, außen Ø240, Dicke 3; geklebt; 1 mm vorstehend |
| Fußschrauben | vier Achsen `(±56,5;0)` und `(0;±56,5)`, Ø4 von `z=0…−4` |
| Kopfauflagen / Werkzeugkanäle | je Ø10 von `z=−4…−34`, Kopfauflage bei `z=−4` |
| Kabeldurchlass | radial Ø20, Polarwinkel +45°, Achshöhe `z=−54`, Werkzeugachse `r=65…125` |
| Zwei Kabelbinderösen | Vollzylinder Ø22, Zentren `r=88`, Winkel +20°/+70°, `z=−57…−49`; axial Ø5 |

Der Ø20-Kabelkanal durchstößt die geneigte Wand vollständig: bei `z=−44` reicht der innere Wandradius nur bis 76,8 mm, bei `z=−64` der äußere bis 120,4 mm. Die Modell-Schneidstrecke `r=65…125` liegt auf beiden Seiten frei. Die Ösen liegen beidseits des Kabelkanals und sind im CAD mit der Wand verschmolzen.

## Verschraubung ausschließlich von unten

Vorgesehen sind **vier M3×16 Innensechskantschrauben nach ISO 4762**, Kopf-Ø höchstens 6 mm, Kopfhöhe höchstens 3 mm. Ø4 im gedruckten Fuß ist eine M3-Durchgangsbohrung; Ø4 wäre für M4 als verlässliches Durchgangsmaß zu klein. Der Kopf liegt bei `z=−4`. Ein gerader Bit oder eine Verlängerung mit maximal Ø8 läuft von unten durch den offenen Fuß in den Ø10-Zugang. Die Kopfaufnahme bietet 4 mm radialen freien Durchmesser gegenüber einem Ø6-Kopf. Das gedruckte Gewinde trägt **keine** Schraubenlast.

Oben liegt ein separater Stahlring: außen Ø124, innen Ø100,4, Dicke 6, `z=6…12`, vier **M3×0,5-6H** durch auf Lochkreis Ø113 (Kernloch Ø2,5 im STEP). Stahl S235JR oder gleichwertig; Ringkanten 0,5×45° entgraten. Der nominelle obere Körper der STL ist Ø99,6, also 0,4 mm radial kleiner als die Ringöffnung. Ein M3×16-Schaft reicht rechnerisch von Kopfauflage `z=−4` bis `z=12`, damit durch 6 mm Stahlgewinde; tatsächliche Schraubenlänge, Flanschdicke und Ringlage sind nachzumessen. Der Ring muss von oben vor dem endgültigen Aufbau eingesetzt werden können.

Für Montage und späteres Lösen zwei passende M3-Führungsstifte **von unten** durch freie Bohrungen in den Ring schrauben; damit bleibt er beim Lösen der letzten Schraube gegen Verdrehen gehalten. Alle vier dauerhaften Befestigungsschrauben werden ausschließlich von unten eingesetzt und gelöst. Zugang zu bereits vorhandenen Motorschrauben und zum Raum oberhalb des Flanschs ist aus der STL nicht belegbar. Der Ring darf keine drehenden Teile berühren. Lastverteilung, Anziehdrehmoment und Dauerfestigkeit müssen an der realen Box geprüft werden.

## Motor und flacher Treiber

Der [Hersteller-Datensatz zum STEPPERONLINE 17HE19-2004S](https://files.omc-stepperonline.com/17HE19-2004S_Full_Datasheet.pdf) nennt eine nominelle Motor-Gehäuselänge 48 mm. **Falls** die Front an der oberen Ebene der 4,95 mm tiefen STL-Motortasche anliegt, endet das Gehäuse bei `z=4,95−48=−43,05`. Zur Bodenebene `z=−70` sind das **26,95 mm**. Das ist eine Rechnung mit Nennmaßen und angenommener Einbaulage, kein gemessener Freiraum.

| Ebene | Innerer Radius des Fußes | Bedeutung |
|---|---:|---|
| `z=−43,05` | 75,9 | nominales Motorende |
| `z=−50` | 82,4 | Treiberbereich |
| `z=−60` | 91,7 | Treiberbereich |
| `z=−66` | 97,2 | möglicher Trägerring nahe Boden |
| `z=−69` | 100,0 | offene Fußunterseite |

Der **gemessene Treiber 100 × 75 × 40 mm** überschreitet den maximalen Raum direkt unter dem Motor **bereits um 13,05 mm**, bevor Montageplatte, Luft und Kabel berücksichtigt sind. Beispiel für eine herausnehmbare 3-mm-Trägerplatte bei `z=−68…−65`: Unter dem Motor bleiben von der Trägeroberseite bis `z=−43,05` 21,95 mm; bei 2 mm Sicherheitsabstand dürften Gerät und überstehende Bauteile höchstens **19,95 mm** hoch sein. Der reale Treiber ist doppelt so hoch. Für direkte Stapelung wären mindestens `43,05+40=83,05 mm` Gesamthöhe nötig, praktisch mehr für Träger, Kabel und Kühlung. Dieses Beispiel ist **noch kein konstruiertes Tray**. Ein nur lose auf den Boden gestellter Treiber ist für Kabelzug, Wärme und Wartung keine dauerhafte Befestigung.

Ein seitlich versetzter, weiterhin flach liegender Treiber könnte den Motor in der Höhe überlappen. Dafür muss die innere Wand im oberen Treiberbereich stark weiter geöffnet werden. Eine reine Rechteck-Hüllkörperrechnung zeigt: Bei 3 mm Abstand zum 42,3-mm-Motor und radial ausgerichteter 75-mm-Treiberseite müsste der Treiber ungefähr 61,7 mm seitlich verschoben werden; seine äußerste Ecke liegt dann schon bei Radius **111,1 mm**. Ein Ø250-Standkreis bietet dort maximal Radius 125 mm. Für Wand, Drucktoleranz, Lüftung und auslaufende Kabel blieben zusammen nur **13,9 mm**. Die aktuelle lineare Kegelform bietet bei `z≈−29` innen nur Radius 62,9 mm und lässt diese Lage **nicht** zu. Eine andere Innen- und Außenkontur wäre erforderlich; ob sie mit Kabeln und stabiler Wand möglich ist, hängt von der noch fehlenden Anschlusslage und dem Freiraumbedarf ab.

Der Motoranschluss wird im Innenraum mit entspannter Schlaufe zum Treiber geführt. Die Kabelbinderösen halten den Strang vor der radialen Durchführung; ein geteilter weicher Kantenschutz sitzt im Ø20-Durchlass, die Ein- und Austrittskanten werden nach dem Druck auf mindestens R2 geglättet. Kein Kabel darf Motor, Welle, Kupplung oder Schraubwerkzeugbahn berühren. Positionen des Treibers, seiner Klemmen, externer Versorgung/Steuerleitung und erforderliche Lüftungsöffnungen lassen sich ohne reale Abmessungen **nicht verbindlich festlegen**. Bei einem geschlossenen Boden oder blockierter Belüftung würde ein Leistungstreiber Wärme stauen; auch das ist am laufenden Aufbau zu prüfen.

## Stabilität, Druck und Passprobe

Die Standbasis ist jetzt Ø250 statt Ø300; der tragende Gummiring reicht nur bis Radius 120. Für eine konservative Kippvorrechnung wird der innere Kontaktradius **105 mm** verwendet. Mit Boxmasse `m`, Schwerpunktversatz `e`, Schwerpunkthöhe `H_S`, Bodenneigung `θ`, Seitenkraft `F` in Höhe `H_F` und gewünschtem Sicherheitsfaktor `S` gilt als Vorprüfung: `e + H_S·tan(θ) + F·H_F/(m·g) ≤ 105/S`. Weder `m`, `e`, `H_S`, `F`, `H_F` noch die Bodenreibung sind bekannt; der Ø250-Fuß ist daher **nicht als kippsicher nachgewiesen**. Gegebenenfalls Ballast, Bodenbefestigung oder eine andere Aufstellung vorsehen.

Der Fuß wird mit der breiten Unterseite auf das Druckbett gestellt. Der effektive Bauraum muss mindestens Ø250 **ohne äußeren Brim** zulassen; Slice-Vorschau und erste Schicht prüfen. Außendurchmesser im Druck auf höchstens 250,0 mm kalibrieren. Als Ausgangspunkt: ASA oder ein für Temperatur und Last geeignetes Material, 5–6 Perimeter, ca. 40 % tragfähiges Infill; die Kontaktfläche plan halten (Ziel-Ebenheit ≤0,3), Höhe ±0,3, Bohrungen Ø4 +0,2/0 und Achslage ±0,2. Diese Druckwerte sind Prozessziele, keine aus der STL gemessenen Eigenschaften. Unvermeidliche Stützen an der inneren Flanke entfernen, Schraubzugang und Kabelkanal frei halten. Nach dem Druck alle Kanten entgraten, insbesondere Kabel-R2. Die fertige Basis darf inklusive Fertigungstoleranz den Druckraum nicht überschreiten.

Digitale Prüfung mit CAD: Fuß und Ring sind jeweils gültige Einzelkörper, Fuß-Bounding-Box `250×250×69`, Ring `124×124×6`. Die Bohrungsachsen und freien Werkzeugkanäle sind im Modell koaxial; das Motor-Hüllmaß und die Abweichung zur STL sind berechnet. `Unten.stl` wurde nur gelesen und per SHA-256 auf Unverändertheit geprüft. Die STEP-Dateien enthalten keine gedrehte Gewindehelix, keinen Gummiring und noch keine Treiberhalterung.

**Für den nächsten passgenauen Schritt fehlen:** Treiber-Bohrbild, Lage und Überstand aller Klemmen und eingesteckten Kabel, erforderlicher Lüftabstand laut realem Gerät, tatsächlicher Abstand vom eingebauten Motorende zur Auflagefläche. Für den Standsicherheitsnachweis zusätzlich Boxmasse und Schwerpunktshöhe/-versatz. Zunächst muss entschieden werden, ob der Treiber innerhalb der 70-mm-Hülle **seitlich versetzt** werden darf oder für eine direkte Stapelung die Höhe erhöht werden soll. Danach lässt sich der Träger mit von unten erreichbaren Schrauben und gesicherter Kabelroute konstruieren und digital gegen Motor und Treiber prüfen.
