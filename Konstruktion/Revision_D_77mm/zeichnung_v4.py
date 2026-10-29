"""A3 envelope drawing, Revision D. Driver mount holes still to be measured."""

from __future__ import annotations

from math import atan, cos, degrees, radians, sin
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon, Rectangle

from standfuss_v4 import (
    HEIGHT, TOP_OUTER_R, BOTTOM_OUTER_R, TOP_INNER_R, BOTTOM_INNER_R,
    BOLT_CIRCLE_R, BOLT_THROUGH_D, HEAD_ACCESS_D, HEAD_SEAT_Z,
    HEAD_ACCESS_LOWER_Z, CABLE_ANGLE_DEG, CABLE_Z, CABLE_PASSAGE_D,
    LUG_R, LUG_PITCH_R, LUG_Z_MIN, LUG_Z_MAX, LUG_HOLE_D,
    VENT_ANGLES_DEG, VENT_Z, VENT_D,
    GROOVE_INNER_R, GROOVE_OUTER_R, GROOVE_DEPTH,
)
from gewindering_v4 import (
    OUTER_R as RING_OUTER_R, INNER_R as RING_INNER_R,
    BOTTOM_Z as RING_BOTTOM_Z, THICKNESS as RING_THICKNESS,
    M3_TAP_DRILL_D,
)

HERE = Path(__file__).resolve().parent
PDF = HERE / "Technische_Zeichnung_Standfuss_Rev_D_77mm_A3.pdf"
INK, BLUE, PALE, GREY, RED = "#142b34", "#17617b", "#e3ebee", "#73858a", "#9e2c29"


def page(title, subtitle, number):
    fig, ax = plt.subplots(figsize=(16.54, 11.69), dpi=150)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set(xlim=(0, 420), ylim=(0, 297), aspect="equal")
    ax.axis("off")
    ax.add_patch(Rectangle((6, 6), 408, 285, fill=False, ec=INK, lw=1))
    ax.plot([6, 414], [272, 272], color=INK, lw=.8)
    ax.plot([6, 414], [24, 24], color=INK, lw=.8)
    ax.text(12, 283, title, fontsize=15, weight="bold", color=INK, va="center")
    ax.text(12, 276, subtitle, fontsize=8, color=BLUE, va="center")
    ax.text(12, 15, "KLIPSCH-DREHPLATTE  |  REVISION D  |  MASSE IN mm  |  06.10.2026",
            fontsize=8, weight="bold", color=INK, va="center")
    ax.text(407, 15, f"BLATT {number}/4  •  A3", fontsize=8, color=INK,
            ha="right", va="center")
    return fig, ax


def txt(ax, x, y, value, size=7.5, color=INK, **kw):
    ax.text(x, y, value, fontsize=size, color=color, **kw)


def ln(ax, a, b, color=INK, width=.6, style="-"):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=width, ls=style)


def dim_h(ax, x1, x2, y, y0, label):
    ln(ax, (x1, y0), (x1, y+2), BLUE, .5)
    ln(ax, (x2, y0), (x2, y+2), BLUE, .5)
    ax.annotate("", (x1, y), (x2, y), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=.7))
    txt(ax, (x1+x2)/2, y+2.6, label, 8, BLUE, ha="center", va="bottom")


def dim_v(ax, y1, y2, x, x0, label):
    ln(ax, (x0, y1), (x+2, y1), BLUE, .5)
    ln(ax, (x0, y2), (x+2, y2), BLUE, .5)
    ax.annotate("", (x, y1), (x, y2), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=.7))
    txt(ax, x+3, (y1+y2)/2, label, 8, BLUE, rotation=90, va="center")


