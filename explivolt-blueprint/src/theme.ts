export type ThemeMode = "light" | "dark";

export interface Palette {
  bg: string;
  bgSubtle: string;
  card: string;
  cardBorder: string;
  ink: string;
  inkMuted: string;
  inkFaint: string;
  shadow: string;
}

export const PALETTES: Record<ThemeMode, Palette> = {
  light: {
    bg: "#F7F5F0",
    bgSubtle: "#EFECE5",
    card: "#FFFFFF",
    cardBorder: "#E2DFD7",
    ink: "#111827",
    inkMuted: "#6B7280",
    inkFaint: "#9CA3AF",
    shadow: "0 20px 50px rgba(17, 24, 39, 0.08)",
  },
  dark: {
    bg: "#09090B",
    bgSubtle: "#121216",
    card: "#16161B",
    cardBorder: "#27272F",
    ink: "#F8FAFC",
    inkMuted: "#94A3B8",
    inkFaint: "#64748B",
    shadow: "0 24px 60px rgba(0, 0, 0, 0.55)",
  },
};

export const ACCENTS = {
  orange: { solid: "#F97316", lightBg: "rgba(249,115,22,0.15)", darkBg: "rgba(249,115,22,0.22)" },
  blue: { solid: "#3B82F6", lightBg: "rgba(59,130,246,0.14)", darkBg: "rgba(59,130,246,0.24)" },
  teal: { solid: "#0D9488", lightBg: "rgba(13,148,136,0.14)", darkBg: "rgba(20,184,166,0.22)" },
  purple: { solid: "#8B5CF6", lightBg: "rgba(139,92,246,0.15)", darkBg: "rgba(139,92,246,0.24)" },
  gold: { solid: "#F59E0B", lightBg: "rgba(245,158,11,0.16)", darkBg: "rgba(245,158,11,0.24)" },
  green: { solid: "#22C55E", lightBg: "rgba(34,197,94,0.15)", darkBg: "rgba(34,197,94,0.22)" },
  red: { solid: "#EF4444", lightBg: "rgba(239,68,68,0.14)", darkBg: "rgba(239,68,68,0.22)" },
} as const;

export type AccentKey = keyof typeof ACCENTS;

export const FONTS = {
  sans: "'Inter', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
  mono: "'JetBrains Mono', 'Space Mono', ui-monospace, monospace",
};

export const SPRINGS = {
  snappy: { damping: 16, stiffness: 180, mass: 0.7 },
  smooth: { damping: 20, stiffness: 120, mass: 0.9 },
  bouncy: { damping: 12, stiffness: 200, mass: 0.65 },
};

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION_SECONDS = 42.1;
export const DURATION_FRAMES = Math.ceil(DURATION_SECONDS * FPS);
