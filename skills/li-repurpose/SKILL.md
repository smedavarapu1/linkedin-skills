---
name: li-repurpose
description: >-
  Turn one long piece (video transcript, podcast, article, newsletter, talk,
  meeting notes) into a week of standalone LinkedIn posts. Use when the user
  says repurpose this, "turn my video/newsletter/article into posts", "get
  LinkedIn posts out of this transcript", or pastes long-form content and
  asks what to post from it.
---

# li-repurpose

Mine one source for several posts, each of which works for someone who never
saw the original.

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

The full text: transcript, article, newsletter, script, notes. If the user
gives a video link and a transcript tool is available in this session, use
it; otherwise ask them to paste the text. Read all of it before pulling
anything out.

Check `~/.claude/linkedin/log.md` too, so you don't repeat recent posts.

## Pull out, don't summarise

Nobody wants a summary of a video they didn't watch. Go through the source
and list what can stand on its own:

| kind | what to look for |
| --- | --- |
| **Claims** | statements someone could argue with |
| **Numbers** | figures, costs, durations, percentages |
| **Stories** | a moment with a person, a place, and something at stake |
| **How-tos** | "here's how it works" explanations |
| **Mistakes** | things that went wrong and what they taught |
| **Lines** | sentences quotable as they stand |

Show the counts and the list before drafting anything. If there are fewer
than four strong items, the source is thin and so will the posts be. Say
that rather than stretching it.

Only use what's in the source. Don't add numbers or stories that aren't
there.

## Plan the week

- One item per post. Each post must stand completely alone: no "as I said
  in my video", no assumed context.
- Give each a different hook from `../li-post/hooks.json`. Same-shaped posts
  in a row read like a content mill.
- Order: strongest claim first, story mid-week, how-to last.
- If the original is public and the user wants to, the link goes in the
  first comment of one post, not in the body.

```
SOURCE   "Lessons from our first 100 customers" (podcast, 42 min)
FOUND    3 claims · 5 numbers · 2 stories · 2 how-tos · 1 mistake · 4 lines

TUE  #1  Contrarian       Free trials attracted our worst customers
WED  #4  The Number       100 customers, 61 from one referral partner
THU  #8  Scene            The call where our biggest prospect said "not yet"
FRI  #21 Give It Away     The 4-question onboarding call script

Say "write Tuesday" and I'll draft it.
```

## Drafting

Draft one at a time, on request, through `/li-post` (which runs
`/li-human`). Don't produce all of them at once: batch-written posts sound
alike, and the user won't edit them individually.

Save the week to `~/.claude/linkedin/plan.md` if the user wants it to be
this week's plan.
