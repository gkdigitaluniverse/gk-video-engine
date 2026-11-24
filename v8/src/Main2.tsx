import React from "react";
import {
  AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig,
  interpolate, spring, Img, staticFile,
} from "remotion";

/* ============================================================
   Video 2 — Google Sheets multi-select. Same L6 cream language.
   Real proof screenshots: Google Workspace blog + Docs Help page.
   ============================================================ */

const CREAM = "#ECECE7";
const PAPER = "#FFFFFF";
const INK = "#111111";
const ORANGE = "#E8551F";
const MINT = "#A8E2C0";
const GREEN = "#22A05A";
const RED = "#D23C2D";
const GREY = "#787874";
const CHROME = "#22242A";
const FPS = 60;

export const B2 = [
  { s: 0.04,  e: 3.98,  top: "(1) OFFICE TRICK / GOOGLE SHEETS",
    l1: "ONE CELL.", box: "MANY CHOICES",
    hero: "chips", chips: ["PENDING", "TESTING", "DONE"] },
  { s: 3.98,  e: 8.54,  top: "(2) WHO THIS IS FOR",
    l1: "TRACKING WORK", box: "IN SHEETS",
    hero: "rows", rows: [["Excel users","WELCOME"],["Project tracker","YES"],["One cell","MANY STATUS"]] },
  { s: 8.54,  e: 13.08, top: "(3) PROOF / ANNOUNCED",
    l1: "26 JULY", box: "2024",
    hero: "proof", img: "blog.png", hl: { x: 6.4, y: 30.2, w: 8.6, h: 2.6 },
    cap: "Google Workspace Updates · 26 July 2024" },
  { s: 13.08, e: 16.10, top: "(4) BEFORE",
    l1: "ONE VALUE", box: "ONLY",
    hero: "single" },
  { s: 16.10, e: 21.90, top: "(5) PROOF / HOW TO TURN IT ON",
    l1: "ALLOW MULTIPLE", box: "SELECTIONS",
    hero: "proof", img: "support.png", hl: { x: 18.8, y: 56.6, w: 27.0, h: 2.6 },
    cap: "support.google.com · Docs Editors Help" },
  { s: 21.90, e: 23.60, top: "(6) DISPLAY STYLE",
    l1: "CHOOSE", box: "CHIP",
    hero: "chips", chips: ["CHIP"] },
  { s: 23.60, e: 29.72, top: "(7) ONE CELL / THREE STATUS",
    l1: "PENDING + TESTING", box: "+ DONE",
    hero: "chips", chips: ["PENDING", "TESTING", "DONE"] },
  { s: 29.72, e: 33.00, top: "(8) PROOF / I CHECKED",
    l1: "I READ THE", box: "HELP PAGE",
    hero: "rows", rows: [["Source","GOOGLE OFFICIAL"],["Checked","24 NOV 2026"],["Guessing","NONE"]] },
  { s: 33.00, e: 38.34, top: "(9) THE CATCH / HONEST",
    l1: "MOBILE APP", box: "NOT YET",
    hero: "rows", rows: [["Computer","MULTI-SELECT"],["Mobile app","SINGLE ONLY"]] },
  { s: 38.34, e: 41.38, top: "(10) SMALL THING THAT BREAKS IT",
    l1: "NO EXTRA", box: "SPACES",
    hero: "rows", rows: [["Option label","CLEAN"],["Leading space","BREAKS IT"]] },
  { s: 41.38, e: 44.96, top: "(11) LINK / DESCRIPTION",
    l1: "OPEN ON A", box: "COMPUTER",
    hero: "url" },
];

