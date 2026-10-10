#!/usr/bin/env python3
"""
Register the KiCAD MCP server's Python dependencies with KiCad's bundled Python.

KiCad's bundled python (Program Files\\KiCad\\<ver>\\bin\\python.exe) ships a
sitecustomize.py that rebuilds sys.path from scratch on startup, which
discards any PYTHONPATH the parent process set. So dependencies installed
into this repo's pylibs/ are registered via usercustomize.py in KiCad's
USER_SITE directory instead — site.py imports usercustomize *after*
sitecustomize.py has finished its rewrite.

Idempotent: re-running overwrites the file in place.

Usage (any python, or KiCad's):
    python tools/scripts/setup-kicad-deps.py
"""

import os
import site
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PYLIBS = os.path.join(REPO_ROOT, "tools", "kicad-mcp", "pylibs").replace("\\", "\\\\")

TEMPLATE = '''\
import os, sys
# KiCad's sitecustomize.py rebuilds sys.path from scratch (ignoring PYTHONPATH).
# This runs after sitecustomize, so it can re-inject the MCP server's deps.
_p = os.environ.get("KICAD_MCP_PYLIBS")
if not _p:
    _p = r"{pylibs}"
if os.path.isdir(_p) and _p not in sys.path:
    sys.path.insert(0, _p)
'''


def main() -> int:
    if not os.path.isdir(PYLIBS):
        print(f"error: pylibs not found at {PYLIBS}", file=sys.stderr)
        print("run `pip install -r tools/kicad-mcp/requirements.txt --target <that dir>` first",
              file=sys.stderr)
        return 1

    # Ask *KiCad's* python where its user site is; site.getusersitepackages()
    # already resolves through KiCad's PYTHONUSERBASE rewrite.
    user_site = site.getusersitepackages()
    os.makedirs(user_site, exist_ok=True)

    target = os.path.join(user_site, "usercustomize.py")
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(TEMPLATE.format(pylibs=PYLIBS))

    print(f"wrote {target}")
    print(f"  resolves pylibs -> {PYLIBS}")
    print(f"  user site      -> {user_site}")
    print("verify with: KiCad\\bin\\python.exe -c \"import sexpdata, skip, kipy, pcbnew\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
