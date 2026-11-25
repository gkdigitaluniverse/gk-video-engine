import React from "react";
import { AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { SlideUp } from "../components/motion/Motion";

/**
 * Scene Templates — har theme me rang badal ke reuse karo.
 * Props se colors/fonts do; structure kabhi dobara mat banao.
 */
const F = "Montserrat, Arial, sans-serif";

export type Theme = { bg: string; bgGlow: string; accent: string; text: string; sub: string };
export const THEMES: Record<string, Theme> = {
  navy:    { bg: "#0A1633", bgGlow: "#0E2150", accent: "#FFD028", text: "#FFFFFF", sub: "#FFE9B0" },
  food:    { bg: "#0A1633", bgGlow: "#13224E", accent: "#FF5722", text: "#FFFFFF", sub: "#FFC9B3" },
  cream:   { bg: "#FAF3E7", bgGlow: "#FFF9EF", accent: "#FF4A1C", text: "#161616", sub: "#7A4A2B" },
  lime:    { bg: "#000000", bgGlow: "#101508", accent: "#C8F542", text: "#FFFFFF", sub: "#D9F99D" },
  festive: { bg: "#2B0A12", bgGlow: "#4A0E1F", accent: "#F5C542", text: "#FFF3D6", sub: "#FFE9A3" },
};

const Backdrop: React.FC<{ theme: Theme; children: React.ReactNode }> = ({ theme, children }) => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 28%, ${theme.bgGlow}, ${theme.bg} 74%)`, fontFamily: F }}>
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 18%, ${theme.accent}24, transparent 58%)` }} />
    {children}
  </AbsoluteFill>
);

export const BrandPill: React.FC<{ name: string; step: string; theme: Theme }> = ({ name, step, theme }) => (
  <div style={{ position: "absolute", top: 62, left: 52, right: 52, display: "flex", justifyContent: "space-between", zIndex: 5 }}>
    <div style={{ background: "rgba(5,8,20,.85)", border: `2px solid ${theme.accent}`, color: "#fff", fontWeight: 900, fontSize: 29, padding: "12px 24px", borderRadius: 999 }}>
      <span style={{ color: theme.accent }}>✳</span> {name}
    </div>
    <div style={{ background: theme.accent, color: "#1A1206", fontWeight: 900, fontSize: 27, padding: "12px 22px", borderRadius: 999 }}>{step}</div>
  </div>
);

/** Template 1 — Hook: bada kinetic sawal/problem + image neeche */
export const HookScene: React.FC<{ theme: Theme; brand: string; lines: string[]; accentLine?: number; img?: string; step?: string }> =
({ theme, brand, lines, accentLine = 1, img, step = "HOOK" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Backdrop theme={theme}>
      {img ? <Img src={staticFile(img)} style={{ position: "absolute", bottom: 0, width: "100%", height: "52%", objectFit: "cover", opacity: 0.9 }} /> : null}
      <AbsoluteFill style={{ background: `linear-gradient(180deg, ${theme.bg}E6, transparent 50%, ${theme.bg}E6)` }} />
      <BrandPill name={brand} step={step} theme={theme} />
      <div style={{ position: "absolute", top: 320, left: 58, right: 58, textAlign: "center" }}>
        {lines.map((l, i) => {
          const p = spring({ frame: frame - i * 8, fps, config: { damping: 13 } });
          return <div key={i} style={{ fontWeight: 900, fontSize: i === accentLine ? 112 : 74, color: i === accentLine ? theme.accent : theme.text, opacity: p, transform: `translateY(${(1 - p) * 52}px)`, lineHeight: 1.1 }}>{l}</div>;
        })}
      </div>
    </Backdrop>
  );
};

