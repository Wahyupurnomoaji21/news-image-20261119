"""News image entry for 19 November 2026 (Python 3.13, stdlib only).

The front-page image lives in this repository as entry.png; the program
copies it byte for byte to /output/entry.png. No network, no randomness,
no timestamps in the output, so both grader runs write identical bytes.

Local check:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
LIMIT_BYTES = 1_048_576


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    data = target.read_bytes()
    if len(data) > LIMIT_BYTES:
        raise SystemExit(
            f"entry.png is {len(data)} bytes, over the 1 MiB limit"
        )
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
