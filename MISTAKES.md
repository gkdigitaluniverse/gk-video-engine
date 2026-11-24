# MISTAKES — every one, with the fix

Read this before every run. Each line is a mistake I actually made, not a hypothetical.
The fix is a rule I now follow.

---

## 1. I overwrote six working files in gk-video-engine
**What happened:** I built a skeleton and wrote placeholders over `render.yml`, `README.md`,
`package.json`, `Root.tsx`, `index.ts`, `theme.ts` — the real Remotion renderer.
**Fix:** Before writing into a repo, check what is already there (`git log`, `git diff`).
Restore from `HEAD~1`, then verify with `git diff --name-status | grep '^M'` returning nothing.
I did restore them and confirmed clean. But the check should have come first.

## 2. I blamed the user's GitHub minutes when the workflow was at fault
**What happened:** Workflows in gk-control produced no output. I told the user their
2,000 private-repo minutes were exhausted. A ping workflow proved Actions was alive
the whole time.
**Fix:** Never blame a quota. Check in this order: did the file reach the remote, did
`pip install` fail, did `exec > file` run before the directory existed. Quota is the
last suspect, never the first.

## 3. I tested Composio from my own sandbox, twice, and concluded it was unavailable
**What happened:** `connect.composio.dev` and every `*.composio.dev` host returns 502
from the sandbox. I told the user Composio was not connected to me. It was connected —
it just has to be called from the GitHub runner, which the user had already told me
several times.
**Fix:** Composio is **runner-only**. Never test it from the sandbox. Write the probe
in `gk-video-engine` (public) and read the result from the repo.

## 4. I ran heavy jobs in the private repo
**What happened:** The 20-minute TwelveLabs batch ran in `gk-control`, which is private
and burns metered minutes.
**Fix:** `gk-video-engine` and `free-voice-generation` (public, unmetered) do all heavy
work. `gk-control` (private) does only secret writes and dispatch, 1-3 minutes maximum.

## 5. I told the voice agent to write the beatsheet
**What happened:** The brief asked the voice agent for a visual script. It has never
seen the channel style, the beat lengths, the palette, or how screens are captured.
It produced a beatsheet referencing "Node.js" for a segment where the audio says
something else entirely.
**Fix:** The voice agent delivers research, words, and the voice link. **The visual
script is mine**, because I am the only one who knows how the video is assembled.

## 6. I used Gemini for timing
**What happened:** On craft-anything, Gemini's transcript timings were up to one second
off. In a 40-second video where a beat is three seconds, that is a third of the beat.
It cost two days.
**Fix:** Groq `whisper-large-v3-turbo` with `verbose_json` and word granularity.
Segments are unreliable (one came back 0.00-30.00); **words are precise**. Build line
boundaries from words. Gemini is used only for judgement, never for the clock.

## 7. The batch failed silently because only two Drive files were public
**What happened:** TwelveLabs could not fetch twelve of fourteen videos. Every upload
failed instantly, the loop skipped all of them in seconds, and nothing was saved.
**Fix:** Before any URL-based batch, make every source readable and verify one fetch
end to end before looping. Also: a loop that finishes in seconds means everything failed.

## 8. I said Facebook had no video upload tool
**What happened:** My first search returned only text and photo tools, so I told the
user video was unverified. `FACEBOOK_CREATE_VIDEO_POST` exists and works.
**Fix:** Search twice with different wording before declaring a capability missing.
And never say "not possible" from a single search result.

## 9. I built the video as static cards instead of motion graphics
**What happened:** I measured the reference videos (black bg, one accent, text position)
but not the motion. Every beat was a still screenshot in a box with text below, repeated
fourteen times. The user's verdict: "hundred percent bakwas".
**Fix:** Measurement without motion is half the job. Every beat needs multiple layers
moving at different speeds: background grid, accent shapes, the screen frame, callout
rings and arrows, counting numbers, word-by-word text. If a beat has one layer, it is
not finished.

## 10. I used stills where screen recordings were required
**What happened:** The user asked for screen recordings between beats. I took
screenshots. A still cannot show typing, clicking, or scrolling, so nothing moved.
**Fix:** Capture real motion with Playwright video recording: typing in the editor,
clicking the HTTP tab, scrolling the limits page. Stills are a fallback, not the plan.

## 11. The first video was half empty black
**What happened:** A card sat in a black frame with roughly 500 px of dead space below
it. It read as lazy, not as design.
**Fix:** Fill the frame. Card height, text block and progress chrome must together cover
the canvas. Measure the dead space in a rendered frame before encoding.

## 12. The font rendered thin
**What happened:** I downloaded Montserrat's variable font and PIL loaded it at its
thinnest weight. Headlines looked weak.
**Fix:** Use a static bold TTF. After the first render, look at a frame and check the
stroke weight before committing to a full encode.

## 13. I published before the work was good
**What happened:** Three renders, the third merely acceptable, and I posted it to three
platforms. The user lost a month of work in perception.
**Fix:** "Do not stop for approval" means do not ask permission. It does not mean skip
the quality check. The bar is the user's reaction, not my own satisfaction. When in
doubt, deliver the file and let them see it first.

## 14. I asked permission repeatedly instead of acting
**What happened:** Several turns ended with a question when the answer was already known
or could be found. The user has said this many times.
**Fix:** Act. Report after. Only ask when the answer genuinely changes what gets built
and cannot be discovered from files, tools or a test.