def sheet1():
    fig, ax = page("STANDFUSS – DRAUFSICHT UND ACHSSCHNITT",
                   "Teil 01  |  Fuß-Hüllkörper für STEP  |  Gesamthöhe mit Gummi 77,0", 1)
    txt(ax, 21, 258, "DRAUFSICHT  1:2", 9, weight="bold")
    cx, cy, s = 104, 177, .5
    for r, style, col in ((BOTTOM_OUTER_R, "--", GREY), (TOP_OUTER_R, "-", INK),
                          (TOP_INNER_R, "-", INK)):
        ax.add_patch(Circle((cx, cy), r*s, fill=False, ec=col, lw=.9, ls=style))
    ax.add_patch(Circle((cx, cy), BOLT_CIRCLE_R*s, fill=False, ec=GREY,
                        lw=.5, ls=(0, (3, 3))))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        ax.add_patch(Circle((cx+x*s, cy+y*s), BOLT_THROUGH_D*s/2,
                            fc="white", ec=INK, lw=.7))
    ln(ax, (cx-77, cy), (cx+77, cy), GREY, .45, "-.")
    ln(ax, (cx, cy-77), (cx, cy+77), GREY, .45, "-.")
    dim_h(ax, cx-TOP_OUTER_R*s, cx+TOP_OUTER_R*s, 231, cy, "Ø124,0 oben")
    dim_h(ax, cx-BOLT_CIRCLE_R*s, cx+BOLT_CIRCLE_R*s, 119, cy, "113,0 Achsabstand")
    txt(ax, 24, 108, "4 × Ø4,0 bei (±56,5;0), (0;±56,5)", 7.7, BLUE)
    txt(ax, 24, 101, "Ø72,0 Innenöffnung; gestrichelt Ø250,0 Basis", 7.6)

    txt(ax, 226, 258, "SCHNITT A–A  1:2  (durch ±X)", 9, weight="bold")
    cc, ty, q = 309, 209, .5
    def p(r, z): return cc+r*q, ty+z*q
    for sign in (-1, 1):
        poly = [p(sign*TOP_INNER_R, 0), p(sign*TOP_OUTER_R, 0),
                p(sign*BOTTOM_OUTER_R, -HEIGHT), p(sign*BOTTOM_INNER_R, -HEIGHT)]
        ax.add_patch(Polygon(poly, closed=True, fc=PALE, ec=INK, lw=.8, hatch="////"))
        bx = cc+sign*BOLT_CIRCLE_R*q
        ax.add_patch(Rectangle((bx-BOLT_THROUGH_D*q/2, ty+HEAD_SEAT_Z*q),
                               BOLT_THROUGH_D*q, -HEAD_SEAT_Z*q,
                               fc="white", ec=INK, lw=.6))
        ax.add_patch(Rectangle((bx-HEAD_ACCESS_D*q/2, ty+HEAD_ACCESS_LOWER_Z*q),
                               HEAD_ACCESS_D*q,
                               (HEAD_SEAT_Z-HEAD_ACCESS_LOWER_Z)*q,
                               fc="white", ec=INK, lw=.6))
        x1, x2 = sorted([cc+sign*GROOVE_INNER_R*q, cc+sign*GROOVE_OUTER_R*q])
        ax.add_patch(Rectangle((x1, ty-HEIGHT*q), x2-x1, GROOVE_DEPTH*q,
                               fc="white", ec=INK, lw=.5))
        ax.add_patch(Rectangle((x1, ty-(HEIGHT+1)*q), x2-x1, 3*q,
                               fc="#999b93", ec=GREY, lw=.5))
    # Nominal motor body only; installation face inferred from the STL pocket.
    motor_rear_z = 4.95 - 48.0
    ax.add_patch(Rectangle((cc-21.15*q, ty+motor_rear_z*q),
                           42.3*q, 48.0*q, fc="#a8b8bd", ec=INK,
                           lw=.7, hatch="xx", alpha=.72))
    txt(ax, cc, ty-20*q, "MOTOR", 6.2, INK, ha="center", va="center")
    ax.add_patch(Rectangle((cc-48.5*q, ty-77*q), 97*q, 28*q,
                           fc="#c8d3da", ec=INK, lw=.7, hatch="..", alpha=.75))
    txt(ax, cc, ty-63*q, "TREIBER", 6.2, INK, ha="center", va="center")
    ln(ax, (cc, ty+4), (cc, ty-(HEIGHT+1)*q-4), GREY, .5, "-.")
    dim_h(ax, cc-BOTTOM_OUTER_R*q, cc+BOTTOM_OUTER_R*q,
          ty-(HEIGHT+1)*q-12, ty-HEIGHT*q, "Ø250,0 unten")
    dim_v(ax, ty-(HEIGHT+1)*q, ty, 395, cc+BOTTOM_OUTER_R*q, "77,0 gesamt")
    txt(ax, 229, 146, "Fußkörper: 76,0; Gummi: 1,0 überstehend", 7.4, BLUE)
    txt(ax, 229, 138, "innen R(z)=36+64·(−z)/76", 7.4, BLUE)
    txt(ax, 229, 130, "außen R(z)=62+63·(−z)/76", 7.4, BLUE)
    txt(ax, 229, 122, "Treiber lose am Boden: oben 5,95 frei (nominal)", 7.0, RED)

    ln(ax, (14, 96), (406, 96), INK, .7)
    txt(ax, 18, 89, "FORM- UND FUNKTIONSMASSE", 8.5, weight="bold")
    left = [
        "A  Bezugsfläche oben z=0; Fußunterkante z=−76",
        "B  Rotationsprofil (r,z): (36,0), (62,0),",
        "    (125,−76), (100,−76); gerade Mantellinien",
        "C  4× Ø4 von z=0 bis Kopfauflage z=−4",
        "D  4× Ø10 Werkzeugkanal z=−4 … −34",
        "E  Lochkreis Ø113; gegenüber 113,0",
    ]
    right = [
        "F  Ringnut unten r=105 … 120, z=−76 … −74",
        "G  EPDM-Ring 70A, radial 15 × axial 3,",
        "    z=−77 … −74; außen Ø240, innen Ø210",
        "H  Kabelbohrung Ø20, θ=45°, z=−54",
        "J  Bohrwerkzeug radial r=65 … 125",
        "K  2 Ösen +20°/+70°: siehe Blatt 2",
    ]
    for i, row in enumerate(left): txt(ax, 18, 80-i*8.0, row, 7.5)
    for i, row in enumerate(right): txt(ax, 215, 80-i*8.0, row, 7.5)
    txt(ax, 18, 29, "Radien linear. Winkel Außenwand zur Standfläche: "
        f"{degrees(atan(HEIGHT/(BOTTOM_OUTER_R-TOP_OUTER_R))):.2f}°. "
        "Mitte unten offen Ø200. Alle nicht genannten Kanten ungerundet im STEP.", 7.4, BLUE)
    return fig


