#!/usr/bin/env python3
"""gkhackter — Cloudflare Workers Playground. Capture real screens, compose, encode."""
import os, json, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG      = (8, 8, 10)
INK     = (245, 245, 240)
ACCENT  = (255, 107, 44)
AMBER   = (255, 209, 102)
GREY    = (120, 122, 130)
CARD    = (20, 20, 24)

os.makedirs("shots", exist_ok=True)
BEATS = json.load(open("beats.json"))
TOTAL = BEATS[-1]["e"]

# ---------------- fonts ----------------
def F(size):
    for p in ["fonts/Montserrat-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                # variable fonts can load at weight 100 -> force bold via stroke later
                return f
            except Exception:
                pass
    return ImageFont.load_default()

def draw_bold(d, xy, txt, font, fill, width=0):
    d.text(xy, txt, font=font, fill=fill, stroke_width=width, stroke_fill=fill)

# ---------------- capture ----------------
def capture():
    from playwright.sync_api import sync_playwright
    jobs = [
        ("playground", "https://workers.cloudflare.com/playground", 9000),
        ("landing",    "https://workers.cloudflare.com/", 5000),
        ("limits",     "https://developers.cloudflare.com/workers/platform/limits/", 4000),
        ("guide",      "https://developers.cloudflare.com/workers/get-started/guide/", 4000),
    ]
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
        for name, url, wait in jobs:
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=70000)
                pg.wait_for_timeout(wait)
                pg.screenshot(path=f"shots/{name}.png")
                print(f"captured {name}", flush=True)
            except Exception as e:
                print(f"FAILED {name}: {e}", flush=True)
        b.close()

need = ("playground", "limits")
if not all(os.path.exists(f"shots/{n}.png") for n in need):
    try: capture()
    except Exception as e: print("capture error:", e, flush=True)

def load_shot(name):
    for cand in (f"shots/{name}.png", "shots/playground.png", "shots/landing.png", "shots/limits.png"):
        if os.path.exists(cand):
            return Image.open(cand).convert("RGB")
    return Image.new("RGB", (1440, 900), CARD)

SHOTS = {n: load_shot(n) for n in ("playground", "limits", "guide", "landing")}
URLS = {"playground": "workers.cloudflare.com/playground",
        "limits": "developers.cloudflare.com/workers/platform/limits",
        "guide": "developers.cloudflare.com/workers/get-started/guide",
        "landing": "workers.cloudflare.com"}

def round_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=r, fill=255)
    return m

def browser_card(shot, t, blen, cw, ch):
    bar = 58
    card = Image.new("RGB", (cw, ch), CARD)
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, cw, bar], fill=(32, 32, 38))
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([20+i*26, 20, 36+i*26, 36], fill=c)
    d.rounded_rectangle([120, 14, cw-18, bar-14], radius=14, fill=(16,16,20))
    u = URLS.get(shot, "")
    f = F(24)
    d.text(((cw+120)/2 - d.textlength(u, font=f)/2, 21), u, font=f, fill=(150,152,160))
    src = SHOTS.get(shot) or SHOTS["playground"]
    vw, vh = cw, ch-bar
    prog = min(1.0, t/max(blen,0.01))
    z = 1.0 + 0.035*prog                      # gentle push-in, never crops content
    bw, bh = vw*z, vh*z
    sc = min(bw/src.width, bh/src.height)     # CONTAIN: whole page always visible
    nw, nh = max(1,int(src.width*sc)), max(1,int(src.height*sc))
    crop = src.resize((nw, nh), Image.LANCZOS)
    px = (vw-nw)//2; py = (vh-nh)//2
    card.paste(crop, (0+px, bar+py))
    card.paste(crop, (0, bar))
    card.putalpha(round_mask((cw, ch), 24))
    return card

def fit(d, txt, maxw, start):
    s = start
    while s > 26:
        f = F(s)
        if d.textlength(txt, font=f) <= maxw: return f, s
        s -= 4
    return F(26), 26

def txt_pair(img, t1, t2, prog, y0, align="left", stroke=3):
    d = ImageDraw.Draw(img)
    maxw = W - 140
    f1, s1 = fit(d, t1, maxw, 104)
    f2, s2 = fit(d, t2, maxw, 104)
    b1 = d.textbbox((0,0), t1, font=f1); b2 = d.textbbox((0,0), t2, font=f2)
    h1, h2 = b1[3]-b1[1], b2[3]-b2[1]
    slide = int((1-min(1.0, prog/0.20))*46)
    for i,(tx,f,fill,hh) in enumerate(((t1,f1,INK,h1),(t2,f2,ACCENT,h2))):
        w = d.textlength(tx, font=f)
        x = 70 if align=="left" else (W-w)/2
        yy = y0 + (0 if i==0 else h1+16)
        d.text((x-slide, yy), tx, font=f, fill=fill, stroke_width=stroke, stroke_fill=fill)
    uw = int(d.textlength(t2, font=f2)*min(1.0, prog/0.32))
    x0 = 70 if align=="left" else (W-d.textlength(t2,font=f2))/2
    d.rectangle([x0, y0+h1+h2+40, x0+uw, y0+h1+h2+52], fill=AMBER)

