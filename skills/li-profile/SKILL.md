---
name: li-profile
description: >-
  Score a LinkedIn profile out of 100 against a 12-part rubric, then rewrite
  the weakest sections first: headline, about, featured, experience, banner.
  Use when the user asks to review, audit, score, fix or rewrite their
  LinkedIn profile, headline or about section, or says "why isn't my profile
  getting views".
---

# li-profile

Score honestly, then fix in order of points lost.

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

Ask the user to paste: headline, about section, current role and the two
before it, top three skills, and whether they have a custom banner, a
featured section, recommendations, and recent activity. A screenshot of the
top of the profile is enough to start. Never sign in to LinkedIn for them.

Read `~/.claude/linkedin/voice.md` if it exists, for who they serve and what
they sell. If it doesn't, ask those two things before rewriting anything.

## 1. Score

Read `rubric.json` in this folder (12 items, 100 points). Score each item,
give a reason, and total it:

```
PROFILE SCORE  43 / 100
  headline             4/12   job title only, no audience or result
  about: opening       2/10   starts "Passionate professional with..."
  about: body          5/10   reads like a CV, no next step
  featured             0/8    empty
  banner               0/6    default
  current role         6/10   duties, one number
  ...
```

Be strict. Most profiles score 30-50 the first time. A generous score helps
no one.

## 2. Rewrite, biggest loss first

Do the sections in order of points lost, one at a time, because the user has
to paste each one in. Typical order:

1. **Headline (up to 220 characters).** A pattern that works:
   `{what you do} for {whom} | {proof} | {how to start}`. Offer three
   options. Avoid opening with "Helping..."; so many profiles do now that it
   reads as a template.
2. **About, first two lines.** That's all most people see on mobile. Say who
   is helped and what changes. No "passionate", "results-driven", "dynamic",
   no third-person, don't start with the user's name.
3. **About, body.** Second person, to one reader: their problem, what the
   user does about it, one proof point with a real number, what to do next.
   Keep it under ~1,400 characters.
4. **Featured.** Recommend three items: best post, proof asset, contact. Say
   which existing posts or assets fit, if the user has shared them.
5. **Experience.** One line of scope per role, then 2-3 results with
   numbers. Older than ten years: one line.
6. **Banner.** One positioning line and one way to reach the user. Give the
   text; designing the image is optional (offer to make a 1584x396 HTML
   banner if they want).
7. **Skills.** Suggest the top three to pin, matching the headline.

Every rewrite goes through `/li-human` before the user sees it.

**Never invent** numbers, clients, titles or results. If a bullet needs a
figure the user hasn't given, write `{{number}}` and ask.

## 3. Re-score

Score the rewritten profile and show before, after and the difference. Be
honest about the ceiling: recommendations, photo, banner image and activity
can't be fixed by rewriting text, so say what's left and what it would take.

Nothing is changed on LinkedIn by this skill. The user pastes each section.
