import pcbnew, os, sys

# 1. Can we create and save a fresh board?
try:
    b = pcbnew.NewBoard("smoke.pcb")
    print("NewBoard: OK")
except Exception as e:
    b = pcbnew.BOARD()
    print("NewBoard failed, used BOARD(): %s" % e)

# 2. Draw a board outline on Edge.Cuts (proof we control geometry)
from pcbnew import PCB_SHAPE, SHAPE_T_RECT
edge = PCB_SHAPE(None, SHAPE_T_RECT)
edge.SetLayer(pcbnew.Edge_Cuts)
edge.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(0)))
edge.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(85), pcbnew.FromMM(40)))
try:
    edge.SetStroke(pcbnew.STROKE(pcbnew.FromMM(0.15), pcbnew.LINE_STYLE_SOLID))
except AttributeError:
    edge.SetWidth(pcbnew.FromMM(0.15))
b.Add(edge)

# 3. Try loading a real footprint from the installed libraries
lib = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"
ok_fp = None
if os.path.isdir(lib):
    try:
        ok_fp = pcbnew.FootprintLoad(lib, "R_0805_2012Metric")
        print("FootprintLoad R_0805: OK -> %s" % ok_fp.GetReference())
        ok_fp.SetReference("R1")
        ok_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20), pcbnew.FromMM(20)))
        b.Add(ok_fp)
    except Exception as e:
        print("FootprintLoad failed: %s" % e)
else:
    print("lib dir missing: %s" % lib)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smoke.kicad_pcb")
b.SetFileName(out)
b.Save(out)
print("Saved: %s" % out)
print("Bounding box: %s" % pcbnew.ToMM(b.GetBoardEdgesBoundingBox().GetWidth()))
