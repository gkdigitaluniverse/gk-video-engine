import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACCENTS, FONTS, PALETTES, SPRINGS, ThemeMode } from "../theme";

/**
 * 1) Hook Scene (B1-B2): MacBook running Cloudflare Workers Playground live in browser
 */
export const MacBookHookScene: React.FC<{ localFrame: number; isB2: boolean }> = ({
  localFrame,
  isB2,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });
  const zoom = isB2 ? 1.05 : 1.0;

  // Animated cursor moving to "Run" button
  const cursorX = interpolate(localFrame, [10, 40], [560, 745], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cursorY = interpolate(localFrame, [10, 40], [310, 118], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const clicked = localFrame > 42;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        transform: `scale(${interpolate(enter, [0, 1], [0.92, zoom])})`,
        opacity: enter,
      }}
    >
      {/* Floating Small Web App badges in B2 */}
      {isB2 && (
        <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
          {["API Route", "Webhook", "Auth Proxy"].map((label, i) => (
            <div
              key={label}
              style={{
                padding: "10px 20px",
                borderRadius: 999,
                backgroundColor: "#FFFFFF",
                border: `2px solid ${ACCENTS.orange.solid}`,
                fontFamily: FONTS.mono,
                fontSize: 20,
                fontWeight: 700,
                color: "#111827",
                boxShadow: "0 10px 25px rgba(249,115,22,0.16)",
                transform: `translateY(${Math.sin((localFrame + i * 12) * 0.14) * 5}px)`,
              }}
            >
              ● {label}
            </div>
          ))}
        </div>
      )}

      {/* MacBook Screen */}
      <div
        style={{
          position: "relative",
          width: 890,
          height: 540,
          backgroundColor: "#0F172A",
          borderRadius: "28px 28px 10px 10px",
          padding: 18,
          boxShadow: "0 30px 70px rgba(17,24,39,0.22)",
          border: "4px solid #1E293B",
        }}
      >
        {/* Inner Browser */}
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#FFFFFF",
            borderRadius: 14,
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* Browser Top Chrome */}
          <div
            style={{
              height: 54,
              backgroundColor: "#F8FAFC",
              borderBottom: "2px solid #E2E8F0",
              display: "flex",
              alignItems: "center",
              padding: "0 20px",
              gap: 12,
            }}
          >
            <div style={{ display: "flex", gap: 8 }}>
              <div style={{ width: 13, height: 13, borderRadius: "50%", backgroundColor: "#EF4444" }} />
              <div style={{ width: 13, height: 13, borderRadius: "50%", backgroundColor: "#F59E0B" }} />
              <div style={{ width: 13, height: 13, borderRadius: "50%", backgroundColor: "#22C55E" }} />
            </div>
            <div
              style={{
                flex: 1,
                backgroundColor: "#FFFFFF",
                border: "1.5px solid #CBD5E1",
                borderRadius: 8,
                padding: "6px 14px",
                fontFamily: FONTS.mono,
                fontSize: 18,
                color: "#334155",
              }}
            >
              🔒 workers.cloudflare.com/playground
            </div>
            <div
              style={{
                backgroundColor: clicked ? "#22C55E" : "#F97316",
                color: "#FFFFFF",
                fontFamily: FONTS.sans,
                fontWeight: 800,
                fontSize: 18,
                padding: "8px 18px",
                borderRadius: 8,
              }}
            >
              {clicked ? "✓ 200 OK" : "▶ Run"}
            </div>
          </div>

          {/* Browser Body: Split Code + Output */}
          <div style={{ flex: 1, display: "flex" }}>
            <div
              style={{
                flex: 1.15,
                backgroundColor: "#111827",
                padding: 24,
                fontFamily: FONTS.mono,
                fontSize: 19,
                lineHeight: 1.65,
                color: "#E2E8F0",
              }}
            >
              <div style={{ color: "#94A3B8", marginBottom: 10 }}>// worker.js — No Server Needed</div>
              <div>
                <span style={{ color: "#C084FC" }}>export default</span> {"{"}
              </div>
              <div style={{ paddingLeft: 18 }}>
                <span style={{ color: "#38BDF8" }}>async fetch</span>(request) {"{"}
              </div>
              <div style={{ paddingLeft: 36 }}>
                <span style={{ color: "#C084FC" }}>return</span> Response.
                <span style={{ color: "#4ADE80" }}>json</span>({"{"}
              </div>
              <div style={{ paddingLeft: 54, color: "#FDBA74" }}>status: "live",</div>
              <div style={{ paddingLeft: 54, color: "#FDBA74" }}>cost: "₹0 / Free"</div>
              <div style={{ paddingLeft: 36 }}>{"});"}</div>
              <div style={{ paddingLeft: 18 }}>{"}"}</div>
              <div>{"};"}</div>
            </div>
            <div
              style={{
                flex: 0.85,
                backgroundColor: "#FFFBF5",
                padding: 24,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                gap: 16,
                borderLeft: "2px solid #E2E8F0",
              }}
            >
              <div
                style={{
                  display: "inline-flex",
                  alignSelf: "flex-start",
                  alignItems: "center",
                  gap: 8,
                  padding: "6px 14px",
                  borderRadius: 999,
                  backgroundColor: "rgba(34,197,94,0.14)",
                  color: "#15803D",
                  fontFamily: FONTS.mono,
                  fontSize: 17,
                  fontWeight: 700,
                }}
              >
                ● LIVE · 4ms
              </div>
              <div
                style={{
                  backgroundColor: "#FFFFFF",
                  border: "2px solid #FDBA74",
                  borderRadius: 14,
                  padding: 18,
                  fontFamily: FONTS.mono,
                  fontSize: 20,
                  color: "#0F172A",
                }}
              >
                {"{\n  \"status\": \"live\",\n  \"cost\": \"₹0 / Free\"\n}"}
              </div>
              <div style={{ fontFamily: FONTS.sans, fontSize: 18, fontWeight: 700, color: "#F97316" }}>
                0 Servers · Instant Edge URL
              </div>
            </div>
          </div>
        </div>

        {/* Animated Cursor */}
        <svg
          width="38"
          height="38"
          viewBox="0 0 24 24"
          style={{
            position: "absolute",
            left: cursorX,
            top: cursorY,
            filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.35))",
          }}
        >
          <path
            d="M4 2 L4 20 L9 15 L14 22 L17 20 L12 13 L19 13 Z"
            fill="#FFFFFF"
            stroke="#0F172A"
            strokeWidth="2"
          />
        </svg>
      </div>

      {/* MacBook Base */}
      <div
        style={{
          width: 960,
          height: 26,
          background: "linear-gradient(180deg, #CBD5E1 0%, #64748B 100%)",
          borderRadius: "4px 4px 18px 18px",
        }}
      />
    </div>
  );
};

