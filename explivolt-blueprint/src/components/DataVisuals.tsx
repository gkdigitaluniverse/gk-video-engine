import React from "react";
import { interpolate, spring, useVideoConfig } from "remotion";
import { ACCENTS, FONTS, PALETTES, SPRINGS } from "../theme";

/**
 * 1) Explivolt-style Dot-Matrix Quota Grid (B8-B9): 100,000 Requests / Day
 */
export const DotMatrixCounter: React.FC<{ localFrame: number; showDocsOnly: boolean }> = ({
  localFrame,
  showDocsOnly,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });

  if (showDocsOnly) {
    return (
      <div
        style={{
          width: 840,
          backgroundColor: PALETTES.dark.card,
          border: "2.5px solid #8B5CF6",
          borderRadius: 24,
          padding: 40,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 18,
          transform: `scale(${interpolate(enter, [0, 1], [0.9, 1])})`,
          boxShadow: "0 0 50px rgba(139,92,246,0.25)",
        }}
      >
        <div
          style={{
            padding: "10px 22px",
            borderRadius: 999,
            backgroundColor: "rgba(34,197,94,0.16)",
            border: "2px solid #22C55E",
            color: "#4ADE80",
            fontFamily: FONTS.mono,
            fontSize: 22,
            fontWeight: 700,
          }}
        >
          ✓ VERIFIED ON OFFICIAL DOCS
        </div>
        <div style={{ fontFamily: FONTS.sans, fontSize: 40, fontWeight: 800, color: "#FFFFFF" }}>
          Cloudflare Workers Limits
        </div>
        <div style={{ fontFamily: FONTS.mono, fontSize: 20, color: "#94A3B8" }}>
          developers.cloudflare.com/workers/platform/limits
        </div>
      </div>
    );
  }

  const count = Math.floor(
    interpolate(localFrame, [0, 38], [0, 100000], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const totalCells = 96;
  const filledCells = Math.floor(
    interpolate(localFrame, [0, 42], [6, totalCells], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  return (
    <div
      style={{
        width: 880,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 24,
        opacity: enter,
      }}
    >
      <div style={{ fontFamily: FONTS.mono, fontSize: 22, color: "#A78BFA", letterSpacing: "0.12em" }}>
        WORKERS FREE PLAN · DAILY QUOTA
      </div>
      <div
        style={{
          fontFamily: FONTS.sans,
          fontSize: 96,
          fontWeight: 900,
          color: "#FFFFFF",
          letterSpacing: "-0.03em",
          lineHeight: 1,
        }}
      >
        {count.toLocaleString("en-IN")}
      </div>
      <div style={{ fontFamily: FONTS.mono, fontSize: 26, color: "#38BDF8", fontWeight: 700 }}>
        REQUESTS / DAY
      </div>

      {/* Glowing Dot Matrix Grid (Explivolt 1M Tokens Style) */}
      <div
        style={{
          width: 840,
          padding: 24,
          borderRadius: 22,
          backgroundColor: "#111116",
          border: "2px solid #27273A",
          display: "grid",
          gridTemplateColumns: "repeat(16, 1fr)",
          gap: 10,
        }}
      >
        {Array.from({ length: totalCells }).map((_, idx) => {
          const active = idx < filledCells;
          const colors = ["#8B5CF6", "#38BDF8", "#34D399", "#A78BFA"];
          const cellColor = colors[(idx * 7) % colors.length];
          return (
            <div
              key={idx}
              style={{
                height: 30,
                borderRadius: 6,
                backgroundColor: active ? cellColor : "#1E1E28",
                opacity: active ? 0.92 : 0.45,
                boxShadow: active ? `0 0 10px ${cellColor}66` : "none",
              }}
            />
          );
        })}
      </div>
    </div>
  );
};

/**
 * 2) 10ms CPU Gauge Card (B10)
 */
export const SpeedMeterBar: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });
  const barPct = interpolate(localFrame, [5, 36], [8, 86], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: 860,
        backgroundColor: PALETTES.dark.card,
        border: "2.5px solid #F59E0B",
        borderRadius: 26,
        padding: 40,
        display: "flex",
        flexDirection: "column",
        gap: 24,
        transform: `scale(${interpolate(enter, [0, 1], [0.92, 1])})`,
        boxShadow: "0 0 50px rgba(245,158,11,0.2)",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <span style={{ fontFamily: FONTS.mono, fontSize: 22, color: "#FBBF24", fontWeight: 700 }}>
          CPU BUDGET / REQUEST
        </span>
        <span style={{ fontFamily: FONTS.mono, fontSize: 20, color: "#94A3B8" }}>FREE TIER</span>
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: 18 }}>
        <span style={{ fontFamily: FONTS.sans, fontSize: 108, fontWeight: 900, color: "#FFFFFF", lineHeight: 1 }}>
          10 ms
        </span>
        <span style={{ fontFamily: FONTS.sans, fontSize: 32, fontWeight: 700, color: "#FBBF24" }}>
          CPU Time
        </span>
      </div>

      {/* Animated Bar */}
      <div
        style={{
          width: "100%",
          height: 36,
          borderRadius: 999,
          backgroundColor: "#27272F",
          overflow: "hidden",
          padding: 4,
        }}
      >
        <div
          style={{
            width: `${barPct}%`,
            height: "100%",
            borderRadius: 999,
            background: "linear-gradient(90deg, #F59E0B 0%, #F97316 100%)",
          }}
        />
      </div>

      <div style={{ fontFamily: FONTS.sans, fontSize: 24, color: "#CBD5E1" }}>
        Fast enough for JSON APIs, Auth & Webhooks — built for lightweight edge logic.
      </div>
    </div>
  );
};

