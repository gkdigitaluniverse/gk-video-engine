# STYLE-ENGINE v2 — असली layout जो काम करता है

v1 गलत था। v1 में सिर्फ़ नाप था — beat कितना लंबा, कौन सा रंग, text कहाँ।
उसमें **layout नहीं था, हरकत नहीं थी, अक्षरों का क्रम नहीं था**। इसीलिए हर render सस्ता आया।
यह v2 उस वीडियो से बना है जो पास हुआ, और उन references से जिन्हें मैंने आख़िरकार देखा।

---

## 1. फ्रेम — पूरा भरा, कभी खाली नहीं

```
0 ────────────────────────────
   kicker        (y = 5%)
   ──── underline
   title         (y = 9%)
   subtitle      (y = 13%)
120 ──────────────────────────
   HERO          (y = 20% → 65%)
   screen panel या data rows
1250 ─────────────────────────
   caption line 1 (y = 68%)
   caption line 2 (accent) + underline
   callout box   (y = 81% → 90%)
1560 ─────────────────────────
   source line   (y = 93%)
1786 ─────────────────────────
   pips + progress bar (y = 99%)
1920 ─────────────────────────
```

**कोई card box के अंदर नहीं।** कुछ भी margin में तैरता नहीं। हर पट्टी भरी हुई है।

---

## 2. अक्षर — चार स्तर, हमेशा चार

| स्तर | आकार | रंग | जगह |
|---|---|---|---|
| kicker | 26px, uppercase, letterspaced | amber | ऊपर बाएँ, नीचे 4px underline |
| title | 56px, bold | white | kicker के नीचे |
| subtitle | 28px, normal | grey | title के नीचे |
| caption 1 | 74px, bold | white | नीचे, hero के बाद |
| caption 2 | 74px, bold | **orange** | caption 1 के नीचे, नीचे amber underline |

- फ़ॉन्ट: **Montserrat Bold** (static TTF, variable नहीं — वरना पतला आ जाता है)
- केस: kicker uppercase, बाकी sentence case
- कभी एक बड़ा headline नहीं। हमेशा यह चार स्तर, पूरे वीडियो में वही।

---

## 3. रंग

```
background   #0A0E20 → #080A14   (ऊपर से नीचे gradient)
glow         #2E1608, 180px blur, ऊपर 40% में
grid         #181E36, 60px, धीरे drift करती है
ghost        #0F1326, 430px, पीछे
white        #F6F7FC
grey         #8C92AA
orange       #FF7A30   ← caption line 2, bars
amber        #FFBE46   ← kicker, underlines
teal         #3CD2B4   ← achha data
red          #FF5C5C   ← bura data, strike
```

background कभी flat नहीं। तीन परतें: gradient + glow + grid।

---

## 4. Hero — दो ही तरह के, और दोनों हिलते हैं

### (अ) Screen panel
- असली screen recording, बड़े panel में (x 6%, y 20%, w 88%, h 48%)
- ऊपर browser chrome: तीन बिंदु, URL pill
- अंदर recording चलती रहती है — Ken Burns 1.0 → 1.10
- यह तब जब line में कोई असली चीज़ दिखानी हो

### (ब) Data rows
- पीछे हल्का panel
- हर row: label (40px) + counting value (46px) + बढ़ती bar
- rows एक-एक करके आती हैं, 0.10s के अंतर से
- value गिनती है और **सही आंकड़े पर रुकती है**
- यह तब जब line में कोई number या तुलना हो

तीसरा कुछ नहीं। न कोई तीसरा layout, न खाली जगह।

---

## 5. हरकत — हर beat में कम से कम पाँच चीज़ें हिल रही हों

1. grid — 12px/s drift
2. glow — साँस लेता है
3. hero — recording चलती है या bar बढ़ती है
4. caption — 0.25s में नीचे से आती है, 34px slide
5. underline — बाएँ से दाएँ खिंचती है, 0.35s
6. callout — 0.4s में फीका से आता है
7. progress bar — लगातार बढ़ता है

अगर किसी beat में पाँच से कम चीज़ें हिल रही हैं, वह beat अधूरा है।

---

## 6. beat की लंबाई

- हर beat = एक VO वाक्य, **2.4 से 3.4 सेकंड**
- beat की सीमा **आवाज़ से नापी** जाती है, कभी अनुमान से नहीं
- अगर एक वाक्य 4s से लंबा है, उसे दो beat में तोड़ो — शब्दों के बीच की ख़ामोशी पर
- अगर छोटा है (1.5s से कम), अगले के साथ जोड़ो

---

## 7. सामग्री का नियम

- screen पर सिर्फ़ अंग्रेज़ी
- कोई कैप्शन नहीं
- हर number के साथ source line में तारीख़
- ईमानदार कमी हर वीडियो में, हमेशा
- CTA: छोटा command सीधे description में, website का URL, या बड़ी फ़ाइल का Drive link

---

## 8. ध्वनि — जो v1 में पूरी तरह छूट गई

- संगीत −26 पर आवाज़ के नीचे
- हर beat बदलाव पर एक छोटा whoosh (0.15s)
- number रुकने पर एक click
- अंत में 3.5s का fade out
- पूरा मिक्स −14 LUFS, peak −1.5

अभी whoosh और click मेरे पास नहीं हैं। जब तक नहीं हैं, यह काम अधूरा है — और यह लिखा रहेगा।

---

## 9. जो मैं बना नहीं सकता — साफ़ लिखा रहे

- असली फ़ोटो
- कार्टून किरदार
- 3D

अगर किसी beat में यह चाहिए, तो उस beat को screen panel या data rows में बदलो, या मुझसे तस्वीर माँगो।
चुपचाप उसकी जगह कुछ और मत रखो।
