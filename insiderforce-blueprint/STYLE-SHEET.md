# GK HACKTER — Motion-Graphics-Only Master Style Sheet (`insiderforce-blueprint`)

> **Architecture Purpose:** Synthesized from 4 high-retention reference reels (`insiderforce.io` x3 + `@Explivolt` hardware explainer), redesigned exclusively for **GK HACKTER** (`@gkhackter`) as a **100% pure Motion Graphics + Real Screenshots + AI 3D Assets** system.
> **Hard Rule:** **NO 2D talking cartoon avatar or fake human presenter.** Every pixel of the 9:16 frame is dedicated to tactile 3D hero objects, real product/code screenshots, kinetic typography, and diagram motion.

---

## 1. Core Aesthetic DNA (Why This Style Holds Retention)

1. **Matte Tactile Studio Canvas (`#EFEFEF`):** Instead of noisy neon gradients or cheap stock video, the stage is a clean Apple-industrial matte light-gray canvas with a subtle architectural dot grid (`28px` pitch) and soft directional studio drop-shadows (`0 30px 70px rgba(0,0,0,0.16)`).
2. **Editorial Kinetic Typography + Inverted Black Pill Highlights:**
   - Secondary words appear in crisp medium gray (`#8E8E93`).
   - Spoken / active emphasis words snap to **Bold Jet Black (`#0D0D0D`)**.
   - Power phrases (1–3 words) punch onto a **Solid Jet Black Inverted Pill (`#0D0D0D` fill, `#FFFFFF` text, deep soft shadow)** — immediately guiding the eye.
3. **AI-Generated 3D Hero Renders (Blended Seamlessly):**
   - Generate topic-specific photorealistic 3D objects on a solid `#F2F2F2` studio background (no text, no watermarks).
   - Render them inside Remotion with `mixBlendMode: "multiply"` so the studio gray melts invisibly into the canvas while keeping crisp 3D shadows and specular reflections!
4. **Real Website / GitHub / Terminal Screenshots in Floating Shadowed Cards:**
   - Never fake a website when the real page exists. Capture live screenshots (via Playwright or GitHub Release assets) and animate them inside rounded white/dark cards with smooth Ken Burns pan/zoom and an optional **animated scanning magnifying glass**.
5. **Tactile Raised 3D Node Diagrams & Stacked Notification Cards:**
   - Flow diagrams use raised white squircle tiles (`box-shadow` + subtle border) connected by razor-thin animated black SVG lines.
   - Limitations / warnings use vertical connected `✕` checklists or cascading stacked alert cards.
6. **Topic-First Visual Adaptation (Never Copy-Paste a Previous Video):**
   - Every topic chooses its own visual grammar from the component library (e.g., Security → 3D Shield + Laser Lock + Magnifying Glass + `.env` Vault; APIs → Live Terminal + Request Cards + Quota Bars).

---

## 2. Layout & Safe-Zone Grid (`1080 × 1920`, 9:16 Vertical)

| Zone | Y-Range (px) | Purpose |
|---|---:|---|
| **Top Safe Margin** | `0 – 110` | Clear of YouTube Shorts / IG Reels top chrome. |
| **Upper Hero Visual Stage** | `140 – 1060` | AI 3D hero render, floating real screenshot card, node diagram, or stacked cards. |
| **Kinetic Editorial Caption** | `1100 – 1560` | Large 64–78px kinetic typography with bold black emphasis + inverted black highlight pill. |
| **Micro Source & Brand Anchor** | `1640 – 1760` | Subtle muted `@gkhackter` watermark + verified source domain (matches `insiderforce.io` clean bottom anchor). |
| **Bottom Safe Margin** | `1760 – 1920` | Clear of YouTube/IG description & buttons. |

---

## 3. Color & Shadow System (`src/theme.ts`)

| Token | Value | Role |
|---|---|---|
| `CANVAS` | `#EFEFEF` | Signature matte studio background |
| `SURFACE` | `#FFFFFF` | Floating raised tiles, cards, browser frames |
| `DARK_CARD` | `#0F1115` | High-contrast code/terminal/warning cards |
| `INK` | `#0D0D0D` | Primary kinetic typography & inverted pill fill |
| `INK_MUTED` | `#8E8E93` | Unemphasized words & secondary captions |
| `EMERALD` | `#10B981` | Verified, protected, `.env` safe state |
| `CRIMSON` | `#EF4444` | Leaked key, blocked push, 50 MB limit |
| `SHADOW_SOFT` | `0 28px 64px rgba(0, 0, 0, 0.14)` | Floating screenshot & tile elevation |
| `SHADOW_PILL` | `0 14px 32px rgba(0, 0, 0, 0.24)` | Inverted black highlight bar elevation |

---

## 4. Reusable Component Library (`src/components/`)

| File | Components | Usage |
|---|---|---|
| `KineticCaption.tsx` | `KineticCaption` | Editorial multi-line kinetic text with word-by-word bolding + inverted black pill bar. |
| `AIHeroVisual.tsx` | `AIHeroVisual` | Renders AI-generated 3D studio renders (`public/ai/*.jpg`) with `multiply` blend + gentle 3D float/zoom. |
| `RealShotCard.tsx` | `RealShotCard`, `ScanningLens` | Floating shadowed browser frame for real Playwright/GitHub screenshots + optional animated magnifying glass scan. |
| `MotionDiagrams.tsx` | `NodeFlowDiagram`, `StackedAlerts`, `BigCounterCard`, `CrossChecklist`, `CodeFixCard` | Tactile 3D node-connector flow, cascading alert stack, animated 532/465 counter, connected `✕` checklist, `.env` fix card. |

---

## 5. How Any Future Agent Builds a New Video Using This Blueprint

1. **Generate 2–3 Topic-Specific AI 3D Hero Images** on a clean `#F2F2F2` studio background (no text/watermarks) and place them in `public/ai/`.
2. **Capture Real Screenshots / Recordings** of the actual repo, docs, or tool UI and place them in `public/shots/`.
3. **Edit `src/data/beats.ts`** with your voiceover's exact timestamps, kinetic caption lines, inverted pill phrase, and chosen visual scene type.
4. **Render via `.github/workflows/insiderforce-blueprint-render.yml`** — produces a 1080×1920 30fps MP4 with mixed audio, 6 QC stills, and GitHub Release upload.
