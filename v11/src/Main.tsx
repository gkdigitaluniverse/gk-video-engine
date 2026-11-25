import React from "react";
import {
  AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig,
  interpolate, spring, Img, staticFile, continueRender, delayRender,
} from "remotion";

/* ============================================================
   L6 light-editorial cream — GK HACKTER channel language.
   spring() + interpolate() only. Never linear, never CSS animation.
   60fps · 1080x1920 · crf 16
   ============================================================ */

const CREAM = "#ECECE7";
const PAPER = "#FFFFFF";
const INK = "#111111";
const ORANGE = "#E8551F";
const MINT = "#A8E2C0";
const GREEN = "#22A05A";
const RED = "#D23C2D";
const CHROME = "#22242A";
const MUTE = "#96948E";
const SOURCE = "#606680";

const FPS = 60;

export const BEATS = [
  { s: 0.00, e: 4.36, kick: "(1) THE MISTAKE / GITHUB",
    l1: "ONE MISTAKE", l2: "", box: "API KEY",
    hero: "shot", img: "repo-security.png", url: "github.com/gkdigitaluniverse/gk-video-engine",
    stamp: "EXPOSED", chips: ["PUBLIC REPO", "ONE COMMIT"],
    facts: [["What leaks", "API KEY"], ["Where", "PUBLIC REPO"], ["Who sees it", "ANYONE"]] },

  { s: 4.36, e: 8.34, kick: "(2) THE FEATURE / PUSH PROTECTION",
    l1: "IF YOU PUSH", l2: "", box: "TO GITHUB",
    hero: "shot", img: "docs-push.png", url: "docs.github.com/en/code-security",
    chips: ["BUILT IN", "NO EXTRA TOOL"],
    facts: [["Feature", "PUSH PROTECTION"], ["Where", "REPO SETTINGS"], ["Cost", "FREE / PUBLIC"]] },

  { s: 8.34, e: 12.13, kick: "(3) WHAT IT DOES / BEFORE THE REPO",
    l1: "STOPS IT", l2: "", box: "BEFORE THE REPO",
    hero: "flow", img: "docs-push.png", url: "docs.github.com/en/code-security",
    flow: ["YOUR CODE", "BLOCK", "REPO"],
    facts: [["Checks", "ON EVERY PUSH"], ["Blocks", "SUPPORTED SECRETS"], ["When", "BEFORE MERGE"]] },

  { s: 12.13, e: 15.57, kick: "(4) THE OLD WAY / AFTER THE FACT",
    l1: "OLD WAY:", l2: "", box: "TOO LATE",
    hero: "rows", rows: [["1  commit", "GOES IN"], ["2  leak", "LIVE"], ["3  alert", "TOO LATE"]],
    rowsRed: true, after: ["NOW: commit", "BLOCKED"],
    facts: [["Old flow", "AFTER PUSH"], ["Damage", "ALREADY DONE"], ["New flow", "BEFORE PUSH"]] },

  { s: 15.57, e: 18.80, kick: "(5) SUPPORTED = BLOCKED",
    l1: "SUPPORTED", l2: "", box: "= BLOCKED",
    hero: "shot", img: "docs-before.png", url: "docs.github.com/en/code-security",
    ribbon: "PUSH BLOCKED",
    facts: [["Detects", "KNOWN PATTERNS"], ["Action", "BLOCKS PUSH"], ["Bypass", "EXISTS"]] },

  { s: 18.80, e: 22.58, kick: "(6) OFFICIAL LIST / COUNTED TODAY",
    l1: "OFFICIAL", l2: "", box: "PATTERNS",
    hero: "count", img: "awesome-532.png", url: "github.com/advanced-security/awesome-secret-scanning",
    num: 532, unit: "SUPPORTED PATTERNS  ·  465 WITH PUSH PROTECTION",
    facts: [["Partner types", "532"], ["With push protection", "465"], ["Checked", "25 NOV 2026"]] },

  { s: 22.58, e: 24.52, kick: "(7) THE CATCH / HONEST",
    l1: "NOT EVERY", l2: "", box: "SECRET",
    hero: "chips", img: "docs-subset.png", url: "docs.github.com/en/code-security",
    crossChips: ["OLD TOKENS", "TOO LARGE PUSH", "GENERIC PASSWORDS"],
    facts: [["Blocks", "A SUBSET"], ["Not all", "PATTERNS"], ["So", "STILL BE CAREFUL"]] },

  { s: 24.52, e: 28.21, kick: "(8) THE LIMIT / PUBLIC REPOS",
    l1: "OVER 50 MB", l2: "", box: "NO SCAN",
    hero: "count2", img: "docs-50mb.png", url: "docs.github.com/en/code-security",
    num: 50, unit: "MB  ·  PUSH SKIPPED, NOT SCANNED",
    facts: [["Limit", "50 MB PUSH"], ["Scope", "PUBLIC REPOS"], ["Then", "SKIPPED"]] },

  { s: 28.42, e: 32.46, kick: "(9) DO THIS INSTEAD / ENV VARS",
    l1: "NEVER IN", l2: "", box: "CODE",
    hero: "checks", checks: [["key in code", false], [".env + env var", true]],
    code: "process.env.API_KEY",
    facts: [["Keep in", "ENV VAR"], ["Never in", "GIT"], ["Add", ".gitignore"]] },

  { s: 32.54, e: 33.87, kick: "(10) FULL GUIDE / DESCRIPTION",
    l1: "FULL GUIDE", l2: "", box: "DESCRIPTION",
    hero: "urlcard", img: "docs-scanning.png", url: "docs.github.com › code-security",
    facts: [["Source", "GITHUB DOCS"], ["Checked", "25 NOV 2026"], ["Setup", "REPO SETTINGS"]] },

  { s: 33.87, e: 35.60, kick: "(10) FULL GUIDE / DESCRIPTION",
    l1: "FULL GUIDE", l2: "", box: "DESCRIPTION",
    hero: "urlcard", img: "docs-scanning.png", url: "docs.github.com › code-security",
    facts: [["Source", "GITHUB DOCS"], ["Checked", "25 NOV 2026"], ["Setup", "REPO SETTINGS"]] },
];

