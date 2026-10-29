"""Revision C 70 mm stand-foot envelope, all dimensions in millimetres.

User-specified interface: Ø124 top, four Ø4 holes, opposite centres 113 mm,
overall installed height 70 mm including the 1 mm proud rubber ring.
z=0 is the mating face; the printed cone extends to z=-69.
Driver mounts await measured dimensions of the actual driver.
"""

from __future__ import annotations

from math import cos, radians, sin

from cadgen import build123d as bd
from cadgen import step


HEIGHT = 69.0  # printed body; 3 mm rubber in a 2 mm groove reaches z=-70
TOP_OUTER_R = 62.0
BOTTOM_OUTER_R = 125.0  # Ø250, user's maximum printer envelope
TOP_INNER_R = 36.0
BOTTOM_INNER_R = 100.0  # 25 mm radial base wall
BOLT_CIRCLE_R = 56.5  # opposite hole centres 113 mm
BOLT_THROUGH_D = 4.0  # M3 clearance in the printed foot
HEAD_ACCESS_D = 10.0
HEAD_SEAT_Z = -4.0
HEAD_ACCESS_LOWER_Z = -34.0  # open straight tool path into the inner cavity
CABLE_ANGLE_DEG = 45.0
CABLE_Z = -54.0
CABLE_PASSAGE_D = 20.0
LUG_R = 11.0
LUG_PITCH_R = 88.0
LUG_Z_MIN = -57.0
LUG_Z_MAX = -49.0
LUG_HOLE_D = 5.0
GROOVE_INNER_R = 105.0
GROOVE_OUTER_R = 120.0
GROOVE_DEPTH = 2.0


def z_cylinder(radius: float, z0: float, z1: float, x: float = 0, y: float = 0):
    return bd.Solid.make_cylinder(radius, z1 - z0, bd.Plane(origin=(x, y, z0)))


def body():
    outer = bd.Solid.make_cone(
        BOTTOM_OUTER_R, TOP_OUTER_R, HEIGHT, bd.Plane(origin=(0, 0, -HEIGHT))
    )
    inner = bd.Solid.make_cone(
        BOTTOM_INNER_R, TOP_INNER_R, HEIGHT, bd.Plane(origin=(0, 0, -HEIGHT))
    )
    part = outer.cut(inner)

    positions = ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R))
    for x, y in positions:
        part = part.cut(z_cylinder(BOLT_THROUGH_D / 2, HEAD_SEAT_Z, 0.1, x, y))
        part = part.cut(z_cylinder(HEAD_ACCESS_D / 2,
                                   HEAD_ACCESS_LOWER_Z, HEAD_SEAT_Z, x, y))

    direction = (cos(radians(CABLE_ANGLE_DEG)), sin(radians(CABLE_ANGLE_DEG)), 0)
    # Span both flanks even at the ±10 mm axial extremes of the passage.
    cable_start_r = 65.0
    part = part.cut(bd.Solid.make_cylinder(
        CABLE_PASSAGE_D / 2, 60.0,
        bd.Plane(origin=(direction[0] * cable_start_r,
                         direction[1] * cable_start_r, CABLE_Z),
                 z_dir=direction)))

    for angle in (20.0, 70.0):
        x = LUG_PITCH_R * cos(radians(angle))
        y = LUG_PITCH_R * sin(radians(angle))
        part = part.fuse(z_cylinder(LUG_R, LUG_Z_MIN, LUG_Z_MAX, x, y))
        part = part.cut(z_cylinder(LUG_HOLE_D / 2,
                                   LUG_Z_MIN - 0.1, LUG_Z_MAX + 0.1, x, y))

    groove = z_cylinder(GROOVE_OUTER_R, -HEIGHT - 0.1, -HEIGHT + GROOVE_DEPTH)
    groove = groove.cut(z_cylinder(GROOVE_INNER_R,
                                    -HEIGHT - 0.2, -HEIGHT + GROOVE_DEPTH + 0.1))
    part = part.cut(groove)
    part.label = "Standfuss_Revision_C_70mm_envelope"
    return part


@step(out="standfuss_v3.step")
def standfuss_v3():
    return body()


if __name__ == "__main__":
    standfuss_v3()
