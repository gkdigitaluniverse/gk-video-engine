#!/usr/bin/env python3
"""Render the gkhackter Cloudflare video: capture real screens, compose, encode."""
import os, json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG      = (10, 10, 12)
INK     = (245, 245, 240)
ACCENT  = (255, 107, 44)
AMBER   = (255, 209, 102)
GREY    = (110, 112, 120)
CARD    = (20, 20, 24)

os.makedirs("shots", exist_ok=True)
os.makedirs("fonts", exist_ok=True)
BEATS = json.load(open("beats.json"))

# ---------- fonts ----------
def get_font(size, bold=True):
    for p in ["fonts/Montserrat-Bold.ttf" if bold else "fonts/Montserrat-Medium.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

F_HUGE = get_font(104)
F_BIG  = get_font(86)
F_MID  = get_font(52)
F_SM   = get_font(34, bold=False)
F_TINY = get_font(28, bold=False)

# ---------- capture ----------
def capture():
    from playwright.sync_api import sync_playwright
    jobs = [
        ("playground", "https://workers.cloudflare.com/", 5000),
        ("limits", "https://developers.cloudflare.com/workers/platform/limits/", 4000),
        ("guide", "https://developers.cloudflare.com/workers/get-started/guide/", 4000),
    ]
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        for name, url, wait in jobs:
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(wait)
                pg.screenshot(path=f"shots/{name}.png")
                print(f"captured {name} from {url}", flush=True)
            except Exception as e:
                print(f"FAILED {name}: {e}", flush=True)
        b.close()

if not all(os.path.exists(f"shots/{n}.png") for n in ("playground", "limits")):
    try:
        capture()
    except Exception as e:
        print("capture error:", e, flush=True)

# ---------- browser card ----------
CARD_X, CARD_Y, CARD_W, CARD_H = 56, 150, 968, 1080
BAR_H = 62

def load_shot(name):
    p = f"shots/{name}.png"
    if not os.path.exists(p):
        p = "shots/playground.png"
    if not os.path.exists(p):
        return Image.new("RGB", (CARD_W, CARD_H - BAR_H), CARD)
    im = Image.open(p).convert("RGB")
    tw, th = CARD_W, CARD_H - BAR_H
    r = max(tw / im.width, th / im.height) * 1.35   # oversize for zoom room
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return im

SHOTS = {n: load_shot(n) for n in ("playground", "limits", "guide")}
URLS = {"playground": "workers.cloudflare.com", "limits": "developers.cloudflare.com/workers/platform/limits",
        "guide": "developers.cloudflare.com/workers/get-started/guide"}

def round_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m

CARD_MASK = round_mask((CARD_W, CARD_H), 26)

def build_card(shot_name, t_in_beat, beat_len):
    """Card with browser chrome + slowly zooming real screenshot."""
    card = Image.new("RGB", (CARD_W, CARD_H), CARD)
    d = ImageDraw.Draw(card)
    # chrome bar
    d.rectangle([0, 0, CARD_W, BAR_H], fill=(30, 30, 36))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([22 + i * 30, 22, 40 + i * 30, 40], fill=c)
    d.rounded_rectangle([130, 16, CARD_W - 22, BAR_H - 16], radius=15, fill=(18, 18, 22))
    url = URLS.get(shot_name, "")
    f = F_TINY
    tw = d.textlength(url, font=f)
    d.text(((CARD_W + 130) / 2 - tw / 2, 24), url, font=f, fill=(150, 152, 160))

    # screenshot window with slow zoom
    src = SHOTS.get(shot_name) or SHOTS["playground"]
    vw, vh = CARD_W, CARD_H - BAR_H
    prog = min(1.0, t_in_beat / max(beat_len, 0.01))
    zoom = 1.0 + 0.10 * prog
    cw, ch = int(vw * zoom), int(vh * zoom)
    cx = (src.width - cw) // 2
    cy = max(0, int((src.height - ch) * 0.42))
    crop = src.crop((cx, cy, cx + cw, cy + ch)).resize((vw, vh), Image.LANCZOS)
    card.paste(crop, (0, BAR_H))
    card.putalpha(CARD_MASK)
    return card

# ---------- text ----------
def fit_font(draw, text, max_w, start_size, bold=True):
    size = start_size
    while size > 30:
        f = get_font(size, bold)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return get_font(30, bold)

def draw_text_block(img, t1, t2, prog):
    d = ImageDraw.Draw(img)
    maxw = W - 130
    f1 = fit_font(d, t1, maxw, 100)
    f2 = fit_font(d, t2, maxw, 100)
    h1 = d.textbbox((0, 0), t1, font=f1)[3]
    h2 = d.textbbox((0, 0), t2, font=f2)[3]
    gap = 18
    total = h1 + gap + h2
    y = 1320 + (150 - total) // 2
    # slide-in
    slide = int((1 - min(1.0, prog / 0.22)) * 40)
    d.text((64 - slide, y), t1, font=f1, fill=INK)
    d.text((64 - slide, y + h1 + gap), t2, font=f2, fill=ACCENT)
    # accent underline grows under t2
    lw = d.textlength(t2, font=f2)
    uw = int(lw * min(1.0, prog / 0.35))
    d.rectangle([64, y + h1 + gap + h2 + 20, 64 + uw, y + h1 + gap + h2 + 30], fill=AMBER)

def draw_chrome(img, beat_idx, prog_total):
    d = ImageDraw.Draw(img)
    d.text((W - 250, 74), "@gkhackter", font=F_MID, fill=(70, 72, 80))
    # progress bar
    d.rectangle([0, H - 10, W, H], fill=(24, 24, 28))
    d.rectangle([0, H - 10, int(W * prog_total), H], fill=ACCENT)
    # beat pips
    n = len(BEATS)
    for i in range(n):
        x = 56 + i * 20
        d.rectangle([x, H - 42, x + 12, H - 36],
                    fill=ACCENT if i <= beat_idx else (40, 40, 46))

# ---------- frames ----------
def frame_for(t):
    idx = 0
    for i, b in enumerate(BEATS):
        if b["s"] <= t < b["e"]:
            idx = i
            break
    else:
        idx = len(BEATS) - 1
    b = BEATS[idx]
    local = t - b["s"]
    blen = max(0.05, b["e"] - b["s"])
    prog = min(1.0, local / blen)

    img = Image.new("RGB", (W, H), BG)
    # subtle vignette blocks
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 120], fill=BG)

    card = build_card(b["shot"], local, blen)
    img.paste(card, (CARD_X, CARD_Y), card)

    draw_text_block(img, b["t1"], b["t2"], prog)
    draw_chrome(img, idx, t / BEATS[-1]["e"])
    return img

def main():
    total = BEATS[-1]["e"]
    nframes = int(round(total * FPS))
    print(f"rendering {nframes} frames at {W}x{H} {FPS}fps for {total}s", flush=True)
    cmd = ["ffmpeg", "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", "voice.wav",
           "-i", "channel-bgm.mp3",
           "-filter_complex",
           "[1:a]volume=1.0[v];[2:a]volume=0.16,atrim=0:42.1,afade=t=out:st=38.5:d=3.5[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest",
           "video-noaudio.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nframes):
        t = i / FPS
        fr = frame_for(t)
        p.stdin.write(fr.tobytes())
        if i % 150 == 0:
            print(f"  frame {i}/{nframes}", flush=True)
    p.stdin.close()
    p.wait()
    print("encode exit", p.returncode, flush=True)

    # thumbnail from the strongest beat
    img = frame_for(27.6)
    img.save("thumb.png")
    print("thumb saved", flush=True)

main()
