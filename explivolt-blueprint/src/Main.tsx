import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ACCENTS, PALETTES } from "./theme";
import { BEATS } from "./data/videoData";
import { TopCaption } from "./components/TopCaption";
import { ChapterStepper } from "./components/ChapterStepper";
import { PresenterAvatar } from "./components/PresenterAvatar";
import { LiveTestScene, MacBookHookScene, NoSetupScene } from "./components/DeviceMockups";
import {
  CatchCompatMatrix,
  DeployAndCTAScene,
  DotMatrixCounter,
  SpeedMeterBar,
} from "./components/DataVisuals";

export const ExplivoltMain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentSec = frame / fps;

  // Find active beat
  const activeBeat =
    BEATS.find((b) => currentSec >= b.startSec && currentSec < b.endSec) ||
    BEATS[BEATS.length - 1];

  const palette = PALETTES[activeBeat.mode];
  const accentColor = ACCENTS[activeBeat.accent].solid;
  const localFrame = Math.max(0, frame - Math.floor(activeBeat.startSec * fps));

  const renderHeroStage = () => {
    switch (activeBeat.id) {
      case "B1":
        return <MacBookHookScene localFrame={localFrame} isB2={false} />;
      case "B2":
        return <MacBookHookScene localFrame={localFrame} isB2={true} />;
      case "B3":
        return <NoSetupScene localFrame={localFrame} isCompare={false} />;
      case "B4":
        return <NoSetupScene localFrame={localFrame} isCompare={true} />;
      case "B5":
        return <LiveTestScene localFrame={localFrame} phase="split" />;
      case "B6":
        return <LiveTestScene localFrame={localFrame} phase="edit" />;
      case "B7":
        return <LiveTestScene localFrame={localFrame} phase="http" />;
      case "B8":
        return <DotMatrixCounter localFrame={localFrame} showDocsOnly={true} />;
      case "B9":
        return <DotMatrixCounter localFrame={localFrame} showDocsOnly={false} />;
      case "B10":
        return <SpeedMeterBar localFrame={localFrame} />;
      case "B11":
        return <CatchCompatMatrix localFrame={localFrame} showMatrix={false} />;
      case "B12":
        return <CatchCompatMatrix localFrame={localFrame} showMatrix={true} />;
      case "B13":
        return <DeployAndCTAScene localFrame={localFrame} isCTA={false} />;
      case "B14":
      default:
        return <DeployAndCTAScene localFrame={localFrame} isCTA={true} />;
    }
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: palette.bg,
        overflow: "hidden",
      }}
    >
      {/* Font loading */}
      <style>
        {`
          @font-face {
            font-family: 'Inter';
            src: url('${staticFile("fonts/Inter-Bold.ttf")}') format('truetype');
            font-weight: 400 900;
            font-style: normal;
          }
          @font-face {
            font-family: 'JetBrains Mono';
            src: url('${staticFile("fonts/SpaceMono-Bold.ttf")}') format('truetype');
            font-weight: 400 900;
            font-style: normal;
          }
        `}
      </style>

      {/* Subtle Ambient Accent Glow */}
      <div
        style={{
          position: "absolute",
          top: 420,
          left: "50%",
          transform: "translateX(-50%)",
          width: 960,
          height: 960,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${accentColor}${
            activeBeat.mode === "dark" ? "26" : "18"
          } 0%, transparent 68%)`,
          pointerEvents: "none",
        }}
      />

      {/* 1. Top-Center Word-Boxed Caption */}
      <TopCaption
        text={activeBeat.caption}
        startSec={activeBeat.startSec}
        endSec={activeBeat.endSec}
        mode={activeBeat.mode}
        accent={activeBeat.accent}
      />

      {/* 2. Persistent 5-Chapter Stepper + Source Citation */}
      <ChapterStepper
        activeChapter={activeBeat.chapterIndex}
        mode={activeBeat.mode}
        sourceCitation={activeBeat.sourceCitation}
      />

      {/* 3. Hero Visual Stage (Centered cleanly between stepper and avatar) */}
      <div
        style={{
          position: "absolute",
          top: 410,
          left: 60,
          right: 60,
          height: 930,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 10,
        }}
      >
        {renderHeroStage()}
      </div>

      {/* 4. Bottom 2D Illustrated Presenter Avatar */}
      <PresenterAvatar pose={activeBeat.pose} speaking={true} />
    </AbsoluteFill>
  );
};
