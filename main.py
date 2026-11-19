"""News image entry for 19 November 2026 (Python 3.13, standard library only).

The front page image lives in this repository as entry.png; the program
copies it byte for byte to /output/entry.png. No network, no randomness,
so both grader runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"


MAX_BYTES = 1048576


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    size = dest.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    print(f"wrote {dest} ({size} bytes)")


if __name__ == "__main__":
    main()
