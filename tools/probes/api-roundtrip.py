import pcbnew, os, sys
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\lib\python3\dist-packages")

# 1. Reload the saved board to prove round-trip integrity
b = pcbnew.LoadBoard(os.path.join(os.path.dirname(os.path.abspath(__file__)), "smoke.kicad_pcb"))
print("LoadBoard returned: %s" % ("OK" if b else "None"))
drawings = b.Drawings() if hasattr(b, "Drawings") else []
print("Reloaded: %d footprints, %d drawings" % (len(b.Footprints()), len(drawings)))
for fp in b.Footprints():
    print("  FP: %s at %.1f,%.1f" % (fp.GetReference(), pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y)))

# 2. Can we reach the symbol libraries (needed for schematic generation)?
try:
    from pcbnew import SYMBOL_LIB
    print("SYMBOL_LIB: present")
except Exception as e:
    print("SYMBOL_LIB: %s" % e)

# Find installed symbol libs
for root, dirs, files in os.walk(r"C:\Program Files\KiCad\10.0\share\kicad\symbols"):
    kssym = [f for f in files if f.endswith(".kicad_sym")]
    print("Symbol libs found: %d" % len(kssym))
    if kssym[:3]:
        print("  e.g. %s" % ", ".join(kssym[:3]))
    break

# 3. DRC engine reachable?
try:
    drc = pcbnew.DRC()
    print("DRC engine: present")
except Exception as e:
    print("DRC: %s" % e)
