import React from "react";
import {
  AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { MONO } from "./theme";

/* ============================================================
   GK HACKTECH — light-editorial house style, built from the
   five reference videos (02-REF + 00-GOLD-STANDARD).
   Rules: collage not card · one orange-boxed word per headline ·
   terracotta starbursts · sticker pills · 700px screenshots ·
   hot orange · caption with a highlighted word.
   ============================================================ */

const CREAM = "#F3EDE6";
const INK = "#14100C";
const ORANGE = "#EA580C";
const TERRA = "#E08469";
const WHITE = "#FFFFFF";
const GRAY = "#7A7068";
const DARK = "#1B1720";

const FONT = "Montserrat, Inter, Helvetica, Arial, sans-serif";


export const BEATS = [
  { s: 0.00, e: 1.60 },  // hook
  { s: 1.60, e: 3.30 },  // 3 steps
  { s: 3.30, e: 5.10 },  // craft anything / pure rust
  { s: 5.10, e: 6.30 },  // website app game
  { s: 6.30, e: 7.70 },  // copies anything
  { s: 7.70, e: 13.85 }, // STEP 1 STUDY (gemini audio-verified)
  { s: 13.85, e: 15.09 },// STEP 2 BUILD
  { s: 15.09, e: 16.40 },// claude code
  { s: 16.40, e: 19.84 },// any language
  { s: 19.84, e: 21.75 },// STEP 3 CHECK
  { s: 21.75, e: 23.99 },// compared
  { s: 23.99, e: 26.08 },// fix
  { s: 26.08, e: 30.74 },// 91%
  { s: 30.74, e: 32.29 },// i checked
  { s: 32.29, e: 35.54 },// stars
  { s: 35.54, e: 37.65 },// early alpha
  { s: 37.65, e: 40.40 },// own software
  { s: 40.40, e: 42.22 },// comment craft
  { s: 42.22, e: 44.04 },// live demo
];

/* ---------- brand furniture ---------- */
const Starburst: React.FC<{ x: number; y: number; r?: number; o?: number }> = ({ x, y, r = 120, o = 0.55 }) => {
  const spikes = 14;
  const pts: string[] = [];
  for (let i = 0; i < spikes * 2; i++) {
    const a = (Math.PI * i) / spikes;
    const rad = i % 2 === 0 ? r : r * 0.62;
    pts.push(`${Math.cos(a) * rad},${Math.sin(a) * rad}`);
  }
  return (
    <svg style={{ position: "absolute", left: x, top: y, opacity: o, pointerEvents: "none" }}
      width={r * 2.4} height={r * 2.4} viewBox={`${-r * 1.2} ${-r * 1.2} ${r * 2.4} ${r * 2.4}`}>
      <polygon points={pts.join(" ")} fill={TERRA} />
    </svg>
  );
};

const Sticker: React.FC<{ t: string; x: number; y: number; rot?: number; s?: number; size?: number }> = ({
  t, x, y, rot = 0, s = 1, size = 30,
}) => (
  <div style={{
    position: "absolute", left: x, top: y, transform: `rotate(${rot}deg) scale(${s})`,
    background: WHITE, border: `3px solid ${INK}`, borderRadius: 12,
    padding: `${size * 0.34}px ${size * 0.72}px`, fontFamily: FONT, fontWeight: 900,
    fontSize: size, color: INK, whiteSpace: "nowrap",
    boxShadow: "0 6px 0 rgba(20,16,12,0.10)",
  }}>{t}</div>
);

const Chip: React.FC<{ logo?: string; a: string; b?: string }> = ({ logo, a, b }) => (
  <div style={{
    position: "absolute", left: 54, top: 54, display: "flex", alignItems: "center", gap: 12,
    background: WHITE, border: `3px solid ${INK}`, borderRadius: 999, padding: "10px 22px 10px 14px",
  }}>
    {logo ? <Img src={staticFile(logo)} style={{ width: 34, height: 34, borderRadius: 8 }} /> : null}
    <span style={{ fontFamily: FONT, fontWeight: 900, fontSize: 26, color: INK }}>{a}</span>
    {b ? <span style={{ fontFamily: MONO, fontSize: 20, color: GRAY }}>{b}</span> : null}
  </div>
);

/* headline with exactly one orange-boxed word */
const Boxed: React.FC<{ pre?: string; box: string; post?: string; size?: number; color?: string }> = ({
  pre = "", box, post = "", size = 92, color = INK,
}) => (
  <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1.06, letterSpacing: -size * 0.035, color, textAlign: "left" }}>
    {pre}
    <span style={{
      display: "inline-block", background: ORANGE, color: WHITE, borderRadius: size * 0.14,
      padding: `${size * 0.03}px ${size * 0.14}px`, margin: `0 ${size * 0.06}px`,
    }}>{box}</span>
    {post}
  </div>
);