const Surface: React.FC<{ f: number }> = ({ f }) => {
  const off = (f * 0.14) % 38;
  return (
    <AbsoluteFill style={{ backgroundColor: CREAM }}>
      <svg width="1080" height="1920" style={{ position: "absolute" }}>
        <defs>
          <pattern id="d2" width="38" height="38" patternUnits="userSpaceOnUse" x={off} y={off / 2}>
            <circle cx="2" cy="2" r="2.2" fill="#D6D4CC" />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#d2)" />
      </svg>
      <div style={{
        position: "absolute", top: 900, width: "100%", textAlign: "center",
        fontFamily: "monospace", fontSize: 54, color: "#E2E0D8", letterSpacing: 2,
      }}>gkhackter</div>
    </AbsoluteFill>
  );
};

const Starburst: React.FC<{ cx: number; cy: number; r: number; seed: number; rot: number }> =
({ cx, cy, r, seed, rot }) => {
  const rnd = (i: number) => { const x = Math.sin(seed * 99 + i * 7.13) * 10000; return x - Math.floor(x); };
  const pts: string[] = [];
  for (let i = 0; i < 22; i++) {
    const a = rot + (i * Math.PI) / 11;
    const rr = i % 2 === 0 ? r : r * (0.42 + rnd(i) * 0.18);
    pts.push(`${cx + Math.cos(a) * rr},${cy + Math.sin(a) * rr}`);
  }
  return <polygon points={pts.join(" ")} fill={ORANGE} opacity={0.16} />;
};

const Bursts: React.FC = () => {
  const f = useCurrentFrame(); const t = f / FPS;
  const spots = [[130, 200, 100], [950, 260, 120], [120, 800, 74], [980, 1200, 90], [100, 1600, 110]];
  return (
    <svg width="1080" height="1920" style={{ position: "absolute" }}>
      {spots.map((s, i) => (
        <Starburst key={i} cx={s[0]} cy={s[1]} r={s[2] * (1 + 0.05 * Math.sin(t * 1.3 + i))}
          seed={i + 1} rot={t * 0.22 + i * 0.7} />
      ))}
    </svg>
  );
};

const Headline: React.FC<{ beat: any; f: number }> = ({ beat, f }) => {
  const rows = [{ t: beat.l1, boxed: false }, { t: beat.box, boxed: true }];
  return (
    <div style={{ position: "absolute", left: 56, top: 130, width: 968 }}>
      {rows.map((r, i) => {
        const d = Math.max(0, f - 4 - i * 5);
        const sp = spring({ frame: d, fps: FPS, config: { damping: 16, stiffness: 130, mass: 0.6 } });
        const y = interpolate(sp, [0, 1], [46, 0]);
        const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
        const mp = interpolate(f - 4 - i * 5 - 10, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const size = r.t.length > 16 ? 68 : r.t.length > 12 ? 82 : 96;
        return (
          <div key={i} style={{ position: "relative", height: 108, opacity: op, transform: `translateY(${y}px)` }}>
            {r.boxed ? (
              <span style={{
                display: "inline-block", fontFamily: "Anton, Impact, sans-serif",
                fontSize: size, lineHeight: "98px", letterSpacing: -1, color: "#fff",
                background: ORANGE, padding: "0 16px", whiteSpace: "nowrap",
                clipPath: "polygon(0 4%, 100% 0%, 100% 96%, 0 100%)",
                transform: `scaleX(${0.55 + 0.45 * mp})`, transformOrigin: "left center",
                opacity: 0.4 + 0.6 * mp,
              }}>{r.t}</span>
            ) : (
              <span style={{
                fontFamily: "Anton, Impact, sans-serif", fontSize: size,
                lineHeight: "108px", letterSpacing: -1, color: INK, whiteSpace: "nowrap",
              }}>{r.t}</span>
            )}
          </div>
        );
      })}
    </div>
  );
};

const Card: React.FC<{ f: number; start: number; y: number; h: number; w?: number; title?: string; pill?: string; children?: React.ReactNode }> =
({ f, start, y, h, w = 948, title, pill, children }) => {
  const d = Math.max(0, f - start);
  const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
  const sc = interpolate(sp, [0, 1], [0.93, 1]);
  const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 66, top: y, width: w, height: h,
      transform: `scale(${sc})`, opacity: op, boxShadow: "0 22px 48px rgba(0,0,0,0.22)" }}>
      <div style={{ width: "100%", height: "100%", borderRadius: 20, border: "3px solid #1C1C1C",
        overflow: "hidden", background: PAPER, display: "flex", flexDirection: "column" }}>
        {title && (
          <div style={{ height: 46, background: CHROME, display: "flex", alignItems: "center",
            paddingLeft: 16, flexShrink: 0 }}>
            {["#FF5F56", "#FFBD2E", "#27C93F"].map((c, i) => (
              <div key={i} style={{ width: 14, height: 14, borderRadius: 7, background: c, marginRight: 8 }} />
            ))}
            <span style={{ fontFamily: "monospace", fontSize: 20, color: "#D2D6E0", marginLeft: 14 }}>{title}</span>
          </div>
        )}
        <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>{children}</div>
      </div>
      {pill && (
        <div style={{ position: "absolute", right: -8, top: -16, background: ORANGE, color: "#fff",
          fontFamily: "monospace", fontSize: 20, padding: "5px 12px", borderRadius: 8 }}>{pill}</div>
      )}
    </div>
  );
};

