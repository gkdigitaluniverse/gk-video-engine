import React from "react";
import { Img, interpolate, spring, staticFile, useVideoConfig } from "remotion";
import { SPRINGS } from "../theme";

interface AIHeroVisualProps {
  /** Path inside public/ai/, e.g. "shield.jpg" */
  fileName: string;
  localFrame: number;
  size?: number;
}

/**
 * Renders an AI-generated 3D studio hero asset seamlessly onto our matte #F2F2F2 canvas:
 * - Uses `mixBlendMode: "multiply"` + slight contrast/brightness lift so #F2F2F2 studio paper
 *   matches the exact canvas value.
 * - Applies a soft radial CSS mask so zero square box edges ever appear.
 */
export const AIHeroVisual: React.FC<AIHeroVisualProps> = ({
  fileName,
  localFrame,
  size = 640,
}) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: SPRINGS.snappy });
  const floatY = Math.sin(localFrame * 0.11) * 10;
  const subtleZoom = interpolate(localFrame, [0, 120], [1.0, 1.07], {
    extrapolateRight: "clamp",
  });

  const radialMask =
    "radial-gradient(ellipse 68% 68% at 50% 50%, #000000 58%, rgba(0,0,0,0.4) 76%, transparent 94%)";

  return (
    <div
      style={{
        width: size,
        height: size,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${interpolate(enter, [0, 1], [0.85, 1]) * subtleZoom}) translateY(${floatY}px)`,
        opacity: enter,
      }}
    >
      <Img
        src={staticFile(`ai/${fileName}`)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
          mixBlendMode: "multiply",
          filter: "brightness(1.06) contrast(1.05)",
          maskImage: radialMask,
          WebkitMaskImage: radialMask,
        }}
      />
    </div>
  );
};
