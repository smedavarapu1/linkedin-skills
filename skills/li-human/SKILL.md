---
name: li-human
description: >-
  Clean AI tells out of a draft and score it before anyone sees it: removes
  invisible Unicode characters, em dashes, curly quotes and stock "AI"
  vocabulary, flags formulaic sentence shapes, and rates the result on five
  local checks. Use when the user says humanize, de-slop, "does this sound
  like AI", "remove the em dashes", "will this get flagged", and run it on
  every post, comment, reply, DM or profile section the other li-* skills
  write before showing it to the user.
---

# li-human

The other skills write. This one makes sure what they wrote sounds like a
person. Its scripts live next to this file; run them rather than judging by
eye.

## The gate (what every other skill runs)

```bash
python gate.py draft.txt -o clean.txt
```

`gate.py` humanizes every piece in the file (pieces separated by a line
containing only `---`), scores each one, lists the lines that need a hand
rewrite, and ends with a receipt such as
`humanized: 2 pieces · 5 fixes · 84 PASS / SHORT PASS`. Exit code 0 means
everything passed.

Pieces under 40 words (comments, replies, connection notes, headlines) are
too short for rhythm and voice scores, so they get **SHORT PASS** only when
they have no stock words, no invisible characters or fancy typography, and no
structural flags.

The rule for every li-* skill: show the user only the gate's cleaned output,
always with the receipt line, and re-run it after every edit. The same applies
when this skill is used directly on the user's own text.

## The underlying tools

```bash
python humanize.py draft.txt -o clean.txt --report   # clean + list every change
python detect.py clean.txt                           # five-check score
python detect.py draft.txt clean.txt                 # before vs after
```

Use `python3` where `python` is not on the path. Both scripts read
`slop.json` (the lexicon) from this folder, have no dependencies, and never
send text anywhere. Write the draft to a temp file first; do not put the
user's text on the command line.

## What humanize.py fixes on its own

1. **Invisible characters.** Zero-width spaces and joiners, word joiners,
   byte-order marks, soft hyphens, Unicode tag characters, and any other
   format character it finds. Non-breaking and thin spaces become normal
   spaces. Nobody types these; they arrive with generated text and survive
   copy-paste.
2. **Typography.** Em dash to comma, en dash to hyphen, curly quotes to
   straight, the single-character ellipsis to three dots, bullets to hyphens.
   It tidies the double punctuation the dash swap can leave.
3. **Stock vocabulary.** Roughly 120 words and phrases (delve, leverage,
   robust, seamless, "in today's fast-paced world", "let that sink in"...)
   swapped for plain words, or deleted when they carry no meaning.
   Capitalisation is kept. URLs are never touched.

## What it only flags

Sentence shapes need judgement, so the script reports them with a line
number and a suggested fix, and leaves the rewrite to you:

- "It's not just X, it's Y" / "Not only X but also Y"
- "No X. No Y." staccato
- Lists of three that close a sentence
- One-line reveals: "The result?"
- Stock emoji (rocket, fire, bulb, sparkles, dart, pointing finger, check)
- Four or more hashtags in a row
- Closing bait: "Thoughts?", "Agree?", "Who else?"
- Drumroll lines that end in a colon, "Imagine if...", "In a world where...",
  "Let's dive in"

Rewrite each flagged line yourself, keeping the meaning, in the user's voice
from `~/.claude/linkedin/voice.md` if it exists.

## The five checks (detect.py)

| check | measures | looks machine-made when |
| --- | --- | --- |
| BURSTINESS | spread of sentence lengths | every sentence is about the same length |
| SPECIFICITY | numbers, dates, names per 100 words | it is all abstractions |
| SLOP DENSITY | lexicon hits per 100 words | stock words everywhere |
| FINGERPRINT | invisible chars, em dashes, curly quotes | typography is too perfect |
| VOICE | contractions, I/you, structural tells | formal, impersonal, formulaic |

Overall = 60% of the mean + 40% of the weakest check. **PASS** needs 70+
overall with no check under 55. **REVIEW** is 45+. Below that is
**FLAGGED**.

## How to run it

1. Save the draft, run `humanize.py ... -o clean.txt --report`.
2. Rewrite every flagged line in `clean.txt` by hand.
3. Run `detect.py draft.txt clean.txt`.
4. Not PASS? Fix the check named as weakest and run again. Low SPECIFICITY
   usually means the draft needs a real number or name from the user, so ask
   for one; never invent it. After three rounds without a PASS, the draft
   needs rewriting from scratch, not more cleaning.
5. Show the user the cleaned text **and** the score line. Never the score on
   its own.

## Be straight about what this is

These are local heuristics built around the signals AI detectors commonly
use. They are not GPTZero, Originality.ai, Copyleaks or any other product,
they do not call those services, and a PASS here does not guarantee anything
there. Never tell the user their text is "undetectable". The honest claim is
narrower: the draft no longer has the obvious tells.

The invisible-character pass removes stray format characters. It does not
defeat, and does not claim to defeat, cryptographic watermarking.

## Tuning

`slop.json` is meant to be edited. If the user genuinely says "leverage" in
real life, delete that entry. Add their own pet phrases to `words` or
`phrases`. New sentence-shape flags go in `structures` as a regex plus a fix.
