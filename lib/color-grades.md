# Color Grade Presets (FFmpeg) — copy-paste

Phone footage को एक जैसा premium look देने के लिए। हमेशा पहले 5s test render करके frame देखो, फिर पूरे पर लगाओ।

## 1. Clean Punch (default, food/reel)
```
ffmpeg -i in.mp4 -vf "eq=contrast=1.08:saturation=1.18:brightness=0.02,unsharp=5:5:0.6" -c:a copy out.mp4
```

## 2. Warm Food (खाना appetizing लगे)
```
ffmpeg -i in.mp4 -vf "colorbalance=rs=0.08:gs=0.02:bs=-0.08,eq=saturation=1.22:contrast=1.05" -c:a copy out.mp4
```

## 3. Dark Moody (navy creator style के साथ)
```
ffmpeg -i in.mp4 -vf "eq=contrast=1.15:saturation=0.92:brightness=-0.03,curves=all='0/0 0.5/0.48 1/0.96'" -c:a copy out.mp4
```

## 4. Soft/Clean Talking Head
```
ffmpeg -i in.mp4 -vf "eq=contrast=1.04:saturation=1.05:brightness=0.03,unsharp=5:5:0.4" -c:a copy out.mp4
```

## 5. Screen Recording Clarity (app demo — कोई color change नहीं, सिर्फ़ sharpen)
```
ffmpeg -i in.mp4 -vf "unsharp=5:5:0.8,eq=contrast=1.03" -c:a copy out.mp4
```

## नियम
- एक video = एक grade. Scenes के बीच grade मत बदलो।
- Skin tones देखकर ही final — चेहरा orange/red हो तो saturation 0.05 घटाओ।
- Grade हमेशा crop/blur के बाद, loudnorm से पहले लगाओ।
- Screenshot/UI assets पर grade नहीं — सिर्फ़ camera footage पर।