def sheet2():
    fig, ax = page("DETAILS – VERSCHRAUBUNG, GEWINDERING, KABEL",
                   "Teil 01 + Teil 02  |  Vier Schrauben ausschließlich von unten montieren und lösen", 2)
    txt(ax, 18, 258, "TEIL 02: STAHL-GEWINDERING  1:1", 9, weight="bold")
    cx, cy = 85, 186
    ax.add_patch(Circle((cx, cy), RING_OUTER_R, fc=PALE, ec=INK, lw=.9))
    ax.add_patch(Circle((cx, cy), RING_INNER_R, fc="white", ec=INK, lw=.8))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        ax.add_patch(Circle((cx+x, cy+y), M3_TAP_DRILL_D/2, fc="white", ec=INK, lw=.6))
    txt(ax, 18, 109, "Außen Ø124,0   •   Innen Ø100,4", 7.8)
    txt(ax, 18, 102, "4 × M3×0,5-6H durch; Kernloch Ø2,5", 7.8)
    txt(ax, 18, 95, "Lochkreis Ø113; Dicke 6; z=6 … 12", 7.8)
    txt(ax, 18, 88, "Stahl S235JR; Kanten 0,5×45° entgraten", 7.8)

    txt(ax, 185, 258, "DETAIL B: SCHRAUBACHSE  (Schema)", 9, weight="bold")
    sx, sy = 222, 202
    ax.add_patch(Rectangle((sx-27, sy-17), 54, 17, fc=PALE, ec=INK, hatch="////"))
    ax.add_patch(Rectangle((sx-27, sy), 54, 21, fc="white", ec=GREY, hatch="...."))
    ax.add_patch(Rectangle((sx-27, sy+21), 54, 21, fc="#c8d2d6", ec=INK, hatch="xx"))
    ax.add_patch(Rectangle((sx-4, sy-17), 8, 59, fc="white", ec=INK))
    ax.add_patch(Rectangle((sx-10, sy-45), 20, 28, fc="white", ec=INK))
    ax.add_patch(Rectangle((sx-3, sy-17), 6, 59, fc="#848f96", ec=INK))
    ax.add_patch(Rectangle((sx-6, sy-25), 12, 8, fc="#848f96", ec=INK))
    dim_v(ax, sy-17, sy, 260, sx+27, "4 Fuß")
    dim_v(ax, sy, sy+21, 272, sx+27, "6 STL")
    dim_v(ax, sy+21, sy+42, 285, sx+27, "6 Stahl")
    txt(ax, 188, 140, "M3×16 ISO 4762; Kopf Ø≤6, H≤3", 7.5, BLUE)
    txt(ax, 188, 132, "4 mm Fußbohrung; 10 mm Werkzeugkanal", 7.5, BLUE)
    txt(ax, 188, 124, "Bit/Verlängerung Außen-Ø≤8; von unten", 7.5, BLUE)
    txt(ax, 188, 116, "6 mm Stahlgewinde; M3-Bolzen bis z=12", 7.5, BLUE)
    txt(ax, 188, 108, "Auflagefläche des Kopfes z=−4", 7.5, BLUE)

    ln(ax, (14, 81), (406, 81), INK, .7)
    txt(ax, 18, 74, "KABELAUSGANG UND ZUGENTLASTUNG", 8.5, weight="bold")
    cable = [
        "Radialkanal Ø20; Achse θ=45° ab +X gegen +Y; z=−54; Schnitt r=65 … 125.",
        "2 Ösen: Vollzylinder Ø22; Mittelpunkt r=88 bei θ=20° und 70°; z=−57 … −49.",
        "Je Öse Ø5 axial durchgehend. Zwei Kabelbinder halten eine entspannte Kabelschlaufe.",
        "Geteilter weicher Einsatz/Silikonschlauch im Ø20-Durchlass; Innen-Ø passend zum Ist-Kabel.",
        "Ein- und Austrittskanten des Kabelkanals nach dem Druck glätten, Mindest-R2; keine Klemmstelle.",
        "3 Lüftungsöffnungen Ø18 radial bei θ=135°/225°/315°, z=−60; Achse r=70 … 130.",
    ]
    for i, row in enumerate(cable): txt(ax, 18, 66-i*6, row, 7.25)
    return fig


