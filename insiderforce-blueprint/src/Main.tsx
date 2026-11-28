import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, FONTS } from "./theme";
import { BEATS } from "./data/beats";
import { KineticCaption } from "./components/KineticCaption";
import { AIHeroVisual } from "./components/AIHeroVisual";
import { RealShotCard } from "./components/RealShotCard";
import {
  BigCounterWithShot,
  CrossChecklist,
  EditorialCTA,
  EnvVaultFix,
  Limit50MBCard,
  NodeFlowDiagram,
  StackedAlerts,
} from "./components/MotionDiagrams";

export const InsiderForceMain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentSec = frame / fps;

  const activeBeat =
    BEATS.find((b) => currentSec >= b.startSec && currentSec < b.endSec) ||
    BEATS[BEATS.length - 1];

  const localFrame = Math.max(0, frame - Math.floor(activeBeat.startSec * fps));

  const renderHero = () => {
    switch (activeBeat.scene) {
      case "hook_laser":
        return <AIHeroVisual fileName="lock_laser.jpg" localFrame={localFrame} size={680} />;
      case "shield_docs":
        return (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
            <AIHeroVisual fileName="shield.jpg" localFrame={localFrame} size={420} />
            <RealShotCard
              shotFile="docs-push.png"
              urlLabel="docs.github.com/en/code-security"
              localFrame={localFrame}
              width={840}
              height={320}
              badgeText="BUILT-IN"
            />
          </div>
        );
      case "node_flow":
        return <NodeFlowDiagram localFrame={localFrame} />;
      case "stacked_alerts":
        return <StackedAlerts localFrame={localFrame} />;
      case "scan_lens":
        return (
          <RealShotCard
            shotFile="docs-before.png"
            urlLabel="docs.github.com/en/code-security/push-protection"
            localFrame={localFrame}
            width={880}
            height={560}
            withMagnifier={true}
            badgeText="PUSH BLOCKED"
            badgeColor={COLORS.crimson}
          />
        );
      case "counter_532":
        return <BigCounterWithShot localFrame={localFrame} />;
      case "cross_checklist":
        return <CrossChecklist localFrame={localFrame} />;
      case "limit_50mb":
        return <Limit50MBCard localFrame={localFrame} />;
      case "env_vault":
        return <EnvVaultFix localFrame={localFrame} />;
      case "cta_guide":
      default:
        return <EditorialCTA localFrame={localFrame} />;
    }
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.canvas,
        overflow: "hidden",
      }}
    >
      {/* Fonts */}
      <style>
        {`
          @font-face {
            font-family: 'Inter';
            src: url('${staticFile("fonts/Inter-Bold.ttf")}') format('truetype');
            font-weight: 400 900;
            font-style: normal;
          }
          @font-face {
            font-family: 'Space Mono';
            src: url('${staticFile("fonts/SpaceMono-Bold.ttf")}') format('truetype');
            font-weight: 400 900;
            font-style: normal;
          }
        `}
      </style>

      {/* Architectural Studio Dot Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: "radial-gradient(rgba(13, 13, 13, 0.11) 1.5px, transparent 1.5px)",
          backgroundSize: "32px 32px",
          opacity: 0.55,
          pointerEvents: "none",
        }}
      />

      {/* Subtle Top-to-Bottom Studio Vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 34%, transparent 45%, rgba(0,0,0,0.05) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Upper Hero Stage (Pure Motion Graphics + AI 3D + Real Screenshots — ZERO 2D Avatar) */}
      <div
        style={{
          position: "absolute",
          top: 140,
          left: 60,
          right: 60,
          height: 920,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 10,
        }}
      >
        {renderHero()}
      </div>

      {/* Editorial Kinetic Typography + Inverted Highlight Pill */}
      <KineticCaption
        leadText={activeBeat.leadText}
        pillText={activeBeat.pillText}
        pillAccent={activeBeat.pillAccent}
        startSec={activeBeat.startSec}
        endSec={activeBeat.endSec}
      />

      {/* Clean Bottom Brand Anchor + Source Micro-Citation (InsiderForce Style) */}
      <div
        style={{
          position: "absolute",
          bottom: 130,
          left: 64,
          right: 64,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 8,
          zIndex: 20,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.sans,
            fontSize: 30,
            fontWeight: 700,
            color: "rgba(13, 13, 13, 0.24)",
            letterSpacing: "0.02em",
          }}
        >
          gkhackter.in
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 18,
            color: COLORS.inkMuted,
          }}
        >
          {activeBeat.sourceLabel}
        </div>
      </div>
    </AbsoluteFill>
  );
};
