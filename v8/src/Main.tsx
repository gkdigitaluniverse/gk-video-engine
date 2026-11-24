import React from "react";
import {
  AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig,
  interpolate, spring, Img, OffthreadVideo, staticFile,
} from "remotion";

/* ============================================================
   L6 light-editorial cream — the craft-anything language.
   Rules from the Remotion motion-graphics skills:
   - spring() + interpolate() only, never CSS animation
   - layered: scene surface -> paper card -> marker -> text
   - marker sits BEHIND words, drawn left-to-right, sequenced
   - slow camera push, restrained perspective
   - zero neon, zero glow, zero glass
   ============================================================ */

const CREAM = "#ECECE7";
const PAPER = "#FFFFFF";
const INK = "#111111";
const ORANGE = "#E8551F";
const MINT = "#A8E2C0";
const GREEN = "#22A05A";
const GREY = "#787874";
const CHROME = "#22242A";

export const BEATS = [
  { s: 0.00,  e: 2.62,  top: "(1) FREE TIER / CLOUDFLARE",
    l1: "NO SERVER.", l2: "NO ACCOUNT.", box: "TEST IN BROWSER",
    hero: "screen", rec: 8.0,  chip: "PLAYGROUND", chip2: "NO SIGN-IN" },
  { s: 2.62,  e: 5.48,  top: "(2) THE SETUP YOU SKIP",
    l1: "3 STEPS", l2: "BEFORE YOU SEE", box: "ANYTHING",
    hero: "rows", rows: [["Node.js install","STEP 1"],["npm + wrangler","STEP 2"],["Deploy to test","STEP 3"]] },
  { s: 5.48,  e: 10.40, top: "(3) FREE TIER / LIVE",
    l1: "CLOUDFLARE", l2: "WORKERS", box: "PLAYGROUND",
    hero: "screen", rec: 10.6, chip: "NO AUTH", chip2: "LIVE PREVIEW" },
  { s: 10.40, e: 14.06, top: "(4) BEFORE vs NOW",
    l1: "SETUP GONE.", l2: "PREVIEW", box: "LIVE",
    hero: "rows", rows: [["Pehle: setup + deploy","MINUTES"],["Ab: editor + preview","LIVE"]] },
  { s: 14.06, e: 17.86, top: "(5) LIVE / SIDE BY SIDE",
    l1: "EDITOR +", l2: "LIVE", box: "PREVIEW",
    hero: "screen", rec: 18.6, chip: "SIDE BY SIDE", chip2: "INSTANT" },
  { s: 17.86, e: 22.02, top: "(6) LIVE / EDIT",
    l1: "CHANGE", l2: "HELLO", box: "WORLD",
    hero: "screen", rec: 21.8, chip: "YOUR RESPONSE", chip2: "SEE OUTPUT" },
  { s: 22.02, e: 25.32, top: "(7) HTTP / REQUEST",
    l1: "SEND AN", l2: "HTTP", box: "REQUEST",
    hero: "rows", rows: [["GET /","200 OK"],["Response","FAST"]] },
  { s: 25.32, e: 26.72, top: "(8) PROOF / I CHECKED",
    l1: "I CHECKED", l2: "THE", box: "DOCS",
    hero: "screen", rec: 26.4, chip: "OFFICIAL PAGE", chip2: "TODAY" },
  { s: 26.72, e: 29.38, top: "(9) PROOF / VERIFIED TODAY",
    l1: "FREE PLAN", l2: "", box: "REQUESTS",
    hero: "stat", num: "100,000", unit: "REQUESTS PER DAY  ·  RESET MIDNIGHT UTC" },
  { s: 29.38, e: 32.32, top: "(10) PROOF / VERIFIED TODAY",
    l1: "CPU PER", l2: "", box: "REQUEST",
    hero: "stat", num: "10 ms", unit: "AVERAGE WORKER USES 2.2 ms" },
  { s: 32.32, e: 34.44, top: "(11) THE CATCH / HONEST",
    l1: "ONE", l2: "IT IS", box: "CATCH",
    hero: "rows", rows: [["Chrome / Firefox","WORKS"],["Mobile browser","NOT THIS"]] },
  { s: 34.44, e: 37.66, top: "(12) THE CATCH / DEPLOY",
    l1: "TEST: NO ACCOUNT", l2: "DEPLOY:", box: "ACCOUNT",
    hero: "rows", rows: [["Test in playground","NO ACCOUNT"],["Deploy to edge","ACCOUNT"]] },
  { s: 37.66, e: 39.72, top: "(13) NEXT / WHEN READY",
    l1: "DEPLOY", l2: "WHEN YOU", box: "WANT",
    hero: "screen", rec: 6.0, chip: "EDGE NETWORK", chip2: "YOUR CALL" },
  { s: 39.72, e: 42.07, top: "(14) LINK / DESCRIPTION",
    l1: "LINK IN", l2: "", box: "DESCRIPTION",
    hero: "url" },
];

