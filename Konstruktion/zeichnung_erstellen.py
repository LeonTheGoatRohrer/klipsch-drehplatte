"""Create the three-sheet, dimensioned A3 drawing for stand foot and nut ring.

All dimensions and datums are mirrored from standfuss.py / gewindering.py.
Run with the project's Python environment; no STL is written or modified.
"""

from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon, Rectangle

from standfuss import (
    BOLT_CIRCLE_R, BOLT_THROUGH_D, BOSS_BOTTOM_Z, BOSS_R, BOSS_TOP_Z,
    BOTTOM_INNER_R, BOTTOM_OUTER_R, CABLE_ANGLE_DEG, CABLE_PASSAGE_D,
    CABLE_Z, GROOVE_DEPTH, GROOVE_INNER_R, GROOVE_OUTER_R,
    HEAD_ACCESS_D, HEAD_ACCESS_LOWER_Z, HEAD_SEAT_Z, HEIGHT, LUG_HOLE_D,
    LUG_PITCH_R, LUG_R, LUG_Z_MAX, LUG_Z_MIN, TOP_INNER_R, TOP_OUTER_R,
)
from gewindering import INNER_R as RING_INNER_R
from gewindering import OUTER_R as RING_OUTER_R
from gewindering import THICKNESS as RING_THICKNESS


HERE = Path(__file__).resolve().parent
PDF = HERE / "Technische_Zeichnung_Standfuss_A3.pdf"
INK = "#13232b"
FILL = "#dfe7e9"
OLD = "#76919c"
DIM = "#235d73"


def page(title: str, subtitle: str, sheet: str):
    fig, ax = plt.subplots(figsize=(16.54, 11.69), dpi=150)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 297)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((6, 6), 408, 285, fill=False, ec=INK, lw=1.0))
    ax.plot([6, 414], [274, 274], color=INK, lw=0.8)
    ax.plot([6, 414], [24, 24], color=INK, lw=0.8)
    ax.text(12, 284, title, fontsize=15, weight="bold", color=INK, va="center")
    ax.text(12, 277, subtitle, fontsize=7.8, color=INK, va="center")
    ax.text(12, 15, "KLIPSCH DREHPLATTE  |  STANDFUSS  |  ALLE MASSE IN mm", fontsize=8,
            weight="bold", color=INK, va="center")
    ax.text(405, 15, f"06.10.2026  •  BLATT {sheet}/3", fontsize=7.5,
            color=INK, ha="right", va="center")
    return fig, ax


def line(ax, xy1, xy2, color=INK, lw=0.7, ls="-"):
    ax.plot((xy1[0], xy2[0]), (xy1[1], xy2[1]), color=color, lw=lw, ls=ls)


def text(ax, x, y, s, size=8, **kw):
    ax.text(x, y, s, fontsize=size, color=kw.pop("color", INK), **kw)


def dim_h(ax, x1, x2, y, from_y, label, size=7.5):
    line(ax, (x1, from_y), (x1, y + 2), DIM, 0.5)
    line(ax, (x2, from_y), (x2, y + 2), DIM, 0.5)
    ax.annotate("", (x1, y), (x2, y), arrowprops=dict(arrowstyle="<->", color=DIM,
                                                    lw=0.7, mutation_scale=7))
    text(ax, (x1 + x2) / 2, y + 2.3, label, size, color=DIM, ha="center", va="bottom")


def dim_v(ax, y1, y2, x, from_x, label, size=7.5):
    line(ax, (from_x, y1), (x + 2, y1), DIM, 0.5)
    line(ax, (from_x, y2), (x + 2, y2), DIM, 0.5)
    ax.annotate("", (x, y1), (x, y2), arrowprops=dict(arrowstyle="<->", color=DIM,
                                                    lw=0.7, mutation_scale=7))
    text(ax, x + 3, (y1 + y2) / 2, label, size, color=DIM, rotation=90,
         va="center", ha="left")


