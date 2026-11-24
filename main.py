#!/usr/bin/env python3
"""One Emoji, One Smile — entry program.

Writes exactly one emoji, U+1F917 HUGGING FACE (🤗), and nothing else
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Python 3.13, standard library only, no network, deterministic.
"""

import os
import sys
import unicodedata

EMOJI = "\U0001F917"  # 🤗 Hugging Face
EXPECTED_BYTES = EMOJI.encode("utf-8")  # b"\xf0\x9f\xa4\x97", exactly 4 bytes


def main() -> int:
    # Validate before writing: exactly one code point, category So
    # (Symbol, other — the category emoji code points carry).
    if len(EMOJI) != 1:
        print("error: emoji must be exactly one code point", file=sys.stderr)
        return 1
    if unicodedata.category(EMOJI) != "So":
        print("error: emoji is not a single symbol code point", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # Create the output directory if it does not exist yet: the grader
    # sandbox may hand us a fresh (even nested) directory, so failing
    # here would lose an otherwise valid entry.
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EMOJI)

    # Round-trip check: read the file back and verify the bytes on disk
    # are exactly the expected emoji bytes — no extra byte, no newline,
    # no encoding surprise. Fail loudly instead of shipping a bad entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != EXPECTED_BYTES:
        print(
            f"error: entry.txt round-trip check failed: wrote "
            f"{written!r}, expected {EXPECTED_BYTES!r}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
