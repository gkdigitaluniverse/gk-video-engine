#!/usr/bin/env python3
"""Speaker cutout (sticker style) के लिए background हटाओ।
चाहिए: pip install rembg  (पहली बार model download होगा)
Usage: python3 remove_background.py in.png out.png
Video के लिए: पहले ffmpeg से frames निकालो, हर frame पर चलाओ, फिर image-sequence की तरह Remotion में जोड़ो।"""
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: remove_background.py <in.png> <out.png>"); sys.exit(1)
    try:
        from rembg import remove
    except ImportError:
        print("rembg नहीं है — पहले: pip install rembg"); sys.exit(2)
    with open(sys.argv[1], "rb") as f:
        data = f.read()
    with open(sys.argv[2], "wb") as f:
        f.write(remove(data))
    print("OK:", sys.argv[2])

if __name__ == "__main__":
    main()
