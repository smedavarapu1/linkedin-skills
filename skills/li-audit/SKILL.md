---
name: li-audit
description: >-
  Review the user's past LinkedIn posts to find what actually works: ranks
  posts by engagement rate and reach rather than raw impressions, compares
  the top and bottom performers, and says what to do more and less of. Use
  when the user shares LinkedIn analytics, an export CSV, or post stats and
  asks what's working, why posts flopped, or what to change.
---

# li-audit

Look back at what's been posted and find the real pattern, if there is one.

## Input

Any of these, best first:

1. The LinkedIn analytics export (an .xlsx or CSV from the analytics page).
2. Screenshots of each post's stats: impressions, reactions, comments,
   reposts.
3. Just the posts and their reaction and comment counts. Enough for a first
   look.

Also ask for the current follower count, and read
`~/.claude/linkedin/log.md` if it exists: it records which hook each post
used.

## Measure the right things

Impressions mostly reflect follower count, so they're the weakest signal.
Work out these, and show the calculation:

| metric | formula | tells you |
| --- | --- | --- |
| **Engagement rate** | (reactions + comments + reposts) / impressions | did the post earn its reach |
| **Comment ratio** | comments / reactions | did it start a conversation or just get nods |
| **Reach multiple** | impressions / followers | did it travel beyond existing followers |
| **Saves / sends** | if the export has them | strong sign of genuinely useful content |

Rank by engagement rate and reach multiple. A post with 1,000 impressions
and 35 comments outperformed one with 10,000 impressions and 4.

If the data is a spreadsheet, compute with a short script rather than by
hand, and keep the numbers exact.

## Find the pattern

Put the top five and bottom five side by side and compare:

- **Hook type** (from the log or by reading the first line against
  `../li-post/hooks.json`)
- **Format**: text, image, document, video, poll
- **Length**
- **Theme**
- **Whether the user replied** to comments in the first hour
- **Day and time**: check this last. It's rarely the real cause.

State each finding as a claim with its evidence and how confident you are.
Sample size matters: with around 30 posts a pattern can show; with 6 it
can't, and you should say so instead of finding one anyway. Don't tell the
user what they want to hear; if their favourite format is underperforming,
say it.

## Output

```
AUDIT  ·  28 posts  ·  Aug 4 - Nov 10  ·  2,140 followers

TOP 5 BY ENGAGEMENT RATE
  7.4%  #3  Owned Mistake     "I hired for culture fit..."         1,610 imp
  ...

BOTTOM 5
  0.6%  #5  Specific List     "7 AI tools I use daily"            9,800 imp
  ...

FINDINGS
1. Posts where you admit a mistake: avg 6.1% vs 1.4% for the rest (n=5).
   Strongest signal here.
2. Tool lists get impressions but almost no comments. 3 of the bottom 5.
3. Posting day shows no clear effect. Tue and Fri averages are within noise.

DO MORE:  owned mistakes with a cost attached
DO LESS:  tool lists
```

Save the findings to `~/.claude/linkedin/audit.md` so `/li-plan` builds next
week from the user's own results rather than general advice.
