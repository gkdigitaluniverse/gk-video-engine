import React from "react";
import {
  AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { C, FONT, MONO } from "./theme";
import CAPTIONS from "./captions.json";

type Cap = { s: number; e: number; t: string };
const CAPS = CAPTIONS as Cap[];

export const BEATS = [
  { s: 0.0, e: 1.83 }, { s: 1.83, e: 3.28 }, { s: 3.28, e: 5.32 }, { s: 5.32, e: 7.49 },
  { s: 7.49, e: 9.85 }, { s: 9.85, e: 13.82 }, { s: 13.82, e: 15.08 }, { s: 15.08, e: 16.74 },
  { s: 16.74, e: 19.83 }, { s: 19.83, e: 21.73 }, { s: 21.73, e: 23.99 }, { s: 23.99, e: 26.08 },
  { s: 26.08, e: 30.74 }, { s: 30.74, e: 32.29 }, { s: 32.29, e: 35.53 }, { s: 35.53, e: 37.56 },
  { s: 37.56, e: 40.39 }, { s: 40.39, e: 42.22 }, { s: 42.22, e: 44.04 },
];

/* ---------- primitives ---------- */
const useSp = (delay = 0, damping = 12, stiffness = 140) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: f - delay, fps, config: { damping, stiffness } });
};

const Head: React.FC<{ t: string; size?: number; color?: string; style?: React.CSSProperties }> = ({
  t, size = 96, color = C.ink, style,
}) => (
  <div style={{
    fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 0.98,
    letterSpacing: -size * 0.03, color, textAlign: "center", ...style,
  }}>{t}</div>
);

const Mono: React.FC<{ t: string; size?: number; color?: string; style?: React.CSSProperties }> = ({
  t, size = 28, color = C.gray, style,
}) => (
  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: size, color, letterSpacing: 1, ...style }}>{t}</div>
);

const Card: React.FC<{ children?: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{
    position: "absolute", background: C.white, borderRadius: 40,
    border: `7px solid ${C.ink}`,
    boxShadow: "0 24px 0 rgba(20,22,26,0.10), 0 20px 46px rgba(20,22,26,0.14)",
    ...style,
  }}>{children}</div>
);

const Badge: React.FC<{ t: string; bg: string; fg: string; size?: number }> = ({ t, bg, fg, size = 28 }) => (
  <div style={{
    display: "inline-block", background: bg, color: fg, fontFamily: FONT, fontWeight: 900,
    fontSize: size, padding: `${size * 0.34}px ${size * 0.7}px`, borderRadius: 12, whiteSpace: "nowrap",
  }}>{t}</div>
);

const Tick: React.FC<{ s?: number; size?: number }> = ({ s = 1, size = 46 }) => (
  <div style={{
    width: size * s, height: size * s, borderRadius: "50%", background: C.green,
    display: "flex", alignItems: "center", justifyContent: "center",
    color: "#fff", fontFamily: FONT, fontWeight: 900, fontSize: size * 0.58 * s,
  }}>✓</div>
);

const Cross: React.FC<{ s?: number; size?: number }> = ({ s = 1, size = 46 }) => (
  <div style={{
    width: size * s, height: size * s, borderRadius: "50%", background: C.red,
    display: "flex", alignItems: "center", justifyContent: "center",
    color: "#fff", fontFamily: FONT, fontWeight: 900, fontSize: size * 0.5 * s,
  }}>✕</div>
);

/* ---------- syntaix-style blocks ---------- */
const WhatWhy: React.FC<{ what: string; why: string[]; lf: number }> = ({ what, why, lf }) => {
  const a = useSp(2), b = useSp(8);
  return (
    <div style={{ display: "flex", gap: 22, width: 880 }}>
      {[{ k: "WHAT IS IT?", body: what, sp: a, bg: C.yellow }, { k: "WHY CARE?", body: why, sp: b, bg: C.green2 }].map((col, i) => (
        <div key={i} style={{
          flex: 1, background: C.white, border: `6px solid ${C.ink}`, borderRadius: 24,
          padding: 22, transform: `translateY(${40 * (1 - col.sp)}px)`, opacity: Math.min(1, col.sp * 2),
        }}>
          <div style={{ display: "inline-block", background: col.bg, border: `4px solid ${C.ink}`, borderRadius: 10, padding: "6px 14px", fontFamily: FONT, fontWeight: 900, fontSize: 22 }}>{col.k}</div>
          {typeof col.body === "string" ? (
            <div style={{ fontFamily: MONO, fontSize: 22, lineHeight: 1.45, marginTop: 14, color: C.ink2 }}>{col.body}</div>
          ) : (
            (col.body as string[]).map((l, j) => (
              <div key={j} style={{ display: "flex", gap: 10, alignItems: "flex-start", marginTop: 12 }}>
                <div style={{ width: 12, height: 12, borderRadius: "50%", background: C.red, marginTop: 8, flexShrink: 0 }} />
                <div style={{ fontFamily: MONO, fontSize: 21, lineHeight: 1.35, color: C.ink2 }}>{l}</div>
              </div>
            ))
          )}
        </div>
      ))}
    </div>
  );
};