const Proof: React.FC<{ f: number; img: string; hl: any; start: number; y: number; h: number }> =
({ f, img, hl, start, y, h }) => {
  const hp = interpolate(f - start - 18, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Card f={f} start={start} y={y} h={h} title="google.com" pill="PROOF">
      <div style={{ position: "absolute", inset: 0 }}>
        <Img src={staticFile(img)} style={{ width: "100%", height: "100%", objectFit: "contain", objectPosition: "top" }} />
        <div style={{
          position: "absolute", left: `${hl.x}%`, top: `${hl.y}%`,
          width: `${hl.w * hp}%`, height: `${hl.h}%`,
          border: "5px solid #E8551F", borderRadius: 8,
          background: `rgba(232,85,31,${0.14 * hp})`,
          boxShadow: `0 0 0 ${3 * hp}px rgba(232,85,31,0.16)`,
        }} />
      </div>
    </Card>
  );
};

const ChipRow: React.FC<{ f: number; labels: string[]; start: number; y: number; big?: boolean }> =
({ f, labels, start, y, big }) => (
  <div style={{ position: "absolute", left: 66, top: y, width: 948, display: "flex", gap: 14, flexWrap: "wrap" }}>
    {labels.map((lab, i) => {
      const d = Math.max(0, f - start - i * 8);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 11, stiffness: 170, mass: 0.5 } });
      const sc = interpolate(sp, [0, 1], [0.5, 1]);
      const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
      const col = i === 0 ? ORANGE : i === 1 ? "#1A73E8" : GREEN;
      return (
        <div key={i} style={{
          opacity: op, transform: `scale(${sc})`,
          background: PAPER, border: `3px solid ${col}`, borderRadius: 999,
          padding: big ? "18px 34px" : "14px 28px",
          fontFamily: "Anton, Impact, sans-serif", fontSize: big ? 52 : 40,
          color: col, letterSpacing: 1, boxShadow: "0 10px 22px rgba(0,0,0,0.14)",
        }}>{lab}</div>
      );
    })}
  </div>
);

