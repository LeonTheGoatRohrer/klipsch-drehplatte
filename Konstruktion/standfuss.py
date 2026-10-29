"""Dimensioned CAD reference for the additional Klipsch stand foot.

Coordinates: underside of existing Unten.stl is z=0. The stand extends to
z=-90. Units: mm. This file deliberately exports STEP, never edits an STL.
"""

from __future__ import annotations

from math import cos, radians, sin

from cadgen import build123d as bd
from cadgen import step


HEIGHT = 90.0
TOP_OUTER_R = 66.0
BOTTOM_OUTER_R = 150.0
TOP_INNER_R = 36.0
BOTTOM_INNER_R = 125.0
BOLT_CIRCLE_R = 57.8
BOLT_THROUGH_D = 5.2
HEAD_ACCESS_D = 10.0
HEAD_SEAT_Z = -15.0
HEAD_ACCESS_LOWER_Z = -29.0
BOSS_R = 11.0
BOSS_BOTTOM_Z = -26.0
BOSS_TOP_Z = -5.0
CABLE_ANGLE_DEG = 45.0
CABLE_Z = -50.0
CABLE_PASSAGE_D = 20.0
LUG_R = 9.0
LUG_PITCH_R = 84.0
LUG_Z_MIN = -53.0
LUG_Z_MAX = -43.0
LUG_HOLE_D = 5.0
GROOVE_INNER_R = 130.0
GROOVE_OUTER_R = 145.0
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

    # Full-depth, integral load pads around the four mounting channels.
    positions = ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
                 (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R))
    for x, y in positions:
        part = part.fuse(z_cylinder(BOSS_R, BOSS_BOTTOM_Z, BOSS_TOP_Z, x, y))

    # Two integral zip-tie lugs, away from the radial cable outlet.
    for angle in (30.0, 60.0):
        x = LUG_PITCH_R * cos(radians(angle))
        y = LUG_PITCH_R * sin(radians(angle))
        part = part.fuse(z_cylinder(LUG_R, LUG_Z_MIN, LUG_Z_MAX, x, y))

    for x, y in positions:
        part = part.cut(z_cylinder(BOLT_THROUGH_D / 2, HEAD_SEAT_Z, 0.1, x, y))
        part = part.cut(z_cylinder(HEAD_ACCESS_D / 2,
                                   HEAD_ACCESS_LOWER_Z, HEAD_SEAT_Z, x, y))

    # Radial cable passage, angle 45 degrees between mounting channels.
    direction = (cos(radians(CABLE_ANGLE_DEG)), sin(radians(CABLE_ANGLE_DEG)), 0)
    cable_axis_start_r = 75.0
    cable_tool = bd.Solid.make_cylinder(
        CABLE_PASSAGE_D / 2, 60.0,
        bd.Plane(origin=(direction[0] * cable_axis_start_r,
                         direction[1] * cable_axis_start_r, CABLE_Z),
                 z_dir=direction),
    )
    part = part.cut(cable_tool)

    for angle in (30.0, 60.0):
        x = LUG_PITCH_R * cos(radians(angle))
        y = LUG_PITCH_R * sin(radians(angle))
        part = part.cut(z_cylinder(LUG_HOLE_D / 2,
                                   LUG_Z_MIN - 0.1, LUG_Z_MAX + 0.1, x, y))

    # Annular underside groove: 15-mm strip, 3-mm rubber -> 1 mm proud.
    groove = z_cylinder(GROOVE_OUTER_R, -HEIGHT - 0.1, -HEIGHT + GROOVE_DEPTH)
    groove = groove.cut(z_cylinder(GROOVE_INNER_R,
                                    -HEIGHT - 0.2, -HEIGHT + GROOVE_DEPTH + 0.1))
    part = part.cut(groove)
    part.label = "Standfuss"
    return part


@step(out="standfuss.step")
def standfuss():
    return body()


if __name__ == "__main__":
    standfuss()
