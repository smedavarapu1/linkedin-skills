# linkedin-skills

Eleven [Claude Code](https://claude.com/claude-code) skills for running a
LinkedIn presence: posts, comments, replies, profile, weekly plan, DMs,
inbox, carousels, repurposing, analytics, and a humanizer that cleans and
scores every draft before you see it.

No API keys, no accounts to connect, nothing uploaded. **Nothing is ever
posted for you**: each skill hands you text to review and paste yourself.

## Install

As a plugin, in Claude Code:

```
/plugin marketplace add smedavarapu1/linkedin-skills
/plugin install linkedin-skills@linkedin-skills
```

Or copy the skills in directly:

```bash
git clone https://github.com/smedavarapu1/linkedin-skills.git
cp -r linkedin-skills/skills/li-* ~/.claude/skills/
```

For one project only, copy them into that project's `.claude/skills/`
instead.

**Then set up your voice.** Copy [`templates/voice.md`](templates/voice.md)
to `~/.claude/linkedin/voice.md` and fill it in, or paste three of your own
posts into Claude and ask it to write the file for you. Every skill reads it.

## The skills

| command | what it does |
| --- | --- |
| `/li-post` | One idea into a post: three hooks from [21 formulas](skills/li-post/hooks.json), one draft, cleaned by `/li-human`. |
| `/li-comment` | Comments on other people's posts, picked from nine types. Never "Great post!". |
| `/li-reply` | Sorts the comments under your post (lead, substance, peer, support, noise) and drafts replies in that order. |
| `/li-profile` | Scores your profile against a [100-point rubric](skills/li-profile/rubric.json) and rewrites the weakest parts first. |
| `/li-plan` | The week: what to post, when, which hook, and ten people to engage with. Saves `plan.md`. |
| `/li-human` | The humanizer: two Python scripts that clean a draft and score it. |
| `/li-carousel` | Document posts: slide copy, caption, and a 1080x1350 PDF. |
| `/li-repurpose` | One transcript, article or newsletter into a week of standalone posts. |
| `/li-dm` | Connection note (under 200 chars), first message, and two follow-ups. |
| `/li-inbox` | Sorts pasted messages into lead, recruiter, peer, ask and spam, and spots automated sequences. |
| `/li-audit` | Ranks past posts by engagement rate and reach, not impressions, and says what to do more and less of. |

## Shared files

The skills share state in `~/.claude/linkedin/`:

| file | written by | read by |
| --- | --- | --- |
| `voice.md` | you (or `/li-post` on first run) | all |
| `plan.md` | `/li-plan`, `/li-repurpose` | `/li-post`, `/li-comment` |
| `log.md` | `/li-post`, `/li-comment` | `/li-plan`, `/li-audit`, `/li-repurpose` |
| `audit.md` | `/li-audit` | `/li-plan` |

## The humanizer

[`skills/li-human`](skills/li-human) has two dependency-free Python scripts
that run locally:

```bash
python humanize.py draft.txt -o clean.txt --report   # clean it, list the changes
python detect.py clean.txt                           # score it
python detect.py draft.txt clean.txt                 # before vs after
```

**Fixed automatically:** invisible Unicode characters (zero-width spaces,
joiners, BOMs, tag characters, odd spaces), em dashes, curly quotes and
other typography, and ~120 stock words and phrases from
[`slop.json`](skills/li-human/slop.json), with capitalisation kept and URLs
untouched.

**Flagged for you to rewrite:** "it's not just X, it's Y", triads, one-line
reveals ("The result?"), stock emoji, hashtag walls, bait closers like
"Thoughts?", and a few more. Changing sentence shape needs judgement, so the
script points and you rewrite.

**Five checks**, 0-100, higher is more human:

| check | measures |
| --- | --- |
| BURSTINESS | variation in sentence length |
| SPECIFICITY | numbers, dates and names per 100 words |
| SLOP DENSITY | stock vocabulary per 100 words |
| FINGERPRINT | invisible characters, em dashes, curly quotes |
| VOICE | contractions, first/second person, structural tells |

The overall score is 60% the average and 40% the weakest check. PASS is 70+
with nothing under 55.

## Limits, stated plainly

- **These skills don't post to LinkedIn.** Automating a personal account
  with bots, browser scripts or third-party tools is against
  [LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement)
  and can get an account restricted. You paste everything yourself.
- **The detector is a local heuristic,** not GPTZero, Originality.ai or any
  other product, and it calls none of them. It measures the same kinds of
  signals, so improving it tends to help, but no one can promise
  "undetectable".
- **Nothing is invented.** If a draft needs a number or result you haven't
  given, it comes back with `{{number}}` for you to fill in.

## Adding a skill

1. Copy [`templates/SKILL.template.md`](templates/SKILL.template.md) to
   `skills/<name>/SKILL.md`.
2. Write the `description` carefully; it's what Claude uses to decide when
   to run the skill.
3. Put supporting files (JSON, scripts) in the same folder.
4. Add it to the table above.

## Credit

Inspired by the LinkedIn agent skill pack by Jake Schincariol
([opusjake.ai](https://opusjake.ai)), shared at
[mf4996-code/avi691-linkedin-agent-skill](https://github.com/mf4996-code/avi691-linkedin-agent-skill)
(MIT). This repo follows the same set of skills; the text, data and code here
were written independently.

## License

[MIT](LICENSE)
