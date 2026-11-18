import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Composition,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Craft } from "./Craft";
import { C, FONT } from "./theme";

/* ---- font loading (blocks render until Montserrat is ready) ---- */
const FontGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [handle] = useState(() => delayRender("Loading Montserrat"));
  useEffect(() => {
    const style = document.createElement("style");
    style.innerHTML = `@font-face{font-family:'Montserrat';src:url('${staticFile(
      "fonts/Montserrat-Black.ttf"
    )}') format('truetype');font-weight:900;font-style:normal;font-display:block;}`;
    document.head.appendChild(style);
    document.fonts
      .load("900 100px Montserrat")
      .then(() => document.fonts.ready)
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  return <AbsoluteFill style={{ fontFamily: FONT }}>{children}</AbsoluteFill>;
};

const Smoke: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 12, stiffness: 120 } });
  const x = interpolate(s, [0, 1], [-420, 0]);
  const op = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.cream, justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(#D6D6CD 2px, transparent 2px)", backgroundSize: "46px 46px" }} />
      <div style={{ transform: `translateX(${x}px) scale(${0.7 + 0.3 * s})`, opacity: op, textAlign: "center" }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 150, color: C.ink, letterSpacing: -4 }}>ENGINE</div>
        <div style={{ display: "inline-block", marginTop: 24, padding: "18px 44px", borderRadius: 28, background: C.orange, color: "#fff", fontFamily: FONT, fontWeight: 900, fontSize: 92 }}>WORKS</div>
      </div>
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Smoke" component={Smoke} durationInFrames={90} fps={30} width={1080} height={1920} />
    <Composition
      id="Craft"
      component={() => (
        <FontGate>
          <Craft />
        </FontGate>
      )}
      durationInFrames={1322}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);
