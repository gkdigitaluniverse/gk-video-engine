import { AccentKey, ThemeMode } from "../theme";

export type AvatarPose =
  | "explain"
  | "pointUp"
  | "thumbsUp"
  | "thinking"
  | "shocked"
  | "okSign"
  | "wave";

export interface ChapterDef {
  id: string;
  label: string;
  accent: AccentKey;
}

export interface BeatDef {
  id: string;
  startSec: number;
  endSec: number;
  chapterIndex: number;
  mode: ThemeMode;
  accent: AccentKey;
  /** Hinglish/English caption words matching the spoken Hindi voiceover */
  caption: string;
  /** Word index (or indices) to give extra accent emphasis */
  highlightWords?: string[];
  pose: AvatarPose;
  sourceCitation: string;
}

export const CHANNEL_HANDLE = "@gkhackter";

export const CHAPTERS: ChapterDef[] = [
  { id: "hook", label: "HOOK", accent: "orange" },
  { id: "nosetup", label: "NO SETUP", accent: "blue" },
  { id: "livetest", label: "LIVE TEST", accent: "teal" },
  { id: "limits", label: "FREE LIMITS", accent: "purple" },
  { id: "catch", label: "THE CATCH", accent: "red" },
];

export const BEATS: BeatDef[] = [
  {
    id: "B1",
    startSec: 0.0,
    endSec: 2.62,
    chapterIndex: 0,
    mode: "light",
    accent: "orange",
    caption: "API bina server kharide browser mein test karo",
    highlightWords: ["API", "browser"],
    pose: "explain",
    sourceCitation: "workers.cloudflare.com/playground",
  },
  {
    id: "B2",
    startSec: 2.62,
    endSec: 5.48,
    chapterIndex: 0,
    mode: "light",
    accent: "orange",
    caption: "Agar aap chhota web app banate hain",
    highlightWords: ["web", "app"],
    pose: "pointUp",
    sourceCitation: "workers.cloudflare.com/playground",
  },
  {
    id: "B3",
    startSec: 5.48,
    endSec: 10.4,
    chapterIndex: 1,
    mode: "dark",
    accent: "blue",
    caption: "Playground mein bina account code likho aur live preview dekho",
    highlightWords: ["Playground", "account", "live"],
    pose: "explain",
    sourceCitation: "Cloudflare Workers Playground · Zero Signup",
  },
  {
    id: "B4",
    startSec: 10.4,
    endSec: 14.06,
    chapterIndex: 1,
    mode: "dark",
    accent: "blue",
    caption: "Pehle project setup aur deploy karna padta tha",
    highlightWords: ["setup", "deploy"],
    pose: "thinking",
    sourceCitation: "Old workflow vs Instant Browser Sandbox",
  },
  {
    id: "B5",
    startSec: 14.06,
    endSec: 17.86,
    chapterIndex: 2,
    mode: "light",
    accent: "teal",
    caption: "Yahan editor aur live preview saath chalte hain",
    highlightWords: ["editor", "preview"],
    pose: "explain",
    sourceCitation: "workers.cloudflare.com/playground · Split IDE",
  },
  {
    id: "B6",
    startSec: 17.86,
    endSec: 22.02,
    chapterIndex: 2,
    mode: "light",
    accent: "teal",
    caption: "Hello World badlo, response likho, output turant dekho",
    highlightWords: ["response", "output"],
    pose: "pointUp",
    sourceCitation: "Instant hot-reload Worker response",
  },
  {
    id: "B7",
    startSec: 22.02,
    endSec: 25.32,
    chapterIndex: 2,
    mode: "light",
    accent: "green",
    caption: "HTTP tab se direct request bhi bhej sakte ho",
    highlightWords: ["HTTP", "request"],
    pose: "okSign",
    sourceCitation: "Built-in HTTP Request Tester · JSON 200 OK",
  },
  {
    id: "B8",
    startSec: 25.32,
    endSec: 26.72,
    chapterIndex: 3,
    mode: "dark",
    accent: "purple",
    caption: "Maine khud official docs check kiya",
    highlightWords: ["check"],
    pose: "thumbsUp",
    sourceCitation: "developers.cloudflare.com/workers/platform/limits",
  },
  {
    id: "B9",
    startSec: 26.72,
    endSec: 29.38,
    chapterIndex: 3,
    mode: "dark",
    accent: "purple",
    caption: "Free plan mein 1,00,000 requests roz milti hain",
    highlightWords: ["1,00,000", "requests"],
    pose: "shocked",
    sourceCitation: "Cloudflare Workers Free Plan · Official Limits",
  },
  {
    id: "B10",
    startSec: 29.38,
    endSec: 32.32,
    chapterIndex: 3,
    mode: "dark",
    accent: "gold",
    caption: "Har request ko 10 ms CPU time milta hai",
    highlightWords: ["10", "ms", "CPU"],
    pose: "pointUp",
    sourceCitation: "Cloudflare Workers Free Plan · 10ms CPU / req",
  },
  {
    id: "B11",
    startSec: 32.32,
    endSec: 34.44,
    chapterIndex: 4,
    mode: "light",
    accent: "red",
    caption: "Lekin iski asli kami kya hai?",
    highlightWords: ["kami"],
    pose: "thinking",
    sourceCitation: "Honest limitation check · GK HACKTER",
  },
  {
    id: "B12",
    startSec: 34.44,
    endSec: 37.66,
    chapterIndex: 4,
    mode: "light",
    accent: "red",
    caption: "Playground sirf Chrome aur Firefox desktop par chalta hai",
    highlightWords: ["Chrome", "Firefox", "desktop"],
    pose: "explain",
    sourceCitation: "Browser support: Desktop Chrome & Firefox only",
  },
  {
    id: "B13",
    startSec: 37.66,
    endSec: 39.72,
    chapterIndex: 4,
    mode: "dark",
    accent: "orange",
    caption: "Live deploy karne ke liye account chahiye",
    highlightWords: ["deploy", "account"],
    pose: "pointUp",
    sourceCitation: "Test = No account · Deploy = Free Cloudflare account",
  },
  {
    id: "B14",
    startSec: 39.72,
    endSec: 42.1,
    chapterIndex: 4,
    mode: "dark",
    accent: "green",
    caption: "Link description mein hai — try karke dekho",
    highlightWords: ["Link", "description"],
    pose: "thumbsUp",
    sourceCitation: "workers.cloudflare.com/playground · @gkhackter",
  },
];
