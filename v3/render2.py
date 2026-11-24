#!/usr/bin/env python3
"""gkhackter v2 — layered motion graphics over the REAL screen recording."""
import os, json, math, subprocess, glob, shutil

W, H, FPS = 1080, 1920, 30
CREAM  = (236, 236, 231)
INK    = (20, 20, 20)
ORANGE = (234, 88, 12)
AMBER  = (255, 176, 32)
DIM    = (150, 148, 142)
WHITE  = (255, 255, 255)

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BEATS = json.load(open("beats.json"))
TOTAL = BEATS[-1]["e"]
os.makedirs("frames", exist_ok=True)

# ---------- font ----------
def F(sz):
    for p in ["fonts/Montserrat-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

# ---------- extract recording frames at 30fps ----------
REC = "rec/play.mp4"
FDIR = "frames"
if not os.path.exists(f"{FDIR}/000000.jpg"):
    print("extracting recording frames...", flush=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",REC,"-vf","fps=30",
                    "-q:v","3", f"{FDIR}/%06d.jpg"], check=False)
RF = sorted(glob.glob(f"{FDIR}/*.jpg"))
print("recording frames:", len(RF), flush=True)
_cache = {}
def rec_frame(i):
    if not RF: return Image.new("RGB",(1280,800),INK)
    i = max(0, min(len(RF)-1, i))
    if i not in _cache:
        if len(_cache) > 90: _cache.clear()
        _cache[i] = Image.open(RF[i]).convert("RGB")
    return _cache[i]

# ---------- beat -> recording window + crop ----------
# (rec_start_sec, crop_box on 1280x800, ken_burns_zoom)
PLAN = {
 "B1":  (8.0,  (0,   0, 1280, 800), 1.00),
 "B2":  (10.6, (60,  60, 700,  640), 1.06),
 "B3":  (13.4, (60,  60, 700,  640), 1.10),
 "B4":  (2.2,  (0,   0, 1280, 800), 1.00),
 "B5":  (18.6, (60,  60, 1220, 640), 1.04),
 "B6":  (21.8, (60,  60, 1220, 700), 1.06),
 "B7":  (25.6, (760, 560, 520,  240), 1.14),
 "B8":  (26.4, (280, 0,  720,  520), 1.02),
 "B9":  (27.2, (280, 0,  720,  420), 1.12),
 "B10": (28.2, (280, 0,  720,  420), 1.16),
 "B11": (29.6, (280, 0,  720,  520), 1.04),
 "B12": (30.6, (280, 0,  720,  520), 1.02),
 "B13": (6.0,  (0,   0, 1280, 800), 1.04),
 "B14": (8.6,  (0,   0, 1280, 800), 1.00),
}

def ease(x):
    return 1 - (1 - min(1.0, max(0.0, x))) ** 3