const Rows: React.FC<{ f: number; rows: string[][]; start: number; y: number }> = ({ f, rows, start, y }) => (
  <div style={{ position: "absolute", left: 66, top: y, width: 948 }}>
    {rows.map((r, i) => {
      const d = Math.max(0, f - start - i * 7);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 14, stiffness: 140, mass: 0.55 } });
      const x = interpolate(sp, [0, 1], [-70, 0]);
      const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
      const bad = /SINGLE ONLY|BREAKS|NO$/.test(r[1]);
      return (
        <div key={i} style={{
          height: 92, background: bad ? "#FBD9D4" : MINT,
          border: "3px solid #181818", borderRadius: 14,
          display: "flex", alignItems: "center", padding: "0 20px",
          marginBottom: 18, transform: `translateX(${x}px)`, opacity: op,
          boxShadow: "0 12px 26px rgba(0,0,0,0.16)",
        }}>
          <div style={{ width: 32, height: 32, borderRadius: 16, background: bad ? RED : GREEN,
            color: "#fff", display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: "sans-serif", fontWeight: 800, fontSize: 20, marginRight: 16 }}>
            {bad ? "!" : "✓"}
          </div>
          <div style={{ flex: 1, fontFamily: "Archivo Black, sans-serif", fontSize: 28, color: INK }}>{r[0]}</div>
          <div style={{ fontFamily: "monospace", fontSize: 21, color: bad ? "#8C2A20" : "#1E5A3C" }}>{r[1]}</div>
        </div>
      );
    })}
  </div>
);

const STRIP2: Record<number, [string,string][]> = {
  0:  [["WHERE","SHEETS"],["COST","FREE"],["STYLE","CHIP"]],
  1:  [["USE","TRACKING"],["IN","ONE CELL"],["SETUP","NONE"]],
  2:  [["DATE","26 JUL 2024"],["SOURCE","GOOGLE BLOG"],["VERIFIED","TODAY"]],
  3:  [["BEFORE","ONE VALUE"],["AFTER","MANY"],["SAME CELL","YES"]],
  4:  [["MENU","DATA VALIDATION"],["CHOOSE","DROPDOWN"],["TICK","MULTIPLE"]],
  5:  [["STYLE","CHIP"],["OTHER","DISABLED"],["ONLY WAY","CHIP"]],
  6:  [["CELL","ONE"],["STATUS","THREE"],["CHIPS","YES"]],
  7:  [["SOURCE","OFFICIAL"],["READ","TODAY"],["GUESS","NONE"]],
  8:  [["COMPUTER","YES"],["MOBILE","NOT YET"],["HONEST","YES"]],
  9:  [["LABEL","CLEAN"],["SPACES","REMOVE"],["BREAKS","YES"]],
  10: [["SITE","SHEETS"],["OPEN","COMPUTER"],["LINK","BELOW"]],
};

const BottomStrip: React.FC<{ f: number; items: [string,string][] }> = ({ f, items }) => (
  <div style={{ position: "absolute", left: 66, top: 1480, width: 948, display: "flex", gap: 14 }}>
    {items.map((it, i) => {
      const d = Math.max(0, f - 34 - i * 7);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 14, stiffness: 150, mass: 0.5 } });
      const y = interpolate(sp, [0, 1], [34, 0]);
      const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{ flex: 1, background: PAPER, border: "3px solid #1C1C1C", borderRadius: 14,
          padding: "16px 18px", transform: `translateY(${y}px)`, opacity: op,
          boxShadow: "0 12px 26px rgba(0,0,0,0.14)" }}>
          <div style={{ fontFamily: "monospace", fontSize: 16, color: GREY, letterSpacing: 1 }}>{it[0]}</div>
          <div style={{ fontFamily: "Anton, Impact, sans-serif", fontSize: 30, color: INK, marginTop: 6 }}>{it[1]}</div>
        </div>
      );
    })}
  </div>
);

