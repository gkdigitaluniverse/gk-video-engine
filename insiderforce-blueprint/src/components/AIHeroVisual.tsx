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
 * Renders an AI-generated 3D studio hero asset (generated on #F2F2F2 matte gray)
 * seamlessly blended onto our studio canvas via `mixBlendMode: "multiply"` with subtle 3D levitation.
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
          borderRadius: 28,
        }}
      />
    </div>
  );
};