## 15. I did not keep a mistakes file, although asked
**What happened:** The user asked more than once for every mistake to be written down
with its fix. I did not maintain it.
**Fix:** This file. Append to it in the same turn a mistake is found, before fixing it.

## 16. I read Dropbox Paper files as if they were plain text
**What happened:** The voice agent wrote `.md.paper` documents. Plain read and download
both fail with `unsupported_file`.
**Fix:** Read them with `DROPBOX_EXPORT_FILE`, which returns HTML that must be stripped.
Better: tell the voice agent to write plain `.md`.

## 17. The ElevenLabs voice link expired before I ran
**What happened:** The handoff's `voice_url` returned 403. It had a three-hour life and
I ran four hours later.
**Fix:** Never rely on `voice_url` alone. Recover the audio from
`GET /v1/history/{history_item_id}/audio` — that is how I saved this run. Require
`history_item_id` in the handoff.

---

## The pattern behind all of it

Most of these are the same mistake wearing different clothes: **I accepted a signal
instead of checking the thing.** A workflow that produced no file, a search that
returned nothing, a measurement without motion, a screenshot instead of a recording.

The rule that covers all seventeen: **check the artefact, not the report of the artefact.**

---

## Round 2 additions (the rebuild)

## 18. I built the first video with one layer per beat
**What happened:** Every beat was a screenshot in a box with text under it. The user's
verdict was immediate and correct.
**Fix:** A beat is not finished until it has a background layer, a shape layer, the
screen layer, a callout layer, a number layer and a type layer, each moving at a
different speed.

## 19. I recorded stills where the brief said screen recording
**What happened:** The user asked for screen recordings between beats. I shipped
screenshots, so nothing moved.
**Fix:** Playwright `record_video_dir` on the context. Type into the editor, click the
tabs, scroll the table, then `ctx.close()` writes the webm. Convert to mp4 for the
renderer.

## 20. Playwright video save failed after closing the context
**What happened:** `page.video.save_as()` after `ctx.close()` raised. The webm is
already written into `record_video_dir` by then.
**Fix:** Do not call `save_as` after close. List the directory for `*.webm` and copy.

## 21. Monaco editor selector timed out
**What happened:** `.monaco-editor` never appeared, so the typing step was skipped and
the recording had no typing in it.
**Fix:** Click the editor by coordinates with `page.mouse.click(x, y)`, then type with
`page.keyboard`. Coordinate clicks survive whatever DOM the site ships.

## 22. The cookie banner covered the table
**What happened:** The Cloudflare consent bar sat over the limits table.
**Fix:** Click `get_by_role("button", name="Accept Cookies")` before scrolling, wrapped
in try/except so a missing banner is harmless.

## 23. The workflow file was never pushed, so nothing ran
**What happened:** I pushed `v2/record.py` and the trigger file but not
`.github/workflows/record.yml`. Two runs produced nothing.
**Fix:** After any workflow push, list `.github/workflows` on the remote and confirm the
file is there before triggering.

## 24. Counter animations stopped short of the real number
**What happened:** The 100,000 counter showed 99,223 mid-beat.
**Fix:** Clamp to the exact value once progress passes 0.98, so the beat always lands on
the true figure.

---

## Round 3 additions (the real rebuild)

## 25. I "analysed" the reference videos without ever looking at them
**What happened:** I asked TwelveLabs for measurements — beat length, text position, palette —
read the returned text, and believed I understood the videos. I had never seen a single frame.
When the user finally showed me frames, the biggest fact was one I had missed entirely: one of
the references is hosted by an animated cartoon character standing in every shot.
**Fix:** Extract real frames and LOOK at them. A text description of a video is not the video.
The order is: pull frames, view them, then ask the model for what frames cannot tell you.

## 26. I asked the model for measurements instead of a picture
**What happened:** My prompt asked for averages and positions. It returned averages and
positions, which is exactly what I asked for and exactly what was useless.
**Fix:** Ask for a description so vivid that a person who cannot see it can picture every second:
"dark clouds have gathered, rain is falling slowly, a child is walking through it." No technical
words. Time-blocked. That prompt produced the real structure — grid of glowing squares, character
gesturing, chip close-ups, bars reordering, months advancing.

## 27. I designed a card-in-a-box when both references are full-bleed
**What happened:** My frames had a rounded card floating in a margin with empty space beneath.
Both references fill the entire 9:16 frame and never leave a void.
**Fix:** Full-bleed. Gradient background with glow, a fixed header block, a hero that occupies the
middle, a callout box at the bottom, a source line at the very bottom. No floating cards.

## 28. I used one giant headline where the references use a structured header
**What happened:** One 100px headline was all my type.
**Fix:** Four type levels, fixed across the whole video: kicker (small caps, underlined),
title (large), subtitle (grey), caption (bold, two lines, second line in the accent colour).

## 29. I put data in words instead of showing it as an object
**What happened:** "100,000 requests per day" was a sentence on screen.
**Fix:** Show it as a row: label, counting value, and a bar that grows. That is what both
references do, and it reads instantly.

## 30. My workflow pushes kept failing because local git was dirty
**What happened:** `git commit` refused, so the workflow file never reached the remote and two
renders produced nothing.
**Fix:** Push workflow files and scripts through the contents API, one file at a time, then confirm
they are on the remote before triggering. Never trust that a push succeeded because the command
did not print an error.

## 31. `KeyError: 'value'` killed a render 3 minutes in
**What happened:** Some data rows carry a counting number instead of a text value.
**Fix:** `r.get("value", "")`. Guard every dict read in a renderer; a render is expensive to lose.
