# `explivolt-blueprint/` — High-Retention Remotion Video System

This folder is a **self-contained, production-ready video architecture** modeled on the `@Explivolt` visual system and built for **GK HACKTER** (`@gkhackter`).

- **Blueprint & Design Rules:** Read [`STYLE-SHEET.md`](./STYLE-SHEET.md) first.
- **Demo Video Included:** Full remake of **Cloudflare Workers Playground** (`42.07s`) using the existing Hindi voiceover (`../v1/voice.wav`), BGM (`../v1/channel-bgm.mp3`), and beat timings (`../v7/beats.json`).
- **Automated Render Workflow:** `.github/workflows/explivolt-blueprint-render.yml`

## Folder Structure

```text
explivolt-blueprint/
├── STYLE-SHEET.md           # Full visual & motion blueprint ("घर का नक्शा")
├── README.md                # Quick-start guide
├── package.json             # Remotion 4.0.546 + React 19
├── tsconfig.json
├── index.ts                 # Remotion entry point
├── src/
│   ├── theme.ts             # Light/Dark palettes, accents, typography, springs
│   ├── Root.tsx             # Composition registration (1080x1920 @ 30fps)
│   ├── Main.tsx             # Full 14-beat Cloudflare Workers Playground remake
│   ├── data/
│   │   └── videoData.ts     # Declarative chapters, beats, captions & avatar poses
│   └── components/
│       ├── TopCaption.tsx       # Word-by-word boxed highlight caption
│       ├── ChapterStepper.tsx   # Persistent 5-step progress bar + source note
│       ├── PresenterAvatar.tsx  # 2D animated vector presenter (7 poses + lip-sync)
│       ├── DeviceMockups.tsx    # MacBook, Split IDE, HTTP Tab, Terminal Compare
│       └── DataVisuals.tsx      # 100k Dot-Matrix Grid, 10ms Bar, Catch Matrix, CTA
└── out/                     # QC stills & render log committed by GitHub Actions
```

## Render Locally or via GitHub Actions

```bash
npm install
npx remotion render index.ts ExplivoltDemo out/video_silent.mp4 --codec=h264 --crf=18 --concurrency=2
```

Or push any change inside `explivolt-blueprint/` to trigger `.github/workflows/explivolt-blueprint-render.yml`, which automatically renders the MP4, mixes `v1/voice.wav` + ducked `v1/channel-bgm.mp3` via FFmpeg, captures 6 QC stills, and uploads the final MP4 to GitHub Release `explivolt-blueprint-v1`.
