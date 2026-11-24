import React from "react";
import { Composition } from "remotion";
import { Main } from "./Main";
export const RemotionRoot: React.FC = () => (
  <Composition id="Main" component={Main}
    durationInFrames={2524} fps={60} width={1080} height={1920} />
);