/**
 * 2) No-Setup Scene (B3-B4): Dark Mode Zero-Signup Flow + Old Terminal vs Instant Sandbox
 */
export const NoSetupScene: React.FC<{ localFrame: number; isCompare: boolean }> = ({
  localFrame,
  isCompare,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });

  if (!isCompare) {
    return (
      <div
        style={{
          width: 880,
          display: "flex",
          flexDirection: "column",
          gap: 28,
          transform: `translateY(${(1 - enter) * 28}px)`,
          opacity: enter,
        }}
      >
        {/* Top Zero-Signup Pills */}
        <div style={{ display: "flex", justifyContent: "center", gap: 18 }}>
          {["NO ACCOUNT", "NO CREDIT CARD", "NO INSTALL"].map((badge) => (
            <div
              key={badge}
              style={{
                padding: "12px 22px",
                borderRadius: 12,
                backgroundColor: "rgba(59,130,246,0.16)",
                border: "2px solid #3B82F6",
                color: "#93C5FD",
                fontFamily: FONTS.mono,
                fontSize: 20,
                fontWeight: 700,
              }}
            >
              ✓ {badge}
            </div>
          ))}
        </div>

        {/* 3-Node Pipeline Flow */}
        <div
          style={{
            backgroundColor: PALETTES.dark.card,
            border: `2px solid ${PALETTES.dark.cardBorder}`,
            borderRadius: 24,
            padding: 36,
            display: "flex",
            flexDirection: "column",
            gap: 28,
          }}
        >
          <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#60A5FA", letterSpacing: "0.08em" }}>
            INSTANT BROWSER FLOW
          </div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            {[
              { step: "01", title: "Open URL", sub: "workers.cloudflare.com", color: "#3B82F6" },
              { step: "02", title: "Write JS/TS", sub: "In-browser editor", color: "#8B5CF6" },
              { step: "03", title: "Live Preview", sub: "Instant response", color: "#22C55E" },
            ].map((item, idx) => (
              <React.Fragment key={item.step}>
                <div
                  style={{
                    width: 240,
                    padding: 24,
                    borderRadius: 18,
                    backgroundColor: "#0F1014",
                    border: `2px solid ${item.color}`,
                    display: "flex",
                    flexDirection: "column",
                    gap: 8,
                  }}
                >
                  <span style={{ fontFamily: FONTS.mono, fontSize: 18, color: item.color, fontWeight: 700 }}>
                    STEP {item.step}
                  </span>
                  <span style={{ fontFamily: FONTS.sans, fontSize: 28, color: "#F8FAFC", fontWeight: 800 }}>
                    {item.title}
                  </span>
                  <span style={{ fontFamily: FONTS.mono, fontSize: 17, color: "#94A3B8" }}>
                    {item.sub}
                  </span>
                </div>
                {idx < 2 && (
                  <span style={{ fontSize: 34, color: "#64748B", fontWeight: 800 }}>→</span>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // B4: Old Terminal Setup vs New Instant Sandbox
  return (
    <div
      style={{
        width: 880,
        display: "flex",
        flexDirection: "column",
        gap: 24,
        transform: `translateY(${(1 - enter) * 24}px)`,
        opacity: enter,
      }}
    >
      {/* Old Way (Struck Out) */}
      <div
        style={{
          backgroundColor: "#171114",
          border: "2px solid #7F1D1D",
          borderRadius: 22,
          padding: 30,
          opacity: 0.78,
        }}
      >
        <div style={{ fontFamily: FONTS.mono, fontSize: 19, color: "#F87171", marginBottom: 16, fontWeight: 700 }}>
          ✕ OLD WAY (LOCAL SETUP)
        </div>
        {["$ npm create cloudflare@latest", "$ npx wrangler login", "$ npx wrangler deploy  (45s wait...)"].map(
          (cmd) => (
            <div
              key={cmd}
              style={{
                fontFamily: FONTS.mono,
                fontSize: 23,
                color: "#FCA5A5",
                textDecoration: "line-through",
                marginBottom: 10,
              }}
            >
              {cmd}
            </div>
          )
        )}
      </div>

      {/* New Way */}
      <div
        style={{
          backgroundColor: "#0D1914",
          border: "2.5px solid #22C55E",
          borderRadius: 22,
          padding: 32,
          boxShadow: "0 0 40px rgba(34,197,94,0.18)",
        }}
      >
        <div style={{ fontFamily: FONTS.mono, fontSize: 20, color: "#4ADE80", marginBottom: 12, fontWeight: 700 }}>
          ✓ PLAYGROUND WAY (0 SECONDS)
        </div>
        <div style={{ fontFamily: FONTS.sans, fontSize: 36, fontWeight: 800, color: "#FFFFFF" }}>
          Open Tab → Edit → Live Output
        </div>
      </div>
    </div>
  );
};

/**
 * 3) Live Test Scene (B5-B7): Light Mode Split IDE + Code Edit + HTTP Tab Request
 */
export const LiveTestScene: React.FC<{
  localFrame: number;
  phase: "split" | "edit" | "http";
}> = ({ localFrame, phase }) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });

  const typedChars = Math.min(28, Math.floor(localFrame * 0.9));
  const customResp = '{"ok": true, "user": "GK"}'.slice(0, typedChars);

  return (
    <div
      style={{
        width: 900,
        backgroundColor: "#FFFFFF",
        border: "2.5px solid #D6D3CB",
        borderRadius: 26,
        overflow: "hidden",
        boxShadow: PALETTES.light.shadow,
        transform: `scale(${interpolate(enter, [0, 1], [0.95, 1])})`,
        opacity: enter,
      }}
    >
      {/* Top IDE Tabs */}
      <div
        style={{
          height: 62,
          backgroundColor: "#F1EFEA",
          borderBottom: "2px solid #E2DFD7",
          display: "flex",
          alignItems: "center",
          padding: "0 24px",
          gap: 16,
          fontFamily: FONTS.mono,
          fontSize: 20,
          fontWeight: 700,
        }}
      >
        <div
          style={{
            padding: "8px 18px",
            borderRadius: 10,
            backgroundColor: phase !== "http" ? "#0D9488" : "transparent",
            color: phase !== "http" ? "#FFFFFF" : "#6B7280",
          }}
        >
          worker.js
        </div>
        <div
          style={{
            padding: "8px 18px",
            borderRadius: 10,
            backgroundColor: phase === "http" ? "#22C55E" : "transparent",
            color: phase === "http" ? "#FFFFFF" : "#6B7280",
          }}
        >
          HTTP Tab
        </div>
        <div style={{ marginLeft: "auto", color: "#0D9488", fontSize: 18 }}>● LIVE SYNC</div>
      </div>

      {phase !== "http" ? (
        <div style={{ display: "flex", height: 470 }}>
          {/* Left Code Editor */}
          <div
            style={{
              flex: 1.15,
              backgroundColor: "#0F172A",
              padding: 28,
              fontFamily: FONTS.mono,
              fontSize: 21,
              lineHeight: 1.7,
              color: "#E2E8F0",
            }}
          >
            <div style={{ color: "#64748B" }}>1  export default {"{"}</div>
            <div style={{ color: "#94A3B8" }}>2    async fetch() {"{"}</div>
            {phase === "edit" ? (
              <>
                <div style={{ color: "#F87171", textDecoration: "line-through", opacity: 0.7 }}>
                  3      return new Response("Hello World");
                </div>
                <div
                  style={{
                    backgroundColor: "rgba(20,184,166,0.22)",
                    borderLeft: "4px solid #14B8A6",
                    padding: "4px 10px",
                    color: "#5EEAD4",
                    marginTop: 6,
                  }}
                >
                  3  return Response.json({customResp}▌)
                </div>
              </>
            ) : (
              <div style={{ color: "#5EEAD4" }}>3      return new Response("Hello World");</div>
            )}
            <div style={{ color: "#94A3B8" }}>4    {"}"}</div>
            <div style={{ color: "#64748B" }}>5  {"};"}</div>
          </div>

          {/* Right Live Preview */}
          <div
            style={{
              flex: 0.85,
              backgroundColor: "#F8FAFC",
              padding: 28,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              gap: 18,
              borderLeft: "2px solid #E2E8F0",
            }}
          >
            <div style={{ fontFamily: FONTS.mono, fontSize: 18, color: "#0D9488", fontWeight: 700 }}>
              LIVE PREVIEW
            </div>
            <div
              style={{
                backgroundColor: "#FFFFFF",
                border: "2px solid #99F6E4",
                borderRadius: 16,
                padding: 22,
                fontFamily: FONTS.mono,
                fontSize: 22,
                color: "#0F172A",
                fontWeight: 700,
              }}
            >
              {phase === "edit" ? '{"ok": true, "user": "GK"}' : "Hello World!"}
            </div>
            <div style={{ fontFamily: FONTS.sans, fontSize: 19, color: "#475569" }}>
              Instant update on every keystroke
            </div>
          </div>
        </div>
      ) : (
        /* HTTP Tab View (B7) */
        <div style={{ padding: 32, display: "flex", flexDirection: "column", gap: 22, height: 470 }}>
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <div
              style={{
                padding: "12px 20px",
                borderRadius: 12,
                backgroundColor: "#DBEAFE",
                color: "#1D4ED8",
                fontFamily: FONTS.mono,
                fontSize: 22,
                fontWeight: 800,
              }}
            >
              POST
            </div>
            <div
              style={{
                flex: 1,
                padding: "12px 18px",
                borderRadius: 12,
                border: "2px solid #CBD5E1",
                fontFamily: FONTS.mono,
                fontSize: 21,
                color: "#1E293B",
              }}
            >
              https://playground.workers.dev/api/test
            </div>
            <div
              style={{
                padding: "12px 24px",
                borderRadius: 12,
                backgroundColor: "#22C55E",
                color: "#FFFFFF",
                fontFamily: FONTS.sans,
                fontSize: 22,
                fontWeight: 800,
              }}
            >
              Send ↗
            </div>
          </div>

          <div
            style={{
              flex: 1,
              backgroundColor: "#0F172A",
              borderRadius: 18,
              padding: 26,
              display: "flex",
              flexDirection: "column",
              gap: 14,
            }}
          >
            <div style={{ display: "flex", gap: 16, fontFamily: FONTS.mono, fontSize: 20 }}>
              <span style={{ color: "#4ADE80", fontWeight: 800 }}>Status: 200 OK</span>
              <span style={{ color: "#94A3B8" }}>Time: 6 ms</span>
              <span style={{ color: "#94A3B8" }}>Size: 42 B</span>
            </div>
            <div style={{ fontFamily: FONTS.mono, fontSize: 24, color: "#F8FAFC", lineHeight: 1.6 }}>
              {"{\n  \"ok\": true,\n  \"tested_in\": \"HTTP Tab\"\n}"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