const THUMB_FROM = 17.55;
const THUMB_TO = 18.05;

/* ---------- fonts ---------- */
const FontLoader: React.FC = () => {
  const [handle] = React.useState(() => delayRender("fonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    const css = `
      @font-face{font-family:'Anton';src:url('${staticFile("fonts/Anton-Regular.ttf")}') format('truetype');}
      @font-face{font-family:'SpaceMono';font-weight:400;src:url('${staticFile("fonts/SpaceMono-Regular.ttf")}') format('truetype');}
      @font-face{font-family:'SpaceMono';font-weight:700;src:url('${staticFile("fonts/SpaceMono-Bold.ttf")}') format('truetype');}
    `;
    const st = document.createElement("style");
    st.textContent = css;
    document.head.appendChild(st);
    Promise.all([
      document.fonts.load("96px Anton"),
      document.fonts.load("700 24px SpaceMono"),
      document.fonts.load("24px SpaceMono"),
    ]).then(() => document.fonts.ready).then(() => { setReady(true); continueRender(handle); })
      .catch(() => { setReady(true); continueRender(handle); });
  }, [handle]);
  return ready ? null : null;
};

const HEAD: React.CSSProperties = { fontFamily: "Anton", color: INK, lineHeight: 0.92, letterSpacing: -1 };
const MONO = (s: number, w = 400, c = SOURCE): React.CSSProperties =>
  ({ fontFamily: "SpaceMono", fontSize: s, fontWeight: w, color: c, letterSpacing: 0.5 });

/* ---------- surface ---------- */
const Surface: React.FC<{ f: number }> = ({ f }) => {
  const off = (f * 0.14) % 38;
  return (
    <AbsoluteFill style={{ backgroundColor: CREAM }}>
      <svg width="1080" height="1920" style={{ position: "absolute" }}>
        <defs>
          <pattern id="dots" width="38" height="38" patternUnits="userSpaceOnUse" x={off} y={off / 2}>
            <circle cx="2" cy="2" r="2.2" fill="#D6D4CC" />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#dots)" />
      </svg>
      <div style={{ position: "absolute", top: 930, left: 0, width: "100%", textAlign: "center",
        fontFamily: "SpaceMono", fontSize: 54, color: "#E2E0D8", letterSpacing: 2 }}>gkhackter</div>
    </AbsoluteFill>
  );
};

/* ---------- starburst ---------- */
const Starburst: React.FC<{ cx: number; cy: number; r: number; seed: number; rot: number; op: number }> =
({ cx, cy, r, seed, rot, op }) => {
  const rnd = (i: number) => { const x = Math.sin(seed * 99 + i * 7.13) * 10000; return x - Math.floor(x); };
  const N = 11; const pts: string[] = [];
  for (let i = 0; i < N * 2; i++) {
    const a = rot + (i * Math.PI) / N;
    const rr = i % 2 === 0 ? r : r * (0.42 + rnd(i) * 0.18);
    pts.push(`${cx + Math.cos(a) * rr},${cy + Math.sin(a) * rr}`);
  }
  return <polygon points={pts.join(" ")} fill={ORANGE} opacity={op} />;
};

/* ---------- kicker + rule ---------- */
const Kicker: React.FC<{ text: string; local: number }> = ({ text, local }) => {
  const sp = spring({ frame: local, fps: FPS, config: { damping: 18, stiffness: 140, mass: 0.6 } });
  const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
  const w = interpolate(sp, [0, 1], [0, 968]);
  return (
    <>
      <div style={{ position: "absolute", left: 56, top: 52, ...MONO(23, 700, MUTE), opacity: op }}>{text}</div>
      <div style={{ position: "absolute", left: 56, top: 92, height: 2, width: w, background: "#C9C7BE" }} />
    </>
  );
};

/* ---------- headline ---------- */
const Headline: React.FC<{ beat: any; local: number }> = ({ beat, local }) => {
  const rows: { txt: string; boxed: boolean }[] = [];
  if (beat.l1) rows.push({ txt: beat.l1, boxed: false });
  if (beat.l2) rows.push({ txt: beat.l2, boxed: false });
  if (beat.box) rows.push({ txt: beat.box, boxed: true });
  return (
    <div style={{ position: "absolute", left: 56, top: 130, width: 968 }}>
      {rows.map((r, i) => {
        const d = Math.max(0, local - i * 5);
        const sp = spring({ frame: d, fps: FPS, config: { damping: 16, stiffness: 130, mass: 0.6 } });
        const y = interpolate(sp, [0, 1], [46, 0]);
        const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
        const mp = interpolate(local - i * 5 - 8, [0, 12], [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const size = r.txt.length > 12 ? 84 : 104;
        return (
          <div key={i} style={{ position: "relative", height: size * 0.98, opacity: op,
            transform: `translateY(${y}px)` }}>
            {r.boxed && (
              <div style={{ position: "absolute", left: -4, top: size * 0.02, height: size * 0.86,
                width: `calc(${(mp * 100).toFixed(1)}% + ${(mp * 30).toFixed(1)}px)`,
                background: ORANGE, borderRadius: 8, transformOrigin: "left center" }} />
            )}
            <div style={{ ...HEAD, fontSize: size, position: "relative",
              color: r.boxed ? PAPER : INK, paddingLeft: r.boxed ? 22 : 0, paddingRight: r.boxed ? 22 : 0 }}>
              {r.txt}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ---------- paper card with chrome ---------- */
const ShotCard: React.FC<{ img: string; url: string; local: number; h?: number; ribbon?: string;
  dim?: boolean; hl?: number }> =
({ img, url, local, h = 610, ribbon, dim, hl = 0 }) => {
  const sp = spring({ frame: local, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
  const y = interpolate(sp, [0, 1], [44, 0]);
  const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
  const zoom = interpolate(local, [0, 150], [1.0, 1.06], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 60, top: 440, width: 960, opacity: op,
      transform: `translateY(${y}px)` }}>
      <div style={{ background: PAPER, borderRadius: 18, overflow: "hidden",
        boxShadow: "0 26px 60px rgba(17,17,17,0.18)" }}>
        <div style={{ height: 62, background: CHROME, display: "flex", alignItems: "center",
          padding: "0 22px", gap: 10 }}>
          {[0, 1, 2].map(i => <div key={i} style={{ width: 13, height: 13, borderRadius: 7,
            background: i === 0 ? "#FF5F57" : i === 1 ? "#FEBC2E" : "#28C840" }} />)}
          <div style={{ marginLeft: 14, background: "#33363E", borderRadius: 14, padding: "7px 18px",
            ...MONO(19, 400, "#D2D6E0") }}>{url}</div>
        </div>
        <div style={{ position: "relative", height: h, overflow: "hidden" }}>
          <Img src={staticFile("shots/" + img)} style={{ width: "100%", height: "100%",
            objectFit: "cover", objectPosition: "top center",
            transform: `scale(${zoom})`, filter: dim ? "saturate(0.7) brightness(0.92)" : "none" }} />
          {hl > 0 && (
            <div style={{ position: "absolute", left: "6%", top: "42%", height: 44,
              width: `${hl * 88}%`, background: "rgba(232,85,31,0.30)", borderBottom: `4px solid ${ORANGE}` }} />
          )}
          {ribbon && (
            <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 84,
              background: RED, display: "flex", alignItems: "center", justifyContent: "center",
              transform: `scaleX(${interpolate(sp, [0, 1], [0, 1])})`, transformOrigin: "left center" }}>
              <div style={{ ...HEAD, fontSize: 52, color: PAPER, letterSpacing: 2 }}>{ribbon}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

/* ---------- big number ---------- */
const BigNum: React.FC<{ to: number; unit: string; local: number; suffix?: string }> =
({ to, unit, local, suffix }) => {
  const p = interpolate(local, [6, 52], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - p, 3);
  const val = Math.round(eased * to);
  const sp = spring({ frame: local, fps: FPS, config: { damping: 14, stiffness: 110, mass: 0.7 } });
  const sc = interpolate(sp, [0, 1], [0.9, 1]);
  return (
    <div style={{ position: "absolute", left: 56, top: 470, width: 968, transform: `scale(${sc})`,
      transformOrigin: "left top" }}>
      <div style={{ ...HEAD, fontSize: 232, color: ORANGE }}>{val.toLocaleString("en-US")}{suffix || ""}</div>
      <div style={{ ...MONO(22, 700, SOURCE), marginTop: 8, letterSpacing: 1.2 }}>{unit}</div>
    </div>
  );
};

/* ---------- small screenshot strip ---------- */
const ShotStrip: React.FC<{ img: string; local: number; top?: number }> = ({ img, local, top = 900 }) => {
  const sp = spring({ frame: local, fps: FPS, config: { damping: 16, stiffness: 120, mass: 0.7 } });
  const y = interpolate(sp, [0, 1], [50, 0]);
  return (
    <div style={{ position: "absolute", left: 60, top, width: 960, transform: `translateY(${y}px)`,
      borderRadius: 16, overflow: "hidden", background: PAPER,
      boxShadow: "0 18px 44px rgba(17,17,17,0.16)", border: "2px solid #E3E1D8" }}>
      <Img src={staticFile("shots/" + img)} style={{ width: "100%", height: 380,
        objectFit: "cover", objectPosition: "top center" }} />
    </div>
  );
};

/* ---------- fact cards ---------- */
const FactCards: React.FC<{ facts: string[][]; local: number }> = ({ facts, local }) => (
  <div style={{ position: "absolute", left: 56, top: 1470, width: 968, display: "flex", gap: 16 }}>
    {facts.map(([k, v], i) => {
      const d = Math.max(0, local - 18 - i * 7);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
      const y = interpolate(sp, [0, 1], [38, 0]);
      const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{ flex: 1, background: PAPER, borderRadius: 14, padding: "22px 20px",
          opacity: op, transform: `translateY(${y}px)`, boxShadow: "0 10px 26px rgba(17,17,17,0.10)" }}>
          <div style={{ ...HEAD, fontSize: 26, color: INK, marginBottom: 10 }}>{k}</div>
          <div style={{ ...MONO(20, 700, i === 2 ? ORANGE : GREEN) }}>{v}</div>
        </div>
      );
    })}
  </div>
);

/* ---------- flow chips ---------- */
const Flow: React.FC<{ items: string[]; local: number }> = ({ items, local }) => (
  <div style={{ position: "absolute", left: 56, top: 640, width: 968, display: "flex",
    alignItems: "center", justifyContent: "space-between" }}>
    {items.map((t, i) => {
      const d = Math.max(0, local - 8 - i * 8);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 125, mass: 0.65 } });
      const sc = interpolate(sp, [0, 1], [0.6, 1]);
      const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
      const mid = i === 1;
      const pulse = mid ? 1 + 0.08 * Math.sin(Math.max(0, local - 40) / 8) : 1;
      return (
        <React.Fragment key={i}>
          <div style={{ opacity: op, transform: `scale(${sc * pulse})`, background: mid ? ORANGE : PAPER,
            borderRadius: 12, padding: "20px 18px", minWidth: 240, textAlign: "center",
            boxShadow: "0 12px 28px rgba(17,17,17,0.14)" }}>
            <div style={{ ...HEAD, fontSize: 34, color: mid ? PAPER : INK }}>{t}</div>
          </div>
          {i < items.length - 1 && (
            <div style={{ opacity: op, ...HEAD, fontSize: 44, color: "#B9B7AE" }}>→</div>
          )}
        </React.Fragment>
      );
    })}
  </div>
);

/* ---------- rows ---------- */
const Rows: React.FC<{ rows: string[][]; red?: boolean; local: number; after?: string[] }> =
({ rows, red, local, after }) => (
  <div style={{ position: "absolute", left: 56, top: 560, width: 968 }}>
    {rows.map(([a, b], i) => {
      const d = Math.max(0, local - 6 - i * 7);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
      const y = interpolate(sp, [0, 1], [40, 0]);
      const op = interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" });
      return (
        <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
          background: PAPER, borderRadius: 14, padding: "24px 26px", marginBottom: 16, opacity: op,
          transform: `translateY(${y}px)`, boxShadow: "0 10px 26px rgba(17,17,17,0.10)" }}>
          <div style={{ ...HEAD, fontSize: 40, color: INK }}>{a}</div>
          <div style={{ ...MONO(21, 700, red ? RED : GREEN) }}>{b}</div>
        </div>
      );
    })}
    {after && (
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
        background: MINT, borderRadius: 14, padding: "24px 26px", marginTop: 10,
        opacity: interpolate(local, [34, 46], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        transform: `translateY(${interpolate(spring({ frame: Math.max(0, local - 34), fps: FPS,
          config: { damping: 15, stiffness: 120, mass: 0.7 } }), [0, 1], [34, 0])}px)` }}>
        <div style={{ ...HEAD, fontSize: 40, color: INK }}>{after[0]}</div>
        <div style={{ ...MONO(21, 700, GREEN) }}>{after[1]}</div>
      </div>
    )}
  </div>
);

/* ---------- check rows ---------- */
const Checks: React.FC<{ rows: [string, boolean][]; code?: string; local: number }> =
({ rows, code, local }) => (
  <div style={{ position: "absolute", left: 56, top: 600, width: 968 }}>
    {rows.map(([t, ok], i) => {
      const d = Math.max(0, local - 6 - i * 8);
      const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
      const y = interpolate(sp, [0, 1], [40, 0]);
      return (
        <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
          background: ok ? MINT : PAPER, borderRadius: 14, padding: "26px 26px", marginBottom: 18,
          opacity: interpolate(sp, [0, 0.6], [0, 1], { extrapolateRight: "clamp" }),
          transform: `translateY(${y}px)`, boxShadow: "0 10px 26px rgba(17,17,17,0.10)" }}>
          <div style={{ ...HEAD, fontSize: 38, color: INK }}>{t}</div>
          <div style={{ ...HEAD, fontSize: 46, color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</div>
        </div>
      );
    })}
    {code && (
      <div style={{ marginTop: 8, background: CHROME, borderRadius: 12, padding: "22px 26px",
        opacity: interpolate(local, [30, 44], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
        <div style={{ ...MONO(26, 700, "#A8E2C0") }}>{code}</div>
      </div>
    )}
  </div>
);

/* ---------- url card ---------- */
const UrlCard: React.FC<{ url: string; local: number; img: string }> = ({ url, local, img }) => {
  const sp = spring({ frame: local, fps: FPS, config: { damping: 15, stiffness: 115, mass: 0.75 } });
  const y = interpolate(sp, [0, 1], [60, 0]);
  return (
    <div style={{ position: "absolute", left: 56, top: 520, width: 968 }}>
      <div style={{ background: PAPER, borderRadius: 18, padding: "34px 32px",
        transform: `translateY(${y}px)`, boxShadow: "0 22px 50px rgba(17,17,17,0.16)" }}>
        <div style={{ ...MONO(20, 700, MUTE), marginBottom: 14 }}>GITHUB OFFICIAL DOCS</div>
        <div style={{ ...HEAD, fontSize: 54, color: INK, lineHeight: 1.05 }}>{url}</div>
        <div style={{ height: 2, background: "#E6E4DB", margin: "26px 0" }} />
        <div style={{ display: "flex", gap: 14 }}>
          {["PUSH PROTECTION", "SECRET SCANNING", "PATTERNS"].map((t, i) => {
            const d = Math.max(0, local - 14 - i * 6);
            const s2 = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 130, mass: 0.6 } });
            return <div key={t} style={{ background: i === 0 ? ORANGE : "#F2F0E9", borderRadius: 10,
              padding: "12px 16px", ...MONO(18, 700, i === 0 ? PAPER : INK),
              transform: `scale(${interpolate(s2, [0, 1], [0.7, 1])})` }}>{t}</div>;
          })}
        </div>
      </div>
      <ShotStrip img={img} local={local - 20} top={300} />
    </div>
  );
};

/* ---------- progress ---------- */
const Progress: React.FC<{ f: number; total: number; beats: number }> = ({ f, total, beats }) => (
  <div style={{ position: "absolute", left: 56, top: 1884, width: 968 }}>
    <div style={{ height: 8, background: "#DAD8CF", borderRadius: 4, overflow: "hidden" }}>
      <div style={{ height: 8, width: `${(f / total) * 100}%`, background: ORANGE, borderRadius: 4 }} />
    </div>
    <div style={{ display: "flex", gap: 8, marginTop: 14 }}>
      {Array.from({ length: beats }).map((_, i) => (
        <div key={i} style={{ width: 26, height: 6, borderRadius: 3,
          background: i / beats <= f / total ? ORANGE : "#DAD8CF" }} />
      ))}
    </div>
  </div>
);

/* ---------- main ---------- */
export const Main: React.FC = () => {
  const f = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = f / fps;

  const beatIdx = Math.max(0, BEATS.findIndex(b => t >= b.s && t < b.e));
  const beat = BEATS[beatIdx === -1 ? BEATS.length - 1 : beatIdx];
  const local = (t - beat.s) * fps;

  const cam = interpolate(t, [0, 35.6], [1.0, 1.035]);
  const rot = f * 0.22 / fps * 10;

  const thumbOn = t >= THUMB_FROM && t < THUMB_TO;

  return (
    <AbsoluteFill style={{ backgroundColor: CREAM }}>
      <FontLoader />
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        <Surface f={f} />

        <svg width="1080" height="1920" style={{ position: "absolute" }}>
          <Starburst cx={980} cy={210} r={110} seed={3} rot={rot} op={0.20} />
          <Starburst cx={70} cy={1290} r={86} seed={7} rot={-rot} op={0.17} />
          <Starburst cx={1010} cy={1620} r={70} seed={11} rot={rot * 0.8} op={0.16} />
          <Starburst cx={120} cy={640} r={64} seed={17} rot={-rot * 1.1} op={0.16} />
        </svg>

        <Kicker text={beat.kick} local={local} />
        <Headline beat={beat} local={local} />

        {beat.hero === "shot" && (
          <ShotCard img={beat.img} url={beat.url} local={local} ribbon={beat.ribbon}
            dim={beatIdx === 0} hl={beatIdx === 2 ? interpolate(local, [26, 40], [0, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0} />
        )}
        {beat.hero === "flow" && <Flow items={beat.flow!} local={local} />}
        {beat.hero === "rows" && <Rows rows={beat.rows!} red={beat.rowsRed} local={local} after={beat.after} />}
        {beat.hero === "count" && (
          <>
            <BigNum to={beat.num!} unit={beat.unit!} local={local} />
            <ShotStrip img={beat.img!} local={local - 10} top={1010} />
          </>
        )}
        {beat.hero === "count2" && (
          <>
            <BigNum to={beat.num!} unit={beat.unit!} local={local} suffix=" MB" />
            <ShotStrip img={beat.img!} local={local - 10} top={1010} />
          </>
        )}
        {beat.hero === "chips" && (
          <>
            <div style={{ position: "absolute", left: 56, top: 520, width: 968, display: "flex",
              flexWrap: "wrap", gap: 14 }}>
              {beat.crossChips!.map((c, i) => {
                const d = Math.max(0, local - 6 - i * 7);
                const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 125, mass: 0.65 } });
                return <div key={c} style={{ background: PAPER, borderRadius: 12, padding: "18px 22px",
                  border: `3px solid ${RED}`, transform: `scale(${interpolate(sp, [0, 1], [0.7, 1])})`,
                  opacity: interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" }) }}>
                  <div style={{ ...HEAD, fontSize: 30, color: RED }}>✗ {c}</div></div>;
              })}
            </div>
            <ShotStrip img={beat.img!} local={local - 8} top={780} />
          </>
        )}
        {beat.hero === "checks" && <Checks rows={beat.checks! as any} code={beat.code} local={local} />}
        {beat.hero === "urlcard" && <UrlCard url={beat.url} local={local} img={beat.img!} />}

        {beat.facts && <FactCards facts={beat.facts} local={local} />}

        <div style={{ position: "absolute", left: 56, top: 1790, width: 968,
          ...MONO(19, 400, SOURCE) }}>
          github.com docs · checked 25 Nov 2026
        </div>
        <Progress f={f} total={durationInFrames} beats={BEATS.length} />
      </AbsoluteFill>

      {thumbOn && (
        <AbsoluteFill>
          <Img src={staticFile("thumbnail.png")} style={{ width: 1080, height: 1920 }} />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

// build 1 — thumbnail committed, shots from release run1
