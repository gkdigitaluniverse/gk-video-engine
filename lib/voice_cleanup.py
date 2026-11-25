#!/usr/bin/env python3
"""Voice cleanup: DeepFilterNet हो तो वही (best), वरना ffmpeg fallback chain.
Usage: python3 voice_cleanup.py in.wav out.wav
Original को कभी overwrite मत करो — हमेशा नई file दो।"""
import sys, subprocess, shutil

def main():
    if len(sys.argv) != 3:
        print("Usage: voice_cleanup.py <in.wav> <out.wav>"); sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    if shutil.which("deepFilter"):
        # DeepFilterNet CLI: deepFilter in.wav --output-dir <dir>
        import os, tempfile
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["deepFilter", src, "--output-dir", d], check=True)
            made = [f for f in os.listdir(d) if f.endswith(".wav")]
            if made:
                shutil.copy(os.path.join(d, made[0]), dst)
                print("OK (DeepFilterNet):", dst); return
    # Fallback: high-pass (room rumble) + FFT denoise + gentle normalize
    subprocess.run(["ffmpeg", "-y", "-i", src,
                    "-af", "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5",
                    dst], check=True)
    print("OK (ffmpeg fallback):", dst)

if __name__ == "__main__":
    main()
