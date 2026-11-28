import React from "react";
import { Img, interpolate, spring, staticFile, useVideoConfig } from "remotion";
import { COLORS, FONTS, SHADOWS, SPRINGS } from "../theme";

interface RealShotCardProps {
  /** Filename inside public/shots/, e.g. "docs-push.png" */
  shotFile: string;
  urlLabel: string;
  localFrame: number;
  width?: number;
  height?: number;
  withMagnifier?: boolean;
  badgeText?: string;
  badgeColor?: string;
}

/**
 * Floating shadowed browser window showcasing a REAL GitHub/Docs screenshot
 * with smooth Ken Burns zoom and an optional InsiderForce-style scanning magnifying glass.
 */
export const RealShotCard: React.FC<RealShotCardProps> = ({
  shotFile,
  urlLabel,
  localFrame,
  width = 880,
  height = 540,
  withMagnifier = false,
  badgeText,
  badgeColor = COLORS.emerald,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });
  const zoom = interpolate(localFrame, [0, 120], [1.02, 1.12], {
    extrapolateRight: "clamp",
  });

  // Animated magnifying glass sweep
  const lensX = interpolate(localFrame, [8, 72], [180, 620], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lensY = interpolate(localFrame, [8, 40, 72], [290, 210, 320], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        borderRadius: 26,
        backgroundColor: COLORS.surface,
        border: `2px solid ${COLORS.border}`,
        boxShadow: SHADOWS.card,
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        transform: `scale(${interpolate(enter, [0, 1], [0.92, 1])}) translateY(${(1 - enter) * 24}px)`,
        opacity: enter,
      }}
    >
      {/* Minimal Browser Top Chrome */}
      <div
        style={{
          height: 52,
          backgroundColor: "#FAFAFB",
          borderBottom: `1.5px solid ${COLORS.border}`,
          display: "flex",
          alignItems: "center",
          padding: "0 20px",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", gap: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#FF5F56" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#FFBD2E" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#27C93F" }} />
        </div>
        <div
          style={{
            flex: 1,
            fontFamily: FONTS.mono,
            fontSize: 17,
            color: COLORS.inkMuted,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          🔒 {urlLabel}
        </div>
        {badgeText && (
          <div
            style={{
              backgroundColor: badgeColor,
              color: "#FFFFFF",
              fontFamily: FONTS.mono,
              fontSize: 15,
              fontWeight: 700,
              padding: "5px 14px",
              borderRadius: 999,
            }}
          >
            {badgeText}
          </div>
        )}
      </div>

      {/* Real Screenshot Body */}
      <div style={{ flex: 1, overflow: "hidden", position: "relative", backgroundColor: "#0D1117" }}>
        <Img
          src={staticFile(`shots/${shotFile}`)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "top center",
            transform: `scale(${zoom})`,
          }}
        />
      </div>

      {/* Optional Scanning Magnifying Glass (InsiderForce VibeSec Style) */}
      {withMagnifier && (
        <div
          style={{
            position: "absolute",
            left: lensX,
            top: lensY,
            transform: "translate(-50%, -50%)",
            pointerEvents: "none",
          }}
        >
          <svg width="210" height="210" viewBox="0 0 210 210">
            <defs>
              <filter id="lensShadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="10" stdDeviation="10" floodColor="#000" floodOpacity="0.35" />
              </filter>
            </defs>
            <g filter="url(#lensShadow)">
              <circle cx="88" cy="88" r="64" fill="rgba(239,68,68,0.16)" stroke="#111111" strokeWidth="11" />
              <circle cx="88" cy="88" r="56" fill="none" stroke="#EF4444" strokeWidth="3" strokeDasharray="8 6" />
              <line x1="136" y1="136" x2="188" y2="188" stroke="#111111" strokeWidth="16" strokeLinecap="round" />
              {/* Warning triangle inside lens */}
              <path d="M88 56 L118 110 L58 110 Z" fill="#FACC15" stroke="#111111" strokeWidth="4" strokeLinejoin="round" />
              <text x="88" y="102" textAnchor="middle" fontSize="34" fontWeight="900" fill="#111111">!</text>
            </g>
          </svg>
        </div>
      )}
    </div>
  );
};
