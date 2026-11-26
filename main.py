"""The Worst Pizza Topping — a one-line entry for make.fun.

One breath of pizza heresy: pineapple is not the villain here.
The real crime is the anchovy — a tiny fishy traitor that turns a
perfectly good slice into a salty science experiment gone wrong.
Only the Python standard library is used.
"""

import os
import sys

TOPPING_LINE = "Pineapple on pizza isn't the crime — it's the anchovies, tiny fishy traitors that turn a perfectly good slice into a salty science experiment gone wrong."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def validate_line(text):
    """Return the topping line once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line, not only whitespace, with no trailing newline in the file
    and no control characters anywhere in it.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters; gate allows 1 to %d" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def describe_topping(text):
    """Summarise the topping line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII verdict
    reads the same either way while a line with wide characters
    would not. Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    words = len(text.split())
    return "%d characters, %d UTF-8 bytes, %d words" % (chars, byte_count, words)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = validate_line(TOPPING_LINE)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print("wrote %s (%s)" % (path, describe_topping(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
