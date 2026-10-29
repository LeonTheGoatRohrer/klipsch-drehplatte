"""Print exports of drawing Revision D, mm, broad bottom at z=0.

Printed body height 76 mm; installed height 77 mm with the specified EPDM ring.
The assembly-datum model remains unchanged in standfuss_v4.py.
"""

from cadgen import step, stl
from standfuss_v4 import HEIGHT, body


@step(out="Standfuss_77mm_D250_Druck.step")
@stl(out="Standfuss_77mm_D250_Druck.stl",
     mesh_tolerance=1e-4, mesh_angular_tolerance=0.1)
def standfuss_druck():
    part = body().translate((0, 0, HEIGHT))
    part.label = "Standfuss_Rev_D_D250_Druck_mm"
    return part


if __name__ == "__main__":
    standfuss_druck()
