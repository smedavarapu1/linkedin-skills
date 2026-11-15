---
name: li-carousel
description: >-
  Turn an idea with steps or parts into a LinkedIn document (carousel) post:
  slide-by-slide copy, the caption that goes above it, and a 1080x1350 PDF
  ready to upload. Use when the user asks for a carousel, a document post,
  slides for LinkedIn, a PDF post, or wants a framework, checklist or
  step-by-step guide turned into swipeable slides.
---

# li-carousel

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

## Is it a carousel at all?

Carousels work when the idea has **order or parts**: steps, a framework, a
before-and-after, a checklist, a ranked list. A single claim stretched over
eight slides is a weak text post. If that's what the user has, say so and
send them to `/li-post`.

## Structure

8-12 slides. Fewer and it should be a text post; many more and people stop
swiping.

```
1          COVER     the hook in 6 words or fewer, plus one line of promise
2          WHY       why this matters, one sentence
3..N       ONE IDEA PER SLIDE: 3-7 word headline, at most 25 words below it
N+1        SUMMARY   everything on one slide, so a screenshot is useful alone
LAST       CTA       one action: follow, comment, save, or visit a link
```

## Copy rules

- **The cover decides everything.** Short, big, specific.
- **Number the slides** ("4/10"). Seeing the end keeps people swiping.
- **No paragraphs.** Over 25 words on a slide means two slides.
- **The summary slide is the one people save.** It must make sense alone.
- **Handle on every slide**, small, in a corner. Screenshots travel.
- **Never invent** numbers or results. Use `{{number}}` and ask.

Read `~/.claude/linkedin/voice.md` if it exists; slide copy should still
sound like the user.

## Workflow

1. Write the slide copy as a numbered list the user can scan in seconds.
2. Write the **caption**: 2-4 lines that appear above the document in the
   feed. It needs its own hook (pick one from `../li-post/hooks.json`).
3. Run the caption and slide copy through `/li-human`.
4. **Wait for the user to approve the copy.** Then build the PDF.

## Building the PDF

LinkedIn accepts PDF documents. Use 1080x1350 px (4:5) pages; that fills the
most screen on mobile.

Write one HTML file with a `<section>` per slide:

```css
@page { size: 1080px 1350px; margin: 0; }
section { width: 1080px; height: 1350px; page-break-after: always;
          box-sizing: border-box; padding: 96px; }
```

- One accent colour, high contrast, nothing smaller than about 28px: people
  read these on phones.
- If the project has a brand guide or design system, use it rather than
  inventing one.
- Ask before using any logo or image the user didn't provide.

Print it to PDF with headless Chrome or Edge, for example:

```bash
chrome --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=carousel.pdf carousel.html
```

(On Windows the binary is usually `msedge` or the full path to
`chrome.exe`.) Check the page count matches the slide count, and open the
PDF to confirm nothing overflows a page.

## Output

Slide copy, caption, then the PDF path once built. Nothing is uploaded; the
user posts the document themselves.