/** Template 2 — Section Card: scenes ke beech 1s ka bold title pop */
export const SectionCard: React.FC<{ theme: Theme; big: string; accentWord?: string }> = ({ theme, big, accentWord }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 12, stiffness: 210 } });
  if (frame > 32) return null;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", background: `${theme.bg}B8`, zIndex: 8, opacity: frame > 23 ? (32 - frame) / 9 : 1 }}>
      <div style={{ display: "flex", gap: 20, flexWrap: "wrap", justifyContent: "center", padding: "0 56px", transform: `scale(${0.85 + p * 0.15})`, opacity: p }}>
        {big.split(" ").map((w, i) => (
          <span key={i} style={{ fontWeight: 900, fontSize: 98, color: w === accentWord ? theme.accent : "#fff" }}>{w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/** Template 3 — Price/Offer Cards: do prices ka comparison */
export const PriceCompare: React.FC<{ theme: Theme; left: { label: string; price: string }; right: { label: string; price: string } }> =
({ theme, left, right }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const Card = (d: { label: string; price: string }, bad: boolean, delay: number) => {
    const p = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 190 } });
    return (
      <div style={{ background: bad ? "#FFE9E4" : "#FFFFFF", border: `5px solid ${bad ? "#FF3D00" : theme.accent}`, borderRadius: 28, padding: "34px 42px", textAlign: "center", opacity: p, transform: `scale(${0.8 + p * 0.2}) rotate(${bad ? 2 : -2}deg)`, boxShadow: "0 28px 60px rgba(0,0,0,.5)" }}>
        <div style={{ fontWeight: 800, fontSize: 33, color: "#3A2A20" }}>{d.label}</div>
        <div style={{ fontWeight: 900, fontSize: 84, color: bad ? "#D84315" : "#E65100", marginTop: 8 }}>{d.price}</div>
      </div>
    );
  };
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 26 }}>
      {Card(left, false, 6)}
      <div style={{ fontWeight: 900, fontSize: 62, color: "#fff" }}>+</div>
      {Card(right, true, 24)}
    </div>
  );
};

/** Template 4 — Bento Grid: 4 features ek saath. NOTE: icon me emoji mat do (render machine me emoji font nahi hota, box banta hai) — "GO", "1MB", "Rs 0" jaise chhote text-badge do. */
export const BentoGrid: React.FC<{ theme: Theme; title: string; items: { icon: string; head: string; sub: string }[] }> =
({ theme, title, items }) => (
  <Backdrop theme={theme}>
    <div style={{ position: "absolute", top: 250, left: 58, right: 58, textAlign: "center", fontWeight: 900, fontSize: 72, color: theme.text }}>{title}</div>
    <div style={{ position: "absolute", top: 430, left: 58, right: 58, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 26 }}>
      {items.slice(0, 4).map((it, i) => (
        <SlideUp key={i} delay={i * 7}>
          <div style={{ background: "rgba(255,255,255,.96)", borderRadius: 28, padding: "36px 30px", border: `4px solid ${theme.accent}`, boxShadow: "0 24px 54px rgba(0,0,0,.45)", minHeight: 300 }}>
            <div style={{ fontSize: 62 }}>{it.icon}</div>
            <div style={{ fontWeight: 900, fontSize: 42, color: "#171310", marginTop: 14, lineHeight: 1.12 }}>{it.head}</div>
            <div style={{ fontWeight: 600, fontSize: 31, color: "#5A4A3A", marginTop: 10, lineHeight: 1.25 }}>{it.sub}</div>
          </div>
        </SlideUp>
      ))}
    </div>
  </Backdrop>
);