def sheet3():
    fig, ax = page("MASSTABELLE – MONTAGE UND DIGITALER ABGLEICH",
                   "Fuß-Hüllkörper definiert  |  Treiber liegt lose auf dem Boden  |  reale Kabel-/Wärmeprobe nötig", 3)
    txt(ax, 14, 258, "KOORDINATEN UND BAUTEILE", 9, weight="bold")
    rows = [
        "Ursprung: Mitte der Unterseite von Unten.stl; +Z zeigt in die Drehplatte; Fuß nach −Z.",
        "Fuß: Außen Ø124 oben/Ø250 unten; innen Ø72 oben/Ø200 unten; 76 Körper +1 Gummi.",
        "Vier Fußlöcher Ø4: (±56,5;0), (0;±56,5). Ø10 Kopf-/Werkzeugkanal auf denselben Achsen.",
        "Gewindering: Außen Ø124, Innen Ø100,4; z=6 … 12; vier M3×0,5 auf denselben Achsen.",
        "Ringnut: r=105 … 120, z=−76 … −74; EPDM 70A Dicke 3, geklebt.",
        "Kabeldurchlass und Ösen: alle Koordinaten siehe Blatt 2; freies Zentrum ohne Bodenplatte.",
        "Nicht dargestellte Gewindehelix und EPDM-Ring sind Fertigungsangaben, nicht Teil der STEP-Dateien.",
    ]
    for i, row in enumerate(rows): txt(ax, 15, 246-i*9, row, 7.8)

    ln(ax, (14, 174), (406, 174), INK, .7)
    txt(ax, 14, 164, "GEMESSENE STL GEGEN BESTÄTIGTE REALMASSE", 9, weight="bold")
    txt(ax, 15, 151, "Unten.stl: Flansch Ø124,6; 4×Ø4,5; Lochkreis Ø115,6; Motortasche 42,6×42,6×4,95.", 8)
    txt(ax, 15, 140, "Reales Teil laut Nutzer: Auflage Ø124; Gegenabstand 113; Loch-Ø4.", 8)
    txt(ax, 15, 129, "Lochachsen der STL liegen um 1,3 mm radial neben den neuen Achsen.", 8, RED, weight="bold")
    txt(ax, 15, 118, "Mit unveränderter STL ist die Schraubpassung nominell nicht nachgewiesen; reale Passprobe nötig.", 8, RED)

    ln(ax, (14, 108), (406, 108), INK, .7)
    txt(ax, 14, 99, "MOTORABSTAND, TOLERANZEN UND FREIGABE", 9, weight="bold")
    notes = [
        "Motor 17HE19-2004S laut Hersteller: Körperlänge 48,0. Bei Front z=4,95: Rückseite z=−43,05.",
        "Bodenebene mit Gummi z=−77: rechnerisch 33,95 bis zum Motorende, vor Toleranz und Kabeln.",
        "Treiber 97×70×28 lose am Boden: z=−77 … −49, oben 5,95 Luft; 20 mm Kabelzone längsseitig.",
        "Druckziel: Höhe Fuß ±0,3; Loch-Ø4 +0,2/0; Achslage ±0,2; Ebenheit oben ≤0,3.",
        "Passflächen entgraten. 5–6 Perimeter; ASA oder gleichwertig; Material und Last am Muster prüfen.",
        "Drucklage: breite Unterseite auf dem Bett; Ø250 Bauraum ohne äußeren Brim nötig.",
        "Stabilität: Boxmasse, Schwerpunktshöhe/-versatz, seitliche Kraft und Reibung noch unbekannt.",
    ]
    for i, row in enumerate(notes):
        txt(ax, 15, 88-i*8.1, row, 7.45, RED if i in (1, 2) else INK)
    return fig