def leader(ax, xy, end, label, size=7.5, va="center"):
    line(ax, xy, end, DIM, 0.6)
    text(ax, end[0] + 1.2, end[1], label, size, color=DIM, va=va)


def section_polygon(ax, points):
    ax.add_patch(Polygon(points, closed=True, fc=FILL, ec=INK, lw=0.7, hatch="////"))


def make_sheet_1():
    fig, ax = page("TECHNISCHE ZEICHNUNG — STANDFUSS",
                   "Teil 01 • Kegelring • Oberseite z=0 • Unterseite z=−90 • Ansichten 1:2 • technische Sollgeometrie", "1")

    # Top view, including projected lower outer contour.
    cx, cy, scale = 104, 177, 0.50
    text(ax, 25, 258, "DRAUFSICHT  (Blick auf Anschlussflaeche)", 9, weight="bold")
    for radius, style, width in ((BOTTOM_OUTER_R, "--", 0.7),
                                 (TOP_OUTER_R, "-", 0.9),
                                 (TOP_INNER_R, "-", 0.9)):
        ax.add_patch(Circle((cx, cy), radius * scale, fill=False, ec=INK,
                            ls=style, lw=width))
    ax.add_patch(Circle((cx, cy), BOLT_CIRCLE_R * scale, fill=False, ec=OLD,
                        ls=(0, (2, 2)), lw=0.55))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        ax.add_patch(Circle((cx + x * scale, cy + y * scale),
                            BOLT_THROUGH_D * scale / 2, fc="white", ec=INK, lw=0.7))
    line(ax, (cx - 77, cy), (cx + 77, cy), OLD, 0.4, "-.")
    line(ax, (cx, cy - 77), (cx, cy + 77), OLD, 0.4, "-.")
    leader(ax, (cx + TOP_OUTER_R * scale * 0.71, cy + TOP_OUTER_R * scale * 0.71),
           (135, 241), "oben Ø132")
    leader(ax, (cx + TOP_INNER_R * scale * 0.65, cy - TOP_INNER_R * scale * 0.75),
           (128, 146), "Oeffnung Ø72")
    text(ax, 24, 107, "gestrichelt: Standflaeche Ø300", 7.5, color=OLD)

    # Axial section through two opposing screw axes.
    scx, top_y, s = 309, 217, 0.50
    text(ax, 230, 258, "SCHNITT A–A  (durch ±X-Schraubachsen)", 9, weight="bold")
    def P(r, z): return (scx + r * s, top_y + z * s)
    for sign in (-1, 1):
        section_polygon(ax, [P(sign * TOP_INNER_R, 0), P(sign * TOP_OUTER_R, 0),
                             P(sign * BOTTOM_OUTER_R, -HEIGHT),
                             P(sign * BOTTOM_INNER_R, -HEIGHT)])
        bolt_x = scx + sign * BOLT_CIRCLE_R * s
        ax.add_patch(Rectangle((bolt_x - BOLT_THROUGH_D*s/2, top_y + HEAD_SEAT_Z*s),
                               BOLT_THROUGH_D*s, -HEAD_SEAT_Z*s,
                               fc="white", ec=INK, lw=0.45))
        ax.add_patch(Rectangle((bolt_x - HEAD_ACCESS_D*s/2,
                                top_y + HEAD_ACCESS_LOWER_Z*s),
                               HEAD_ACCESS_D*s,
                               (HEAD_SEAT_Z-HEAD_ACCESS_LOWER_Z)*s,
                               fc="white", ec=INK, lw=0.45))
        gx1 = scx + sign * GROOVE_INNER_R * s
        gx2 = scx + sign * GROOVE_OUTER_R * s
        ax.add_patch(Rectangle((min(gx1, gx2), top_y - HEIGHT*s),
                               abs(gx2-gx1), GROOVE_DEPTH*s,
                               fc="white", ec=INK, lw=0.45))
    line(ax, (scx, top_y + 4), (scx, top_y - HEIGHT*s - 3), OLD, 0.4, "-.")
    dim_h(ax, scx - BOTTOM_OUTER_R*s, scx + BOTTOM_OUTER_R*s,
          top_y - HEIGHT*s - 11, top_y - HEIGHT*s, "Ø300")
    dim_h(ax, scx - TOP_OUTER_R*s, scx + TOP_OUTER_R*s,
          top_y + 11, top_y, "Ø132")
    dim_v(ax, top_y - HEIGHT*s, top_y, 397, scx + BOTTOM_OUTER_R*s, "90")
    text(ax, 235, 154, "innen: R=36 + 89·(−z)/90", 7.5, color=DIM)
    text(ax, 235, 148, "aussen: R=66 + 84·(−z)/90", 7.5, color=DIM)

    # Dimension and definition tables.
    line(ax, (14, 97), (406, 97), INK, 0.7)
    text(ax, 17, 92, "HAUPTMASSE  (mm)", 8.5, weight="bold")
    rows_l = [
        "A  Gesamthoehe: 90.0; Bezug oben z=0",
        "B  Aussen: Ø132.0 oben / Ø300.0 unten",
        "C  Innen: Ø72.0 oben / Ø250.0 unten",
        "D  4× Ø5.2 von z=0 bis Kopfauflage z=−15",
        "E  Bohrzentren: (±57.8,0), (0,±57.8)",
        "F  Lochkreis Ø115.6; Gegenabstand 115.6",
        "G  4× Werkzeugkanal Ø10 von z=−15 bis −29",
    ]
    rows_r = [
        "H  4× Boss Ø22; Achse wie E; z=−26 … −5",
        "J  Nut unten: Ø260 / Ø290; Tiefe 2.0",
        "K  Gummi: Ringbreite 15; Dicke 3; 1 vorstehend",
        "L  Kabelbohrung Ø20 radial, Azimut +45°",
        "M  Kabelachse z=−50; radial r=75 … 135",
        "N  2× Kabelbinder-Oese: siehe Blatt 2",
        "P  Kein Boden im Zentrum; Oeffnung unten Ø250",
    ]
    for i, (left, right) in enumerate(zip(rows_l, rows_r)):
        y = 83 - i * 8
        text(ax, 18, y, left, 7.6)
        text(ax, 218, y, right, 7.6)
    text(ax, 18, 28, "Achsen X/Y und Drehsinn: Draufsicht. Konen linear; Bezugsmasse z=0 und z=−90 sind formgebend.",
         7.2, color=DIM)
    return fig


