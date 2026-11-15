---
name: li-inbox
description: >-
  Triage a LinkedIn inbox: sort pasted messages into lead, recruiter, peer,
  ask and spam, spot automated outreach sequences, and draft replies for the
  ones worth answering. Use when the user pastes LinkedIn messages and asks
  what to reply, wants to clear their inbox, asks "is this a real
  recruiter", or says "help me answer my DMs".
---

# li-inbox

Sort first, reply second, and only to what deserves it.

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

The user pastes the messages, or screenshots of them. Never log in to their
account or read the inbox with a browser.

Read `~/.claude/linkedin/voice.md` if it exists, for what they offer and how
they write.

## Sort into five

| bucket | signs | action |
| --- | --- | --- |
| **LEAD** | describes a problem the user solves, or asks about working together | reply today, with a real answer |
| **RECRUITER** | a specific role, company, level or pay range | reply if real and relevant; one line if not |
| **PEER** | someone in the field with something real to say | reply this week |
| **ASK** | wants advice, an intro, time or a favour | help if it's small and specific; decline kindly if not |
| **SPAM** | sales sequences, agency pitches, crypto, "quick question" with no question | archive, no reply |

Show the counts first. "2 leads, 1 recruiter, 23 spam" is most of the value
on its own.

## Spotting a sequence

Automated outreach has a pattern: a vague connection note, a pitch minutes
after accepting, "I noticed you're in {industry}", "quick question", a
calendar link in the first message, then a "bump" a few days later. When you
see it, mark it SPAM and name the giveaway. The user doesn't owe a script a
reply.

## Writing replies

- **LEAD**: answer their question properly, for free. If it's a fit, one
  sentence at the end offers next steps. If it's not, say so and point them
  somewhere useful.
- **RECRUITER**: if interesting, ask what the message left out: pay range,
  level, location or remote policy, and the hiring timeline. If not, one
  polite line, and offer to refer someone only if the user would.
- **PEER**: reply like a person, keep the conversation going.
- **ASK**: if it takes under ten minutes and is specific, help. If it's
  "can I pick your brain", decline warmly and give the one most useful
  answer in the message itself.
- **Declines** are short, kind and final. No "let's reconnect next quarter"
  unless that's true.

Never invent availability, rates, or facts about the user.

## Output

```
INBOX  ·  31 messages  ·  2 LEAD · 1 RECRUITER · 3 PEER · 2 ASK · 23 SPAM

LEAD
Maya Chen (Ops Director, Northwind) - asking how we cut onboarding time
> ...

SPAM (23) - archive
19 follow the same sequence: generic note, pitch within minutes of
accepting, calendar link in message one.
```

Replies only for the buckets that get one, each cleaned with `/li-human`. The
user sends them.