const FPS = 60;

/* ---------- dot-grid surface ---------- */
const Surface: React.FC<{ f: number }> = ({ f }) => {
  const off = (f * 0.14) % 38;
  return (
    <AbsoluteFill style={{ backgroundColor: CREAM }}>
      <svg width="1080" height="1920" style={{ position: "absolute" }}>
        <defs>
          <pattern id="dots" width="38" height="38" patternUnits="userSpaceOnUse"
            x={off} y={off / 2}>
            <circle cx="2" cy="2" r="2.2" fill="#D6D4CC" />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#dots)" />
      </svg>
      <div style={{
        position: "absolute", top: 930, left: 0, width: "100%",
        textAlign: "center", fontFamily: "mono", fontSize: 54,
        color: "#E2E0D8", letterSpacing: 2,
      }}>gkhackter</div>
    </AbsoluteFill>
  );
};

/* ---------- irregular starburst ---------- */
const Starburst: React.FC<{ cx: number; cy: number; r: number; seed: number; rot: number; op: number }> =
({ cx, cy, r, seed, rot, op }) => {
  const rnd = (i: number) => {
    const x = Math.sin(seed * 99 + i * 7.13) * 10000;
    return x - Math.floor(x);
  };
  const N = 11;
  const pts: string[] = [];
  for (let i = 0; i < N * 2; i++) {
    const a = rot + (i * Math.PI) / N;
    const rr = i % 2 === 0 ? r : r * (0.42 + rnd(i) * 0.18);
    pts.push(`${cx + Math.cos(a) * rr},${cy + Math.sin(a) * rr}`);
  }
  return <polygon points={pts.join(" ")} fill={ORANGE} opacity={op} />;
};

/* ---------- marker highlight behind words ---------- */
const Marker: React.FC<{ p: number; w: number; h: number; seed: number }> = ({ p, w, h, seed }) => {
  if (p <= 0) return null;
  const W = w * p;
  const jitter = (i: number) => {
    const x = Math.sin(seed * 41 + i * 3.7) * 10000;
    return (x - Math.floor(x) - 0.5) * 10;
  };
  const top = 4 + jitter(1);
  const bot = h - 6 + jitter(2);
  return (
    <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0 }}>
      <path
        d={`M ${2 + jitter(3)} ${top}
            C ${W * 0.3} ${top - 4}, ${W * 0.7} ${top + 5}, ${W - 4} ${top + 2}
            L ${W - 2} ${bot}
            C ${W * 0.65} ${bot + 4}, ${W * 0.3} ${bot - 4}, ${4 + jitter(4)} ${bot - 2} Z`}
        fill={ORANGE} opacity={0.92}
      />
    </svg>
  );
};

