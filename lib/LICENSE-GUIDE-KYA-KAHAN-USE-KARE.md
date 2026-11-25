# LICENSE GUIDE — क्या कहाँ इस्तेमाल कर सकते हो, कहाँ नहीं
_Library की हर चीज़ के लिए simple नियम. कोई भी AI / editor video बनाने से पहले ये पढ़े._
_Last updated: 2026-10-31_

## 3 रंग के नियम (पहले ये समझो)
- 🟢 **GREEN — सब जगह OK:** खुद के Instagram/YouTube/brand + client/commercial काम, सब में बिना डर इस्तेमाल करो.
- 🟡 **YELLOW — शर्त के साथ OK:** इस्तेमाल कर सकते हो, पर credit देना ज़रूरी है (नीचे हर item में लिखा है क्या credit देना है).
- 🔴 **RED — सिर्फ़ खुद के लिए:** सिर्फ़ अपने personal Instagram/YouTube/brand के funny/reel content में. Client या commercial काम में बिल्कुल नहीं.
- ⚠️ **USER-FORCE RULE (सबसे ऊपर):** अगर user खुद साफ़ कह दे कि "इस्तेमाल करो, कोई दिक्कत नहीं है" — तो RED/YELLOW चीज़ भी इस्तेमाल कर सकते हो. ज़िम्मेदारी user की होगी. Agent पहले एक बार warning ज़रूर दे, फिर user कहे तो मान ले.

---

## 1. Sound Effects (SFX)
| चीज़ | कहाँ है | नियम |
|---|---|---|
| Library के अपने 29 WAV (pop, whoosh, ding, coin...) | `03 - Assets/` root files | 🟢 GREEN — खुद बनाए हुए/generated हैं, हर काम में OK |
| Wyzowl Essential 30 WAV + index | `03/SFX-Wyzowl-CC0-Safe/` | 🟢 GREEN — CC0 license (LICENSE file उसी folder में है). Client work में भी safe |
| Indian Meme Sounds 30 MP3 (MyInstants) | `03/SFX-Indian-Meme-OWN-USE-ONLY/` | 🔴 RED — ये meme/film/TV clips हैं, copyright का कोई भरोसा नहीं. सिर्फ़ खुद के funny reels. Client/commercial में नहीं. User force करे तो उसकी ज़िम्मेदारी |

## 2. Music
| चीज़ | कहाँ है | नियम |
|---|---|---|
| Library के 15 WAV tracks (lofi-chill, upbeat-corporate...) | `03 - Assets/` root files | 🟢 GREEN — generated tracks, हर काम में OK |
| Kevin MacLeod — Carefree, Wallpaper, Local Forecast - Elevator | `03/Music-Kevin MacLeod-CC-BY-Credit-Required/` | 🟡 YELLOW — CC BY 4.0. हर video (खुद का हो या client का) के description में credit ज़रूरी: `Music: Kevin MacLeod (incompetech.com) — CC BY 4.0` |
| Food Masti voiceover MP3s | `05 - Food Masti Project System/Audio-Voiceover/` | 🔴 सिर्फ़ Food Masti project के लिए. किसी और brand/client के video में आवाज़ इस्तेमाल मत करो |

## 3. Fonts — ⚠️ client काम से पहले LICENSE-NOTES.md (01 folder) ज़रूर check करो
| Font | नियम |
|---|---|
| Montserrat Full Family (20 files + OFL.txt) | 🟢 GREEN — SIL Open Font License 1.1, commercial use OK. License file उसी folder में है |
| Poppins-Bold, Inter-Bold, Nunito-Black, ArchivoBlack, PlayfairDisplay-Italic, EBGaramond-Italic, NotoSansDevanagari-Bold | 🟢 GREEN — Google Fonts (OFL), commercial OK |
| Coolvetica.otf, TheBoldFont-FreeVersion.ttf, KomikaAxis.ttf | 🟡/🔴 ध्यान दो — ये "free version" fonts हैं. खुद के काम में OK, पर **client/commercial काम से पहले इनकी website पर license verify करो** (paid license लग सकता है). User force करे तो उसकी ज़िम्मेदारी |

## 4. LUTs / Color Grades (.cube files)
| चीज़ | कहाँ है | नियम |
|---|---|---|
| slay 5 LUTs (amber, fade, neon, film, portrait) | `03/LUTs-Color-Grades/slay-*.cube` | 🟡 YELLOW — CC BY 4.0, credit: slaycamera.com (जहाँ हो सके वहाँ दो) |
| Film LUTs 4 (Kodak Kodachrome 64, Fuji Velvia 50, Kodak Portra 160, Fuji 400H) | `03/LUTs-Color-Grades/` बाकी .cube | 🟢 GREEN अपने/client video पर apply करके render करना OK. **पर .cube file को अलग से बेचना/बाँटना नहीं है** |

## 5. Video / Images
| चीज़ | कहाँ है | नियम |
|---|---|---|
| Completed Videos (Food Masti reel, Diwali, Showcase) | `Completed Videos/` | अपने बनाए हुए demo/portfolio videos हैं. Portfolio/showcase में दिखाना OK. Client को "ये sample है" कहकर दिखा सकते हो, बेचना नहीं है |
| Reference Videos (SnapYT downloads + YouTube references) | `04 - Reference Videos/` | 🔴 सिर्फ़ सीखने/मापने (analysis) के लिए. इनकी footage/footage का हिस्सा किसी video में मत डालो — न खुद के, न client के |
| Food Masti images (pani-puri, dahi-puri, sev-puri, logo...) | `05 - Food Masti Project System/Images/` | 🔴 सिर्फ़ Food Masti के videos के लिए (कुछ photos Wikimedia CC की हैं — ASSET-CREDITS.md देखो). किसी और client के काम में मत लगाओ |
| Gemini PDFs | `gemini/` | Research notes हैं, सिर्फ़ पढ़ने के लिए |

## 6. Code / Skills / Templates
| चीज़ | कहाँ है | नियम |
|---|---|---|
| अपना code (Captions.tsx, Motion.tsx, Templates.tsx, Thumbnail.tsx, scripts) | `02 - Components and Templates (Code)/` | 🟢 अपने हर video (खुद/client) में इस्तेमाल OK. पर code को अलग से बेचना नहीं है जब तक LICENSE-NOTES में साफ़ न लिखा हो |
| Skills / Guides (.md files) | `01 - Skills and Library/` | सीखने और video बनाने के लिए हैं. किसी और को library बेचनी हो तो fonts/code की third-party चीज़ें हटा कर — LICENSE-NOTES.md देखो |
| GitHub repos (GITHUB-REPOS-MASTER-LIST.md) | सिर्फ़ links हैं | हर repo का अपना license है (MIT/CC0 आदि list में लिखा है). Repo खोलकर license देखे बिना उसका code client काम में copy मत करो |

## जल्दी फैसला कैसे करें (agent के लिए)
1. चीज़ 🟢 है → लगा दो.
2. 🟡 है → लगा दो, credit description में डाल दो.
3. 🔴 है और video client/commercial है → **रोको**, user को बताओ "ये सिर्फ़ personal use के लिए है, इसकी जगह 🟢 विकल्प ये है".
4. User फिर भी कहे "करो, कोई दिक्कत नहीं" → कर दो (user-force rule), और delivery note में लिख दो कि user के कहने पर इस्तेमाल हुआ.
