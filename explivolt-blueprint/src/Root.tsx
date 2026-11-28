import React from "react";
import { Composition } from "remotion";
import { ExplivoltMain } from "./Main";
import { DURATION_FRAMES, FPS, HEIGHT, WIDTH } from "./theme";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ExplivoltDemo"
      component={ExplivoltMain}
      durationInFrames={DURATION_FRAMES}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
