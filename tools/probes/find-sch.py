import os
# KiCad's own file IO plugins: does the bundled Python expose the S-expression
# reader/writer for schematics? Check what _IO plugins exist in the install.
base = r"C:\Program Files\KiCad\10.0\bin\Lib\site-packages"
mods = [f for f in os.listdir(base) if f.startswith("kicad") or f.startswith("sch")]
print("kicad-ish modules in site-packages: %s" % mods)

# pcbnew's SWIG layer often exposes IO_MANAGER / SCH_IO indirectly
import pcbnew
names = [n for n in dir(pcbnew) if "SCH" in n or "IO" in n.upper()]
print("pcbnew SCH/IO symbols: %s" % names[:40])