/** Template 5 — Phone Mockup: cropped app asset, rounded frame me */
export const PhoneMockup: React.FC<{ ratio: number; children?: React.ReactNode; src?: string; framesFolder?: string; startFrame?: number }> =
({ ratio, children, src, framesFolder, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const idx = Math.min(149, Math.max(0, startFrame + frame));
  const w = 800;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "relative", width: w, height: w * ratio, borderRadius: 36, overflow: "hidden", boxShadow: "0 44px 100px rgba(0,0,0,.65)", border: "3px solid rgba(255,255,255,.28)", background: "#fff" }}>
        {framesFolder ? (
          <Img src={staticFile(`${framesFolder}/f${String(idx + 1).padStart(3, "0")}.jpg`)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : src ? (
          <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : null}
        {children}
      </div>
    </AbsoluteFill>
  );
};

/** Template 6 — Testimonial / Proof Card */
export const ProofCard: React.FC<{ theme: Theme; quote: string; name: string; badge?: string }> = ({ theme, quote, name, badge }) => (
  <Backdrop theme={theme}>
    <div style={{ position: "absolute", top: 480, left: 58, right: 58 }}>
      <SlideUp>
        <div style={{ background: "#fff", borderRadius: 32, padding: "52px 46px", boxShadow: "0 34px 80px rgba(0,0,0,.5)" }}>
          {badge ? <div style={{ display: "inline-block", background: theme.accent, color: "#1A1206", fontWeight: 900, fontSize: 28, padding: "10px 22px", borderRadius: 999 }}>{badge}</div> : null}
          <div style={{ fontWeight: 800, fontSize: 52, color: "#191410", lineHeight: 1.3, marginTop: 22 }}>"{quote}"</div>
          <div style={{ fontWeight: 700, fontSize: 34, color: "#7A6A55", marginTop: 20 }}>— {name}</div>
        </div>
      </SlideUp>
    </div>
  </Backdrop>
);

/** Template 7 — Before/After */
export const BeforeAfter: React.FC<{ theme: Theme; beforeImg: string; afterImg: string; label?: string }> = ({ theme, beforeImg, afterImg, label }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const split = 50 + Math.sin((frame / durationInFrames) * Math.PI * 2) * 26;
  return (
    <Backdrop theme={theme}>
      <div style={{ position: "absolute", top: 260, left: 70, right: 70, height: 1150, borderRadius: 32, overflow: "hidden", border: `4px solid ${theme.accent}` }}>
        <Img src={staticFile(afterImg)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }} />
        <div style={{ position: "absolute", inset: 0, width: `${split}%`, overflow: "hidden" }}>
          <Img src={staticFile(beforeImg)} style={{ width: 940, height: "100%", objectFit: "cover", filter: "grayscale(.5) brightness(.8)" }} />
        </div>
        <div style={{ position: "absolute", top: 0, bottom: 0, left: `${split}%`, width: 6, background: theme.accent }} />
        <div style={{ position: "absolute", top: 26, left: 26, background: "rgba(0,0,0,.7)", color: "#fff", fontWeight: 900, fontSize: 28, padding: "8px 18px", borderRadius: 999 }}>BEFORE</div>
        <div style={{ position: "absolute", top: 26, right: 26, background: theme.accent, color: "#1A1206", fontWeight: 900, fontSize: 28, padding: "8px 18px", borderRadius: 999 }}>AFTER</div>
      </div>
      {label ? <div style={{ position: "absolute", bottom: 330, left: 58, right: 58, textAlign: "center", fontWeight: 900, fontSize: 54, color: theme.text }}>{label}</div> : null}
    </Backdrop>
  );
};

/** Template 8 — End Card: logo + sawal + chips */
export const EndCard: React.FC<{ theme: Theme; brand: string; questionLines: string[]; accentWord?: string; chips: string[]; sub?: string }> =
({ theme, brand, questionLines, accentWord, chips, sub = "Comment karke batao" }) => (
  <AbsoluteFill style={{ background: `linear-gradient(165deg, ${theme.bgGlow}, ${theme.bg} 60%, #160A04)`, justifyContent: "center", alignItems: "center", padding: 62, fontFamily: F }}>
    <div style={{ background: "rgba(5,8,20,.85)", border: `3px solid ${theme.accent}`, color: "#fff", fontWeight: 900, fontSize: 30, padding: "13px 26px", borderRadius: 999 }}>
      <span style={{ color: theme.accent }}>✳</span> {brand}
    </div>
    <div style={{ fontWeight: 900, fontSize: 100, color: "#fff", textAlign: "center", lineHeight: 1.08, marginTop: 44 }}>
      {questionLines.map((l, i) => (
        <div key={i}>{l.split(" ").map((w, j) => <span key={j} style={{ color: w === accentWord ? theme.accent : "#fff" }}>{w} </span>)}</div>
      ))}
    </div>
    <div style={{ fontWeight: 800, fontSize: 42, color: theme.sub, marginTop: 32 }}>{sub}</div>
    <div style={{ display: "flex", gap: 16, marginTop: 44, flexWrap: "wrap", justifyContent: "center" }}>
      {chips.map((c) => (
        <div key={c} style={{ background: theme.accent, color: "#191104", fontWeight: 900, fontSize: 29, padding: "15px 24px", borderRadius: 999 }}>{c}</div>
      ))}
    </div>
  </AbsoluteFill>
);
