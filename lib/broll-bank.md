# B-Roll Bank — Categories, Prompts, नियम

## पहले यह क्रम (priority)
1. **User के असली assets** (उनके screenshots, recording, photos) — हमेशा पहले।
2. **खुद generate किए** (AI image/video) — जब असली न हो और scene माँगता हो।
3. **Free stock** (Pexels/Pixabay) — source + license note के साथ।

## Category-wise generation prompts (9:16, photorealistic जोड़ो)
| Category | Prompt base |
|---|---|
| Food hero | `overhead shot of [dish], steam rising, dark moody background, restaurant lighting, photorealistic, vertical` |
| Indian street food | `Indian street food stall, [dish] being served, evening light, crowd bokeh, photorealistic, vertical` |
| Shop/local business | `small Indian shop counter, owner smiling, warm light, photorealistic, vertical` |
| Phone in hand | `hand holding smartphone showing food delivery app, cafe table, shallow depth of field, photorealistic, vertical` |
| City/delivery | `delivery rider on scooter at dusk, Indian city street, motion feel, photorealistic, vertical` |
| Money/offer | `Indian rupee notes and coins on dark table, dramatic light, photorealistic, vertical` (या सिर्फ़ graphic card — बेहतर) |
| Talking-head cutaway | speaker की photo से sticker-cutout (scripts/remove_background.py) |
| Abstract bg | theme color का subtle pattern/gradient — code से बनाओ, generate मत करो |

## नियम
- Generated B-roll पर असली brand/logo/text मत बनवाओ — AI text बिगाड़ता है; text हमेशा code से बाद में।
- एक video में generated और real footage का grade एक रखो (references/color-grades.md)।
- कौन-सा asset generated है, delivery के समय user को बता दो।
- B-roll हमेशा HARD cut पर — wipe/घुमाव वाले transitions नहीं (cheap लगते हैं)।
- कोई भी scene 4 second से ज़्यादा static नहीं; B-roll/Ken Burns से movement रखो।
