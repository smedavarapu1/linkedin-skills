---
name: li-comment
description: >-
  Write comments on other people's LinkedIn posts that add something and
  sound like a person, never "Great post!". Use when the user pastes a post
  and asks for a comment, says "comment on this", "what should I say here",
  "help me engage with this", or wants a batch of comments for a daily
  engagement round.
---

# li-comment

A thoughtful comment on a busy post is seen by more people than many of the
user's own posts. A generic one is worse than silence: the author notices,
and so does everyone scrolling past.

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

The post text, plus the author's name and role if the user has them. A
screenshot is fine. If you only get a URL you can't read, ask for the text.
Don't guess what a post says, and don't open or scrape the LinkedIn feed in
a browser.

Read `~/.claude/linkedin/voice.md` if it exists. Comments should sound like
the user's posts.

## Pick a type

Choose by what the post is. The last type is the fallback, not the default.

| # | type | use when | shape |
| --- | --- | --- | --- |
| 1 | **Data point** | the post makes a claim the user has evidence for | "Same here: when we tried X, Y went from 12 to 30." |
| 2 | **Edge case** | the post is right but leaves out a situation | "Works until {condition}. After that..." |
| 3 | **Polite disagreement** | the user really thinks it's wrong | real agreement first, then where they part ways |
| 4 | **Build on a line** | one sentence in the post is the strongest | quote it, take it one step further |
| 5 | **Sharp question** | the post skips the hard part | one specific question, no "curious to hear more" |
| 6 | **Been there** | the user has done the thing | what happened, in two sentences |
| 7 | **Correction** | there's a factual error | short, kind, and certain. Check before claiming. |
| 8 | **Another angle** | the facts are right but the framing is narrow | "Another way to see this:" |
| 9 | **Short and true** | the post doesn't need more, but presence helps | under 12 words, and actually witty or insightful |

## Rules

- **2-4 sentences.** Longer takes over the thread. Shorter is filler.
- **Banned openers:** "Great post", "Love this", "So true", "Couldn't agree
  more", "This resonates", "{Name}!", and any emoji as the first character.
- **Don't summarise the post back.** Everyone just read it.
- **One point per comment.**
- **Specific test:** if the comment could sit under any post on this topic,
  rewrite it.
- **Disagree when it's warranted**, but lead with what's genuinely right.
- **No pitching** in someone else's comments, ever.
- **No invented experience.** If the user hasn't done the thing, don't write
  a "Been there" comment for them.

## Output

Two options of different types, labelled, each already run through
`/li-human` (short text makes AI tells more obvious, not less). Then one line
on which to post and why.

```
COMMENTS  ·  on Priya Raman's post about async standups

[6 · Been there]
We went fully async for a quarter. Shipping speed held, but two new hires
told us at their 90-day check-in that they felt invisible. We kept async and
added one live call a week just for questions.

[5 · Sharp question]
How do you catch the blocker someone doesn't realise is a blocker? That was
the thing our written standups kept missing.

Post the first: it's a real result and admits a downside, which is what
gets replies.
```

## Batch mode

For an engagement round, ask for 5-10 posts pasted in one message and return
one comment for each in a single block. Keep a list of who the user has
commented on in `~/.claude/linkedin/log.md` (date, name, post topic). If the
same three people show up every day, point it out and suggest names from the
engage list in `~/.claude/linkedin/plan.md`.

## Never

Never post the comment, and never use a browser or tool to comment on the
user's behalf. That's automation LinkedIn's User Agreement forbids. The user
pastes it.
