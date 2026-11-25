# Thumbnail Skill — हर video के साथ thumbnail

## Formula (reference videos से नापा हुआ pattern)
- **3–4 शब्द से ज़्यादा नहीं**, उनमें से 1 शब्द accent color में या serif-italic में।
- चेहरा हो तो expression साफ़, frame के एक तरफ़; text दूसरी तरफ़। चेहरा न हो तो hero object (खाना/phone/product) बड़ा।
- Background: video के theme का ही color (navy/cream/black) — thumbnail और video एक ही दुनिया लगें।
- Font: Montserrat Black / Archivo Black, size frame height का 12–18%, मोटा dark outline या solid pill पीछे।
- एक ही visual hook: arrow, circle highlight, before/after split, या बड़ा number (₹0, 1MB, 80/20 type)।

## Sizes
- YouTube: 1280×720 (`templates/Thumbnail.tsx` → `YouTubeThumb`)
- Reel/Shorts cover: 1080×1920 (`ReelCover`) — safe zone: ऊपर-नीचे 250px में text नहीं (UI overlay आता है)।

## Process
1. Video का theme + सबसे मज़बूत एक line चुनो (hook line ही thumbnail text बने)।
2. Template में text/रंग बदलो, hero image लगाओ।
3. Still render करके 10% size पर देखो — छोटा करके भी पढ़ा जाए तो पास।
4. A/B चाहिए तो सिर्फ़ accent color या एक शब्द बदलकर दूसरा version — पूरा design नहीं।

## कभी नहीं
- Clickbait झूठ (जो video में नहीं है वो thumbnail पर नहीं)।
- 5+ शब्द, छोटा text, emoji (render में tofu हो सकता है — text badge इस्तेमाल करो)।
- चेहरे पर text।