const RepoCard: React.FC<{ lf: number }> = ({ lf }) => {
  const s = useSp(4);
  return (
    <div style={{
      width: 880, background: C.white, border: `7px solid ${C.ink}`, borderRadius: 24,
      padding: "22px 26px", display: "flex", alignItems: "center", gap: 22,
      transform: `translateY(${50 * (1 - s)}px)`, opacity: Math.min(1, s * 2),
      boxShadow: "0 18px 0 rgba(20,22,26,0.08)",
    }}>
      <Img src={staticFile("assets/craft_icon.png")} style={{ width: 92, height: 92, borderRadius: 18 }} />
      <div style={{ flex: 1 }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 44, color: C.ink, lineHeight: 1 }}>Craft Anything</div>
        <Mono t="JAVASCRIPT · RUST APP CLONER" size={20} />
      </div>
      <Badge t="OPEN SOURCE" bg="#3FA34D" fg="#fff" size={24} />
    </div>
  );
};

const StepStrip: React.FC<{ labels: string[]; lf: number }> = ({ labels, lf }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 14, width: 900, justifyContent: "center" }}>
    {labels.map((l, i) => {
      const s = spring({ frame: lf - i * 7, fps: 30, config: { damping: 12, stiffness: 150 } });
      return (
        <React.Fragment key={l}>
          <div style={{
            width: 230, height: 150, background: [C.blue, C.yellow, C.green2][i], border: `6px solid ${C.ink}`,
            borderRadius: 22, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
            transform: `scale(${0.6 + 0.4 * s})`, opacity: Math.min(1, s * 2),
          }}>
            <Head t={`${i + 1}`} size={54} />
            <Mono t={l} size={20} />
          </div>
          {i < labels.length - 1 && (
            <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 46, color: C.orangeD, opacity: Math.min(1, s * 2) }}>→</div>
          )}
        </React.Fragment>
      );
    })}
  </div>
);

const BigNumber: React.FC<{ v: string; label: string; sub?: string; size?: number; lf: number }> = ({
  v, label, sub, size = 200, lf,
}) => {
  const s = useSp(2, 11, 150);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div style={{
        fontFamily: FONT, fontWeight: 900, fontSize: size, color: C.orangeD, lineHeight: 1,
        letterSpacing: -size * 0.04, transform: `scale(${1.5 - 0.5 * s})`, opacity: Math.min(1, s * 2),
      }}>{v}</div>
      <Head t={label} size={86} style={{ marginTop: 4 }} />
      {sub ? <Mono t={sub} size={24} style={{ marginTop: 16 }} /> : null}
    </div>
  );
};

