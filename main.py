#!/usr/bin/env python3
"""Copy the composed front page to the make.fun output directory.

The entry image is rendered by compose.py (same directory) and copied
here byte-for-byte -- this script does no rendering, no resizing and
no network access. The output must stay under 1 MiB (1,048,576 bytes).

Local check (from this directory):
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Then compare the copy with the source:
    cmp entry.png out/entry.png && sha256sum entry.png out/entry.png
The two hashes must match exactly.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SRC):
        print(f"error: source image not found: {SRC}", file=sys.stderr)
        print("run: python3 compose.py", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, over the "
              f"{MAX_BYTES} byte limit", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"copied {len(data)} bytes to {dest}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