/* ---------- headline with boxed word ---------- */
const Headline: React.FC<{ beat: any; f: number; start: number }> = ({ beat, f, start }) => {
  const local = f - start;
  const lh = 104;
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
        const mp = interpolate(local - i * 5 - 10, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return (
          <div key={i} style={{ position: "relative", height: lh, opacity: op, transform: `translateY(${y}px)` }}>
            {r.boxed ? (
              <span style={{
                position: "relative", display: "inline-block",
                fontFamily: "Anton, Impact, sans-serif",
                fontSize: 92, lineHeight: `${lh - 10}px`, letterSpacing: -1,
                color: "#FFFFFF", whiteSpace: "nowrap",
                background: ORANGE, padding: "0 16px",
                clipPath: "polygon(0 4%, 100% 0%, 100% 96%, 0 100%)",
                transform: `scaleX(${0.55 + 0.45 * mp})`,
                transformOrigin: "left center",
                opacity: 0.4 + 0.6 * mp,
              }}>{r.txt}</span>
            ) : (
              <span style={{
                position: "relative",
                fontFamily: "Anton, Impact, sans-serif",
                fontSize: 100, lineHeight: `${lh}px`, letterSpacing: -1,
                color: INK, whiteSpace: "nowrap",
              }}>{r.txt}</span>
            )}
          </div>
        );
      })}
    </div>
  );
};

/* ---------- white card with chrome ---------- */
const Card: React.FC<{ f: number; start: number; title?: string; pill?: string; x?: number; y: number; w?: number; h: number; children?: React.ReactNode }> =
({ f, start, title, pill, x = 66, y, w = 948, h, children }) => {
  const d = Math.max(0, f - start);
  const sp = spring({ frame: d, fps: FPS, config: { damping: 15, stiffness: 120, mass: 0.7 } });
  const sc = interpolate(sp, [0, 1], [0.92, 1]);
  const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h,
      transform: `scale(${sc})`, opacity: op,
      borderRadius: 20, overflow: "visible",
      boxShadow: "0 22px 48px rgba(0,0,0,0.22)",
    }}>
      <div style={{
        width: "100%", height: "100%", borderRadius: 20,
        border: "3px solid #1C1C1C", overflow: "hidden", background: PAPER,
        display: "flex", flexDirection: "column",
      }}>
        {title && (
          <div style={{ height: 46, background: CHROME, display: "flex", alignItems: "center", paddingLeft: 16, flexShrink: 0 }}>
            {["#FF5F56", "#FFBD2E", "#27C93F"].map((c, i) => (
              <div key={i} style={{ width: 14, height: 14, borderRadius: 7, background: c, marginRight: 8 }} />
            ))}
            <span style={{ fontFamily: "monospace", fontSize: 21, color: "#D2D6E0", marginLeft: 16 }}>{title}</span>
          </div>
        )}
        <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>{children}</div>
      </div>
      {pill && (
        <div style={{
          position: "absolute", right: -8, top: -16, background: ORANGE,
          color: "#fff", fontFamily: "monospace", fontSize: 20, padding: "5px 12px",
          borderRadius: 8, letterSpacing: 1,
        }}>{pill}</div>
      )}
    </div>
  );
};

/* ---------- screen recording inside the card ---------- */
const ScreenClip: React.FC<{ rec: number; local: number; dur: number }> = ({ rec, local, dur }) => {
  const kb = interpolate(local, [0, dur], [1.0, 1.09]);
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <OffthreadVideo
        src={staticFile("play.mp4")}
        startFrom={Math.round(rec * 30)}
        muted
        style={{
          width: "100%", height: "100%", objectFit: "cover",
          transform: `scale(${kb})`,
        }}
      />
    </div>
  );
};

/* ---------- mint check row ---------- */
const CheckRow: React.FC<{ f: number; start: number; label: string; value: string; y: number }> =
({ f, start, label, value, y }) => {
  const d = Math.max(0, f - start);
  const sp = spring({ frame: d, fps: FPS, config: { damping: 14, stiffness: 140, mass: 0.55 } });
  const x = interpolate(sp, [0, 1], [-70, 0]);
  const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", left: 66, top: y, width: 948, height: 92,
      transform: `translateX(${x}px)`, opacity: op,
      background: MINT, border: "3px solid #181818", borderRadius: 14,
      boxShadow: "0 12px 26px rgba(0,0,0,0.16)",
      display: "flex", alignItems: "center", padding: "0 20px",
    }}>
      <div style={{
        width: 34, height: 34, borderRadius: 17, background: GREEN, color: "#fff",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: "sans-serif", fontWeight: 800, fontSize: 22, marginRight: 18,
      }}>✓</div>
      <div style={{ flex: 1, fontFamily: "Archivo Black, sans-serif", fontSize: 30, color: INK }}>{label}</div>
      <div style={{ fontFamily: "monospace", fontSize: 22, color: "#1E5A3C" }}>{value}</div>
    </div>
  );
};

