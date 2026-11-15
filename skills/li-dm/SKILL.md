---
name: li-dm
description: >-
  Write LinkedIn outreach that gets answered: the connection note (under 200
  characters), the first message after they accept, and at most two
  follow-ups. Use when the user wants to connect with or message someone on
  LinkedIn, asks for a connection request note, a cold DM, outreach to a
  prospect, recruiter or hiring manager, or a follow-up to someone who went
  quiet.
---

# li-dm

Short, specific outreach, sent by hand.

## First, get the specifics

Ask in one message:

1. **Who**: name, role, company.
2. **Why now**: a real, specific reason. Something they posted, something
   their company launched, a shared connection, a talk. "They match my
   target customer" isn't a reason they care about.
3. **What the user wants**: a chat, advice, a referral, a job, a sale. Be
   honest about it internally, even if the first message doesn't lead with
   it.

If there's no specific reason to reach out now, say so and suggest how to
get one (comment on their posts for a couple of weeks with `/li-comment`).
Reasonless messages are why most outreach gets ignored.

Read `~/.claude/linkedin/voice.md` if it exists.

## Connection note (max 200 characters)

`{one specific thing about them} + {who the user is, briefly} + {no ask}`

The note makes accepting easy. It asks for nothing. Count every character
including spaces, and show the count.

```
Your post on cutting standups to 3 a week matched what we found at our
team of 9. I lead platform eng at a fintech. Would be good to stay in touch.
                                                                  [158/200]
```

## First message (after they accept)

Wait at least a day, then:

- **2-4 sentences.** A long block gets skipped.
- **Pick up the thread** from the note.
- **Give before you ask**: an answer, a resource, a useful name, a data point.
- **One small ask.** "Open to a 15-minute call next week?" Not a demo, not
  "pick your brain".
- **No calendar link** in the first message.

## Follow-ups: two, then stop

- **Day +4**: something new and useful. Never "just bumping this". Nothing
  new means no follow-up.
- **Day +10**: close the loop. Say this is the last message, kindly, and
  leave the door open. This often gets a reply because it removes pressure.

A third follow-up rarely helps and costs goodwill.

## Never

- Never send messages or invites for the user, and never suggest automation
  tools. Automated outreach breaks LinkedIn's User Agreement and gets
  accounts restricted.
- Never invent a mutual connection, shared school, or having read something
  the user hasn't read.
- No "I hope this message finds you well".
- Suggest no more than about 20 invites a day; LinkedIn limits accounts that
  send too many, especially with many unaccepted.

## Output

Connection note with its character count, first message, both follow-ups
with the day each goes out. All cleaned with `/li-human`. The user sends
each one themselves.
