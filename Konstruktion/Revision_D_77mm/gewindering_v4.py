"""Six-millimetre steel nut ring, matching the measured real hole pitch.

The four 2.5 mm tap drills stand for M3 x 0.5 through threads.
"""

from cadgen import build123d as bd
from cadgen import step

OUTER_R = 62.0
INNER_R = 50.2  # 0.4 mm radial clearance to STL nominal Ø99.6 upper body
BOTTOM_Z = 6.0
THICKNESS = 6.0
BOLT_CIRCLE_R = 56.5
M3_TAP_DRILL_D = 2.5


@step(out="gewindering_v4.step")
def gewindering_v4():
    plane = bd.Plane(origin=(0, 0, BOTTOM_Z))
    part = bd.Solid.make_cylinder(OUTER_R, THICKNESS, plane)
    part = part.cut(bd.Solid.make_cylinder(INNER_R, THICKNESS, plane))
    for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
        part = part.cut(bd.Solid.make_cylinder(
            M3_TAP_DRILL_D / 2, THICKNESS,
            bd.Plane(origin=(x, y, BOTTOM_Z))))
    part.label = "Gewindering_Revision_D_M3"
    return part


if __name__ == "__main__":
    gewindering_v4()
