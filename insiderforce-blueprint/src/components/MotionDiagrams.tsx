import React from "react";
import { interpolate, spring, useVideoConfig } from "remotion";
import { COLORS, FONTS, SHADOWS, SPRINGS } from "../theme";
import { RealShotCard } from "./RealShotCard";
import { AIHeroVisual } from "./AIHeroVisual";

/**
 * Beat 3: Tactile 3D Node-Connector Diagram (YOUR CODE → PUSH PROTECTION → PUBLIC REPO)
 */
export const NodeFlowDiagram: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const { fps } = useVideoConfig();
  const s1 = spring({ frame: localFrame, fps, config: SPRINGS.snappy });
  const s2 = spring({ frame: Math.max(0, localFrame - 10), fps, config: SPRINGS.pop });
  const s3 = spring({ frame: Math.max(0, localFrame - 20), fps, config: SPRINGS.snappy });

  return (
    <div style={{ width: 880, display: "flex", flexDirection: "column", alignItems: "center", gap: 36 }}>
      {/* Top Node */}
      <div
        style={{
          padding: "22px 42px",
          borderRadius: 22,
          backgroundColor: COLORS.surface,
          border: `2px solid ${COLORS.border}`,
          boxShadow: SHADOWS.tile,
          transform: `scale(${s1})`,
          fontFamily: FONTS.mono,
          fontSize: 28,
          fontWeight: 700,
          color: COLORS.ink,
        }}
      >
        💻 git push origin main
      </div>

      {/* Connector Line 1 */}
      <div style={{ width: 3, height: 54, backgroundColor: COLORS.ink }} />

      {/* Center Shield Gate Node */}
      <div
        style={{
          padding: "28px 46px",
          borderRadius: 26,
          backgroundColor: COLORS.darkCard,
          border: `3px solid ${COLORS.emerald}`,
          boxShadow: "0 24px 55px rgba(16,185,129,0.28)",
          transform: `scale(${s2})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
        }}
      >
        <span style={{ fontFamily: FONTS.mono, fontSize: 20, color: COLORS.emerald, fontWeight: 700 }}>
          🛡️ GITHUB PUSH PROTECTION
        </span>
        <span style={{ fontFamily: FONTS.sans, fontSize: 38, color: "#FFFFFF", fontWeight: 800 }}>
          SECRET DETECTED → BLOCKED
        </span>
      </div>

      {/* Connector Line 2 (Blocked) */}
      <div
        style={{
          width: 3,
          height: 54,
          borderLeft: `3px dashed ${COLORS.crimson}`,
        }}
      />

      {/* Bottom Node (Safe Public Repo) */}
      <div
        style={{
          padding: "20px 38px",
          borderRadius: 22,
          backgroundColor: COLORS.surface,
          border: `2px solid ${COLORS.emerald}`,
          boxShadow: SHADOWS.tile,
          transform: `scale(${s3})`,
          fontFamily: FONTS.sans,
          fontSize: 28,
          fontWeight: 700,
          color: COLORS.emerald,
        }}
      >
        ✓ Public Repo Stays Clean
      </div>
    </div>
  );
};

/**
 * Beat 4: Cascading Stacked Notification Cards (InsiderForce "Credits Exhausted" style)
 */
export const StackedAlerts: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const { fps } = useVideoConfig();
  const cards = [
    { step: "STEP 1", title: "Secret committed to main", sub: "API key pushed publicly", color: COLORS.amber, delay: 0 },
    { step: "STEP 2", title: "Bots scrape key in seconds", sub: "Unauthorized usage begins", color: COLORS.crimson, delay: 12 },
    { step: "STEP 3", title: "Email alert arrives", sub: "Cleanup only — damage already done", color: "#991B1B", delay: 24 },
  ];

  return (
    <div style={{ width: 840, display: "flex", flexDirection: "column", gap: 22, alignItems: "center" }}>
      {cards.map((c, idx) => {
        const sp = spring({ frame: Math.max(0, localFrame - c.delay), fps, config: SPRINGS.snappy });
        return (
          <div
            key={c.step}
            style={{
              width: 780 + idx * 20,
              backgroundColor: COLORS.surface,
              border: `2px solid ${COLORS.border}`,
              borderLeft: `8px solid ${c.color}`,
              borderRadius: 20,
              padding: "26px 32px",
              boxShadow: SHADOWS.tile,
              transform: `translateY(${(1 - sp) * 32}px) scale(${interpolate(sp, [0, 1], [0.94, 1])})`,
              opacity: sp,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <div style={{ fontFamily: FONTS.mono, fontSize: 17, color: c.color, fontWeight: 700 }}>{c.step}</div>
              <div style={{ fontFamily: FONTS.sans, fontSize: 32, fontWeight: 800, color: COLORS.ink }}>{c.title}</div>
              <div style={{ fontFamily: FONTS.sans, fontSize: 22, color: COLORS.inkMuted }}>{c.sub}</div>
            </div>
            <div style={{ fontSize: 36, color: c.color, fontWeight: 900 }}>✕</div>
          </div>
        );
      })}
    </div>
  );
};

/**
 * Beat 6: Animated 532 / 465 Counter + Floating Real Repo Screenshot
 */
export const BigCounterWithShot: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const count = Math.floor(
    interpolate(localFrame, [0, 32], [0, 532], { extrapolateRight: "clamp" })
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
      <RealShotCard
        shotFile="awesome-532.png"
        urlLabel="github.com/advanced-security/awesome-secret-scanning"
        localFrame={localFrame}
        width={860}
        height={400}
        badgeText="VERIFIED"
      />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 32,
          backgroundColor: COLORS.surface,
          border: `2px solid ${COLORS.border}`,
          borderRadius: 24,
          padding: "22px 44px",
          boxShadow: SHADOWS.tile,
        }}
      >
        <div style={{ fontFamily: FONTS.sans, fontSize: 84, fontWeight: 900, color: COLORS.ink, lineHeight: 1 }}>
          {count}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <span style={{ fontFamily: FONTS.sans, fontSize: 28, fontWeight: 800, color: COLORS.ink }}>
            Partner Patterns
          </span>
          <span style={{ fontFamily: FONTS.mono, fontSize: 22, fontWeight: 700, color: COLORS.emerald }}>
            ● 465 PUSH-PROTECTED
          </span>
        </div>
      </div>
    </div>
  );
};

/**
 * Beat 7: InsiderForce Vertical Connected `✕` Checklist
 */
export const CrossChecklist: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const { fps } = useVideoConfig();
  const items = [
    "Old or unsupported token formats",
    "Generic passwords & custom strings",
    "Not every secret pattern is covered",
  ];

  return (
    <div
      style={{
        width: 820,
        backgroundColor: COLORS.surface,
        border: `2px solid ${COLORS.border}`,
        borderRadius: 28,
        padding: "46px 48px",
        boxShadow: SHADOWS.card,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        gap: 34,
      }}
    >
      {/* Vertical connector line behind X circles */}
      <div
        style={{
          position: "absolute",
          left: 75,
          top: 76,
          bottom: 76,
          width: 3,
          backgroundColor: COLORS.ink,
        }}
      />

      {items.map((text, idx) => {
        const sp = spring({ frame: Math.max(0, localFrame - idx * 8), fps, config: SPRINGS.snappy });
        return (
          <div
            key={text}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 28,
              opacity: sp,
              transform: `translateX(${(1 - sp) * 24}px)`,
              zIndex: 2,
            }}
          >
            <div
              style={{
                width: 56,
                height: 56,
                borderRadius: "50%",
                backgroundColor: COLORS.ink,
                color: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: FONTS.sans,
                fontSize: 28,
                fontWeight: 900,
                flexShrink: 0,
              }}
            >
              ✕
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 34, fontWeight: 700, color: COLORS.ink }}>
              {text}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/**
 * Beat 8: 50 MB Limit Dark Contrast Card + Real Docs Screenshot
 */
export const Limit50MBCard: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
      <RealShotCard
        shotFile="docs-50mb.png"
        urlLabel="docs.github.com/en/code-security"
        localFrame={localFrame}
        width={860}
        height={380}
        badgeText="LIMIT"
        badgeColor={COLORS.crimson}
      />
      <div
        style={{
          width: 860,
          backgroundColor: COLORS.darkCard,
          border: `3px solid ${COLORS.crimson}`,
          borderRadius: 24,
          padding: "28px 40px",
          boxShadow: SHADOWS.card,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#FCA5A5", fontWeight: 700 }}>
            PUBLIC REPO PUSH LIMIT
          </div>
          <div style={{ fontFamily: FONTS.sans, fontSize: 56, fontWeight: 900, color: "#FFFFFF" }}>
            &gt; 50 MB
          </div>
        </div>
        <div
          style={{
            padding: "14px 26px",
            borderRadius: 14,
            backgroundColor: COLORS.crimson,
            color: "#FFFFFF",
            fontFamily: FONTS.mono,
            fontSize: 24,
            fontWeight: 800,
          }}
        >
          SKIPPED · NO SCAN
        </div>
      </div>
    </div>
  );
};

/**
 * Beat 9: AI 3D Smoked-Glass Vault + Safe `.env` Code Card
 */
export const EnvVaultFix: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      <AIHeroVisual fileName="env_vault.jpg" localFrame={localFrame} size={460} />
      <div
        style={{
          width: 820,
          backgroundColor: COLORS.darkCard,
          borderRadius: 22,
          padding: "24px 34px",
          boxShadow: SHADOWS.card,
          fontFamily: FONTS.mono,
          fontSize: 25,
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        <div style={{ color: "#F87171", textDecoration: "line-through", opacity: 0.7 }}>
          ✕ const key = "sk_live_99482...";
        </div>
        <div style={{ color: "#34D399", fontWeight: 700 }}>
          ✓ const key = process.env.API_KEY;
        </div>
      </div>
    </div>
  );
};

/**
 * Beat 10: Editorial CTA with Floating Docs Card + Brand Emblem
 */
export const EditorialCTA: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 28 }}>
      <RealShotCard
        shotFile="docs-scanning.png"
        urlLabel="docs.github.com/en/code-security/secret-scanning"
        localFrame={localFrame}
        width={840}
        height={440}
        badgeText="OFFICIAL DOCS"
      />
      <div
        style={{
          padding: "14px 32px",
          borderRadius: 999,
          backgroundColor: COLORS.surface,
          border: `2px solid ${COLORS.border}`,
          boxShadow: SHADOWS.tile,
          fontFamily: FONTS.mono,
          fontSize: 24,
          fontWeight: 700,
          color: COLORS.ink,
        }}
      >
        GK HACKTER · @gkhackter
      </div>
    </div>
  );
};