/* ---------- big stat ---------- */
const BigStat: React.FC<{ f: number; start: number; num: string; unit: string; y: number }> =
({ f, start, num, unit, y }) => {
  const d = Math.max(0, f - start);
  const sp = spring({ frame: d, fps: FPS, config: { damping: 18, stiffness: 90, mass: 1.1 } });
  const sc = interpolate(sp, [0, 1], [0.72, 1]);
  const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
  const size = num.length > 5 ? 190 : 240;
  return (
    <div style={{ position: "absolute", left: 0, top: y, width: 1080, textAlign: "center", opacity: op, transform: `scale(${sc})` }}>
      <div style={{ fontFamily: "Anton, Impact, sans-serif", fontSize: size, lineHeight: `${size * 1.02}px`, color: ORANGE, letterSpacing: -2 }}>{num}</div>
      <div style={{ fontFamily: "monospace", fontSize: 30, color: INK, marginTop: 10 }}>{unit}</div>
    </div>
  );
};

/* ---------- chip ---------- */
const Chip: React.FC<{ f: number; start: number; text: string; x: number; y: number; green?: boolean }> =
({ f, start, text, x, y, green }) => {
  const d = Math.max(0, f - start);
  const sp = spring({ frame: d, fps: FPS, config: { damping: 12, stiffness: 170, mass: 0.45 } });
  const sc = interpolate(sp, [0, 1], [0.6, 1]);
  const op = interpolate(sp, [0, 0.5], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", left: x, top: y, opacity: op, transform: `scale(${sc})`,
      background: PAPER, border: `2.5px solid ${green ? GREEN : ORANGE}`, borderRadius: 9,
      padding: "7px 14px", fontFamily: "monospace", fontSize: 22,
      color: green ? GREEN : ORANGE, letterSpacing: 1,
    }}>{text}</div>
  );
};

