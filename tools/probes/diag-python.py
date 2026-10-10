import os, sys
# Diagnose: does the spawned python see pylibs on sys.path?
print("PYTHONPATH env:", os.environ.get("PYTHONPATH", "<unset>"), file=sys.stderr)
print("executable:", sys.executable, file=sys.stderr)
print("sexpdata importable:", end=" ", file=sys.stderr)
try:
    import sexpdata
    print("YES", file=sys.stderr)
except Exception as e:
    print("NO -> %s" % e, file=sys.stderr)
