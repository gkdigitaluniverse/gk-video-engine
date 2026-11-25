import React from "react";
import { interpolate, spring, useCurrentFrame } from "remotion";

/**
 * 7 Subtitle Styles — ready components (see references/subtitle-styles.md)
 * Usage (har style ke liye same API):
 *   <Style6ClassicViral text="Delivery charge seedha zero" frames={90} accent="#FF5722" />
 * - text: caption line (2-7 words best)
 * - frames: is line ki duration frames me (voice ke word timing se)
 * - keyWord: highlight hone wala shabd (na do to beech wala bada shabd khud chunta hai — meaning se dena behtar)
 * Fonts: library ke assets/fonts se @font-face load karo (Fonts.tsx dekho).
 */

type CapProps = {
  text: string;
  frames: number;
  keyWord?: string;
  accent?: string;
  dark?: boolean; // light background par hai to true
};

const useWords = (text: string, frames: number) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  const active = Math.min(words.length - 1, Math.floor((frame / Math.max(1, frames)) * words.length));
  return { frame, words, active };
};

const pickKey = (words: string[], keyWord?: string) =>
  keyWord ? words.findIndex((w) => w.toLowerCase() === keyWord.toLowerCase()) : Math.floor(words.length / 2);

const wrap: React.CSSProperties = {
  position: "absolute", left: 50, right: 50, bottom: 150,
  display: "flex", justifyContent: "center", textAlign: "center",
};

/** 1 — Clean Caps: ALL CAPS, white, soft shadow */
export const Style1CleanCaps: React.FC<CapProps> = ({ text, frames }) => {
  const { frame, words, active } = useWords(text.toUpperCase(), frames);
  return (
    <div style={wrap}>
      <div style={{ fontFamily: "Nunito Black, Montserrat, sans-serif", fontWeight: 900, fontSize: 46, letterSpacing: 1 }}>
        {words.map((w, i) => (
          <span key={i} style={{ color: "#fff", textShadow: "0 4px 22px rgba(0,0,0,.65)", opacity: interpolate(frame, [i * 3, i * 3 + 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), marginRight: 13 }}>{w}</span>
        ))}
        <span style={{ display: "none" }}>{active}</span>
      </div>
    </div>
  );
};

/** 2 — Lowercase + Serif Tail: key word italic serif */
export const Style2SerifTail: React.FC<CapProps> = ({ text, frames, keyWord, dark }) => {
  const { words, active } = useWords(text.toLowerCase(), frames);
  const key = pickKey(words, keyWord);
  const col = dark ? "#141414" : "#fff";
  return (
    <div style={wrap}>
      <div style={{ fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: 46 }}>
        {words.map((w, i) =>
          i === key ? (
            <span key={i} style={{ fontFamily: "Playfair Display, serif", fontStyle: "italic", fontWeight: 600, fontSize: 54, color: col, marginRight: 13 }}>{w}</span>
          ) : (
            <span key={i} style={{ color: col, opacity: i <= active ? 1 : 0.55, textShadow: dark ? "none" : "0 3px 16px rgba(0,0,0,.6)", marginRight: 13 }}>{w}</span>
          ),
        )}
      </div>
    </div>
  );
};

/** 3 — Pill: white rounded pill, spoken dark / upcoming grey */
export const Style3Pill: React.FC<CapProps> = ({ text, frames }) => {
  const { words, active } = useWords(text.toLowerCase(), frames);
  return (
    <div style={wrap}>
      <div style={{ background: "#fff", borderRadius: 999, padding: "16px 34px", fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: 40, boxShadow: "0 16px 40px rgba(0,0,0,.35)" }}>
        {words.map((w, i) => (
          <span key={i} style={{ color: i <= active ? "#161616" : "#A9A9A9", marginRight: 11 }}>{w}</span>
        ))}
      </div>
    </div>
  );
};

/** 4 — Serif Italic: sab serif italic, naya shabd heavy */
export const Style4SerifItalic: React.FC<CapProps> = ({ text, frames }) => {
  const { words, active } = useWords(text.toLowerCase(), frames);
  return (
    <div style={wrap}>
      <div style={{ fontFamily: "EB Garamond, serif", fontStyle: "italic", fontSize: 50 }}>
        {words.map((w, i) => (
          <span key={i} style={{ color: "#fff", fontWeight: i === active ? 800 : 500, textShadow: "0 3px 16px rgba(0,0,0,.6)", marginRight: 12 }}>{w}</span>
        ))}
      </div>
    </div>
  );
};

/** 5 — Editorial: bold sans + EK bada italic serif accent word (default lime) */
export const Style5Editorial: React.FC<CapProps> = ({ text, frames, keyWord, accent = "#C8F542" }) => {
  const { frame, words } = useWords(text, frames);
  const key = pickKey(words, keyWord);
  return (
    <div style={wrap}>
      <div style={{ fontFamily: "Montserrat, sans-serif", fontWeight: 800, fontSize: 46 }}>
        {words.map((w, i) => {
          if (i === key) {
            const p = spring({ frame: frame - Math.floor((i / words.length) * frames), fps: 30, config: { damping: 12, stiffness: 240 } });
            return (
              <span key={i} style={{ display: "inline-block", fontFamily: "Playfair Display, serif", fontStyle: "italic", fontWeight: 700, fontSize: 66, color: accent, transform: `scale(${0.85 + p * 0.15})`, marginRight: 14 }}>{w}</span>
            );
          }
          return <span key={i} style={{ color: "#fff", textShadow: "0 3px 16px rgba(0,0,0,.6)", marginRight: 13 }}>{w}</span>;
        })}
      </div>
    </div>
  );
};

/** 6 — Classic Viral: UPPERCASE, black outline, active word accent me pop (default yellow) */
export const Style6ClassicViral: React.FC<CapProps> = ({ text, frames, accent = "#FFD028" }) => {
  const { frame, words, active } = useWords(text.toUpperCase(), frames);
  return (
    <div style={wrap}>
      <div style={{ fontFamily: "Montserrat, sans-serif", fontWeight: 900, fontSize: 54 }}>
        {words.map((w, i) => {
          const isA = i === active;
          const p = isA ? spring({ frame: frame - Math.floor((i / words.length) * frames), fps: 30, config: { damping: 10, stiffness: 260 } }) : 1;
          return (
            <span key={i} style={{
              display: "inline-block", color: isA ? accent : "#fff",
              WebkitTextStroke: "2px rgba(0,0,0,.9)", textShadow: "0 5px 0 rgba(0,0,0,.85), 0 10px 26px rgba(0,0,0,.5)",
              transform: `scale(${isA ? 0.9 + p * 0.22 : 1})`, marginRight: 14,
            }}>{w}</span>
          );
        })}
      </div>
    </div>
  );
};

/** 7 — Documentary: chhota white uppercase, koi pop nahi, ek line */
export const Style7Documentary: React.FC<CapProps> = ({ text }) => {
  return (
    <div style={{ ...wrap, bottom: 120 }}>
      <div style={{ fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: 36, letterSpacing: 2, color: "#fff", textTransform: "uppercase", textShadow: "0 2px 12px rgba(0,0,0,.7)" }}>
        {text}
      </div>
    </div>
  );
};