/* ---------- one beat ---------- */
const Beat: React.FC<{ beat: any; dur: number; idx: number }> = ({ beat, dur, idx }) => {
  const f = useCurrentFrame();
  const prog = f / dur;

  // slow camera push, whole scene
  const camScale = interpolate(f, [0, dur], [1.0, 1.035]);
  const camY = interpolate(f, [0, dur], [0, -10]);

  const heroTop = 440;

  return (
    <AbsoluteFill style={{ transform: `scale(${camScale}) translateY(${camY}px)` }}>
      {/* top mono label */}
      <div style={{ position: "absolute", left: 56, top: 56, fontFamily: "monospace", fontSize: 22, color: "#96948E", letterSpacing: 1 }}>
        {beat.top}
      </div>
      <div style={{ position: "absolute", left: 56, top: 92, width: 968, height: 2, background: "#CECCC4" }} />

      <Headline beat={beat} f={f} start={4} />

      {beat.hero === "screen" && (
        <>
          <Card f={f} start={16} y={heroTop} h={880} title="workers.cloudflare.com/playground" pill="LIVE">
            <ScreenClip rec={beat.rec} local={f / FPS} dur={dur / FPS} />
          </Card>
          <Chip f={f} start={40} text={beat.chip} x={66} y={heroTop + 906} />
          <Chip f={f} start={52} text={beat.chip2} x={66 + beat.chip.length * 15 + 46} y={heroTop + 906} green />
        </>
      )}

      {beat.hero === "rows" && (
        <>
          {beat.rows.map((r: any, i: number) => (
            <CheckRow key={i} f={f} start={16 + i * 7} label={r[0]} value={r[1]} y={heroTop + i * 132} />
          ))}
          <div style={{
            position: "absolute", left: 66, top: heroTop + beat.rows.length * 132 + 30,
            width: 948, height: 88, background: PAPER, border: "3px solid #1C1C1C",
            borderRadius: 14, display: "flex", alignItems: "center", paddingLeft: 24,
            boxShadow: "0 12px 26px rgba(0,0,0,0.16)",
            fontFamily: "Archivo Black, sans-serif", fontSize: 28, color: INK,
            opacity: interpolate(f, [26, 40], [0, 1], { extrapolateRight: "clamp" }),
          }}>The playground skips all of this.</div>
        </>
      )}

      {beat.hero === "stat" && (
        <>
          <BigStat f={f} start={8} num={beat.num} unit={beat.unit} y={heroTop + 230} />
          <div style={{ position: "absolute", left: 66, top: heroTop + 700, width: 948, opacity: interpolate(f, [30, 46], [0, 1], { extrapolateRight: "clamp" }) }}>
            {[["Verified at", "developers.cloudflare.com"], ["Checked", "24 Nov 2026"]].map((r, i) => (
              <div key={i} style={{
                height: 70, background: PAPER, border: "3px solid #1C1C1C", borderRadius: 12,
                display: "flex", alignItems: "center", justifyContent: "space-between",
                padding: "0 22px", marginBottom: 16,
                fontFamily: "monospace", fontSize: 25,
              }}>
                <span style={{ color: GREY }}>{r[0]}</span>
                <span style={{ color: INK }}>{r[1]}</span>
              </div>
            ))}
          </div>
        </>
      )}

      {beat.hero === "url" && (
        <>
          <div style={{
            position: "absolute", left: 66, top: heroTop + 240, width: 948, height: 130,
            background: INK, borderRadius: 18, display: "flex", alignItems: "center",
            justifyContent: "center", boxShadow: "0 20px 44px rgba(0,0,0,0.25)",
            fontFamily: "monospace", fontSize: 34, color: "#fff", letterSpacing: 0.5,
            opacity: interpolate(f, [10, 26], [0, 1], { extrapolateRight: "clamp" }),
          }}>workers.cloudflare.com/playground</div>
          <Chip f={f} start={34} text="FREE TIER" x={66} y={heroTop + 420} green />
          <Chip f={f} start={44} text="NO ACCOUNT" x={266} y={heroTop + 420} />
          <Chip f={f} start={54} text="BROWSER ONLY" x={490} y={heroTop + 420} />
        </>
      )}

      {/* progress */}
      <div style={{ position: "absolute", left: 0, bottom: 0, width: 1080, height: 10, background: "#DCDAD2" }}>
        <div style={{ width: `${Math.min(100, (idx + prog) / BEATS.length * 100)}%`, height: 10, background: ORANGE }} />
      </div>
      <div style={{ position: "absolute", left: 56, bottom: 30, display: "flex", gap: 6 }}>
        {BEATS.map((_, i) => (
          <div key={i} style={{ width: 11, height: 8, background: i <= idx ? ORANGE : "#C8C6BE" }} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- starbursts, global ---------- */
const Bursts: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const spots = [
    [120, 190, 95], [955, 250, 120], [140, 770, 70],
    [985, 1180, 88], [90, 1520, 108], [1000, 640, 78],
  ];
  return (
    <svg width="1080" height="1920" style={{ position: "absolute" }}>
      {spots.map((s, i) => (
        <Starburst key={i} cx={s[0]} cy={s[1]} r={s[2] * (1 + 0.05 * Math.sin(t * 1.3 + i))}
          seed={i + 1} rot={t * 0.22 + i * 0.7} op={0.16} />
      ))}
    </svg>
  );
};

export const Main: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;

  let idx = BEATS.length - 1;
  for (let i = 0; i < BEATS.length; i++) {
    if (t >= BEATS[i].s && t < BEATS[i].e) { idx = i; break; }
  }
  const b = BEATS[idx];
  const startF = Math.round(b.s * fps);
  const durF = Math.round((b.e - b.s) * fps);

  return (
    <AbsoluteFill>
      <Surface f={f} />
      <Bursts />
      <Sequence from={startF} durationInFrames={durF}>
        <Beat beat={b} dur={durF} idx={idx} />
      </Sequence>
    </AbsoluteFill>
  );
};
