#!/bin/bash
U='https://elevenlabsusercontent.com/database/workspace/66f2b42f1c6d4839af89eb4b92f33586/content_generation/iOcNGHJ6TI6yCziW2k5N/DfYsFo8LqnpMPu8pzvWm/content.mp3?Expires=1795496400&KeyName=assets-cdn-key-1&Signature=i2xzCGQDJhON3JKJqa9rhDdGAkk='
echo "date: $(date -u)  IST: $(TZ=Asia/Kolkata date)"
code=$(curl -sL --max-time 180 -A "Mozilla/5.0" "$U" -o voice.mp3 -w "%{http_code}")
echo "HTTP $code bytes $(stat -c%s voice.mp3 2>/dev/null || echo 0)"
file voice.mp3
ffprobe -v error -show_entries format=duration,bit_rate -of default=nw=1 voice.mp3 2>&1 | head -4