/* ---------- 2D character ---------- */
const Dev: React.FC<{ x?: number; y?: number; scale?: number; pose?: "point" | "magnifier" | "shield" }> = ({
  x = 540, y = 1150, scale = 1, pose = "point",
}) => {
  const s = useSp(2);
  const b = (l: number, t: number, w: number, h: number, bg: string, r = 0): React.CSSProperties => ({
    position: "absolute", left: l, top: t, width: w, height: h, background: bg,
    borderRadius: r, border: `7px solid ${C.ink}`,
  });
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: 0, height: 0,
      transform: `translate(-50%,-50%) scale(${scale * (0.75 + 0.25 * s)})`, opacity: Math.min(1, s * 2),
    }}>
      <div style={b(-44, 78, 30, 62, C.blue, 10)} />
      <div style={b(14, 78, 30, 62, C.blue, 10)} />
      <div style={b(-64, 0, 128, 100, C.yellow, 30)} />
      <div style={b(-106, 18, 46, 20, C.ink, 10)} />
      <div style={b(60, 18, 46, 20, C.ink, 10)} />
      <div style={{ position: "absolute", left: -86, top: -140, width: 172, height: 172, borderRadius: "50%", background: C.blue, border: `7px solid ${C.ink}` }} />
      <div style={{ position: "absolute", left: -34, top: -76, width: 22, height: 22, borderRadius: "50%", background: C.ink }} />
      <div style={{ position: "absolute", left: 12, top: -76, width: 22, height: 22, borderRadius: "50%", background: C.ink }} />
      <div style={{ position: "absolute", left: -20, top: -34, width: 40, height: 9, borderRadius: 5, background: C.ink }} />
      {pose === "magnifier" && <>
        <div style={{ position: "absolute", left: 78, top: -110, width: 84, height: 84, borderRadius: "50%", border: `7px solid ${C.ink}`, background: "rgba(255,255,255,0.55)" }} />
        <div style={{ position: "absolute", left: 140, top: -36, width: 18, height: 50, background: C.ink, borderRadius: 9, transform: "rotate(-20deg)" }} />
      </>}
      {pose === "shield" && <div style={{ position: "absolute", left: 74, top: -20, width: 80, height: 96, background: C.green2, border: `7px solid ${C.ink}`, borderRadius: 16 }} />}
      {pose === "point" && <div style={{ position: "absolute", left: 106, top: 14, width: 26, height: 26, borderRadius: "50%", background: C.ink }} />}
    </div>
  );
};

