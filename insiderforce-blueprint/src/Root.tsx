import React from "react";
import { Composition } from "remotion";
import { InsiderForceMain } from "./Main";
import { DURATION_FRAMES, FPS, HEIGHT, WIDTH } from "./theme";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="InsiderForceDemo"
      component={InsiderForceMain}
      durationInFrames={DURATION_FRAMES}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
