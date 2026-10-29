"""Read-only geometric checks on Revision C CAD and the original STL."""

from __future__ import annotations

import hashlib
from pathlib import Path

from cadgen import build123d as bd

from standfuss_v3 import (
    HEIGHT, BOLT_CIRCLE_R, BOLT_THROUGH_D, HEAD_ACCESS_D,
    BOTTOM_OUTER_R, TOP_OUTER_R, TOP_INNER_R, BOTTOM_INNER_R,
    CABLE_Z, CABLE_PASSAGE_D, body,
)
from gewindering_v3 import OUTER_R, INNER_R, BOTTOM_Z, THICKNESS

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

ring = bd.import_step(str(HERE / "gewindering_v3.step"))
assert ring.is_valid, "Ring B-Rep invalid"
assert len(ring.solids()) == 1, "Ring must be a single connected solid"
rb = ring.bounding_box()
assert abs(rb.min.X + OUTER_R) < 1e-5
assert abs(rb.max.X - OUTER_R) < 1e-5
assert abs(rb.min.Z - BOTTOM_Z) < 1e-5
assert abs(rb.max.Z - (BOTTOM_Z + THICKNESS)) < 1e-5

assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == EXPECTED_SHA256

def inner_radius(z):
    return TOP_INNER_R + (BOTTOM_INNER_R - TOP_INNER_R) * (-z) / HEIGHT

def outer_radius(z):
    return TOP_OUTER_R + (BOTTOM_OUTER_R - TOP_OUTER_R) * (-z) / HEIGHT

assert 65.0 < inner_radius(CABLE_Z + CABLE_PASSAGE_D / 2)
assert 125.0 > outer_radius(CABLE_Z - CABLE_PASSAGE_D / 2)

# From the exact dimensions of Unten.stl and the specified Revision B interface.
source_pitch_radius = 57.8
source_hole_radius = 2.25
new_hole_radius = BOLT_THROUGH_D / 2
center_offset = source_pitch_radius - BOLT_CIRCLE_R
nominal_m3_motion_allowance = (source_hole_radius - 1.5) + (new_hole_radius - 1.5)
motor_rear_z = 4.95 - 48.0
ground_z = -70.0
print("foot_valid", foot.is_valid, "single_solid", len(foot.solids()) == 1)
print("foot_bbox", tuple(bbox.min), tuple(bbox.max), "volume_mm3", round(foot.volume, 2))
print("ring_valid", ring.is_valid, "single_solid", len(ring.solids()) == 1)
print("ring_bbox", tuple(rb.min), tuple(rb.max), "volume_mm3", round(ring.volume, 2))
print("hole_axis_offset_mm", round(center_offset, 3),
      "M3_total_radial_allowance_mm", round(nominal_m3_motion_allowance, 3))
print("nominal_motor_floor_clearance_mm", round(motor_rear_z - ground_z, 3))
print("driver_body_height_mm", 40.0,
      "direct_stack_height_shortfall_mm", round(40.0 - (motor_rear_z-ground_z), 3))
print("top_outer_ligament_to_D4_mm", TOP_OUTER_R - (BOLT_CIRCLE_R + new_hole_radius))
print("M3_head_D6_in_D10_access_diametral_clearance_mm", HEAD_ACCESS_D - 6.0)
print("original_STL_sha256", EXPECTED_SHA256)
