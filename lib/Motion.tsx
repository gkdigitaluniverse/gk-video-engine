import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * Motion Presets — naam se bulao, har video me same feel.
 * <PunchZoom from={1} to={1.25} fx={0.5} fy={0.3}> <Img/> </PunchZoom>
 */

/** Apple-style smooth zoom/pan wrapper (spring-like ease) */
export const PunchZoom: React.FC<{
  from?: number; to?: number; fx?: number; fy?: number; children: React.ReactNode;
}> = ({ from = 1, to = 1.2, fx = 0.5, fy = 0.4, children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - t, 4); // easeOutQuart ≈ Apple feel
  return (
    <div style={{ width: "100%", height: "100%", transform: `scale(${from + (to - from) * eased})`, transformOrigin: `${fx * 100}% ${fy * 100}%` }}>
      {children}
    </div>
  );
};

/** Ken Burns: slow zoom + halka pan (photo/B-roll ke liye) */
export const KenBurns: React.FC<{ panX?: number; panY?: number; children: React.ReactNode }> = ({ panX = 24, panY = -16, children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ width: "100%", height: "100%", transform: `scale(${1.06 + t * 0.14}) translate(${t * panX}px, ${t * panY}px)` }}>
      {children}
    </div>
  );
};

/** Draw-on highlight border (asset ke andar %, zoom ke saath exact chalta hai) */
export const DrawHighlight: React.FC<{
  l: number; t: number; w: number; h: number; delay?: number; color?: string;
}> = ({ l, t, w, h, delay = 6, color = "#FFD028" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 17, stiffness: 175 } });
  return (
    <div style={{
      position: "absolute", left: `${l}%`, top: `${t}%`, width: `${w}%`, height: `${h}%`,
      border: `6px solid ${color}`, borderRadius: 18, opacity: p,
      transform: `scale(${0.96 + p * 0.04})`,
      boxShadow: `0 0 34px ${color}99, inset 0 0 20px ${color}33`,
    }} />
  );
};

/** Stamp: ghum ke zor se girne wala badge (offer/dhamaka ke liye) */
export const Stamp: React.FC<{ text: string; color?: string; delay?: number; fontSize?: number }> = ({ text, color = "#FF3D00", delay = 10, fontSize = 72 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 9, stiffness: 210 } });
  return (
    <div style={{
      display: "inline-block", background: color, color: "#fff",
      fontFamily: "Montserrat, Arial, sans-serif", fontWeight: 900, fontSize,
      padding: "18px 42px", borderRadius: 18, border: "4px solid rgba(255,255,255,.85)",
      transform: `scale(${2.1 - p * 1.1}) rotate(${-14 + p * 11}deg)`, opacity: p,
      boxShadow: "0 26px 60px rgba(0,0,0,.55)",
    }}>{text}</div>
  );
};

/** Counter: 0 se target tak ginti (price/views ke liye) */
export const Counter: React.FC<{ to: number; prefix?: string; suffix?: string; color?: string; fontSize?: number }> = ({ to, prefix = "", suffix = "", color = "#fff", fontSize = 92 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const v = Math.round(interpolate(frame, [0, Math.min(durationInFrames, 45)], [0, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <span style={{ fontFamily: "Montserrat, Arial, sans-serif", fontWeight: 900, fontSize, color }}>
      {prefix}{v.toLocaleString("en-IN")}{suffix}
    </span>
  );
};

/** Slide-up reveal (cards/text ke liye) */
export const SlideUp: React.FC<{ delay?: number; children: React.ReactNode }> = ({ delay = 0, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 15, stiffness: 180 } });
  return <div style={{ opacity: p, transform: `translateY(${(1 - p) * 56}px)` }}>{children}</div>;
};
