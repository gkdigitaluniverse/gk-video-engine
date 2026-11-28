# Explivolt-Grade Video Style Sheet & Architectural Blueprint (GK HACKTER)

> **Purpose (घर का पूरा नक्शा):** This document is a **complete, self-contained visual & code blueprint** reverse-engineered from high-retention tech explainer shorts (reference: `@Explivolt` 96s Claude breakdown) and upgraded for **GK HACKTER** (`@gkhackter`). Any AI agent or developer can read this file + `src/components/` and build an identical-or-better high-retention Short **without ever needing to watch the reference video**.

---

## 1. Why High-Retention Explainers Beat 95% Skip Rate

Traditional "slide + stock B-roll + huge bouncing text" shorts get swiped away in 2 seconds because they look automated and static. This blueprint eliminates skip rate with **6 structural rules**:

1. **0–3s Action Hook (Zero Slow Intro):** Frame 1 opens directly on a crisp, clean Light Canvas (`#F7F5F0`) with a live interactive UI mockup (e.g., MacBook / Browser / App) already *doing something* (cursor clicking, code running, lid closing).
2. **Persistent Top Chapter Stepper (Open Loop):** A horizontal 5-chapter progress bar (`HOOK → NO SETUP → LIVE TEST → FREE LIMITS → CATCH`) sits under the top caption. Viewers stay because they visually see the next chapter lighting up.
3. **Light ↔ Dark Pattern Breaks Every 10–20s:** Alternate between **Warm Cream Light Mode (`#F7F5F0`)** and **Deep Obsidian Dark Mode (`#09090B`)** at chapter boundaries. This resets visual fatigue instantly.
4. **Top-Center Word-Boxed Captions (Never Center-Screen Spam):** Captions live in a fixed top safe zone (`y: 95px–230px`). Every word is legible, while ONLY the **currently spoken word** gets a crisp tinted bounding box + subtle spring pop matching the active chapter's accent color.
5. **Code-Drawn Concept Diagrams (Zero Generic Stock Clutter):** Every technical claim is visualized as an animated UI widget: split-pane IDE, live typing code, animated cursor click, dot-matrix quota grid, horizontal speed gauges, red-struck vs green-checked comparison cards.
6. **Bottom 2D Presenter Avatar (Human Anchor):** A clean 2D vector presenter sits at the bottom (`y: 1380px–1920px`) with subtle breathing, eye blinks, mouth lip-sync pulse while speaking, and **beat-driven hand/expression poses** (`explain`, `pointUp`, `thumbsUp`, `thinking`, `shocked`, `okSign`, `count3`, `wave`).

---

## 2. Canvas, Layout & Safe-Zone Grid (`1080 × 1920` Vertical 9:16)

| Zone | Y-Range (px) | Height | Content | Rule |
|---|---:|---:|---|---|
| **Top Safe Margin** | `0 – 90` | 90px | Empty / status clearance | Never put text here (YouTube/IG top UI overlap). |
| **Caption Zone** | `90 – 250` | 160px | Word-by-word boxed caption | Max 2 lines, 42–48px bold, centered, fixed Y. |
| **Handle + Stepper** | `265 – 370` | 105px | `@gkhackter` tag + 5-dot chapter stepper + micro source citation | Always aligned; source citation in 18px muted mono. |
| **Hero Visual Stage** | `390 – 1370` | 980px | Primary animated UI mockup / diagram / cards | 80px left/right padding (`width: 920px`). Max 1 focal object per beat. |
| **Presenter Layer** | `1380 – 1920` | 540px | 2D animated presenter avatar (bottom-center/right) | Never covers hero text; right-side UI buttons stay clear of bottom-right IG/YT icons. |

---

## 3. Exact Color System (`src/theme.ts`)

### Surface Tokens
- **Light Mode Canvas:** `#F7F5F0` (Warm Editorial Cream) — Card Surface: `#FFFFFF`, Card Border: `#E4E2DC`, Primary Ink: `#111111`, Muted Ink: `#6B7280`.
- **Dark Mode Canvas:** `#09090B` (Deep Obsidian) — Card Surface: `#141418`, Card Border: `#27272A`, Primary Ink: `#F8FAFC`, Muted Ink: `#94A3B8`.