/**
 * 3) Catch / Desktop-Only Matrix (B11-B12)
 */
export const CatchCompatMatrix: React.FC<{ localFrame: number; showMatrix: boolean }> = ({
  localFrame,
  showMatrix,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.bouncy });

  if (!showMatrix) {
    return (
      <div
        style={{
          padding: "36px 56px",
          borderRadius: 28,
          backgroundColor: "#FEF2F2",
          border: "3.5px solid #EF4444",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          transform: `scale(${interpolate(enter, [0, 1], [0.82, 1])})`,
          boxShadow: "0 20px 50px rgba(239,68,68,0.18)",
        }}
      >
        <span style={{ fontSize: 64 }}>⚠️</span>
        <span style={{ fontFamily: FONTS.sans, fontSize: 56, fontWeight: 900, color: "#DC2626" }}>
          THE CATCH
        </span>
        <span style={{ fontFamily: FONTS.mono, fontSize: 22, color: "#991B1B" }}>
          2 REAL LIMITATIONS TO KNOW
        </span>
      </div>
    );
  }

  return (
    <div
      style={{
        width: 880,
        display: "flex",
        flexDirection: "column",
        gap: 20,
        opacity: enter,
      }}
    >
      <div style={{ display: "flex", gap: 20 }}>
        {[
          { name: "Chrome Desktop", ok: true, sub: "Supported" },
          { name: "Firefox Desktop", ok: true, sub: "Supported" },
        ].map((item) => (
          <div
            key={item.name}
            style={{
              flex: 1,
              backgroundColor: "#FFFFFF",
              border: "3px solid #22C55E",
              borderRadius: 22,
              padding: 30,
              display: "flex",
              flexDirection: "column",
              gap: 10,
              boxShadow: PALETTES.light.shadow,
            }}
          >
            <span style={{ fontFamily: FONTS.mono, fontSize: 22, fontWeight: 800, color: "#16A34A" }}>
              ✓ WORKS
            </span>
            <span style={{ fontFamily: FONTS.sans, fontSize: 32, fontWeight: 800, color: "#111827" }}>
              {item.name}
            </span>
            <span style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#6B7280" }}>{item.sub}</span>
          </div>
        ))}
      </div>

      {/* Mobile Blocked */}
      <div
        style={{
          backgroundColor: "#FEF2F2",
          border: "3px solid #EF4444",
          borderRadius: 22,
          padding: "26px 32px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <div style={{ fontFamily: FONTS.sans, fontSize: 32, fontWeight: 800, color: "#991B1B" }}>
            Mobile Browsers
          </div>
          <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#B91C1C" }}>
            Playground requires Desktop Chrome / Firefox
          </div>
        </div>
        <div
          style={{
            padding: "10px 22px",
            borderRadius: 12,
            backgroundColor: "#EF4444",
            color: "#FFFFFF",
            fontFamily: FONTS.mono,
            fontSize: 22,
            fontWeight: 800,
          }}
        >
          ✕ NOT SUPPORTED
        </div>
      </div>
    </div>
  );
};

/**
 * 4) Deploy Requirement (B13) + Spotlight End Card (B14)
 */
export const DeployAndCTAScene: React.FC<{ localFrame: number; isCTA: boolean }> = ({
  localFrame,
  isCTA,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });

  if (!isCTA) {
    return (
      <div
        style={{
          width: 860,
          display: "flex",
          flexDirection: "column",
          gap: 20,
          transform: `translateY(${(1 - enter) * 24}px)`,
          opacity: enter,
        }}
      >
        <div
          style={{
            backgroundColor: "#0F1D17",
            border: "2.5px solid #22C55E",
            borderRadius: 22,
            padding: 30,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#4ADE80" }}>STEP 1 · TESTING</div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 34, fontWeight: 800, color: "#FFFFFF" }}>
              Test in Playground
            </div>
          </div>
          <div style={{ fontFamily: FONTS.mono, fontSize: 22, color: "#4ADE80", fontWeight: 800 }}>
            ✓ NO ACCOUNT
          </div>
        </div>

        <div
          style={{
            backgroundColor: "#1C140E",
            border: `2.5px solid ${ACCENTS.orange.solid}`,
            borderRadius: 22,
            padding: 30,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#FDBA74" }}>STEP 2 · PRODUCTION</div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 34, fontWeight: 800, color: "#FFFFFF" }}>
              Deploy Live URL
            </div>
          </div>
          <div style={{ fontFamily: FONTS.mono, fontSize: 22, color: "#F97316", fontWeight: 800 }}>
            🔒 FREE ACCOUNT
          </div>
        </div>
      </div>
    );
  }

  // B14: Explivolt-style Spotlight CTA End Card
  return (
    <div
      style={{
        width: 860,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 28,
        transform: `scale(${interpolate(enter, [0, 1], [0.92, 1])})`,
        opacity: enter,
      }}
    >
      <div
        style={{
          padding: "10px 26px",
          borderRadius: 999,
          backgroundColor: "#18181F",
          border: "2px solid #F97316",
          fontFamily: FONTS.mono,
          fontSize: 24,
          fontWeight: 700,
          color: "#FDBA74",
        }}
      >
        GK HACKTER · @gkhackter
      </div>

      <div
        style={{
          width: "100%",
          padding: "26px 34px",
          borderRadius: 24,
          backgroundColor: "#FFFFFF",
          border: "4px solid #22C55E",
          boxShadow: "0 0 60px rgba(34,197,94,0.35)",
          textAlign: "center",
          fontFamily: FONTS.mono,
          fontSize: 32,
          fontWeight: 800,
          color: "#0F172A",
        }}
      >
        🔒 workers.cloudflare.com/playground
      </div>

      <div
        style={{
          padding: "14px 36px",
          borderRadius: 999,
          backgroundColor: "#22C55E",
          color: "#052E16",
          fontFamily: FONTS.sans,
          fontSize: 30,
          fontWeight: 900,
          transform: `translateY(${Math.sin(localFrame * 0.28) * 6}px)`,
        }}
      >
        Link in Description ↓
      </div>
    </div>
  );
};