def sheet4():
    fig, ax = page("XY-LAGEPLAN – MOTOR, TREIBER UND KABELRAUM",
                   "Koordinatenprojektion: +X rechts, +Y oben  |  Die z-Höhen stehen in der Tabelle rechts", 4)
    cx, cy, s = 114, 151, .78
    txt(ax, 21, 258, "PROJEKTION AUF XY  ca. 1:1,3", 9, weight="bold")
    for r, style, col in ((125, "-", INK), (120, "--", GREY),
                          (105, "--", GREY), (100, "-", INK), (36, "-", GREY)):
        ax.add_patch(Circle((cx, cy), r*s, fill=False, ec=col, lw=.75, ls=style))
    ln(ax, (cx-102, cy), (cx+102, cy), GREY, .35, "-.")
    ln(ax, (cx, cy-102), (cx, cy+102), GREY, .35, "-.")

    # Nominal driver with one 20 mm cable strip on its long +Y edge.
    ax.add_patch(Rectangle((cx-48.5*s, cy-40*s), 97*s, 70*s,
                           fc="#cad8dc", ec=INK, lw=.75, alpha=.72))
    ax.add_patch(Rectangle((cx-48.5*s, cy+30*s), 97*s, 20*s,
                           fc="#eee0b9", ec=BLUE, lw=.65, alpha=.8))
    txt(ax, cx, cy-11*s, "TREIBER 97×70", 6.5, ha="center", va="center")
    txt(ax, cx, cy+40*s, "+20 KABEL", 6.3, ha="center", va="center")
    ax.add_patch(Rectangle((cx-21.15*s, cy-21.15*s), 42.3*s, 42.3*s,
                           fill=False, ec=RED, lw=.85, ls="--"))
    txt(ax, cx, cy+2*s, "MOTOR", 6.1, RED, ha="center", va="center")

    # Screw and straight tool sweep axes.
    for x, y in ((56.5, 0), (0, 56.5), (-56.5, 0), (0, -56.5)):
        ax.add_patch(Circle((cx+x*s, cy+y*s), 4*s, fc="white", ec=BLUE, lw=.85))
        ax.add_patch(Circle((cx+x*s, cy+y*s), 2*s, fc="white", ec=INK, lw=.5))

    # Cable port at 45 degrees, lugs on either side; vents in the other sectors.
    for angle in (20, 70):
        x = 88*cos(radians(angle)); y = 88*sin(radians(angle))
        ax.add_patch(Circle((cx+x*s, cy+y*s), 11*s, fill=False,
                            ec=BLUE, lw=.7, ls="--"))
        ax.add_patch(Circle((cx+x*s, cy+y*s), 2.5*s, fc="white", ec=BLUE, lw=.6))
    for angle in (45, 135, 225, 315):
        inner = (cx+104*s*cos(radians(angle)), cy+104*s*sin(radians(angle)))
        outer = (cx+126*s*cos(radians(angle)), cy+126*s*sin(radians(angle)))
        ln(ax, inner, outer, RED if angle == 45 else BLUE, 3.3)
    txt(ax, 14, 35, "rot: Kabel Ø20  |  blau: 3× Lüftung Ø18  |  Kreise: Ösen und Werkzeugachsen", 7, BLUE)

    ln(ax, (228, 40), (228, 255), INK, .65)
    txt(ax, 238, 251, "LAGE UND HÖHEN", 9, weight="bold")
    rows = [
        "XY-DATUM: Motorachse (0;0)",
        "Körper: Ø124 oben / Ø250 unten",
        "Gummi: r=105…120, z=−77…−74",
        "Treiber: x=−48,5…48,5",
        "            y=−40…30; z=−77…−49",
        "Kabelraum: x=−48,5…48,5",
        "             y=30…50; z=−77…−49",
        "Motor: x/y≈±21,15; Ende z=−43,05*",
        "Axial frei: 5,95 bei 0 mm Unterlage*",
        "*Motorlage und Kabel nachmessen.",
        "4× Fußloch Ø4: (±56,5;0)/(0;±56,5)",
        "4× Werkzeugbahn Ø8 senkrecht, unten",
        "Kabel Ø20: θ=45°, z=−54, r=65…125",
        "Ösen Ø22/Ø5: θ=20°/70°, r=88",
        "               z=−57…−49",
        "Lüftung 3×Ø18: θ=135°/225°/315°",
        "               z=−60, r=70…130",
        "Koordinatenprojektion: z-Lagen beachten.",
    ]
    for i, row in enumerate(rows):
        txt(ax, 238, 239-i*10.5, row, 7.15, RED if i in (7, 8, 9) else INK)
    return fig


def main():
    sheets = [sheet1(), sheet2(), sheet3(), sheet4()]
    with PdfPages(PDF) as pdf:
        for n, fig in enumerate(sheets, 1):
            pdf.savefig(fig)
            fig.savefig(HERE / f"zeichnung_rev_d_blatt_{n}.png", dpi=150)
            plt.close(fig)
    print(PDF)


if __name__ == "__main__":
    main()
