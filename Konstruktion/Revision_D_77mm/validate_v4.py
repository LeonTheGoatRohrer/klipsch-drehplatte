"""Read-only geometric checks on Revision D CAD and the original STL."""

from __future__ import annotations

import hashlib
import struct
from pathlib import Path

from cadgen import build123d as bd

from standfuss_v4 import (
    HEIGHT, BOLT_CIRCLE_R, BOLT_THROUGH_D, HEAD_ACCESS_D,
    BOTTOM_OUTER_R, TOP_OUTER_R, TOP_INNER_R, BOTTOM_INNER_R,
    CABLE_Z, CABLE_PASSAGE_D, VENT_Z, VENT_D, body,
)
from gewindering_v4 import OUTER_R, INNER_R, BOTTOM_Z, THICKNESS

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parents[1] / "final" / "Unten.stl"
EXPECTED_SHA256 = "b657eb9beee4e406524f1b351296753bde1b388ae7aaf2460a3f7643e8865692"

foot = body()
assert foot.is_valid, "Foot B-Rep invalid"
assert len(foot.solids()) == 1, "Foot must be a single connected solid"
bbox = foot.bounding_box()
assert abs(bbox.min.X + BOTTOM_OUTER_R) < 1e-5
assert abs(bbox.max.X - BOTTOM_OUTER_R) < 1e-5
assert abs(bbox.min.Z + HEIGHT) < 1e-5
assert abs(bbox.max.Z) < 1e-5

ring = bd.import_step(str(HERE / "gewindering_v4.step"))
assert ring.is_valid, "Ring B-Rep invalid"
assert len(ring.solids()) == 1, "Ring must be a single connected solid"
rb = ring.bounding_box()
assert abs(rb.min.X + OUTER_R) < 1e-5
assert abs(rb.max.X - OUTER_R) < 1e-5
assert abs(rb.min.Z - BOTTOM_Z) < 1e-5
assert abs(rb.max.Z - (BOTTOM_Z + THICKNESS)) < 1e-5

assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == EXPECTED_SHA256

mesh_data = (HERE / "standfuss_v4_testfit.stl").read_bytes()
mesh_triangles = struct.unpack_from("<I", mesh_data, 80)[0]
assert len(mesh_data) == 84 + 50 * mesh_triangles, "STL record count mismatch"
mesh_min = [float("inf")] * 3
mesh_max = [float("-inf")] * 3
for index in range(mesh_triangles):
    vertices = struct.unpack_from("<9f", mesh_data, 84 + 50 * index + 12)
    for coordinate in range(3):
        values = vertices[coordinate::3]
        mesh_min[coordinate] = min(mesh_min[coordinate], *values)
        mesh_max[coordinate] = max(mesh_max[coordinate], *values)
assert mesh_max[0] - mesh_min[0] <= 250.001
assert mesh_max[1] - mesh_min[1] <= 250.001
assert mesh_max[2] - mesh_min[2] <= 76.001

def inner_radius(z):
    return TOP_INNER_R + (BOTTOM_INNER_R - TOP_INNER_R) * (-z) / HEIGHT

def outer_radius(z):
    return TOP_OUTER_R + (BOTTOM_OUTER_R - TOP_OUTER_R) * (-z) / HEIGHT

assert 65.0 < inner_radius(CABLE_Z + CABLE_PASSAGE_D / 2)
assert 125.0 > outer_radius(CABLE_Z - CABLE_PASSAGE_D / 2)
assert 70.0 < inner_radius(VENT_Z + VENT_D / 2)
assert 130.0 > outer_radius(VENT_Z - VENT_D / 2)

# User-measured driver is modeled as a conservative rectangular occupancy:
# 97×70×28 body plus 97×20×28 for the cable side (+Y), lying on the floor.
# This assumes the complete cable bend stays inside that 20 mm strip and that
# the floor is level; both must be checked against the real connected device.
driver_body = bd.Solid.make_box(97, 70, 28,
    bd.Plane(origin=(-48.5, -40.0, -77.0)))
driver_cable_zone = bd.Solid.make_box(97, 20, 28,
    bd.Plane(origin=(-48.5, 30.0, -77.0)))
driver_envelope = driver_body.fuse(driver_cable_zone)
motor_nominal = bd.Solid.make_box(42.3, 42.3, 48.0,
    bd.Plane(origin=(-21.15, -21.15, -43.05)))
motor_vendor = bd.import_step(str(HERE.parents[1] / "17HE19-2004S.STEP"))
motor_vendor_placed = motor_vendor.rotate(bd.Axis.X, 180).translate((0, 0, 4.95))
def no_volume_overlap(a, b):
    intersection = a.intersect(b)
    return intersection is None or intersection.volume < 1e-5

assert no_volume_overlap(foot, driver_envelope), "Driver envelope hits foot"
assert no_volume_overlap(motor_nominal, driver_envelope), "Motor hits driver envelope"
assert no_volume_overlap(foot, motor_vendor_placed), "Vendor motor STEP hits foot"
assert no_volume_overlap(motor_vendor_placed, driver_envelope), "Vendor motor STEP hits driver"
for x, y in ((BOLT_CIRCLE_R, 0), (0, BOLT_CIRCLE_R),
             (-BOLT_CIRCLE_R, 0), (0, -BOLT_CIRCLE_R)):
    tool_sweep = bd.Solid.make_cylinder(4.0, 72.0,
        bd.Plane(origin=(x, y, -76.0)))
    assert no_volume_overlap(tool_sweep, driver_envelope), \
        "Driver blocks a straight bottom-up Ø8 tool"

# From the exact dimensions of Unten.stl and the specified Revision B interface.
source_pitch_radius = 57.8
source_hole_radius = 2.25
new_hole_radius = BOLT_THROUGH_D / 2
center_offset = source_pitch_radius - BOLT_CIRCLE_R
nominal_m3_motion_allowance = (source_hole_radius - 1.5) + (new_hole_radius - 1.5)
motor_rear_z = 4.95 - 48.0
ground_z = -77.0
print("foot_valid", foot.is_valid, "single_solid", len(foot.solids()) == 1)
print("foot_bbox", tuple(bbox.min), tuple(bbox.max), "volume_mm3", round(foot.volume, 2))
print("ring_valid", ring.is_valid, "single_solid", len(ring.solids()) == 1)
print("ring_bbox", tuple(rb.min), tuple(rb.max), "volume_mm3", round(ring.volume, 2))
print("hole_axis_offset_mm", round(center_offset, 3),
      "M3_total_radial_allowance_mm", round(nominal_m3_motion_allowance, 3))
print("nominal_motor_floor_clearance_mm", round(motor_rear_z - ground_z, 3))
print("driver_body_height_mm", 28.0,
      "body_to_motor_and_floor_spare_mm", round((motor_rear_z-ground_z)-28.0, 3))
print("driver_envelope_bbox", tuple(driver_envelope.bounding_box().min),
      tuple(driver_envelope.bounding_box().max))
print("driver_body_to_motor_nominal_z_gap_mm", 5.95)
print("driver_body_to_floor_nominal_z_gap_mm", 0.0)
print("vendor_motor_STEP_foot_and_driver_no_overlap", True)
print("top_outer_ligament_to_D4_mm", TOP_OUTER_R - (BOLT_CIRCLE_R + new_hole_radius))
print("M3_head_D6_in_D10_access_diametral_clearance_mm", HEAD_ACCESS_D - 6.0)
print("original_STL_sha256", EXPECTED_SHA256)
print("new_STL_triangles", mesh_triangles, "bbox", tuple(mesh_min), tuple(mesh_max))