const Beat: React.FC<{ beat: any; dur: number; idx: number }> = ({ beat, dur, idx }) => {
  const f = useCurrentFrame();
  const camScale = interpolate(f, [0, dur], [1.0, 1.035]);
  const camY = interpolate(f, [0, dur], [0, -10]);
  const heroTop = 440;

  return (
    <AbsoluteFill style={{ transform: `scale(${camScale}) translateY(${camY}px)` }}>
      <div style={{ position: "absolute", left: 56, top: 56, fontFamily: "monospace", fontSize: 22,
        color: "#96948E", letterSpacing: 1 }}>{beat.top}</div>
      <div style={{ position: "absolute", left: 56, top: 92, width: 968, height: 2, background: "#CECCC4" }} />

      <Headline beat={beat} f={f} />

      {beat.hero === "proof" && (
        <>
          <Proof f={f} img={beat.img} hl={beat.hl} start={14} y={heroTop} h={780} />
          <div style={{ position: "absolute", left: 66, top: heroTop + 812, width: 948,
            fontFamily: "monospace", fontSize: 24, color: GREY,
            opacity: interpolate(f, [40, 56], [0, 1], { extrapolateRight: "clamp" }) }}>
            {beat.cap}
          </div>
        </>
      )}

      {beat.hero === "chips" && <ChipRow f={f} labels={beat.chips} start={18} y={heroTop + 120} big />}

      {beat.hero === "rows" && <Rows f={f} rows={beat.rows} start={16} y={heroTop + 40} />}

      {beat.hero === "single" && (
        <div style={{ position: "absolute", left: 66, top: heroTop + 120, width: 948 }}>
          <div style={{ background: PAPER, border: "3px solid #1C1C1C", borderRadius: 14,
            padding: "22px 26px", boxShadow: "0 12px 26px rgba(0,0,0,0.16)",
            opacity: interpolate(f, [16, 30], [0, 1], { extrapolateRight: "clamp" }) }}>
            <div style={{ fontFamily: "monospace", fontSize: 20, color: GREY }}>STATUS</div>
            <div style={{ fontFamily: "Anton, Impact, sans-serif", fontSize: 44, color: INK, marginTop: 8 }}>PENDING</div>
          </div>
          <div style={{ marginTop: 22, fontFamily: "Anton, Impact, sans-serif", fontSize: 60, color: RED,
            opacity: interpolate(f, [44, 58], [0, 1], { extrapolateRight: "clamp" }) }}>
            ONLY ONE. NO SECOND CHOICE.
          </div>
        </div>
      )}

      {beat.hero === "url" && (
        <>
          <div style={{ position: "absolute", left: 66, top: heroTop + 60, width: 948, height: 130,
            background: INK, borderRadius: 18, display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: "monospace", fontSize: 36, color: "#fff",
            boxShadow: "0 20px 44px rgba(0,0,0,0.25)",
            opacity: interpolate(f, [10, 26], [0, 1], { extrapolateRight: "clamp" }) }}>
            sheets.google.com
          </div>
          <ChipRow f={f} labels={["COMPUTER", "FREE", "LINK BELOW"]} start={34} y={heroTop + 230} />
        </>
      )}

      <BottomStrip f={f} items={STRIP2[idx] || STRIP2[0]} />

      <div style={{ position: "absolute", left: 0, bottom: 0, width: 1080, height: 10, background: "#DCDAD2" }}>
        <div style={{ width: `${Math.min(100, (idx + f / dur) / B2.length * 100)}%`, height: 10, background: ORANGE }} />
      </div>
      <div style={{ position: "absolute", left: 56, bottom: 30, display: "flex", gap: 6 }}>
        {B2.map((_, i) => (
          <div key={i} style={{ width: 13, height: 8, background: i <= idx ? ORANGE : "#C8C6BE" }} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Main2: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  let idx = B2.length - 1;
  for (let i = 0; i < B2.length; i++) if (t >= B2[i].s && t < B2[i].e) { idx = i; break; }
  const b = B2[idx];
  return (
    <AbsoluteFill>
      <Surface f={f} />
      <Bursts />
      <Sequence from={Math.round(b.s * fps)} durationInFrames={Math.round((b.e - b.s) * fps)}>
        <Beat beat={b} dur={Math.round((b.e - b.s) * fps)} idx={idx} />
      </Sequence>
    </AbsoluteFill>
  );
};
