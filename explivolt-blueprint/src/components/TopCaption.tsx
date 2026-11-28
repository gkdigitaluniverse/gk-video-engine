import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACCENTS, AccentKey, FONTS, PALETTES, SPRINGS, ThemeMode } from "../theme";

interface TopCaptionProps {
  text: string;
  startSec: number;
  endSec: number;
  mode: ThemeMode;
  accent: AccentKey;
}

/**
 * Explivolt-style top-center word-by-word boxed caption.
 * - Keeps the entire phrase visible so viewers can scan effortlessly.
 * - Highlights ONLY the currently spoken word with a crisp accent border + soft fill.
 */
export const TopCaption: React.FC<TopCaptionProps> = ({
  text,
  startSec,
  endSec,
  mode,
  accent,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const palette = PALETTES[mode];
  const acc = ACCENTS[accent];

  const words = text.split(" ").filter(Boolean);
  const currentSec = frame / fps;
  const duration = Math.max(0.25, endSec - startSec);
  const progress = Math.min(0.999, Math.max(0, (currentSec - startSec) / duration));
  const activeIdx = Math.min(words.length - 1, Math.floor(progress * words.length));

  const beatLocalFrame = Math.max(0, frame - Math.floor(startSec * fps));
  const enter = spring({ frame: beatLocalFrame, fps, config: SPRINGS.snappy });

  return (
    <div
      style={{
        position: "absolute",
        top: 86,
        left: 64,
        right: 64,
        height: 162,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `translateY(${(1 - enter) * 14}px)`,
        opacity: Math.min(1, enter * 1.4),
        zIndex: 20,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          columnGap: 12,
          rowGap: 8,
          maxWidth: 940,
          fontFamily: FONTS.sans,
          fontSize: 44,
          fontWeight: 700,
          lineHeight: 1.28,
          letterSpacing: "-0.02em",
          textAlign: "center",
        }}
      >
        {words.map((word, idx) => {
          const isActive = idx === activeIdx;
          const isPast = idx < activeIdx;
          const color = isActive
            ? palette.ink
            : isPast
              ? mode === "light"
                ? "#374151"
                : "#CBD5E1"
              : mode === "light"
                ? "#9CA3AF"
                : "#52525B";

          return (
            <span
              key={`${idx}-${word}`}
              style={{
                display: "inline-block",
                padding: isActive ? "3px 12px" : "3px 4px",
                borderRadius: 10,
                color,
                backgroundColor: isActive
                  ? mode === "light"
                    ? acc.lightBg
                    : acc.darkBg
                  : "transparent",
                border: isActive
                  ? `2.5px solid ${acc.solid}`
                  : "2.5px solid transparent",
                transform: isActive ? "scale(1.04)" : "scale(1)",
                transition: "none",
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
