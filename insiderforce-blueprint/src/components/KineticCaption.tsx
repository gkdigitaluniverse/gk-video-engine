import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, FONTS, SHADOWS, SPRINGS } from "../theme";

interface KineticCaptionProps {
  leadText: string;
  pillText: string;
  pillAccent?: string;
  startSec: number;
  endSec: number;
}

/**
 * InsiderForce-grade editorial kinetic typography:
 * - Words progressively illuminate from muted gray to crisp jet black.
 * - The key phrase punches into a solid jet-black (or accent) inverted bar with deep studio shadow.
 */
export const KineticCaption: React.FC<KineticCaptionProps> = ({
  leadText,
  pillText,
  pillAccent,
  startSec,
  endSec,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentSec = frame / fps;
  const dur = Math.max(0.4, endSec - startSec);
  const progress = Math.min(1, Math.max(0, (currentSec - startSec) / (dur * 0.72)));

  const words = leadText.split(" ").filter(Boolean);
  const revealedCount = Math.max(1, Math.ceil(progress * words.length));

  const localFrame = Math.max(0, frame - Math.floor(startSec * fps));
  const pillDelay = Math.min(18, Math.floor(words.length * 2.2));
  const pillSpring = spring({
    frame: Math.max(0, localFrame - pillDelay),
    fps,
    config: SPRINGS.pop,
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 1120,
        left: 72,
        right: 72,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 24,
        zIndex: 20,
      }}
    >
      {/* Editorial kinetic lead line */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          columnGap: 16,
          rowGap: 8,
          maxWidth: 920,
          fontFamily: FONTS.sans,
          fontSize: 58,
          fontWeight: 500,
          lineHeight: 1.22,
          letterSpacing: "-0.03em",
          textAlign: "center",
        }}
      >
        {words.map((word, idx) => {
          const isLit = idx < revealedCount;
          const isLatest = idx === revealedCount - 1;
          return (
            <span
              key={`${idx}-${word}`}
              style={{
                color: isLit ? COLORS.ink : COLORS.inkFaint,
                fontWeight: isLatest ? 800 : isLit ? 600 : 400,
                opacity: isLit ? 1 : 0.65,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>

      {/* Inverted Solid Black Highlight Pill */}
      <div
        style={{
          backgroundColor: pillAccent || COLORS.ink,
          color: "#FFFFFF",
          fontFamily: FONTS.sans,
          fontSize: 64,
          fontWeight: 800,
          letterSpacing: "-0.025em",
          padding: "14px 36px",
          borderRadius: 14,
          boxShadow: SHADOWS.pill,
          transform: `scale(${interpolate(pillSpring, [0, 1], [0.84, 1])}) translateY(${interpolate(
            pillSpring,
            [0, 1],
            [22, 0]
          )}px)`,
          opacity: Math.min(1, pillSpring * 1.5),
        }}
      >
        {pillText}
      </div>
    </div>
  );
};