# ---------- layers ----------
def dot_grid(t, prog):
    g = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(g)
    off = int((t * 9) % 44)
    for y in range(-44, H + 44, 44):
        for x in range(-44, W + 44, 44):
            d.ellipse([x + off - 2, y + off // 2 - 2, x + off + 2, y + off // 2 + 2],
                      fill=(214, 212, 205))
    return g

def floaters(t, seed):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    specs = [((ORANGE, 90), 0.9, 140, 300), ((AMBER, 80), 1.3, 820, 260),
             ((ORANGE, 70), 0.7, 880, 1500), ((AMBER, 90), 1.1, 170, 1620)]
    for i, ((col, sz), spd, bx, by) in enumerate(specs):
        a = t * spd + seed + i * 1.7
        x = bx + math.sin(a) * 34
        y = by + math.cos(a * 0.8) * 26
        alpha = 26 + int(14 * (0.5 + 0.5 * math.sin(a * 1.4)))
        d.ellipse([x - sz/2, y - sz/2, x + sz/2, y + sz/2], fill=col + (alpha,))
    return lay

def browser_frame(screen_img, prog, url, card):
    """Real recording inside a browser card. card=(x,y,w,h)."""
    x, y, w, h = card
    bar = 54
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, w, h], radius=22, fill=(255, 255, 255, 255))
    d.rounded_rectangle([0, 0, w, bar], radius=22, fill=(28, 28, 32, 255))
    d.rectangle([0, bar - 22, w, bar], fill=(28, 28, 32, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([16 + i*24, 18, 32 + i*24, 34], fill=c + (255,))
    d.rounded_rectangle([108, 12, w - 16, bar - 12], radius=12, fill=(14, 14, 18, 255))
    f = F(22)
    d.text(((w + 108) / 2 - d.textlength(url, font=f) / 2, 18), url, font=f, fill=(160, 162, 170, 255))
    # content
    cw, ch = w - 4, h - bar - 2
    shot = screen_img.resize((cw, ch), Image.LANCZOS)
    out.paste(shot, (2, bar + 1))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=22, fill=255)
    out.putalpha(mask)
    return out

def callout_ring(draw_img, cx, cy, r, prog, col=ORANGE):
    if prog <= 0: return
    p = ease(min(1.0, prog / 0.45))
    rr = int(r * (0.5 + 0.5 * p))
    a = int(235 * p)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col + (a,), width=7)
    draw_img.alpha_composite(ov)

def kinetic_text(base, t1, t2, prog, y0, size=100, col1=INK, col2=ORANGE, align="left"):
    d = ImageDraw.Draw(base)
    maxw = W - 120
    def fit(txt, s):
        while s > 30:
            f = F(s)
            if d.textlength(txt, font=f) <= maxw: return f
            s -= 4
        return F(30)
    f1 = fit(t1, size); f2 = fit(t2, size)
    words = [(t1, f1, col1), (t2, f2, col2)]
    yy = y0
    idx = 0
    for txt, f, col in words:
        parts = txt.split()
        line = ""
        lines = []
        for wd in parts:
            test = (line + " " + wd).strip()
            if d.textlength(test, font=f) <= maxw:
                line = test
            else:
                lines.append(line); line = wd
        if line: lines.append(line)
        for ln in lines:
            appear = min(1.0, max(0.0, (prog - idx * 0.10) / 0.30))
            if appear > 0:
                sl = int((1 - ease(appear)) * 34)
                d.text((62 - sl, yy), ln, font=f, fill=col + (int(255 * appear),))
            hh = d.textbbox((0, 0), ln, font=f)[3]
            yy += hh + 8
            idx += 1
        yy += 6
    return yy

def chrome(base, idx, t):
    d = ImageDraw.Draw(base)
    f = F(28)
    lab = "@gkhackter"
    d.text((W - 60 - d.textlength(lab, font=f), 58), lab, font=f, fill=(120, 118, 112, 255))
    d.rectangle([0, H - 9, W, H], fill=(214, 212, 205, 255))
    d.rectangle([0, H - 9, int(W * t / TOTAL), H], fill=ORANGE + (255,))
    for i in range(len(BEATS)):
        x = 62 + i * 17
        d.rectangle([x, H - 38, x + 10, H - 32],
                    fill=(ORANGE + (255,)) if i <= idx else ((190, 188, 182) + (255,)))

def big_counter(base, value, label, prog, sub=""):
    d = ImageDraw.Draw(base)
    panel = Image.new("RGBA", (W, 470), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle([40, 0, W - 40, 470], radius=30, fill=(20, 20, 20, 238))
    base.alpha_composite(panel, (0, 700))
    shown = int(value * ease(min(1.0, prog / 0.6)))
    txt = f"{shown:,}"
    f = F(150)
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, 720), txt, font=f, fill=WHITE + (255,))
    f2 = F(52)
    w2 = d.textlength(label, font=f2)
    d.text(((W - w2) / 2, 900), label, font=f2, fill=AMBER + (255,))
    if sub:
        f3 = F(34)
        w3 = d.textlength(sub, font=f3)
        d.text(((W - w3) / 2, 980), sub, font=f3, fill=(200, 200, 196, 255))
    uw = int((w) * min(1.0, prog / 0.5))
    d.rectangle([(W - w) / 2, 890, (W - w) / 2 + uw, 898], fill=AMBER + (255,))

