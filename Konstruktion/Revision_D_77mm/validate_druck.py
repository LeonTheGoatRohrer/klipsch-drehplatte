"""Check saved print STEP/STL: dimensions, unchanged volume and closed mesh."""
from pathlib import Path
from collections import Counter
import hashlib
import struct
from cadgen import build123d as bd

here = Path(__file__).resolve().parent
part = bd.import_step(str(here / "Standfuss_77mm_D250_Druck.step"))
original_part = bd.import_step(str(here / "standfuss_v4.step"))
assert part.is_valid and len(part.solids()) == 1
box = part.bounding_box()
expected_min, expected_max = (-125, -125, 0), (125, 125, 76)
assert all(abs(a-b) < 1e-5 for a,b in zip(box.min, expected_min))
assert all(abs(a-b) < 1e-5 for a,b in zip(box.max, expected_max))
assert abs(part.volume - original_part.volume) < 1e-4

data = (here / "Standfuss_77mm_D250_Druck.stl").read_bytes()
count = struct.unpack_from("<I", data, 80)[0]
assert len(data) == 84 + 50 * count
edges = Counter()
low, high = [float("inf")]*3, [float("-inf")]*3
volume = 0.0
for i in range(count):
    coords = struct.unpack_from("<9f", data, 84+50*i+12)
    a,b,c = [tuple(coords[j:j+3]) for j in (0,3,6)]
    cross = (b[1]*c[2]-b[2]*c[1], b[2]*c[0]-b[0]*c[2], b[0]*c[1]-b[1]*c[0])
    volume += sum(a[j]*cross[j] for j in range(3))/6
    ab,ac = [b[j]-a[j] for j in range(3)], [c[j]-a[j] for j in range(3)]
    area_cross = (ab[1]*ac[2]-ab[2]*ac[1], ab[2]*ac[0]-ab[0]*ac[2], ab[0]*ac[1]-ab[1]*ac[0])
    assert sum(v*v for v in area_cross) > 0, "Degenerate triangle"
    for p in (a,b,c):
        for j in range(3):
            low[j],high[j] = min(low[j],p[j]),max(high[j],p[j])
    for p,q in ((a,b),(b,c),(c,a)):
        edges[tuple(sorted((p,q)))] += 1
assert all(n == 2 for n in edges.values()), "Open or nonmanifold mesh edge"
assert volume > 0, "Mesh normals reversed"
assert abs(volume-part.volume)/part.volume < 0.001
assert all(abs(a-b) < 0.001 for a,b in zip(low,expected_min))
assert all(abs(a-b) < 0.001 for a,b in zip(high,expected_max))
source = here.parents[1] / "final" / "Unten.stl"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "b657eb9beee4e406524f1b351296753bde1b388ae7aaf2460a3f7643e8865692"
print("STEP valid, single solid, unchanged volume:", round(part.volume,3), "mm3")
print("STL closed, no degenerate triangles, outward winding; triangles:",count)
print("Print bounds (mm):",low,high)
print("STL volume deviation (%):",round((volume-part.volume)/part.volume*100,5))
print("Original Unten.stl unchanged")
