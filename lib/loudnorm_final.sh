#!/bin/bash
# Usage: loudnorm_final.sh in.mp4 out.mp4  (final -14 LUFS, true-peak -1)
ffmpeg -y -i "$1" -af loudnorm=I=-14:TP=-1:LRA=11 -c:v copy "$2" && echo "OK: $2"
