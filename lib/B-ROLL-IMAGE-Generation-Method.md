# B-Roll Method — जहाँ footage कम पड़े, वहाँ image से B-roll
_सख्त नियम: B-roll तभी, जहाँ सच में ज़रूरत हो. हर जगह ठूँसना मना है — असली footage हमेशा पहले._

## कब B-roll चाहिए होता है (पहले Plan में बताना होगा)
- Script कुछ कह रही है पर वैसी clip footage में नहीं है
- खाली/सुस्त हिस्सा है जहाँ viewer भागेगा
- Product/खाने का hero shot ही नहीं है

## तरीका 1 — Agent खुद image बनाए (सबसे तेज़)
Agent के पास image generation है. ज़रूरी frame agent खुद बनाए — पर वो रुकी हुई तस्वीर है. उसे video में 2 ढंग से ज़िंदा करो:
- **Ken Burns / parallax:** Remotion में धीमा zoom-pan + हल्की depth — 3-5 सेकंड के लिए काफ़ी अच्छा लगता है
- **Layer animation:** sticker/text/SFX के साथ चले तो तस्वीर भी लगती नहीं

## तरीका 2 — User से 8-10s की असली B-roll clip बनवाना (जब हिलती हुई clip ही चाहिए)
AI video tools एक बार में ~8-10 सेकंड की ही clip बनाते हैं — इसलिए B-roll भी उतनी ही माँगो, ज़्यादा नहीं.
Agent user को **एक साथ** ये देगा:
1. **तैयार image** (agent ने बनाई हुई — user को कुछ बनाने की ज़रूरत नहीं)
2. **तैयार motion prompt** (नीचे format) — user सिर्फ़ copy-paste करेगा
3. साफ़ हिदायत: "इस image को [tool] में upload करो, ये prompt डालो, बनी हुई 8-10s clip Drive के `06 - User Inputs` में डालकर मुझे बता दो — मैं उसे सही जगह काटकर लगा दूँगा."

### Motion prompt का format (agent हर बार ऐसा ही देगा)
```
[Image upload करो] + Prompt:
"Slow push-in on [विषय], steam rising, warm street light, shallow depth of field,
no text, no people faces close-up, 9:16 vertical, photorealistic, smooth motion"
अवधि: 8-10s • Ratio: video जैसा (9:16 या 16:9)
```

## नियम
- एक video में user से ज़्यादा से ज़्यादा 1-2 clips मँगवाओ — उससे ज़्यादा चाहिए तो agent stock (ONLINE-ASSET-SOURCING-METHOD) या अपनी बनाई images से काम चलाए.
- User की clip आते ही agent उसे खुद trim करके सही second पर लगाएगा — user को editing नहीं करनी.
- Generated/AI B-roll को असली footage कहकर कभी पेश मत करो. Client के काम में AI B-roll लगे तो delivery note में साफ़ लिखो.