/* browser window: the hero of most frames */
const Browser: React.FC<{
  x: number; y: number; w: number; h: number; src: string; label?: string; labelBg?: string;
  rot?: number; s?: number;
}> = ({ x, y, w, h, src, label, labelBg = ORANGE, rot = -2, s = 1 }) => (
  <div style={{
    position: "absolute", left: x, top: y, width: w, height: h,
    transform: `rotate(${rot}deg) scale(${s})`, transformOrigin: "center",
    background: WHITE, borderRadius: 18, border: `4px solid ${INK}`, overflow: "hidden",
    boxShadow: "0 22px 0 rgba(20,16,12,0.10), 0 26px 50px rgba(20,16,12,0.18)",
  }}>
    <div style={{ height: 46, background: "#EDE7E0", borderBottom: `3px solid ${INK}`, display: "flex", alignItems: "center", paddingLeft: 16, gap: 9 }}>
      {["#EE6A5A", "#F4BF4F", "#62C56A"].map((c) => (
        <div key={c} style={{ width: 15, height: 15, borderRadius: "50%", background: c }} />
      ))}
      <div style={{ flex: 1, marginLeft: 12, marginRight: 12, height: 22, background: WHITE, borderRadius: 11, border: `2px solid #D8D0C8` }} />
    </div>
    <Img src={staticFile(src)} style={{ width: "100%", height: h - 46, objectFit: "cover", objectPosition: "top" }} />
    {label ? (
      <div style={{
        position: "absolute", right: -18, top: 84, background: labelBg, color: WHITE,
        fontFamily: FONT, fontWeight: 900, fontSize: 24, padding: "8px 18px",
        borderRadius: 10, border: `3px solid ${INK}`,
      }}>{label}</div>
    ) : null}
  </div>
);

const StepBand: React.FC<{ t: string; bg: string; y?: number }> = ({ t, bg, y = 190 }) => (
  <div style={{
    position: "absolute", left: 54, right: 54, top: y, background: bg, border: `4px solid ${INK}`,
    borderRadius: 16, padding: "14px 26px",
  }}>
    <span style={{ fontFamily: FONT, fontWeight: 900, fontSize: 40, color: INK }}>{t}</span>
  </div>
);

const DataPill: React.FC<{ t: string; x: number; y: number; bg?: string; size?: number }> = ({ t, x, y, bg = WHITE, size = 26 }) => (
  <div style={{
    position: "absolute", left: x, top: y, background: bg, border: `3px solid ${INK}`,
    borderRadius: 999, padding: "8px 20px", fontFamily: MONO, fontWeight: 700, fontSize: size, color: INK,
  }}>{t}</div>
);

