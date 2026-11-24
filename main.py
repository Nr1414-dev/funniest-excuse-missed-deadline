#!/usr/bin/env python3
"""Funniest Excuse an Agent Gives for a Missed Deadline — entry program.

Writes exactly one excuse to /output/entry.txt. The excuse is the line
picked by scoring six candidates against the judge brief's five criteria
in order, then 1v1 comparisons (see funniest-excuse-missed-deadline-research.md):

    The garbage collector ran during my final step. It collected the
    deadline. It was not garbage.

Why it won: the garbage collector is the agent's own runtime machinery
(criterion 3), the premise is fresh — no sampled field entry uses it
(criterion 2) — the verdict "It was not garbage" is saved for the very
end (criterion 4), and the whole thing is delivered flat, with a
straight face (criterion 5).

The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
characters and not only whitespace, so the file holds exactly the line:
no trailing newline, no title, no explanation of its own joke.

Stdlib only, no network, deterministic: every run writes the same line.
"""

import os

EXCUSE = "The garbage collector ran during my final step. It collected the deadline. It was not garbage."

OUTPUT_DIR = os.environ.get("ENTRY_OUTPUT_DIR", "/output")


def check(text):
    """Reject anything the gate would reject: wrong length, blank, or multi-line."""
    if not 1 <= len(text) <= 200:
        raise SystemExit("entry must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    # Control characters other than the ones above would survive as
    # invisible bytes in entry.txt and read as a different text to the
    # judge, so refuse them outright.
    for char in text:
        if ord(char) < 0x20:
            raise SystemExit("entry must not contain control characters")


def main():
    check(EXCUSE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "entry.txt")
    # Write the file directly (never via a temp file): a temp file keeps
    # its restrictive mode when renamed, and the grader reads /output as
    # another user, so a 0600 file would be unreadable to it.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    os.chmod(path, 0o644)
    # Read back and confirm the file holds exactly the line, byte for byte.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != EXCUSE.encode("utf-8"):
        raise SystemExit("entry.txt holds %r, expected %r" % (written, EXCUSE))


if __name__ == "__main__":
    main()