/* ---------- composition ---------- */
export const Craft: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  let idx = 0;
  for (let i = 0; i < BEATS.length; i++) if (t >= BEATS[i].s) idx = i;
  const b = BEATS[idx];
  const lf = frame - b.s * fps;
  const blen = (b.e - b.s) * fps;

  const ein = Math.min(1, Math.max(0, lf / 7));
  const ex = Math.min(1, Math.max(0, (lf - (blen - 6)) / 6));
  const push = 1 + 0.035 * Math.min(1, lf / blen);
  const sc = (0.955 + 0.045 * ein) * push;
  const yoff = 80 * (1 - ein) - 110 * ex;
  const op = (ein < 0.1 ? ein / 0.1 : 1) * (1 - ex);

  const cap = CAPS.find((c) => t >= c.s && t < c.e) || CAPS[CAPS.length - 1];
  const capLf = frame - cap.s * fps;
  const capS = spring({ frame: capLf, fps, config: { damping: 15, stiffness: 170 } });

  const hold = frame >= 626 && frame <= 640;
  const wipe = ein < 1 ? 1080 * (1 - Math.pow(1 - ein, 3)) : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: C.cream }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(#D6D6CD 2.4px, transparent 2.4px)", backgroundSize: "46px 46px" }} />

      {hold && <Img src={staticFile("assets/thumb.png")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />}

      <div style={{ position: "absolute", inset: 0, transform: `translateY(${yoff}px) scale(${sc})`, opacity: hold ? 0 : op }}>

        {/* 0 — HOOK */}
        {idx === 0 && <>
          {["COPY ANY", "APP?"].map((w, i) => {
            const s = spring({ frame: lf - i * 6, fps, config: { damping: 11, stiffness: 150 } });
            return <Head key={w} t={w} size={126} color={i ? C.orangeD : C.ink}
              style={{ position: "absolute", top: 190 + i * 132, width: "100%", transform: `translateY(${60 * (1 - s)}px)`, opacity: Math.min(1, s * 2) }} />;
          })}
          <Card style={{ left: 150, top: 620, width: 300, height: 340, background: C.purple }} />
          <Card style={{ left: 630, top: 620, width: 300, height: 340, background: C.green2, transform: "rotate(4deg)" }} />
          <div style={{ position: "absolute", left: 470, top: 780, width: 140, height: 14, background: C.ink, borderRadius: 7 }} />
          <Dev y={1180} />
        </>}

        {/* 1 — 3 STEPS */}
        {idx === 1 && <>
          <Head t="IN 3 STEPS" size={104} style={{ position: "absolute", top: 250, width: "100%" }} />
          <div style={{ position: "absolute", top: 640, width: "100%", display: "flex", justifyContent: "center" }}>
            <StepStrip labels={["STUDY", "BUILD", "CHECK"]} lf={lf} />
          </div>
          <Dev y={1210} />
        </>}

        {/* 2 — WHAT IS IT */}
        {idx === 2 && <Card style={{ left: 90, top: 300, width: 900, height: 1000 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 44, gap: 24 }}>
            <Img src={staticFile("assets/craft_icon.png")} style={{ width: 190, height: 190 }} />
            <Head t="CRAFT ANYTHING" size={72} />
            <div style={{ display: "flex", gap: 14 }}>
              <Badge t="RUST" bg={C.purple} fg={C.ink} size={24} />
              <Badge t="APACHE-2.0" bg={C.yellow} fg={C.ink} size={24} />
              <Badge t="OPEN SOURCE" bg="#3FA34D" fg="#fff" size={24} />
            </div>
            <WhatWhy lf={lf} what="A Rust engine that studies an app, then rebuilds it as a new project." why={["Website, app or game", "Any language you pick", "Runs on your machine"]} />
          </div>
        </Card>}

        {/* 3 — WEBSITE APP GAME */}
        {idx === 3 && <>
          <Head t="WEBSITE · APP · GAME" size={62} style={{ position: "absolute", top: 250, width: "100%" }} />
          {["project-website.png", "project-game.png", "make.png"].map((n, i) => {
            const s = spring({ frame: lf - i * 6, fps, config: { damping: 12, stiffness: 140 } });
            return (
              <div key={n} style={{
                position: "absolute", left: 105 + i * 292, top: 470, width: 268, height: 330,
                borderRadius: 20, overflow: "hidden", border: `6px solid ${C.ink}`,
                transform: `translateY(${110 * (1 - s)}px) rotate(${(i - 1) * 6 * (1 - s)}deg)`, opacity: Math.min(1, s * 2),
              }}>
                <Img src={staticFile(`assets/${n}`)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              </div>
            );
          })}
          <div style={{ position: "absolute", top: 850, width: "100%", display: "flex", justifyContent: "center" }}>
            <StepStrip labels={["CLONE", "EDIT", "SHIP"]} lf={lf - 10} />
          </div>
          <Dev y={1230} />
        </>}

        {/* 4 — ANYTHING */}
        {idx === 4 && <>
          <Head t="ANYTHING" size={126} style={{ position: "absolute", top: 260, width: "100%" }} />
          <Card style={{ left: 150, top: 600, width: 290, height: 330, background: C.purple }} />
          <Card style={{ left: 640, top: 600, width: 290, height: 330, background: C.green2 }} />
          <div style={{ position: "absolute", left: 470, top: 750, width: 150, height: 14, background: C.ink, borderRadius: 7 }} />
          <div style={{ position: "absolute", left: 830, top: 700 }}><Tick size={64} /></div>
          <Dev y={1160} />
        </>}

        {/* 5 — STUDY */}
        {idx === 5 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ position: "absolute", left: 46, top: 40, background: C.orange, border: `6px solid ${C.ink}`, borderRadius: 16, padding: "8px 22px", fontFamily: FONT, fontWeight: 900, fontSize: 30, color: "#fff" }}>STEP 1</div>
          <Head t="STUDY" size={92} style={{ position: "absolute", top: 104, width: "100%" }} />
          <div style={{ position: "absolute", left: 56, top: 300, width: 720, height: 390, borderRadius: 20, overflow: "hidden", border: `6px solid ${C.ink}` }}>
            <Img src={staticFile("assets/workbench.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </div>
          <div style={{ position: "absolute", left: 56, top: 720, width: 780 }}>
            {["LAYOUT", "COLOURS", "FONTS", "MENUS"].map((l, i) => (
              <div key={l} style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 12, opacity: lf > 10 + i * 8 ? 1 : 0.15 }}>
                <Tick size={34} /><Mono t={l} size={26} color={C.ink} />
              </div>
            ))}
          </div>
          <Dev pose="magnifier" scale={0.5} x={740} y={790} />
        </Card>}

        {/* 6 — BUILD */}
        {idx === 6 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ position: "absolute", left: 46, top: 40, background: C.orange, border: `6px solid ${C.ink}`, borderRadius: 16, padding: "8px 22px", fontFamily: FONT, fontWeight: 900, fontSize: 30, color: "#fff" }}>STEP 2</div>
          <Head t="BUILD" size={92} style={{ position: "absolute", top: 104, width: "100%" }} />
          {[C.blue, C.yellow, C.green2, C.purple].map((col, i) => {
            const s = spring({ frame: lf - i * 5, fps, config: { damping: 12, stiffness: 160 } });
            return <div key={i} style={{ position: "absolute", left: 120 + i * 165, top: 700 - 100 * s, width: 145, height: 88, background: col, border: `6px solid ${C.ink}`, borderRadius: 16 }} />;
          })}
          <div style={{ position: "absolute", left: 100, top: 795, width: 730, height: 8, background: C.ink }} />
          <Dev pose="shield" scale={0.62} x={700} y={540} />
        </Card>}

        {/* 7 — CLAUDE CODE */}
        {idx === 7 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 50, gap: 18 }}>
            <Img src={staticFile("assets/claude.png")} style={{ width: 112, height: 112 }} />
            <Head t="CLAUDE CODE" size={78} />
            <Mono t="CODING AGENT · BUILDER" size={24} />
            <div style={{ width: 790, background: C.ink, borderRadius: 22, padding: 26, minHeight: 320 }}>
              <div style={{ display: "flex", gap: 9, marginBottom: 16 }}>
                {["#EE6A5A", "#F4BF4F", "#62C56A"].map((c) => <div key={c} style={{ width: 18, height: 18, borderRadius: "50%", background: c }} />)}
              </div>
              <Mono t={"$ claude --build".slice(0, Math.max(1, Math.floor(lf / 3)))} size={30} color="#96DCA8" />
              {lf > 26 && <Mono t="> studying target ..." size={24} color="#C8C8C0" style={{ marginTop: 18 }} />}
              {lf > 44 && <Mono t="> writing project ..." size={24} color="#C8C8C0" style={{ marginTop: 10 }} />}
            </div>
          </div>
        </Card>}

        {/* 8 — ANY LANGUAGE */}
        {idx === 8 && <>
          <Head t="ANY LANGUAGE" size={78} style={{ position: "absolute", top: 270, width: "100%" }} />
          {["RUST", "TYPESCRIPT", "PYTHON"].map((l, i) => {
            const s = spring({ frame: lf - i * 6, fps, config: { damping: 12, stiffness: 150 } });
            return <div key={l} style={{
              position: "absolute", left: 300 - 130 * (1 - s), top: 480 + i * 130, width: 480, height: 96,
              background: [C.purple, C.blue, C.yellow][i], border: `6px solid ${C.ink}`, borderRadius: 22,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: FONT, fontWeight: 900, fontSize: 38, opacity: Math.min(1, s * 2),
            }}>{l}</div>;
          })}
          <Dev y={1180} />
        </>}

        {/* 9 — CHECK */}
        {idx === 9 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ position: "absolute", left: 46, top: 40, background: C.orange, border: `6px solid ${C.ink}`, borderRadius: 16, padding: "8px 22px", fontFamily: FONT, fontWeight: 900, fontSize: 30, color: "#fff" }}>STEP 3</div>
          <Head t="CHECK" size={92} style={{ position: "absolute", top: 104, width: "100%" }} />
          <div style={{ position: "absolute", left: 56, top: 300, width: 720, height: 390, borderRadius: 20, overflow: "hidden", border: `6px solid ${C.ink}` }}>
            <Img src={staticFile("assets/make.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </div>
          <div style={{ position: "absolute", left: 56, top: 730, width: 780 }}>
            <Mono t="SCORED vs ORIGINAL · 3 SCREEN WIDTHS" size={24} color={C.ink2} />
          </div>
          <div style={{ position: "absolute", left: 720, top: 620 }}><Tick size={86} /></div>
        </Card>}

        {/* 10 — COMPARED */}
        {idx === 10 && <>
          <Head t="COMPARED" size={80} style={{ position: "absolute", top: 260, width: "100%" }} />
          <Mono t="TO THE ORIGINAL" size={26} style={{ position: "absolute", top: 356, width: "100%", textAlign: "center" }} />
          {["LAYOUT", "COLOURS", "BEHAVIOUR"].map((l, i) => {
            const flip = lf > 12 + i * 6;
            return (
              <div key={l} style={{
                position: "absolute", left: 130, top: 450 + i * 150, width: 820, height: 118,
                background: flip ? C.green2 : C.pink, border: `6px solid ${C.ink}`, borderRadius: 22,
                display: "flex", alignItems: "center", gap: 26, paddingLeft: 26,
              }}>
                {flip ? <Tick size={50} /> : <Cross size={50} />}
                <Head t={l} size={32} style={{ textAlign: "left" }} />
                <div style={{ marginLeft: "auto", marginRight: 26 }}>
                  <Mono t={flip ? "MATCH" : "OFF"} size={28} color={flip ? C.green : C.red} />
                </div>
              </div>
            );
          })}
        </>}

        {/* 11 — FIX */}
        {idx === 11 && <>
          <Head t="FIX WHAT'S OFF" size={74} style={{ position: "absolute", top: 270, width: "100%" }} />
          {[0, 1, 2].map((i) => {
            const s = spring({ frame: lf - i * 6, fps, config: { damping: 13, stiffness: 140 } });
            return <div key={i} style={{
              position: "absolute", left: 140, top: 480 + i * 150, width: 800, height: 118,
              background: C.green2, border: `6px solid ${C.green}`, borderRadius: 22,
              display: "flex", alignItems: "center", gap: 26, paddingLeft: 26, opacity: Math.min(1, s * 2),
            }}>
              <Tick s={s} size={50} />
              <div style={{ width: 430, height: 24, background: C.ink, borderRadius: 12 }} />
            </div>;
          })}
          <Dev scale={0.66} y={1210} />
        </>}

        {/* 12 — 91% */}
        {idx === 12 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 46, gap: 10 }}>
            <Img src={staticFile("assets/ycombinator.png")} style={{ width: 84, height: 84 }} />
            <Mono t="HACKER NEWS" size={26} />
            <BigNumber v="91%" label="IN 29 MIN" sub="REAL TEST · RainyTechLab · DEV + YouTube" size={210} lf={lf} />
            <div style={{ marginTop: 10 }}><RepoCard lf={lf} /></div>
          </div>
        </Card>}

        {/* 13 — I CHECKED */}
        {idx === 13 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <Head t="I CHECKED MYSELF" size={66} style={{ position: "absolute", top: 44, width: "100%" }} />
          <Mono t="LIVE API · NOBODY TOLD ME" size={24} style={{ position: "absolute", top: 130, width: "100%", textAlign: "center" }} />
          <div style={{ position: "absolute", left: 48, top: 200, width: 804, height: 520, background: C.ink, borderRadius: 24, padding: 24 }}>
            <div style={{ display: "flex", gap: 9, marginBottom: 14 }}>
              {["#EE6A5A", "#F4BF4F", "#62C56A"].map((c) => <div key={c} style={{ width: 18, height: 18, borderRadius: "50%", background: c }} />)}
            </div>
            {[
              "$ curl api.github.com/repos/storytold/craft-anything",
              '"full_name":         "storytold/craft-anything"',
              '"forks_count":       7125',
              '"language":          "Rust"',
              '"license":           "Apache-2.0"',
              '"open_issues_count": 387',
            ].map((line, i) => (
              <div key={i} style={{ fontFamily: MONO, fontSize: 21, color: i === 0 ? "#96DCA8" : "#E2E2DC", marginTop: i ? 9 : 0, opacity: lf > 5 + i * 5 ? 1 : 0 }}>{line}</div>
            ))}
          </div>
          <div style={{ position: "absolute", left: 48, top: 760, width: 804 }}>
            <WhatWhy lf={lf} what="GitHub API, called by me, on camera." why={["Live numbers", "No screenshots of screenshots", "Verifiable"]} />
          </div>
        </Card>}

        {/* 14 — STARS */}
        {idx === 14 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 54, gap: 14 }}>
            <Img src={staticFile("assets/github.png")} style={{ width: 110, height: 110 }} />
            <BigNumber v={Math.round(35250 * Math.min(1, Math.max(0, (lf - 2) / 22))).toLocaleString("en-US")}
              label="GITHUB STARS" sub="7,125 FORKS · APACHE-2.0" size={150} lf={lf} />
            <RepoCard lf={lf} />
            <Dev scale={0.5} x={540} y={720} />
          </div>
        </Card>}

        {/* 15 — EARLY ALPHA */}
        {idx === 15 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 70 }}>
            <Head t="EARLY" size={140} /><Head t="ALPHA" size={140} style={{ marginTop: 6 }} />
            <div style={{ marginTop: 34, border: `8px solid ${C.red}`, borderRadius: 16, padding: "16px 54px", transform: "rotate(-8deg)", fontFamily: FONT, fontWeight: 900, fontSize: 68, color: C.red }}>HONEST</div>
            <div style={{ marginTop: 30 }}><Mono t="RESULTS VARY" size={28} /></div>
          </div>
        </Card>}

        {/* 16 — OWN SOFTWARE */}
        {idx === 16 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ position: "absolute", top: 54, width: "100%", textAlign: "center" }}>
            <Head t="YOUR OWN" size={78} /><Head t="SOFTWARE ONLY" size={78} style={{ marginTop: 8 }} />
          </div>
          <Dev pose="shield" scale={0.74} x={380} y={520} />
          <div style={{ position: "absolute", left: 130, top: 640, width: 700 }}>
            {["ALLOWED SOFTWARE ONLY", "NO DRM BYPASS", "NO LOGIN BYPASS"].map((l, i) => (
              <div key={l} style={{ display: "flex", alignItems: "center", gap: 16, marginTop: 26, opacity: lf > 7 + i * 6 ? 1 : 0.12 }}>
                <Tick size={42} /><Mono t={l} size={28} color={C.ink} />
              </div>
            ))}
          </div>
        </Card>}

        {/* 17 — COMMENT */}
        {idx === 17 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 60 }}>
            <Head t="COMMENT" size={88} />
            <div style={{ marginTop: 22, background: C.orange, border: `7px solid ${C.ink}`, borderRadius: 26, padding: "16px 46px", fontFamily: FONT, fontWeight: 900, fontSize: 100, color: "#fff" }}>"CRAFT"</div>
            <div style={{ marginTop: 46, width: 740, height: 124, background: C.paper, border: `6px solid ${C.ink}`, borderRadius: 62, display: "flex", alignItems: "center", paddingLeft: 38, gap: 6 }}>
              <Mono t={"CRAFT".slice(0, Math.max(1, Math.floor(lf / 4)))} size={38} color={C.ink} />
              <div style={{ width: 8, height: 50, background: C.orange, opacity: Math.floor(lf / 7) % 2 === 0 ? 1 : 0 }} />
            </div>
            <Dev scale={0.56} x={540} y={760} />
          </div>
        </Card>}

        {/* 18 — END */}
        {idx === 18 && <Card style={{ left: 90, top: 290, width: 900, height: 1020 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 54, gap: 16 }}>
            <Img src={staticFile("assets/craft_icon.png")} style={{ width: 180, height: 180 }} />
            <Head t="LIVE DEMO" size={84} /><Head t="NEXT VIDEO" size={84} color={C.orangeD} />
            <RepoCard lf={lf} />
            <Mono t="GITHUB LINK IN PINNED COMMENT" size={24} />
            <Dev scale={0.54} x={540} y={720} />
          </div>
        </Card>}
      </div>

      {/* caption */}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 1320, display: "flex", justifyContent: "center",
        transform: `translateY(${30 * (1 - capS)}px) scale(${0.9 + 0.1 * capS})`, opacity: hold ? 0 : Math.min(1, capS * 2),
      }}>
        <div style={{
          background: C.white, border: `6px solid ${C.ink}`, borderRadius: 50, padding: "20px 44px",
          fontFamily: FONT, fontWeight: 900, fontSize: 46, color: C.ink, whiteSpace: "nowrap",
          boxShadow: "0 10px 0 rgba(20,22,26,0.10)",
        }}>{cap.t}</div>
      </div>

      {wipe > 0 && <div style={{ position: "absolute", left: 0, top: 0, width: wipe, height: 12, background: C.orange }} />}

      <div style={{ position: "absolute", left: 74, top: 78 }}><Mono t="GK HACKTECH" size={26} color={C.lgray} /></div>
      <div style={{ position: "absolute", right: 74, bottom: 56 }}><Mono t="gkhacktech" size={26} color={C.lgray} /></div>
    </AbsoluteFill>
  );
};