def chrome(img, idx, t):
    d = ImageDraw.Draw(img)
    f = F(30)
    lab = "@gkhackter"
    d.text((W - 70 - d.textlength(lab, font=f), 66), lab, font=f, fill=(62,64,72))
    d.rectangle([0, H-9, W, H], fill=(22,22,26))
    d.rectangle([0, H-9, int(W*t/TOTAL), H], fill=ACCENT)
    for i in range(len(BEATS)):
        x = 70 + i*18
        d.rectangle([x, H-40, x+11, H-34], fill=ACCENT if i<=idx else (38,38,44))

def vignette(img):
    g = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(g)
    gd.rectangle([0,0,W,H], fill=0)
    for i in range(260):
        a = int(150*(1-i/260))
        gd.rectangle([i, i, W-i, H-i], outline=a)
    g = g.filter(ImageFilter.GaussianBlur(60))
    img.paste(Image.new("RGB",(W,H),BG), (0,0), g)

def frame(t):
    idx = len(BEATS)-1
    for i,b in enumerate(BEATS):
        if b["s"] <= t < b["e"]: idx = i; break
    b = BEATS[idx]
    local = t - b["s"]; blen = max(0.05, b["e"]-b["s"]); prog = min(1.0, local/blen)
    lay = b.get("lay","card_top")

    img = Image.new("RGB",(W,H),BG)
    if lay == "full":
        card = browser_card(b["shot"], local, blen, W-56, 1230)
        img.paste(card, (28, 150), card)
        ov = Image.new("L",(W,H),0)
        ImageDraw.Draw(ov).rectangle([0,1130,W,H], fill=215)
        ov = ov.filter(ImageFilter.GaussianBlur(70))
        img.paste(Image.new("RGB",(W,H),BG),(0,0),ov)
        txt_pair(img, b["t1"], b["t2"], prog, 1240)
    elif lay == "giant":
        card = browser_card(b["shot"], local, blen, W-120, 1060)
        card.putalpha(card.getchannel("A").point(lambda v:int(v*0.30)))
        img.paste(card, (60, 120), card)
        d = ImageDraw.Draw(img)
        panel = Image.new("RGBA", (W, 560), (0,0,0,0))
        ImageDraw.Draw(panel).rounded_rectangle([40,0,W-40,560], radius=34, fill=(8,8,10,238))
        img.paste(panel, (0, 560), panel)
        f, sz = fit(d, b["t2"], W-140, 118)
        fbig = F(min(190, int(sz*1.75)))
        w1 = d.textlength(b["t1"], font=fbig)
        y = 600
        d.text(((W-w1)/2, y), b["t1"], font=fbig, fill=INK, stroke_width=5, stroke_fill=INK)
        w2 = d.textlength(b["t2"], font=f)
        d.text(((W-w2)/2, y+230), b["t2"], font=f, fill=ACCENT, stroke_width=3, stroke_fill=ACCENT)
        uw = int(w2*min(1.0,prog/0.3))
        d.rectangle([(W-w2)/2, y+230+sz+30, (W-w2)/2+uw, y+230+sz+44], fill=AMBER)
    elif lay == "card_bot":
        txt_pair(img, b["t1"], b["t2"], prog, 210)
        card = browser_card(b["shot"], local, blen, W-80, 1180)
        img.paste(card, (40, 600), card)
    else:  # card_top
        card = browser_card(b["shot"], local, blen, W-80, 1210)
        img.paste(card, (40, 160), card)
        txt_pair(img, b["t1"], b["t2"], prog, 1420)

    chrome(img, idx, t)
    return img

def main():
    n = int(round(TOTAL*FPS))
    print(f"{n} frames {W}x{H} {FPS}fps {TOTAL}s", flush=True)
    cmd = ["ffmpeg","-y","-v","error",
           "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
           "-i","voice.wav","-i","channel-bgm.mp3",
           "-filter_complex",
           "[1:a]volume=1.0[v];[2:a]volume=0.15,atrim=0:42.1,afade=t=out:st=38.5:d=3.5[bg];"
           "[v][bg]amix=inputs=2:duration=first:dropout_transition=0[mix];"
           "[mix]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map","0:v","-map","[a]",
           "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
           "-movflags","+faststart","-c:a","aac","-b:a","192k","-shortest","video.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 200 == 0: print(f"  {i}/{n}", flush=True)
    p.stdin.close(); p.wait()
    print("encode exit", p.returncode, flush=True)
    frame(27.6).save("thumb.png")
    print("thumb saved", flush=True)

main()
