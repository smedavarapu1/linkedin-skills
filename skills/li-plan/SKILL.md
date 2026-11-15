---
name: li-plan
description: >-
  Plan a LinkedIn week: which posts to write, which day and time, which hook
  to use, and the ten people to engage with. Saves the plan to
  ~/.claude/linkedin/plan.md for the other skills. Use when the user asks for
  a content plan, content calendar, "what should I post this week", a
  posting schedule, or who to engage with.
---

# li-plan

A week of posts built from what actually happened, not from a topic list.

## Input

Read these if they exist:

- `~/.claude/linkedin/voice.md` - who the user is, what they sell, their
  positions and their proof.
- `~/.claude/linkedin/log.md` - what they've posted recently. Don't repeat a
  theme or hook from the last two weeks.
- `~/.claude/linkedin/audit.md` - what's worked, from `/li-audit`. If it
  exists, its findings override the defaults below.

Then ask, in one message, for anything missing:

1. What they offer, and to whom.
2. The 3-4 themes they want to be known for.
3. **What happened this week**: a client conversation, a number, a mistake,
   something built, a decision, a disagreement. This is the raw material.
4. 10-20 people or companies they want to be visible to.

## What to post

Default to **three or four posts a week**. More is fine only if quality
holds; the extra post is usually the weakest one.

Mix the types, never the same type two days running:

| type | how often | purpose |
| --- | --- | --- |
| **Proof** | weekly | something that happened, with a number |
| **Opinion** | weekly | a stance some of the audience will disagree with |
| **Teach** | weekly | one thing the reader can use today |
| **Story** | every other week | a moment, a person, a cost |
| **Offer** | every other week | what the user sells, said plainly |

For each slot give the type, an **angle** taken from this week's events (not
a topic: "hiring" is a topic, "the candidate who asked us for our onboarding
doc before signing" is an angle), and a hook number from
`../li-post/hooks.json`.

## When to post

For a B2B audience, weekday mornings in the audience's time zone (roughly
7:30-9:30am, Tuesday-Thursday) are a reasonable default, with Monday
afternoon and Friday morning next. Weekends suit personal stories, or rest.

Say it plainly: timing matters much less than the hook. If the user is
tuning hours before their first lines are strong, tell them so. If
`audit.md` has real timing data, use it instead.

## Who to engage with

Ten people, three groups:

- **5 reach**: bigger accounts whose audience the user wants. Comment early,
  while the thread is still small.
- **3 peers**: similar size and field. The people most likely to engage back.
- **2 buyers**: people who could hire or buy. Comment for weeks before any
  DM, and never pitch in a comment.

About 20 minutes a day, ideally just before posting. `/li-comment` writes the
comments.

## Output

```
WEEK OF NOV 16

MON  -        engage only (20 min)
TUE  8:15am   PROOF    #17 Time Compression - month-end close from 2 days to 40 min
WED  -        engage only
THU  8:00am   OPINION  #1  Contrarian       - why we stopped doing quarterly OKRs
FRI  8:30am   TEACH    #21 Give It Away     - the 3-question retro template
SUN  -        rest

ENGAGE
  reach:  ...
  peers:  ...
  buyers: ...

Say "write Tuesday" and I'll draft it with /li-post.
```

Save it to `~/.claude/linkedin/plan.md` (create the folder if needed). Nothing
is scheduled anywhere; the user runs the plan.
