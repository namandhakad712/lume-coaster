import sys, os
sys.path.insert(0, r"C:\Projects\HalfLife-Deskbuddy\tools\kicad-mcp\pylibs")
from skip import Schematic

# Can skip author + save a fresh .kicad_sch?
out = r"C:\Projects\HalfLife-Deskbuddy\tools\probes\probe-sch.kicad_sch"
# Seed a minimal empty schematic so skip can load the tree
seed = """(kicad_sch (version 20261125) (generator "probe")
  (uuid "00000000-0000-0000-0000-000000000000")
  (paper "A3")
  (lib_symbols)
  (sheet_instances (path "/" (page "1")))
)
"""
with open(out, "w", encoding="utf-8") as f:
    f.write(seed)
sch = Schematic(out)
try:
    sch.write(out)
    print("skip.write OK ->", out, os.path.getsize(out), "bytes")
except Exception as e:
    print("skip.write failed:", type(e).__name__, e)

# Can it instantiate a symbol from the installed library?
try:
    sch.add("Device:R", reference="R99", value="10k")
    sch.write(out)
    print("add symbol OK, size now", os.path.getsize(out))
except Exception as e:
    print("add failed:", type(e).__name__, e)
