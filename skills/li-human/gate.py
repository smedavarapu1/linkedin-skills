#!/usr/bin/env python3
"""gate.py - the one command every li-* skill runs before showing text.

Cleans each piece with humanize.py, scores it with detect.py, lists the
sentence shapes that still need a hand rewrite, and prints a receipt line.

Put several pieces (hook options, comments, replies, slides, DM steps) in one
file separated by a line containing only ---. Each piece is judged on its own.

Short pieces (under 40 words: comments, replies, connection notes,
headlines) can't be judged on rhythm or voice, so they PASS when the
mechanical checks are clean: no stock words, no invisible characters or
fancy typography, and no structural flags.

  python gate.py draft.txt -o clean.txt
  exit code 0 = every piece passed, 1 = something still needs work

The text to show the user is what lands in clean.txt (or stdout without -o).
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import detect  # noqa: E402
import humanize  # noqa: E402

SEPARATOR = re.compile(r"(?m)^[ \t]*---[ \t]*$")
SHORT_WORDS = 40


def judge(clean, report, lex):
    words = detect.count_words(clean)
    if words < SHORT_WORDS:
        slop, _ = detect.slop_density(clean, lex)
        fingerprint, _ = detect.fingerprint(clean)
        ok = slop == 100.0 and fingerprint == 100.0 and not report["structures"]
        return ("SHORT PASS" if ok else "SHORT FAIL"), ok, None
    result = detect.score(clean, lex)
    ok = result["verdict"] == "PASS"
    label = "{:.0f} {}".format(result["overall"], result["verdict"])
    return label, ok, result


def main():
    ap = argparse.ArgumentParser(description="Humanize and score every piece before it is shown.")
    ap.add_argument("input", help="draft file; separate pieces with a line containing only ---")
    ap.add_argument("-o", "--out", help="write the cleaned pieces here")
    ap.add_argument("--lexicon", default=humanize.DEFAULT_LEXICON)
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    lex = humanize.load_lexicon(args.lexicon)
    with open(args.input, encoding="utf-8") as fh:
        raw = fh.read()

    pieces = [p.strip("\n") for p in SEPARATOR.split(raw) if p.strip()]
    cleaned, labels, total_fixes, all_ok = [], [], 0, True
    log = sys.stderr if not args.out else sys.stdout

    for i, piece in enumerate(pieces, 1):
        clean, report = humanize.humanize(piece, lex)
        fixes = sum(report["invisible"].values()) + sum(report["typographic"].values()) + len(report["lexical"])
        total_fixes += fixes
        label, ok, result = judge(clean, report, lex)
        all_ok = all_ok and ok
        labels.append(label)
        cleaned.append(clean.strip("\n"))

        log.write("\n[piece {}/{}]  {}  ({} fix{})\n".format(
            i, len(pieces), label, fixes, "" if fixes == 1 else "es"))
        for f in report["structures"]:
            log.write("  REWRITE line {}: {} -> \"{}\"\n           {}\n".format(
                f["line"], f["name"], f["match"], f["fix"]))
        if result and not ok:
            weakest = min(result["checks"], key=lambda c: c["score"])
            log.write("  weakest: {} {:.0f} ({})\n".format(weakest["name"], weakest["score"], weakest["detail"]))

    output = "\n---\n".join(cleaned) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(output)
    else:
        sys.stdout.write(output)

    receipt = "humanized: {} piece{} · {} fix{} · {}".format(
        len(pieces), "" if len(pieces) == 1 else "s",
        total_fixes, "" if total_fixes == 1 else "es",
        " / ".join(labels))
    log.write("\n" + receipt + ("" if all_ok else "  · NOT ALL PASSING") + "\n")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