/* ---------- composition ---------- */
export const Craft: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // beat index comes from the measured BEATS list (speech-verified), not from scenes
  let idx = 0;
  for (let i = 0; i < BEATS.length; i++) if (t >= BEATS[i].s) idx = i;
  const b = BEATS[idx];
  const lf = frame - b.s * fps;
  // a beat stays on screen until the NEXT beat begins, so a pause in the voice
  // never leaves an empty frame; the exit only runs in the last 3 frames
  const bEnd = idx < BEATS.length - 1 ? BEATS[idx + 1].s : BEATS[idx].e;
  const blen = Math.max(6, (bEnd - b.s) * fps);

  const ein = Math.min(1, Math.max(0, lf / 4));
  const ex = Math.min(1, Math.max(0, (lf - (blen - 3)) / 3));
  const push = 1 + 0.03 * Math.min(1, lf / blen);
  const sc = (0.96 + 0.04 * ein) * push;
  const yoff = 70 * (1 - ein) - 100 * ex;
  const op = (ein < 0.1 ? ein / 0.1 : 1) * (1 - ex);

  // caption is locked to the SAME beat as the visual — they can never drift
  const hold = frame >= 626 && frame <= 640;
  const prog = Math.min(1, t / 44.04);

  /* caption with one highlighted word */

  return (
    <AbsoluteFill style={{ backgroundColor: CREAM }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `radial-gradient(#DCD2C6 2.6px, transparent 2.6px)`, backgroundSize: "48px 48px" }} />

      {/* starbursts — always present, always in the corners */}
      <Starburst x={-70} y={-80} r={150} o={0.5} />
      <Starburst x={880} y={250} r={95} o={0.42} />
      <Starburst x={-40} y={1500} r={80} o={0.35} />

      {hold && <Img src={staticFile("assets/thumb.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />}

      <div style={{ position: "absolute", inset: 0, transform: `translateY(${yoff}px) scale(${sc})`, opacity: hold ? 0 : op }}>

        {/* 0 HOOK */}
        {idx === 0 && <>
          <Chip logo="assets/craft_icon.png" a="CRAFT ANYTHING" b="OPEN SOURCE" />
          <div style={{ position: "absolute", left: 54, top: 210 }}>
            <Boxed pre="COPY ANY " box="APP" size={104} /><Boxed pre="" box="IN 3 STEPS" size={104} />
          </div>
          <Browser x={70} y={560} w={430} h={520} src="assets/project-website.png" label="ORIGINAL" labelBg={GRAY} rot={-3} />
          <Browser x={580} y={600} w={430} h={520} src="assets/make.png" label="CLONE" rot={3} />
          <DataPill t="3 STEPS" x={470} y={1040} bg={ORANGE} />
        </>}

        {/* 1 THREE STEPS */}
        {idx === 1 && <>
          <Chip logo="assets/craft_icon.png" a="HOW IT WORKS" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="IN " box="3 STEPS" size={110} />
          </div>
          {["STUDY", "BUILD", "CHECK"].map((l, i) => {
            const s = spring({ frame: lf - i * 7, fps, config: { damping: 12, stiffness: 150 } });
            return (
              <div key={l} style={{
                position: "absolute", left: 54, top: 470 + i * 190, width: 970, height: 150,
                background: [WHITE, WHITE, WHITE][i], border: `4px solid ${INK}`, borderRadius: 18,
                transform: `translateX(${80 * (1 - s)}px)`, opacity: Math.min(1, s * 2),
                display: "flex", alignItems: "center", gap: 28, paddingLeft: 30,
              }}>
                <div style={{ width: 76, height: 76, borderRadius: "50%", background: ORANGE, color: WHITE, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontWeight: 900, fontSize: 42 }}>{i + 1}</div>
                <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 54 }}>{l}</div>
                <div style={{ marginLeft: "auto", marginRight: 30, fontFamily: MONO, fontSize: 24, color: GRAY }}>
                  {["INSPECT THE ORIGINAL", "CLAUDE BUILDS IT", "SCORE & FIX"][i]}
                </div>
              </div>
            );
          })}
        </>}

        {/* 2 WHAT IS IT */}
        {idx === 2 && <>
          <Chip logo="assets/craft_icon.png" a="CRAFT ANYTHING" b="storytold" />
          <div style={{ position: "absolute", left: 54, top: 190 }}>
            <Boxed pre="PURE " box="RUST" post=" ENGINE" size={86} />
          </div>
          <Browser x={40} y={390} w={700} h={520} src="assets/workbench.png" label="OPEN SOURCE" labelBg="#3FA34D" rot={-2} />
          <div style={{ position: "absolute", left: 710, top: 420, width: 320 }}>
            {["RUST + APACHE-2.0", "320 CLI TOOLS", "MCP READY", "NO PAID API"].map((l, i) => (
              <div key={l} style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 22, opacity: lf > 8 + i * 6 ? 1 : 0.2 }}>
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: ORANGE }} />
                <div style={{ fontFamily: MONO, fontSize: 22, fontWeight: 700 }}>{l}</div>
              </div>
            ))}
          </div>
          <Img src={staticFile("assets/rust.png")} style={{ position: "absolute", left: 880, top: 860, width: 110, height: 110 }} />
        </>}

        {/* 3 WEBSITE APP GAME */}
        {idx === 3 && <>
          <Chip a="WORKS ON" b="ANYTHING" />
          <div style={{ position: "absolute", left: 54, top: 190 }}>
            <Boxed pre="WEBSITE · " box="APP" post=" · GAME" size={74} />
          </div>
          {[
            ["assets/project-website.png", "WEBSITE", -3],
            ["assets/project-game.png", "GAME (SNAKE)", 2],
            ["assets/make.png", "DESKTOP APP", -2],
          ].map(([src, label, rot], i) => {
            const s = spring({ frame: lf - i * 6, fps, config: { damping: 12, stiffness: 140 } });
            return (
              <div key={label as string} style={{ opacity: Math.min(1, s * 2) }}>
                <Browser x={44 + i * 330} y={430} w={330} h={430} src={src as string}
                  label={label as string} labelBg={ORANGE} rot={rot as number} s={0.86 + 0.14 * s} />
              </div>
            );
          })}
          <DataPill t="ONE TOOL · THREE TARGETS" x={330} y={900} bg={WHITE} />
        </>}

        {/* 4 ANYTHING */}
        {idx === 4 && <>
          <Chip logo="assets/craft_icon.png" a="THE CLAIM" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="" box="ANYTHING" size={128} /><Boxed pre="YOU CAN " box="POINT AT" size={92} />
          </div>
          <Browser x={54} y={560} w={470} h={470} src="assets/project-website.png" label="SOURCE" labelBg={GRAY} rot={-3} />
          <div style={{ position: "absolute", left: 545, top: 760, fontFamily: FONT, fontWeight: 900, fontSize: 90, color: ORANGE }}>→</div>
          <Browser x={610} y={560} w={420} h={470} src="assets/make.png" label="REBUILT" rot={3} />
        </>}

        {/* 5 STUDY */}
        {idx === 5 && <>
          <Chip logo="assets/github.png" a="STEP 01" b="STUDY & INSPECT" />
          <StepBand t="STEP 01: STUDY & INSPECT" bg="#F4C95D" />
          <Browser x={40} y={290} w={830} h={610} src="assets/workbench.png" label="LIVE UI" rot={-1.5} />
          <div style={{ position: "absolute", left: 850, top: 320, width: 190 }}>
            {["LAYOUT", "COLOURS", "FONTS", "MENUS", "STATES"].map((l, i) => (
              <div key={l} style={{ marginTop: 16, background: lf > 10 + i * 7 ? ORANGE : WHITE, border: `3px solid ${INK}`, borderRadius: 10, padding: "8px 12px", fontFamily: MONO, fontSize: 20, fontWeight: 700, color: lf > 10 + i * 7 ? WHITE : INK }}>{l}</div>
            ))}
          </div>
          <DataPill t="EVERY ELEMENT MEASURED" x={54} y={890} />
        </>}

        {/* 6 BUILD */}
        {idx === 6 && <>
          <Chip a="STEP 02" b="BUILD" />
          <StepBand t="STEP 02: AI BUILD" bg="#9FD3F0" />
          <div style={{ position: "absolute", left: 54, top: 300, width: 970, height: 560, background: DARK, borderRadius: 20, border: `4px solid ${INK}`, padding: 30 }}>
            <div style={{ display: "flex", gap: 9, marginBottom: 18 }}>
              {["#EE6A5A", "#F4BF4F", "#62C56A"].map((c) => <div key={c} style={{ width: 16, height: 16, borderRadius: "50%", background: c }} />)}
            </div>
            <div style={{ fontFamily: MONO, fontSize: 30, color: "#96DCA8" }}>{"$ claude --build".slice(0, Math.max(1, Math.floor(lf / 3)))}</div>
            {lf > 22 && <div style={{ fontFamily: MONO, fontSize: 24, color: "#D8D8D0", marginTop: 18 }}>{"> studying target .................. ok"}</div>}
            {lf > 40 && <div style={{ fontFamily: MONO, fontSize: 24, color: "#D8D8D0", marginTop: 12 }}>{"> writing project ................. ok"}</div>}
            {lf > 58 && <div style={{ fontFamily: MONO, fontSize: 24, color: "#FFB37A", marginTop: 12 }}>{"> new app ready"}</div>}
          </div>
          <Img src={staticFile("assets/claude.png")} style={{ position: "absolute", left: 840, top: 880, width: 130, height: 130 }} />
        </>}

        {/* 7 CLAUDE CODE */}
        {idx === 7 && <>
          <Chip logo="assets/craft_icon.png" a="CLAUDE CODE" b="CODING AGENT" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="STEP 2: " box="CLAUDE" post=" CODE" size={86} /><Boxed pre="BUILDS IT " box="FOR YOU" size={86} />
          </div>
          <Img src={staticFile("assets/craft_icon.png")} style={{ position: "absolute", left: 380, top: 540, width: 300, height: 300, borderRadius: 36 }} />
          <DataPill t="NO HUMAN CODING" x={330} y={900} bg={ORANGE} />
        </>}

        {/* 8 LANGUAGE */}
        {idx === 8 && <>
          <Chip a="YOU CHOOSE" b="THE LANGUAGE" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="IN ANY " box="LANGUAGE" size={96} /><Boxed pre="" box="YOU PICK" size={96} />
          </div>
          {[["RUST","assets/rust.png"],["TYPESCRIPT","assets/typescript.png"],["PYTHON","assets/python.png"],["GO","assets/go.png"]].map(([l, ico], i) => {
            const sp = spring({ frame: lf - i * 5, fps, config: { damping: 12, stiffness: 150 } });
            return <div key={l} style={{
              position: "absolute", left: 54 + (i % 2) * 500, top: 500 + Math.floor(i / 2) * 200, width: 460, height: 150,
              background: WHITE, border: `4px solid ${INK}`, borderRadius: 18, display: "flex", alignItems: "center", justifyContent: "center", gap: 20,
              fontFamily: FONT, fontWeight: 900, fontSize: 46, opacity: Math.min(1, sp * 2), transform: `scale(${0.85 + 0.15 * sp})`,
            }}><Img src={staticFile(ico as string)} style={{ width: 64, height: 64 }} />{l}</div>;
          })}
        </>}

        {/* 9 CHECK */}
        {idx === 9 && <>
          <Chip logo="assets/github.png" a="STEP 03" b="CHECK & COMPARE" />
          <StepBand t="STEP 03: CHECK & COMPARE" bg="#9BE3B8" />
          <Browser x={40} y={290} w={830} h={610} src="assets/make.png" label="SCORED" labelBg="#3FA34D" rot={-1.5} />
          <div style={{ position: "absolute", left: 850, top: 340, width: 190 }}>
            {[["START PAGE", "96%"], ["LIKENESS", "93%"], ["LAYOUT", "98%"]].map(([k, v], i) => (
              <div key={k} style={{ marginTop: 18, opacity: lf > 10 + i * 8 ? 1 : 0.2 }}>
                <div style={{ fontFamily: MONO, fontSize: 18, color: GRAY }}>{k}</div>
                <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 44, color: ORANGE }}>{v}</div>
              </div>
            ))}
          </div>
        </>}

        {/* 10 COMPARED */}
        {idx === 10 && <>
          <Chip a="AUTO-FIXES" b="MISMATCHES" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="" box="COMPARED" post=" TO THE" size={80} /><Boxed pre="" box="ORIGINAL" size={80} />
          </div>
          {["LAYOUT", "COLOURS", "BEHAVIOUR"].map((l, i) => {
            const flip = lf > 12 + i * 6;
            return (
              <div key={l} style={{
                position: "absolute", left: 54, top: 500 + i * 160, width: 970, height: 130,
                background: flip ? "#9BE3B8" : "#F6C7C0", border: `4px solid ${INK}`, borderRadius: 18,
                display: "flex", alignItems: "center", gap: 24, paddingLeft: 26,
              }}>
                <div style={{ width: 52, height: 52, borderRadius: "50%", background: flip ? "#3FA34D" : "#C64A3A", color: WHITE, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontWeight: 900, fontSize: 30 }}>{flip ? "✓" : "✕"}</div>
                <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 40 }}>{l}</div>
                <div style={{ marginLeft: "auto", marginRight: 26, fontFamily: MONO, fontWeight: 700, fontSize: 28, color: flip ? "#2E7D46" : "#C64A3A" }}>{flip ? "MATCH" : "OFF"}</div>
              </div>
            );
          })}
        </>}

        {/* 11 FIX */}
        {idx === 11 && <>
          <Chip a="FIX LOOP" b="UNTIL IT MATCHES" />
          <StepBand t="AUTO-FIXES MISMATCHES" bg="#9BE3B8" />
          <div style={{ position: "absolute", left: 54, top: 330, width: 970 }}>
            {["DIFF ERR → FIXED", "COLOUR DRIFT → MATCHED", "SPACING → ALIGNED"].map((l, i) => {
              const s = spring({ frame: lf - i * 7, fps, config: { damping: 13, stiffness: 140 } });
              return <div key={l} style={{
                marginTop: 26, height: 140, background: WHITE, border: `4px solid ${INK}`, borderRadius: 18,
                display: "flex", alignItems: "center", paddingLeft: 26, gap: 20, opacity: Math.min(1, s * 2),
              }}>
                <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30 }}>{l}</div>
                <div style={{ marginLeft: "auto", marginRight: 26, width: 46, height: 46, borderRadius: "50%", background: "#3FA34D", color: WHITE, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 28, fontWeight: 900 }}>✓</div>
              </div>;
            })}
          </div>
        </>}

        {/* 12 91% */}
        {idx === 12 && <>
          <Chip logo="assets/ycombinator.png" a="HACKER NEWS" b="INDEPENDENT LIVE TEST" />
          <div style={{ position: "absolute", left: 54, top: 190 }}>
            <Boxed pre="A REAL TEST: " box="91%" post=" CLONE" size={72} />
          </div>
          <div style={{ position: "absolute", left: 54, top: 360, display: "flex", alignItems: "flex-end", gap: 20 }}>
            <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 300, color: ORANGE, lineHeight: 0.9, letterSpacing: -14 }}>91%</div>
            <div style={{ marginBottom: 40 }}>
              <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 64, color: INK }}>IN 29 MIN</div>
              <div style={{ fontFamily: MONO, fontSize: 22, color: GRAY, marginTop: 6 }}>RAINYTECHLAB · DEV + YOUTUBE</div>
            </div>
          </div>
          <Browser x={54} y={760} w={560} h={300} src="assets/project-website.png" label="THE CLONE" rot={-2} />
          <DataPill t="2048 GAME: 59% PLAYABLE" x={640} y={800} />
          <DataPill t="HN THREAD: 91% COPY" x={640} y={870} />
        </>}

        {/* 13 I CHECKED */}
        {idx === 13 && <>
          <Chip logo="assets/github.png" a="I CHECKED" b="MYSELF · LIVE API" />
          <div style={{ position: "absolute", left: 54, top: 190 }}>
            <Boxed pre="NOBODY TOLD ME. " box="I RAN IT" size={64} />
          </div>
          <div style={{ position: "absolute", left: 54, top: 340, width: 970, height: 520, background: DARK, borderRadius: 20, border: `4px solid ${INK}`, padding: 26 }}>
            <div style={{ display: "flex", gap: 9, marginBottom: 16 }}>
              {["#EE6A5A", "#F4BF4F", "#62C56A"].map((c) => <div key={c} style={{ width: 16, height: 16, borderRadius: "50%", background: c }} />)}
            </div>
            {[
              "$ curl api.github.com/repos/storytold/craft-anything",
              '"full_name":         "storytold/craft-anything"',
              '"forks_count":       7125',
              '"language":          "Rust"',
              '"license":           "Apache-2.0"',
              '"open_issues_count": 387',
            ].map((line, i) => (
              <div key={i} style={{ fontFamily: MONO, fontSize: 24, color: i === 0 ? "#96DCA8" : "#E2E2DC", marginTop: i ? 10 : 0, opacity: lf > 5 + i * 5 ? 1 : 0 }}>{line}</div>
            ))}
          </div>
        </>}

        {/* 14 STARS */}
        {idx === 14 && <>
          <Chip logo="assets/github.png" a="GITHUB" b="LIVE COUNT" />
          <div style={{ position: "absolute", left: 54, top: 190 }}>
            <Boxed pre="35,250+ " box="STARS" post=" LIVE" size={78} />
          </div>
          <div style={{ position: "absolute", left: 54, top: 340, fontFamily: FONT, fontWeight: 900, fontSize: 230, color: INK, letterSpacing: -12 }}>
            {Math.round(35250 * Math.min(1, Math.max(0, (lf - 2) / 22))).toLocaleString("en-US")}
          </div>
          <DataPill t="7,125 FORKS · APACHE-2.0" x={54} y={640} />
          <Browser x={40} y={720} w={720} h={380} src="assets/live_repo.png" label="GITHUB LIVE" rot={-2} />
          <div style={{ position: "absolute", left: 470, top: 760, width: 210, height: 74, border: `6px solid ${ORANGE}`, borderRadius: 16, boxShadow: `0 0 0 6px rgba(234,88,12,0.22)` }} />
          <div style={{ position: "absolute", left: 470, top: 700, background: ORANGE, color: WHITE, fontFamily: FONT, fontWeight: 900, fontSize: 22, padding: "4px 14px", borderRadius: 8 }}>LIVE STARS</div>
          <Img src={staticFile("assets/github.png")} style={{ position: "absolute", left: 760, top: 780, width: 200, height: 200 }} />
        </>}

        {/* 15 EARLY ALPHA */}
        {idx === 15 && <>
          <Chip a="HONEST BIT" b="NOT HYPE" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="" box="EARLY" size={150} /><Boxed pre="" box="ALPHA" size={150} />
          </div>
          <div style={{ position: "absolute", left: 300, top: 620, border: `10px solid #C64A3A`, borderRadius: 18, padding: "18px 60px", transform: "rotate(-9deg)", fontFamily: FONT, fontWeight: 900, fontSize: 84, color: "#C64A3A" }}>HONEST</div>
          <DataPill t="RESULTS VARY · BUGS EXIST" x={240} y={880} />
        </>}

        {/* 16 OWN SOFTWARE */}
        {idx === 16 && <>
          <Chip a="THE RULE" b="READ THIS" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="YOUR OWN " box="SOFTWARE" size={84} /><Boxed pre="" box="ONLY" size={84} />
          </div>
          <div style={{ position: "absolute", left: 54, top: 520, width: 970 }}>
            {["ALLOWED SOFTWARE ONLY", "NO DRM BYPASS", "NO LOGIN BYPASS"].map((l, i) => (
              <div key={l} style={{ marginTop: 24, height: 130, background: WHITE, border: `4px solid ${INK}`, borderRadius: 18, display: "flex", alignItems: "center", gap: 20, paddingLeft: 26, opacity: lf > 7 + i * 6 ? 1 : 0.2 }}>
                <div style={{ width: 48, height: 48, borderRadius: "50%", background: "#3FA34D", color: WHITE, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 28, fontWeight: 900 }}>✓</div>
                <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 40 }}>{l}</div>
              </div>
            ))}
          </div>
        </>}

        {/* 17 COMMENT */}
        {idx === 17 && <>
          <Chip logo="assets/craft_icon.png" a="NEXT VIDEO" b="LIVE DEMO" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="COMMENT " box="CRAFT" size={110} /><Boxed pre="TO GET THE " box="DEMO" size={92} />
          </div>
          <div style={{ position: "absolute", left: 54, top: 620, width: 970, height: 170, background: WHITE, border: `4px solid ${INK}`, borderRadius: 85, display: "flex", alignItems: "center", paddingLeft: 40, gap: 8 }}>
            <div style={{ fontFamily: MONO, fontSize: 44, fontWeight: 700 }}>{"CRAFT".slice(0, Math.max(1, Math.floor(lf / 4)))}</div>
            <div style={{ width: 8, height: 54, background: ORANGE, opacity: Math.floor(lf / 7) % 2 === 0 ? 1 : 0 }} />
          </div>
          <DataPill t="FOLLOW FOR THE DEMO" x={54} y={840} bg={ORANGE} />
        </>}

        {/* 18 END */}
        {idx === 18 && <>
          <Chip logo="assets/craft_icon.png" a="CRAFT ANYTHING" b="OPEN SOURCE" />
          <div style={{ position: "absolute", left: 54, top: 200 }}>
            <Boxed pre="LIVE DEMO " box="NEXT" size={110} />
          </div>
          <Img src={staticFile("assets/craft_icon.png")} style={{ position: "absolute", left: 60, top: 460, width: 260, height: 260 }} />
          <Browser x={380} y={470} w={640} h={330} src="assets/live_repo.png" label="GITHUB" rot={-2} />
          <DataPill t="GITHUB LINK IN PINNED COMMENT" x={54} y={860} bg={WHITE} />
        </>}
      </div>

      {/* progress bar */}
      <div style={{ position: "absolute", left: 0, top: 0, height: 8, width: 1080 * prog, background: ORANGE }} />
      <div style={{ position: "absolute", right: 46, bottom: 40 }}><span style={{ fontFamily: MONO, fontSize: 24, color: "#A79C90" }}>gkhacktech</span></div>
    </AbsoluteFill>
  );
};
