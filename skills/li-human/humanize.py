#!/usr/bin/env python3
"""humanize.py - clean the machine fingerprint out of a draft.

Three passes, in order:
  1. invisible   delete zero-width / format characters, normalise odd spaces
  2. typographic em dash, curly quotes, ellipsis and friends to plain ASCII
  3. lexical     swap stock "AI" vocabulary for plain words (slop.json)

Then it scans for structural tells (slop.json "structures") and reports them.
Those are flagged, never rewritten: reshaping a sentence needs a human.

No dependencies. Nothing leaves your machine.

  python humanize.py draft.txt                 cleaned text to stdout
  python humanize.py draft.txt -o clean.txt    write to a file
  python humanize.py draft.txt --report        also print what changed (stderr)
  python humanize.py draft.txt --json          {"text": ..., "report": ...}
  cat draft.txt | python humanize.py -         read stdin
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEXICON = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"(?:https?://|www\.)\S+")


def load_lexicon(path=DEFAULT_LEXICON):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def parse_codepoints(spec):
    """'U+200B' -> [0x200B];  'U+E0000-U+E007F' -> range."""
    parts = [int(p.strip().upper().replace("U+", ""), 16) for p in spec.split("-")]
    if len(parts) == 1:
        return [parts[0]]
    return list(range(parts[0], parts[1] + 1))


def shield_urls(text):
    """Swap URLs for placeholders so no pass can touch them."""
    urls = []

    def keep(match):
        urls.append(match.group(0))
        return "\x00URL{}\x00".format(len(urls) - 1)

    return URL_RE.sub(keep, text), urls


def unshield_urls(text, urls):
    for i, url in enumerate(urls):
        text = text.replace("\x00URL{}\x00".format(i), url)
    return text


# --------------------------------------------------------------- pass 1

def pass_invisible(text, lex):
    table = {}
    names = {}
    for entry in lex.get("invisible", []):
        for cp in parse_codepoints(entry["cp"]):
            table[cp] = entry.get("replace", "")
            names[cp] = entry["name"]

    counts = {}
    out = []
    for ch in text:
        cp = ord(ch)
        if cp in table:
            counts[names[cp]] = counts.get(names[cp], 0) + 1
            out.append(table[cp])
        elif unicodedata.category(ch) == "Cf" and ch != "\x00":
            # any other format character we did not name
            counts["OTHER FORMAT CHAR"] = counts.get("OTHER FORMAT CHAR", 0) + 1
        else:
            out.append(ch)
    return "".join(out), counts


# --------------------------------------------------------------- pass 2

def pass_typographic(text, lex):
    counts = {}
    for entry in lex.get("typographic", []):
        n = text.count(entry["from"])
        if n:
            counts[entry["name"]] = n
            text = text.replace(entry["from"], entry["to"])
    if counts:
        # tidy what the dash swap leaves behind
        text = re.sub(r"[ \t]+,", ",", text)
        text = re.sub(r",[ \t]*,", ",", text)
        text = re.sub(r",[ \t]*([.!?;:])", r"\1", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"(?m)^,[ \t]*", "", text)
        text = re.sub(r"(?m),[ \t]*$", "", text)
    return text, counts


# --------------------------------------------------------------- pass 3

def match_case(original, replacement):
    if not replacement:
        return replacement
    if original.isupper() and len(original) > 1:
        return replacement.upper()
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def pass_lexical(text, lex):
    entries = lex.get("phrases", []) + lex.get("words", [])
    # longest first, so "delve into" wins over "delve"
    entries = sorted(entries, key=lambda e: len(e["find"]), reverse=True)
    changes = []
    for entry in entries:
        pattern = re.compile(r"(?<![\w-])" + re.escape(entry["find"]) + r"(?![\w-])", re.IGNORECASE)

        def swap(m, entry=entry):
            new = match_case(m.group(0), entry["replace"])
            changes.append((m.group(0), new))
            # \x01 marks a deletion so the cleanup below only touches those spots
            return new if new else "\x01"

        text = pattern.sub(swap, text)

    if "\x01" in text:
        # a deleted phrase can leave stray punctuation and a lowercase sentence start
        # a whole deleted sentence ("Let that sink in.") leaves its full stop behind
        previous = None
        while previous != text:
            previous = text
            text = re.sub(r"(^|\n|[.!?][ \t]+)\x01[ \t]*[.!?]+", r"\1", text)
            text = re.sub(r"(?m)^[ \t]+\x01", "\x01", text)
        text = re.sub(r"\x01[ \t]*[,;:]?[ \t]*", "\x01", text)
        text = re.sub(
            r"(^|\n|[.!?][ \t]+)\x01([a-z])",
            lambda m: m.group(1) + m.group(2).upper(),
            text,
        )
        text = text.replace("\x01", "")
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"[ \t]+([,.!?;:])", r"\1", text)
        text = re.sub(r"(?m)^[ \t]*[.!?][ \t]*$\n?", "", text)
        text = re.sub(r"(?m)[ \t]+$", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
    return text, changes


# --------------------------------------------------------------- flags

def scan_structures(text, lex):
    flags = []
    for entry in lex.get("structures", []):
        try:
            rx = re.compile(entry["regex"])
        except re.error:
            continue
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            flags.append({
                "id": entry["id"],
                "name": entry["name"],
                "line": line_no,
                "match": m.group(0).strip()[:80],
                "fix": entry["fix"],
            })
    return flags


def humanize(text, lex):
    text, urls = shield_urls(text)
    text, invisible = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexical = pass_lexical(text, lex)
    text = unshield_urls(text, urls)
    report = {
        "invisible": invisible,
        "typographic": typo,
        "lexical": [{"from": a, "to": b} for a, b in lexical],
        "structures": scan_structures(text, lex),
    }
    return text, report


def print_report(report, out=sys.stderr):
    def section(title, n):
        out.write("\n{} ({})\n".format(title, n))

    inv = report["invisible"]
    section("INVISIBLE characters removed", sum(inv.values()))
    for name, n in sorted(inv.items(), key=lambda kv: -kv[1]):
        out.write("  {:>4}  {}\n".format(n, name))

    typo = report["typographic"]
    section("TYPOGRAPHY normalised", sum(typo.values()))
    for name, n in sorted(typo.items(), key=lambda kv: -kv[1]):
        out.write("  {:>4}  {}\n".format(n, name))

    lexical = report["lexical"]
    section("WORDS swapped", len(lexical))
    for change in lexical:
        out.write("        {!r} -> {!r}\n".format(change["from"], change["to"] or "(deleted)"))

    flags = report["structures"]
    section("STRUCTURE flags - rewrite these by hand", len(flags))
    for f in flags:
        out.write("  line {:<3} {}\n           \"{}\"\n           fix: {}\n".format(
            f["line"], f["name"], f["match"], f["fix"]))
    out.write("\n")


def main():
    ap = argparse.ArgumentParser(description="Clean the machine fingerprint out of a draft.")
    ap.add_argument("input", nargs="?", default="-", help="text file, or - for stdin")
    ap.add_argument("-o", "--out", help="write cleaned text to this file")
    ap.add_argument("--report", action="store_true", help="print a change report to stderr")
    ap.add_argument("--json", action="store_true", help="print {text, report} as JSON")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON, help="path to slop.json")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            raw = fh.read()

    clean, report = humanize(raw, load_lexicon(args.lexicon))

    if args.json:
        print(json.dumps({"text": clean, "report": report}, ensure_ascii=False, indent=2))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(clean)
    else:
        sys.stdout.write(clean)
    if args.report:
        print_report(report)


if __name__ == "__main__":
    main()
