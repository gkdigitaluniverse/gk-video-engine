import React from "react";
import { ACCENTS, FONTS, PALETTES, ThemeMode } from "../theme";
import { CHANNEL_HANDLE, CHAPTERS } from "../data/videoData";

interface ChapterStepperProps {
  activeChapter: number;
  mode: ThemeMode;
  sourceCitation: string;
}

/**
 * Persistent top 5-node Chapter Stepper + @gkhackter handle + muted micro-citation.
 * Creates an open loop so viewers stay to see the next dot illuminate.
 */
export const ChapterStepper: React.FC<ChapterStepperProps> = ({
  activeChapter,
  mode,
  sourceCitation,
}) => {
  const palette = PALETTES[mode];
  const activeAccent = ACCENTS[CHAPTERS[activeChapter]?.accent || "orange"].solid;

  return (
    <div
      style={{
        position: "absolute",
        top: 258,
        left: 64,
        right: 64,
        display: "flex",
        flexDirection: "column",
        gap: 10,
        zIndex: 20,
      }}
    >
      {/* Handle row */}
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          fontFamily: FONTS.sans,
          fontSize: 20,
          fontWeight: 600,
          color: palette.inkMuted,
          letterSpacing: "0.01em",
        }}
      >
        {CHANNEL_HANDLE}
      </div>

      {/* Stepper track */}
      <div
        style={{
          position: "relative",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          padding: "0 8px",
        }}
      >
        {/* Background rail */}
        <div
          style={{
            position: "absolute",
            top: 8,
            left: 28,
            right: 28,
            height: 2,
            backgroundColor: palette.cardBorder,
          }}
        />
        {/* Active fill rail */}
        <div
          style={{
            position: "absolute",
            top: 8,
            left: 28,
            width: `${(activeChapter / (CHAPTERS.length - 1)) * 94}%`,
            height: 2.5,
            backgroundColor: activeAccent,
          }}
        />

        {CHAPTERS.map((ch, idx) => {
          const isCurrent = idx === activeChapter;
          const isDone = idx < activeChapter;
          const dotColor = isCurrent || isDone ? ACCENTS[ch.accent].solid : palette.cardBorder;

          return (
            <div
              key={ch.id}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 8,
                zIndex: 2,
                width: 155,
              }}
            >
              <div
                style={{
                  width: isCurrent ? 18 : 14,
                  height: isCurrent ? 18 : 14,
                  marginTop: isCurrent ? 0 : 2,
                  borderRadius: "50%",
                  backgroundColor: dotColor,
                  boxShadow: isCurrent ? `0 0 14px ${dotColor}` : "none",
                  border: `2.5px solid ${palette.bg}`,
                }}
              />
              <span
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 16,
                  fontWeight: isCurrent ? 700 : 500,
                  letterSpacing: "0.08em",
                  color: isCurrent ? ACCENTS[ch.accent].solid : palette.inkFaint,
                }}
              >
                {ch.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Source micro-citation */}
      <div
        style={{
          textAlign: "center",
          fontFamily: FONTS.mono,
          fontSize: 17,
          color: palette.inkFaint,
          marginTop: 2,
        }}
      >
        {sourceCitation}
      </div>
    </div>
  );
};
