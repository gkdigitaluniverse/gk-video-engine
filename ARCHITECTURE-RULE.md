# जो गलती दोबारा नहीं करनी

## नियम 1 — भारी काम सिर्फ़ पब्लिक रेपो में

| रेपो | क्या चलेगा | समय |
|---|---|---|
| `gk-video-engine` (public) | रेंडर, TwelveLabs, Composio, Groq, probes, downloads | जितना लगे |
| `free-voice-generation` (public) | TTS, yt-dlp, downloads | जितना लगे |
| `gk-control` (private) | सिर्फ़ secrets लिखना, dispatch, छोटी scripts | **1-3 मिनट, बस** |

## नियम 2 — Composio सिर्फ़ GitHub runner से

`connect.composio.dev` सैंडबॉक्स से **हमेशा 502**।
runner से **200** और MCP काम करता है।

कभी सैंडबॉक्स से Composio टेस्ट मत करना। सीधे runner।

## नियम 3 — काम न चले तो "मिनट खत्म" मत कहना

पहले जाँचो:
1. क्या workflow फाइल remote पर पहुँची?
2. क्या `pip install` फेल हुआ?
3. क्या `exec > file` से पहले फोल्डर मौजूद था?

मिनट खत्म होने का इल्ज़ाम सबसे आखिरी में।

## नियम 4 — Composio MCP से काम

- Endpoint: `https://connect.composio.dev/mcp`
- Header: `Authorization: Bearer <ck_...>`
- POST only, JSON-RPC
- पहले `initialize`, फिर `notifications/initialized`, फिर `tools/call`
- REST API (`backend.composio.dev/api/v3`) इस key को **रिजेक्ट** करता है। सिर्फ़ MCP चलता है।

## नियम 5 — कनेक्टेड अकाउंट (24-11-2026 को जाँचे)

| Platform | Account ID | नाम |
|---|---|---|
| Instagram | `instagram_quiles-adorer` | @gkhackter |
| Facebook | `facebook_unwise-planch` | Hackter Gk |
| YouTube | `youtube_easier-algoid` | — |

**ध्यान:** किसी भी non-connected toolkit पर `action: list` मत भेजना — Composio उसके लिए
नया pending auth link बना देता है। सिर्फ़ उन्हीं toolkits पर list भेजो जो जुड़े हैं।
