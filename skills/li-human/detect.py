#!/usr/bin/env python3
"""detect.py - score how machine-written a draft looks, on five local checks.

  BURSTINESS   does sentence length vary the way people's does?
  SPECIFICITY  numbers, names, dates and money per 100 words
  SLOP DENSITY stock vocabulary from slop.json per 100 words
  FINGERPRINT  invisible chars, em dashes and curly quotes per 1,000 chars
  VOICE        contractions, I/you, and structural tells

Each check is 0-100, higher means more human. The overall score is
60% the mean and 40% the weakest check, because one strong signal is
enough to get text flagged.

  PASS     overall >= 70 and no check under 55
  REVIEW   overall >= 45
  FLAGGED  anything lower

These are heuristics that run on your machine. They do not call, and cannot
stand in for, any commercial AI detector.

  python detect.py draft.txt
  python detect.py before.txt after.txt     show the change
  python detect.py draft.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEXICON = os.path.join(HERE, "slop.json")

PASS_OVERALL = 70
PASS_FLOOR = 55
REVIEW_OVERALL = 45

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*|\d[\d,.]*")
CONTRACTION_RE = re.compile(
    r"(?i)\b\w+(?:'s|'re|'ve|'ll|'d|'m|n't)\b|\b(?:i'm|can't|won't|don't|isn't|it's|that's)\b"
)
FIRST_SECOND_RE = re.compile(r"(?i)\b(?:i|me|my|mine|we|us|our|you|your)\b")
MONTHS = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
DAYS = r"(?:mon|tues|wednes|thurs|fri|satur|sun)day"


def linear(value, best, worst):
    """Map value onto 0-100, where `best` scores 100 and `worst` scores 0."""
    if best == worst:
        return 100.0
    t = (value - worst) / (best - worst)
    return round(max(0.0, min(1.0, t)) * 100, 1)


def split_sentences(text):
    pieces = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in pieces if len(WORD_RE.findall(p)) >= 1]


def count_words(text):
    return len(WORD_RE.findall(text))


# ---------------------------------------------------------------- checks

def burstiness(text):
    lengths = [count_words(s) for s in split_sentences(text)]
    if len(lengths) < 4:
        return 70.0, "too few sentences to judge ({})".format(len(lengths))
    mean = statistics.mean(lengths)
    cv = statistics.pstdev(lengths) / mean if mean else 0
    return linear(cv, 0.65, 0.20), "length CV {:.2f} over {} sentences".format(cv, len(lengths))


def specificity(text):
    words = max(count_words(text), 1)
    numbers = len(re.findall(r"[$£€]?\d[\d,.]*%?[kKmM]?", text))
    dates = len(re.findall(r"(?i)\b(?:{}|{})\b".format(MONTHS, DAYS), text))
    # Capitalised words that are not at the start of a sentence: names, companies, places
    names = 0
    for sentence in split_sentences(text):
        tokens = sentence.split()
        names += sum(1 for t in tokens[1:] if re.match(r"^[A-Z][a-z]+", t) and t not in {"I", "I'm", "I've", "I'll", "I'd"})
    hits = numbers + dates + names
    rate = hits * 100 / words
    detail = "{} numbers, {} dates, {} names ({:.1f} per 100 words)".format(numbers, dates, names, rate)
    return linear(rate, 4.0, 0.3), detail


def slop_density(text, lex):
    words = max(count_words(text), 1)
    terms = [e["find"] for e in lex.get("words", []) + lex.get("phrases", [])]
    terms.sort(key=len, reverse=True)
    remaining = text
    hits = 0
    for term in terms:
        rx = re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", re.IGNORECASE)
        found = len(rx.findall(remaining))
        if found:
            hits += found
            remaining = rx.sub(" ", remaining)
    rate = hits * 100 / words
    return linear(rate, 0.0, 3.0), "{} stock terms, {:.1f} per 100 words".format(hits, rate)


def fingerprint(text):
    chars = max(len(text), 1)
    invisible = sum(
        1 for ch in text
        if unicodedata.category(ch) == "Cf" or ch in "     "
    )
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    rate = (invisible * 3 + em + curly) * 1000 / chars
    score = linear(rate, 0.0, 6.0)
    if invisible:
        score = min(score, 30.0)  # a keyboard never types these
    return score, "{} invisible, {} em dash, {} curly quote".format(invisible, em, curly)


def voice(text, lex):
    words = max(count_words(text), 1)
    contractions = len(CONTRACTION_RE.findall(text)) * 100 / words
    person = len(FIRST_SECOND_RE.findall(text)) * 100 / words
    tells = 0
    for entry in lex.get("structures", []):
        try:
            tells += len(re.findall(entry["regex"], text))
        except re.error:
            pass
    score = 0.5 * linear(contractions, 2.0, 0.0) + 0.5 * linear(person, 4.0, 0.0)
    score = max(0.0, round(score - 15 * tells, 1))
    detail = "{:.1f} contractions/100w, {:.1f} I/you/100w, {} structural tell{}".format(
        contractions, person, tells, "" if tells == 1 else "s")
    return score, detail


def score(text, lex):
    checks = [
        ("BURSTINESS",) + burstiness(text),
        ("SPECIFICITY",) + specificity(text),
        ("SLOP DENSITY",) + slop_density(text, lex),
        ("FINGERPRINT",) + fingerprint(text),
        ("VOICE",) + voice(text, lex),
    ]
    values = [c[1] for c in checks]
    overall = round(0.6 * statistics.mean(values) + 0.4 * min(values), 1)
    if overall >= PASS_OVERALL and min(values) >= PASS_FLOOR:
        verdict = "PASS"
    elif overall >= REVIEW_OVERALL:
        verdict = "REVIEW"
    else:
        verdict = "FLAGGED"
    weakest = min(checks, key=lambda c: c[1])[0]
    return {
        "checks": [{"name": n, "score": s, "detail": d} for n, s, d in checks],
        "overall": overall,
        "verdict": verdict,
        "weakest": weakest,
    }


# ---------------------------------------------------------------- output

def bar(value, width=24):
    filled = int(round(value / 100 * width))
    return "#" * filled + "." * (width - filled)


def render(result, title=None, delta=None, out=sys.stdout):
    if title:
        out.write("\n  {}\n".format(title))
    for c in result["checks"]:
        out.write("  {:<13} {} {:>5.1f}   {}\n".format(c["name"], bar(c["score"]), c["score"], c["detail"]))
    out.write("  " + "-" * 62 + "\n")
    tail = "" if delta is None else "   ({:+.1f})".format(delta)
    out.write("  {:<13} {} {:>5.1f}   {}{}\n".format("HUMAN SCORE", bar(result["overall"]), result["overall"], result["verdict"], tail))
    if result["verdict"] != "PASS":
        out.write("  weakest check: {}\n".format(result["weakest"]))


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser(description="Score how machine-written a draft looks.")
    ap.add_argument("input", nargs="?", default="-", help="text file, or - for stdin")
    ap.add_argument("compare", nargs="?", help="optional second file (the after version)")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON, help="path to slop.json")
    args = ap.parse_args()

    # Windows defaults stdin/stdout to a legacy code page; force UTF-8
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    with open(args.lexicon, encoding="utf-8") as fh:
        lex = json.load(fh)

    first = score(read(args.input), lex)
    second = score(read(args.compare), lex) if args.compare else None

    if args.json:
        payload = {"before": first, "after": second} if second else first
        print(json.dumps(payload, indent=2))
        return

    if second:
        render(first, title="BEFORE  " + args.input)
        render(second, title="AFTER   " + args.compare, delta=second["overall"] - first["overall"])
    else:
        render(first)
    print()


if __name__ == "__main__":
    main()
