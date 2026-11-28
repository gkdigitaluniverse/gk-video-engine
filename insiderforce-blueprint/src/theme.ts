export const COLORS = {
  canvas: "#F2F2F2",
  surface: "#FFFFFF",
  darkCard: "#0F1115",
  darkBorder: "#262933",
  ink: "#0D0D0D",
  inkMuted: "#8A8A93",
  inkFaint: "#B4B4BC",
  border: "#E2E2E6",
  emerald: "#10B981",
  emeraldSoft: "rgba(16, 185, 129, 0.14)",
  crimson: "#EF4444",
  crimsonSoft: "rgba(239, 68, 68, 0.14)",
  blue: "#2563EB",
  amber: "#F59E0B",
};

export const SHADOWS = {
  card: "0 28px 64px rgba(0, 0, 0, 0.14), 0 4px 14px rgba(0, 0, 0, 0.06)",
  tile: "0 18px 38px rgba(0, 0, 0, 0.12), 0 2px 6px rgba(0, 0, 0, 0.06)",
  pill: "0 16px 36px rgba(0, 0, 0, 0.24)",
};

export const FONTS = {
  sans: "'Inter', system-ui, -apple-system, sans-serif",
  mono: "'Space Mono', ui-monospace, monospace",
};

export const SPRINGS = {
  snappy: { damping: 16, stiffness: 190, mass: 0.7 },
  smooth: { damping: 20, stiffness: 120, mass: 0.9 },
  pop: { damping: 13, stiffness: 220, mass: 0.6 },
};

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION_SECONDS = 35.6;
export const DURATION_FRAMES = Math.ceil(DURATION_SECONDS * FPS);