def make_sheet_2():
    fig, ax = page("DETAILS — BEFESTIGUNG, KABEL, GEWINDERING",
                   "Teil 01 + Teil 02 • Schnitte schematisch, Masse verbindlich • M4-Gewinde vereinfacht ohne Helix im STEP", "2")

    # Nut-ring plan view at 1:1.
    cx, cy = 89, 185
    text(ax, 24, 258, "TEIL 02: GEWINDERING  (Draufsicht 1:1)", 8.7, weight="bold")
    ax.add_patch(Circle((cx, cy), RING_OUTER_R, fc=FILL, ec=INK, lw=0.8))
    ax.add_patch(Circle((cx, cy), RING_INNER_R, fc="white", ec=INK, lw=0.8))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        ax.add_patch(Circle((cx + x, cy + y), 1.65, fc="white", ec=INK, lw=0.6))
    line(ax, (cx-70,cy), (cx+70,cy), OLD, 0.4, "-.")
    line(ax, (cx,cy-70), (cx,cy+70), OLD, 0.4, "-.")
    text(ax, 15, 107, "Aussen Ø132   •   Innen Ø100.4", 7.5)
    text(ax, 15, 100, "4× M4×0.7 durch; LK Ø115.6", 7.5)
    text(ax, 15, 93, "Dicke 4.0, z=6 … 10", 7.5)
    text(ax, 15, 86, "Stahl S235JR, entgraten 0.5", 7.5)

    # Enlarged fastener section, not a complete A-A section.
    sx, sy, ss = 222, 201, 2.0
    text(ax, 189, 258, "DETAIL B: SCHRAUBE  (2:1)", 8.7, weight="bold")
    # Schematic surrounding solid and existing flange.
    ax.add_patch(Rectangle((sx-31, sy-30), 62, 30, fc=FILL, ec=INK, lw=0.7,
                           hatch="////"))
    ax.add_patch(Rectangle((sx-25, sy), 50, 12, fc="white", ec=OLD, lw=0.8,
                           hatch="...."))
    ax.add_patch(Rectangle((sx-25, sy+12), 50, 8, fc="#c9d2d7", ec=INK, lw=0.7,
                           hatch="xx"))
    # Bore Ø5.2 / access Ø10, screw shaft and head.
    ax.add_patch(Rectangle((sx-BOLT_THROUGH_D*ss/2, sy-30),
                           BOLT_THROUGH_D*ss, 50, fc="white", ec=INK, lw=0.6))
    ax.add_patch(Rectangle((sx-HEAD_ACCESS_D*ss/2, sy-58),
                           HEAD_ACCESS_D*ss, 28, fc="white", ec=INK, lw=0.6))
    ax.add_patch(Rectangle((sx-4.0, sy-30), 8.0, 50, fc="#8c9aa0", ec=INK, lw=0.6))
    ax.add_patch(Rectangle((sx-7.0, sy-38), 14.0, 8.0, fc="#8c9aa0", ec=INK, lw=0.6))
    line(ax, (sx,sy+28), (sx,sy-65), OLD, 0.5, "-.")
    dim_v(ax, sy-30, sy, sx+41, sx+31, "15.0")
    dim_v(ax, sy, sy+12, sx+48, sx+25, "6.0 STL")
    dim_v(ax, sy+12, sy+20, sx+55, sx+25, "4.0")
    leader(ax, (sx-7,sy-34), (190, 125), "M4×25, Kopf ≤Ø8")
    text(ax, 191, 116, "Ø10 Werkzeugkanal, Bit ≤Ø10", 7.4, color=DIM)
    text(ax, 191, 109, "Schraubenzugang ausschliesslich unten", 7.4, color=DIM)
    text(ax, 191, 102, "Ring: 4 mm Stahlgewindeeingriff", 7.4, color=DIM)

    # Cable outlet: polar position and lugs (top-projection schematic).
    text(ax, 22, 70, "DETAIL C: KABEL / ZUGENTLASTUNG", 8.5, weight="bold")
    cable_lines = [
        "Radialbohrung Ø20; Achse Azimut +45°; z=−50.",
        "Bohrwerkzeug r=75 … 135 entlang dieser Achse.",
        "2× Innen-Oese: Zylinder Ø18, z=−53 … −43;",
        "Mittelpunkt r=84, Azimut +30° / +60°.",
        "Je Oese Ø5 senkrecht zu z durchgehend.",
        "Kabel: geschlitzter Silikonschlauch ID8/OD12,",
        "L50 + Binder durch beide Oesen; Kanten R2.",
    ]
    for i, row in enumerate(cable_lines):
        text(ax, 22, 61 - 5.0*i, row, 7.2)
    text(ax, 218, 70, "UNTERE AUFLAGE / GUMMI", 8.5, weight="bold")
    base_lines = [
        "Offener Ring von R125 bis R150 bei z=−90.",
        "Nut Ø260 … Ø290, 2 mm tief ab Unterseite.",
        "Gummiring EPDM 70A, 15×3; 1 mm vorstehend.",
        "Gummi vollflaechig umlaufend verkleben.",
        "Gedrucktes Teil: ASA, 5–6 Perimeter, 40 %",
        "Infill; Bosse 100 %; Lage: Anschlussseite Bett.",
        "Alle sonstigen freien Kanten 0.8×45° brechen.",
    ]
    for i, row in enumerate(base_lines):
        text(ax, 218, 61 - 5.0*i, row, 7.2)
    return fig


