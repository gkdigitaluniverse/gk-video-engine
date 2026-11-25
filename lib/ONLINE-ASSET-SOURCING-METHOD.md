# Online से Assets उठाने का तरीका (Link-First Method)

**मूल नियम:** हर image/video/SFX को library में भरकर नहीं रखना। इस file में **तरीका + links** हैं — agent ज़रूरत पड़ने पर उसी समय online से उठाकर, license check करके, सिर्फ़ उस project के लिए इस्तेमाल करेगा। इससे storage/RAM बचता है और assets हमेशा ताज़ा रहते हैं।

## 1. Video B-Roll (stock footage)
| Source | Link | License | कैसे उठाएँ |
|---|---|---|---|
| Pexels Videos | pexels.com/videos | Free, attribution ज़रूरी नहीं | Computer पर **Pexels API key (free)** लेकर API से search+download; browser से भी |
| Pixabay Videos | pixabay.com/videos | Free commercial | API key (free) या browser |
| Coverr | coverr.co | Free | Browser/API |
| Mixkit | mixkit.co/free-stock-video | सिर्फ़ "Free License" वाले | Browser |
| Wikimedia Commons | commons.wikimedia.org | CC — हर file का license अलग, पढ़ो | **API बिना key के चलती है** (नीचे command) |
| Archive.org | archive.org | Public domain/CC वाले चुनो | `yt-dlp` / direct files |
| NASA | images.nasa.gov | ज़्यादातर public domain | Science/space B-roll के लिए |

⚠️ इस छोटी machine से कुछ sites bot को 403 देती हैं — computer के browser/API key से ठीक चलेगा। yt-dlp कई sites से सीधे video उतार देता है: `yt-dlp -f "bv*[height<=720]+ba/b" "PAGE_URL"`

## 2. Images
- **Wikimedia Commons API (बिना key, सबसे भरोसेमंद):**
```bash
curl -s "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch=dabeli&srnamespace=6&srlimit=10"
# फिर किसी file का असली URL:
curl -s "https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:Kachchi%20Dabeli.jpg&prop=imageinfo&iiprop=url|extmetadata"
```
- Unsplash (unsplash.com), Pexels Photos, Pixabay — free photos; computer पर API keys से automation।
- Openverse (openverse.org) — सारे CC images की search; API: `api.openverse.org/v1/images/?q=...`

## 3. Still Image से B-Roll बनाना (हमारी असली ताकत)
जब सही video clip न मिले तो अच्छी photo को ही हिलता हुआ B-roll बनाओ:
- **FFmpeg:** `ffmpeg -loop 1 -i photo.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920" -t 5 -c:v libx264 broll.mp4` (Ken Burns zoom)
- **Remotion में:** हमारे Motion presets (ZoomIn/Pan) किसी भी `public/` photo पर — Food Masti/GKGame videos इसी तरह बने हैं।
- AI से photo बनवानी हो तो agent image generate करके वही zoom/pan लगाएगा — character animation नहीं, सिर्फ़ प्रस्तुति।

## 4. Music/SFX
पहले से तैयार pack Drive `03` में है (`Library-Auto-Downloads-2026-10-31.zip`)। और चाहिए तो: Wyzowl kit (CC0, `git clone https://github.com/wyzowl/sfx-kit`), MyInstants meme sounds (headers वाली fixed script — DOWNLOADED-ASSETS-README में), Pixabay/Freesound (सिर्फ़ CC0)। YouTube Audio Library सबसे safe है पर browser+अपना Google account लगता है।

## 5. Meme/Video clips
- Meme templates के लिए source खोजो, पर **copyright सावधानी:** meme sounds/clips अपने entertainment content में ठीक हैं, client के commercial ad में बिना हक़ के नहीं।
- किसी भी online clip को project में डालने से पहले: (1) license/हक़ check, (2) सिर्फ़ ज़रूरी हिस्सा, (3) project notes में source लिखो।

## 6. AI Image/Video Generation के Free Credits — ईमानदार नियम
Runway, Pika, Kling, Leonardo, Ideogram जैसी services नए account पर कुछ free credits देती हैं। **सही तरीका:** अपने असली account से official free tier इस्तेमाल करो — उतने में काम हो तो बढ़िया, वरना छोटा plan या local open-source tools (computer पर ComfyUI/Stable Diffusion — एक बार setup, फिर unlimited, कोई credit नहीं)।
**जो हम नहीं करेंगे:** temporary/fake email से बार-बार नए accounts बनाकर trial credits इकट्ठा करना। ये उन sites के नियमों के खिलाफ है — accounts ban होते हैं, बने हुए काम का credit भी जा सकता है, और client के काम में ऐसा source कभी भरोसेमंद नहीं होता। Library को 100% करने के लिए ये shortcut ज़रूरी भी नहीं — ऊपर के free/CC sources + local tools से हर visual बन सकता है।

## 7. Setup के समय हम क्या बदलेंगे (आने वाला काम)
जब computer पर setup होगा तब इस file के हर source के लिए: API keys एक `.env` में, हर type के लिए "पहले कहाँ खोजना है" का क्रम skill files में, और B-roll बनाने के ready commands presets में — ताकि आप बस command दो और agent खुद asset खोजकर, बनाकर, लगाकर video दे।
