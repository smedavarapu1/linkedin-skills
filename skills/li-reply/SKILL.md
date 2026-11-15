---
name: li-reply
description: >-
  Draft replies to the comments under the user's own LinkedIn post, sorted
  so the valuable ones get answered first. Use when the user pastes comments
  from their post, says "reply to these", "help with my comments", "someone
  disagreed with my post", "how do I answer this critic", or has a potential
  client asking a question in the comments.
---

# li-reply

Replies under a post count as engagement on it, and the first hour matters
most. But comments aren't equally worth answering, so sort them before
writing anything.

## Humanize gate (required, every time)

No text from this skill is shown to the user until it has passed through the
humanizer. No exceptions: short comments, one-line replies, headlines, hook
options, "quick" drafts and revisions all go through it.

1. Write everything you're about to show into a temp file. Put a line with
   only `---` between separate pieces (each option, comment, reply, slide,
   message).
2. Run the gate from this skill's folder (use `python3` if `python` isn't
   found):
   `python ../li-human/gate.py draft.txt -o clean.txt`
3. If any piece is flagged or not PASS, rewrite those lines by hand in the
   user's voice and run the gate again. At most three rounds; if a piece
   still fails, show it but say which check failed.
4. Show the user only the text from `clean.txt`, never the pre-gate draft.
   Re-run the gate after every edit the user asks for.
5. End the reply with the gate's receipt line, exactly as printed, e.g.
   `humanized: 3 pieces · 7 fixes · 86 PASS / SHORT PASS / SHORT PASS`.
   A draft without a receipt line has not been through the gate.

If Python can't run here, say so plainly, apply `../li-human/slop.json` by
hand, and label the text **not machine-checked**. Never skip the gate
silently.

## Input

The comments, with commenter names and roles if possible. Screenshots are
fine. Don't open LinkedIn to read the thread yourself.

Also read `~/.claude/linkedin/voice.md` if it exists, and ask for the
original post if it isn't pasted. Replies have to fit what the post said.

## Sort first

Put every comment in one bucket and state the counts:

| bucket | what it is | gets |
| --- | --- | --- |
| **LEAD** | someone describing a problem the user solves | a complete answer, plus one line offering help |
| **SUBSTANCE** | adds data, disagrees, extends the idea | the most thoughtful reply in the thread |
| **PEER** | someone the user wants to be seen talking to | a reply that gives them something back |
| **SUPPORT** | "great post", emoji, tags | a like, and at most a few words |
| **NOISE** | pitches, spam, bad faith | nothing |

Write replies in that order. Stop when the value runs out; a short reply to
every "Nice!" isn't required.

## How to reply

- **Answer the question in the reply.** Don't move it to DMs when the
  answer fits in public.
- **Name once,** at the start, no exclamation mark.
- **Match length.** A one-line comment gets a short reply.
- **Critics:** start with what they got right, in their terms, then hold
  the point you still believe. Don't get defensive, don't delete, and reply
  once only.
- **Leads:** answer fully in public. End with one sentence that offers help,
  not a pitch. A good public answer brings in the next person.
- **Pitches in the user's comments:** skip them. A reply boosts them.
- **Never invent** facts, results or offers the user hasn't given you.

## Output

One block, grouped by bucket, each reply ready to paste and already cleaned
by `/li-human`:

```
REPLIES  ·  14 comments  ·  1 LEAD · 2 SUBSTANCE · 3 PEER · 7 SUPPORT · 1 NOISE

LEAD
Tom Alvarez - "we have the same problem onboarding contractors"
> Tom, the fix for us was a one-page "first week" doc that each contractor
> signs off on day one. Cut our setup questions by about half. Happy to share
> the doc if it helps.

SUBSTANCE
Dana Okafor - thinks weekly 1:1s are too often
> Fair point, and with a senior team I'd agree. We only went weekly because
> half the team joined in the last 6 months.

SUPPORT  (like all; reply to the first three)
Lee Wong: "Great read" -> Thanks Lee.

NOISE  (1)
Skipped: a lead-gen pitch. Replying would boost it.
```

Nothing is posted until the user does it. They paste each reply themselves.
