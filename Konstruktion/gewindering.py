"""Companion M4 steel nut ring for the stand foot, dimensions in mm.

Four core holes represent M4x0.7 through threads; the helix is intentionally
specified on the drawing rather than modeled as helical B-Rep geometry.
"""

from cadgen import build123d as bd
from cadgen import step


OUTER_R = 66.0
INNER_R = 50.2
BOTTOM_Z = 6.0
THICKNESS = 4.0
BOLT_CIRCLE_R = 57.8
M4_TAP_DRILL_D = 3.3


@step(out="gewindering.step")
def gewindering():
    plane = bd.Plane(origin=(0, 0, BOTTOM_Z))
    part = bd.Solid.make_cylinder(OUTER_R, THICKNESS, plane)
    part = part.cut(bd.Solid.make_cylinder(INNER_R, THICKNESS, plane))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        part = part.cut(bd.Solid.make_cylinder(
            M4_TAP_DRILL_D / 2, THICKNESS,
            bd.Plane(origin=(x, y, BOTTOM_Z))))
    part.label = "Gewindering_M4"
    return part


if __name__ == "__main__":
    gewindering()