### Chapter Accent Tokens (Used for Active Stepper Dot, Active Word Box, Badges & Glows)
| Role | Hex | Soft Tint (Light) | Soft Tint (Dark) | Use Case |
|---|---|---|---|---|
| **Brand / Hook Orange** | `#F97316` | `rgba(249,115,22,0.14)` | `rgba(249,115,22,0.22)` | Hook, Active Stepper, Brand Highlight |
| **Tech Blue** | `#3B82F6` | `rgba(59,130,246,0.14)` | `rgba(59,130,246,0.22)` | Architecture, Setup, Code Flow |
| **Live Teal** | `#0D9488` | `rgba(13,148,136,0.14)` | `rgba(20,184,166,0.22)` | Live Preview, Real-Time Output |
| **Quota Purple** | `#8B5CF6` | `rgba(139,92,246,0.14)` | `rgba(139,92,246,0.22)` | Scale, Counters, Dot-Matrix Grids |
| **Speed Gold** | `#F59E0B` | `rgba(245,158,11,0.15)` | `rgba(245,158,11,0.22)` | Benchmarks, Latency, Performance |
| **Verified Green** | `#22C55E` | `rgba(34,197,94,0.14)` | `rgba(34,197,94,0.22)` | Success, 200 OK, Checklists, CTA |
| **Catch / Warning Red** | `#EF4444` | `rgba(239,68,68,0.14)` | `rgba(239,68,68,0.22)` | Limitations, Disconnected, Errors |

---

## 4. Typography & Motion Grammar

- **Display & Captions:** `Inter` / `Plus Jakarta Sans` (Weights `600`, `700`, `800`). Clean geometric sans-serif—no cluttered grunge or unreadable condensed fonts for body text.
- **Code, URLs, Metrics & Citations:** `JetBrains Mono` / `Space Mono` (Weights `500`, `700`).
- **Physics Rule:** Use Remotion `spring()` for all entrances (`damping: 16, stiffness: 160, mass: 0.75` for snappy cards; `damping: 20, stiffness: 120` for smooth glides). **Never use flat linear pops.**
- **Micro-Motion Rule:** Even during a 3-second beat, at least 3 elements remain alive (active word box stepping, blinking cursor / pulsing live dot / filling progress bar, avatar eye blink + lip-sync + gentle float).

---

## 5. Component Map (How to Build a New Video in 15 Minutes)

Every reusable building block lives in `explivolt-blueprint/src/components/`:

| File | Exported Components | Purpose |
|---|---|---|
| `src/theme.ts` | `THEME`, `ACCENTS`, `SPRINGS`, `SAFE_ZONES` | Central design tokens for Light/Dark modes & physics. |
| `src/components/TopCaption.tsx` | `TopCaption` | Word-by-word boxed highlight subtitle synced to beat timestamps. |
| `src/components/ChapterStepper.tsx` | `ChapterStepper` | 5-node top progress bar + `@gkhackter` handle + source micro-citation. |
| `src/components/PresenterAvatar.tsx` | `PresenterAvatar` | 2D animated SVG presenter with 7 poses (`explain`, `pointUp`, `thumbsUp`, `thinking`, `shocked`, `okSign`, `wave`), blinking eyes & speech mouth animation. |
| `src/components/DeviceMockups.tsx` | `MacBookFrame`, `BrowserWindow`, `AnimatedCursor`, `TerminalCompare` | Interactive laptop, split-pane IDE, HTTP request tab, animated cursor click. |
| `src/components/DataVisuals.tsx` | `DotMatrixCounter`, `SpeedMeterBar`, `CompatMatrix`, `StepFlowCard`, `EndCardCTA` | Glowing 100k quota grid, 10ms CPU bar, Desktop-only matrix, spotlight CTA. |
| `src/data/videoData.ts` | `CHAPTERS`, `BEATS`, `VIDEO_META` | Pure declarative timing & script data — **swap this file to make a brand-new video!** |

---

## 6. How to Reuse This Blueprint for Any New GK HACKTER Video

1. Copy `explivolt-blueprint/` or update `src/data/videoData.ts` with your new audio duration, 4–5 chapters, and beat timestamps (`s`, `e`, `captionWords`, `chapterIndex`, `pose`, `sourceCitation`).
2. Drop your voiceover (`voice.wav` / `voice.mp3`) and background music (`bgm.mp3`) into `public/audio/`.
3. Map each beat in `src/Main.tsx` to the appropriate reusable visual widget (`MacBookFrame`, `DotMatrixCounter`, `SpeedMeterBar`, `CompatMatrix`, etc.), alternating `mode: "light" | "dark"` at chapter switches.
4. Run the GitHub Actions workflow `.github/workflows/explivolt-blueprint-render.yml` — it renders the final MP4, mixes voice + ducked BGM with FFmpeg `loudnorm`, exports 6 QC stills into `out/`, and publishes the MP4 to GitHub Releases.
