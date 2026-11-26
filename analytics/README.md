# analytics/ — नया फ़ोल्डर (क्यों बनाया गया)

यह फ़ोल्डर **26 नवंबर 2026** को सिर्फ़ एक काम के लिए बनाया गया है:

> YouTube, Instagram और Facebook के असली आँकड़े (views, plays, watch time,
> retention, skip) इकट्ठा करके एक रिपोर्ट बनाना।

## सबसे ज़रूरी बात — पुराना कुछ नहीं बदला

इस फ़ोल्डर को जोड़ते समय रेपो की **कोई पुरानी फाइल नहीं छुई गई** — न `src/`,
न `v11/`, न `public/`, न कोई पुराना workflow, न `README.md`, न `package.json`.
सिर्फ़ **नई फाइलें जोड़ी गई हैं**:

```
analytics/README.md          ← यही फाइल
analytics/fetch.py           ← डेटा लाने वाली स्क्रिप्ट
analytics/data/.gitkeep      ← नतीजे यहाँ आएंगे
.github/workflows/analytics-report.yml   ← नया workflow (पुराने वाले अछूते)
```

`.github/workflows/` में एक नई फाइल रखनी पड़ी, क्योंकि GitHub Actions
को चलाने के लिए workflow उसी फ़ोल्डर में होना ज़रूरी है। वहाँ पहले से मौजूद
26 में से किसी फाइल को छुआ नहीं गया।

## यह फ़ोल्डर क्या नहीं करता

- कोई वीडियो रेंडर नहीं करता
- कुछ पब्लिश नहीं करता
- STYLE, LEDGER, चैनल कॉन्फ़िग — कुछ नहीं बदलता
- पुरानी पाइपलाइन से इसका कोई लेना-देना नहीं

यह **सिर्फ़ पढ़ता है** — प्लेटफ़ॉर्म से आँकड़े लेकर `data/` में लिख देता है।

## चलाने का तरीका

GitHub → Actions → **analytics-report** → Run workflow.

या कमांड से:

```
gh workflow run analytics-report.yml -R gkdigitaluniverse/gk-video-engine
```

चलने के बाद नतीजा यहाँ मिलेगा:

```
analytics/data/latest.json        ← सबसे नया डेटा
analytics/data/<तारीख़>.json       ← उस दिन का डेटा
analytics/data/RUN.txt            ← क्या-क्या चला, कहाँ गड़बड़ हुई
analytics/data/schemas.json       ← टूल्स के schema (गड़बड़ सुधारने के लिए)
```

## साफ़ करना हो तो

पूरा `analytics/` फ़ोल्डर और `.github/workflows/analytics-report.yml` —
दोनों हटा दो, बाकी कुछ नहीं बदलेगा। यह फ़ोल्डर किसी और चीज़ पर निर्भर नहीं है।

## दो बातें जो पहले से पता हैं

- Composio सिर्फ़ GitHub runner से चलता है (सैंडबॉक्स से 502) — यही वजह है
  कि यह काम runner पर होता है।
- YouTube का चैनल-लेवल डेटा पिछली जाँच में 403 दे रहा था; अगर फिर 403 आए तो
  `RUN.txt` में साफ़ लिखा मिलेगा — छुपाया नहीं जाएगा।
