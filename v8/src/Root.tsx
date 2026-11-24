import React from "react";
import { Composition } from "remotion";
import { Main } from "./Main";
import { Main2 } from "./Main2";
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Main" component={Main}
      durationInFrames={2524} fps={60} width={1080} height={1920} />
    <Composition id="Sheets" component={Main2}
      durationInFrames={2698} fps={60} width={1080} height={1920} />
  </>
);
