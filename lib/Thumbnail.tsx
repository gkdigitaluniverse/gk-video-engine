import React from "react";
import { AbsoluteFill, Img } from "remotion";
import { THEMES } from "./Templates";

/**
 * Thumbnail templates — recipe: references/thumbnail-skill.md
 * YouTubeThumb 1280x720 comp में, ReelCover 1080x1920 comp में इस्तेमाल करो।
 * Emoji मत लगाओ (headless में tofu) — badge text इस्तेमाल करो।
 */

export const YouTubeThumb: React.FC<{
  line1: string; keyWord: string; line2?: string; heroSrc?: string; theme?: keyof typeof THEMES; badge?: string;
}> = ({ line1, keyWord, line2 = "", heroSrc, theme = "navy", badge }) => {
  const t = THEMES[theme];
  return (
    <AbsoluteFill style={{ background: t.bg, fontFamily: "Archivo, Montserrat, Arial, sans-serif" }}>
      {heroSrc ? <Img src={heroSrc} style={{ position: "absolute", right: 0, top: 0, height: "100%", width: "46%", objectFit: "cover" }} /> : null}
      <div style={{ position: "absolute", left: 56, top: 120, width: heroSrc ? "52%" : "88%" }}>
        {badge ? <span style={{ background: t.accent, color: t.bg, fontWeight: 900, fontSize: 34, padding: "8px 22px", borderRadius: 999 }}>{badge}</span> : null}
        <div style={{ color: t.text, fontWeight: 900, fontSize: 96, lineHeight: 1.02, marginTop: 28, textTransform: "uppercase" }}>
          {line1} <span style={{ color: t.accent }}>{keyWord}</span> {line2}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const ReelCover: React.FC<{
  line1: string; keyWord: string; heroSrc?: string; theme?: keyof typeof THEMES;
}> = ({ line1, keyWord, heroSrc, theme = "food" }) => {
  const t = THEMES[theme];
  return (
    <AbsoluteFill style={{ background: t.bg, fontFamily: "Archivo, Montserrat, Arial, sans-serif" }}>
      {heroSrc ? <Img src={heroSrc} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.82 }} /> : null}
      {/* safe zone: ऊपर-नीचे 250px खाली */}
      <div style={{ position: "absolute", left: 60, right: 60, top: 560, textAlign: "center" }}>
        <span style={{ background: "rgba(0,0,0,.55)", borderRadius: 28, padding: "26px 10px", display: "block" }}>
          <span style={{ color: "#fff", fontWeight: 900, fontSize: 92, lineHeight: 1.05, textTransform: "uppercase" }}>
            {line1} <span style={{ color: t.accent }}>{keyWord}</span>
          </span>
        </span>
      </div>
    </AbsoluteFill>
  );
};