def make_sheet_3():
    fig, ax = page("SPEZIFIKATION — KOORDINATEN UND PRUEFEN",
                   "Verbindliche Geometriemasse fuer Modellierung • Bezugs-STL bleibt unveraendert • reale Baugruppe vor Druck pruefen", "3")
    # Override the page-count footer on this third sheet.
    ax.text(12, 258, "DATENBLATT ZUR ZEICHNUNG", fontsize=10, weight="bold", color=INK)
    ax.text(12, 246, "Koordinatensystem", fontsize=8.5, weight="bold", color=INK)
    info = [
        "Ursprung (0,0,0): Mitte der Unterseite von final/Unten.stl.",
        "+Z zeigt in die vorhandene Drehplatte; der Standfuss liegt in −Z.",
        "Azimut 0° auf +X, positiv gegen den Uhrzeigersinn nach +Y.",
        "Fusskoerper: Rotationsprofil (r,z) = (36,0), (66,0), (150,−90), (125,−90).",
        "Gerade Mantellinien zwischen den beiden z-Ebenen. Keine Bodenplatte im Zentrum.",
        "4 Boss-Zylinder Ø22: Achsen (±57.8,0) und (0,±57.8), z=−26 bis −5.",
        "4 Bohrungen Ø5.2: gleiche Achsen, z=0 bis −15; 4× Ø10 von −15 bis −29.",
        "2 Oesen Ø18: Polarkoordinaten (r=84, θ=30°/60°), z=−53 bis −43; Ø5 axial.",
        "Kabelkanal Ø20: horizontale Achse θ=45°, z=−50, von r=75 bis r=135.",
        "Ringnut Unterseite: r=130 … 145, z=−90 … −88. Gummi r=130 … 145, 3 dick.",
        "Gewindering: r=50.2 … 66, z=6 … 10, 4× M4×0.7 durch auf denselben Achsen.",
    ]
    for i, row in enumerate(info):
        text(ax, 12, 234 - i*10.3, row, 8)

    line(ax, (12, 112), (408, 112), INK, 0.7)
    text(ax, 12, 102, "TOLERANZEN UND MONTAGE", 8.5, weight="bold")
    checks = [
        "FDM-Fuss: Aussen Ø300 ±1; Hoehe 90 ±0.5; Kontaktflaeche Ebenheit ≤0.3.",
        "4× Bohrung Ø5.2 +0.3/0; Achslage ≤0.2 zum Ursprung; Werkzeug Ø10 +0.5/0.",
        "Gewindering: Aussen/Innen ±0.1; Bohrlage ±0.1; M4×0.7 Gewinde 6H.",
        "Bestehende STL: Flansch Ø124.6×6, 4×Ø4.5 LK Ø115.6; Motortasche 42.6×42.6×4.95.",
        "4× M4×25 Innensechskant, Kopf Ø≤8; keine Schraube greift in Kunststoffgewinde.",
        "Fuss und Ring mit 2 M4-Fuehrungsstiften ausrichten; alle Schrauben von unten einsetzen/loesen.",
        "Geschlitzter Silikonschlauch ID8/OD12×50 im Kabeldurchlass; Binder an beiden Oesen.",
    ]
    for i, row in enumerate(checks):
        text(ax, 12, 92 - i*8.8, row, 7.5)
    line(ax, (12, 30), (408, 30), INK, 0.5)
    text(ax, 12, 27, "VOR EINSATZ PRUEFEN: Boxmasse/Schwerpunkt/Kippmoment, Ist-Motorpassung, Motorbefestigung, Raum oberhalb Flansch, Kabel/Stecker, Druckraum.",
         7.0, weight="bold")
    return fig


def main():
    sheets = [make_sheet_1(), make_sheet_2(), make_sheet_3()]
    with PdfPages(PDF) as pages:
        for i, fig in enumerate(sheets, 1):
            pages.savefig(fig)
            fig.savefig(HERE / f"zeichnung_blatt_{i}.png", dpi=150)
            plt.close(fig)
    print(PDF)


if __name__ == "__main__":
    main()