# ---------- compose ----------
def frame(t):
    idx = len(BEATS) - 1
    for i, b in enumerate(BEATS):
        if b["s"] <= t < b["e"]: idx = i; break
    b = BEATS[idx]
    local = t - b["s"]; blen = max(0.05, b["e"] - b["s"]); prog = min(1.0, local / blen)
    rid = b["id"]
    rstart, crop, kb = PLAN.get(rid, (5.0, (0,0,1280,800), 1.0))

    base = dot_grid(t, prog).convert("RGBA")
    base.alpha_composite(floaters(t, idx * 1.9))

    # real recording, ken-burns zoom inside the crop
    rf = rec_frame(int((rstart + local) * 30))
    cx, cy, cw, ch = crop
    z = 1.0 + (kb - 1.0) * ease(prog)
    sw, sh = int(cw / z), int(ch / z)
    ox = cx + (cw - sw) // 2
    oy = cy + (ch - sh) // 2
    shot = rf.crop((ox, oy, ox + sw, oy + sh))

    lay = b.get("lay", "card_top")
    if lay == "full":
        card = browser_frame(shot, prog, b.get("url", "workers.cloudflare.com/playground"), (36, 150, W - 72, 1180))
        base.alpha_composite(card, (36, 150))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle([0, 1120, W, H], fill=(236, 236, 231, 250))
        base.alpha_composite(ov.filter(ImageFilter.GaussianBlur(40)))
        kinetic_text(base, b["t1"], b["t2"], prog, 1250)
    elif lay == "counter":
        card = browser_frame(shot, prog, b.get("url", ""), (36, 90, W - 72, 620))
        base.alpha_composite(card, (36, 90))
        big_counter(base, b.get("num", 0), b["t1"], prog, b.get("sub", ""))
    elif lay == "card_bot":
        kinetic_text(base, b["t1"], b["t2"], prog, 210)
        card = browser_frame(shot, prog, b.get("url", ""), (48, 620, W - 96, 1000))
        base.alpha_composite(card, (48, 620))
    else:
        card = browser_frame(shot, prog, b.get("url", ""), (48, 140, W - 96, 1000))
        base.alpha_composite(card, (48, 140))
        kinetic_text(base, b["t1"], b["t2"], prog, 1200)

    if b.get("ring"):
        rx, ry, rr = b["ring"]
        callout_ring(base, rx, ry, rr, prog)

    chrome(base, idx, t)
    return base.convert("RGB")

def main():
    n = int(round(TOTAL * FPS))
    print(f"{n} frames", flush=True)
    cmd = ["ffmpeg","-y","-v","error",
           "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
           "-i","voice.wav","-i","channel-bgm.mp3",
           "-filter_complex",
           "[1:a]volume=1.0[v];[2:a]volume=0.13,atrim=0:42.1,afade=t=out:st=38.5:d=3.5[bg];"
           "[v][bg]amix=inputs=2:duration=first:dropout_transition=0[mix];"
           "[mix]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map","0:v","-map","[a]",
           "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
           "-movflags","+faststart","-c:a","aac","-b:a","192k","-shortest","video2.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 200 == 0: print(" ", i, flush=True)
    p.stdin.close(); p.wait()
    print("exit", p.returncode, flush=True)
    for tt, nm in ((1.2, "t1"), (8.0, "t2"), (28.0, "t3"), (41.0, "t4")):
        frame(tt).save(f"check_{nm}.png")
    frame(27.8).save("thumb2.png")
    print("done", flush=True)

main()
