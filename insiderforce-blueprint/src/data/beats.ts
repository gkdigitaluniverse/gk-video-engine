export type SceneKind =
  | "hook_laser"
  | "shield_docs"
  | "node_flow"
  | "stacked_alerts"
  | "scan_lens"
  | "counter_532"
  | "cross_checklist"
  | "limit_50mb"
  | "env_vault"
  | "cta_guide";

export interface MotionBeat {
  id: string;
  startSec: number;
  endSec: number;
  scene: SceneKind;
  /** Words displayed in editorial kinetic typography */
  leadText: string;
  /** Bold jet-black punch phrase rendered inside an inverted black bar */
  pillText: string;
  /** Optional accent color for the pill bar (defaults to jet black #0D0D0D) */
  pillAccent?: string;
  sourceLabel: string;
}

export const BEATS: MotionBeat[] = [
  {
    id: "B1",
    startSec: 0.0,
    endSec: 4.36,
    scene: "hook_laser",
    leadText: "One mistake in a public repo can leak your",
    pillText: "API KEY",
    sourceLabel: "github.com/gkdigitaluniverse",
  },
  {
    id: "B2",
    startSec: 4.36,
    endSec: 8.34,
    scene: "shield_docs",
    leadText: "GitHub ships a built-in shield called",
    pillText: "Push Protection",
    sourceLabel: "docs.github.com/en/code-security",
  },
  {
    id: "B3",
    startSec: 8.34,
    endSec: 12.13,
    scene: "node_flow",
    leadText: "It intercepts secrets automatically",
    pillText: "before the repo",
    sourceLabel: "Runs on every git push",
  },
  {
    id: "B4",
    startSec: 12.13,
    endSec: 15.57,
    scene: "stacked_alerts",
    leadText: "Old alerts arrived after the leak",
    pillText: "already too late",
    pillAccent: "#DC2626",
    sourceLabel: "Prevention vs Post-leak cleanup",
  },
  {
    id: "B5",
    startSec: 15.57,
    endSec: 18.8,
    scene: "scan_lens",
    leadText: "Match any supported pattern and your push is",
    pillText: "blocked instantly",
    sourceLabel: "docs.github.com/en/code-security",
  },
  {
    id: "B6",
    startSec: 18.8,
    endSec: 22.58,
    scene: "counter_532",
    leadText: "Official partner patterns tracked today",
    pillText: "532 types · 465 blocked",
    sourceLabel: "github.com/advanced-security/awesome-secret-scanning",
  },
  {
    id: "B7",
    startSec: 22.58,
    endSec: 24.52,
    scene: "cross_checklist",
    leadText: "The honest catch — it does not block",
    pillText: "every secret",
    sourceLabel: "Verified on GitHub Docs",
  },
  {
    id: "B8",
    startSec: 24.52,
    endSec: 28.21,
    scene: "limit_50mb",
    leadText: "On public repos, any push over 50 MB is",
    pillText: "skipped · no scan",
    pillAccent: "#DC2626",
    sourceLabel: "docs.github.com · 50 MB push limit",
  },
  {
    id: "B9",
    startSec: 28.21,
    endSec: 32.54,
    scene: "env_vault",
    leadText: "Never hardcode keys — keep them safely in",
    pillText: "process.env",
    pillAccent: "#059669",
    sourceLabel: ".env + .gitignore best practice",
  },
  {
    id: "B10",
    startSec: 32.54,
    endSec: 35.6,
    scene: "cta_guide",
    leadText: "Every official docs link is waiting in the",
    pillText: "Description ↓",
    sourceLabel: "gkhackter · Follow for daily tech",
  },
];
