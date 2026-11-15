---
name: li-post
description: >-
  Turn a raw idea into a LinkedIn post in the user's own voice: three hook
  options from 21 formulas, one full draft, cleaned by li-human, and a
  copy-ready block. Use when the user wants a LinkedIn post, a hook, "post
  about X", "turn this into a LinkedIn post", "write Tuesday's post", or asks
  for hook ideas. Never publishes; the user posts it.
---

# li-post

One idea in, one post out that sounds like the person posting it.

## Before drafting

1. **Voice.** Read `~/.claude/linkedin/voice.md`. If it doesn't exist, ask
   the user to paste three posts they wrote themselves, work out the voice
   from them, and save it using `templates/voice.md` from this repo as the
   shape. Don't guess a voice; a post in the wrong voice is worse than none.
2. **Plan.** If `~/.claude/linkedin/plan.md` exists and has a slot for this
   idea, use its angle, hook number and posting time.
3. **Hooks.** Read `hooks.json` in this folder: 21 formulas, each with a
   template, an example, when to use it, and how it usually goes wrong.
4. **Substance.** A thin idea ("post about leadership") can't be fixed by
   writing. Ask once, in one message: what actually happened, who was
   involved, and what it cost or gained, in numbers if possible. Wait for the
   answer.

## Shape of a post

```
Hook       one line, on its own. Must work cut off at ~140 characters.
Line 2     pays off the hook. Not more setup.
Body       1-3 line paragraphs with a blank line between each. No walls.
Turn       one line that changes how the reader sees what came before.
Close      one specific question OR one instruction. Not both.
```

Aim for 900-1,300 characters. Under 400 reads as a passing thought. Over
2,000 has to earn every extra line.

## Steps

1. **Three hooks** from three different formulas that genuinely fit. Number
   them, show the formula name, and say in one sentence which you'd use and
   why.
2. **Draft** the full post on the chosen hook (or the user's pick).
3. **Humanize.** Run the draft through `/li-human` (`humanize.py` then
   `detect.py`) and rewrite the flagged lines. Every post goes through this.
4. **Hand over** the post in a fenced block exactly as it should be pasted,
   then a short receipt:

```
READY TO POST
hook:     #17 Time Compression
length:   1,086 characters
human:    5 fixes, score 82 PASS
when:     Tue 8:15am (from plan.md)
link:     put it in the first comment, not the post
Say "logged" once it's live, or tell me what to change.
```

5. **Log it.** When the user confirms it's posted, append a line to
   `~/.claude/linkedin/log.md`: date, hook number and name, first line, and
   the theme. `/li-audit` and `/li-plan` read this.

## Rules

- **One idea.** Two ideas means two posts; say so and offer the second.
- **Numbers beat adjectives.** "$3,800" not "a lot". No number from the
  user? Ask, or leave `{{number}}` and flag it.
- **Never invent anything** under the user's name: no made-up results,
  clients, quotes, dates or figures, not even as placeholders that look real.
- **No links in the body.** They tend to cut reach. Link goes in the first
  comment.
- **Hashtags: three at most**, at the end, and only real ones.
- **No bait closers.** "Thoughts?" and "Agree?" add nothing. If there's a
  question, it should be one only this post could ask.
- **Respect `voice.md`'s off-limits list**: topics, clients, numbers, claims
  the user can't make (employer policy, NDA, regulated industry).

## Never

Never post, schedule, or open LinkedIn in a browser to publish. Automating a
personal LinkedIn account breaks its User Agreement and risks a restriction.
This skill hands over text; the user posts it.
