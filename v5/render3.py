#!/usr/bin/env python3
"""gkhackter v3 — full-bleed dashboard language, built from the vivid reference descriptions."""
import os, json, math, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
NAVY   = (10, 14, 32)
INK    = (8, 10, 20)
WHITE  = (246, 247, 252)
GREY   = (140, 146, 170)
ORANGE = (255, 122, 48)
AMBER  = (255, 190, 70)
TEAL   = (60, 210, 180)
RED    = (255, 92, 92)

BEATS = json.load(open("beats.json"))
TOTAL = BEATS[-1]["e"]
FDIR = "frames"

def F(sz):
    for p in ["fonts/Montserrat-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

RF = sorted(glob.glob(f"{FDIR}/*.jpg"))
_c = {}
def rf(i):
    if not RF: return Image.new("RGB",(1280,800),INK)
    i = max(0, min(len(RF)-1, i))
    if i not in _c:
        if len(_c) > 80: _c.clear()
        _c[i] = Image.open(RF[i]).convert("RGB")
    return _c[i]

def ease(x): return 1 - (1 - min(1.0, max(0.0, x))) ** 3

# ---------- background ----------
_glow = None
def background(t, hue):
    global _glow
    g = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(g)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(10 + 6*k), int(14 + 4*k), int(32 - 18*k)))
    if _glow is None:
        gl = Image.new("RGB", (W, H), (0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.ellipse([-300, -420, W + 300, 900], fill=hue)
        _glow = gl.filter(ImageFilter.GaussianBlur(180))
    g = Image.blend(g, _glow, 0.30)
    # drifting fine grid
    d = ImageDraw.Draw(g)
    off = int((t * 12) % 60)
    for x in range(-60, W + 60, 60):
        d.line([(x + off, 0), (x + off, H)], fill=(24, 30, 54))
    for y in range(-60, H + 60, 60):
        d.line([(0, y + off // 2), (W, y + off // 2)], fill=(22, 28, 50))
    return g

def ghost(base, txt, prog, y=520):
    d = ImageDraw.Draw(base)
    f = F(430)
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=(28, 34, 62))

# ---------- fixed header ----------
def header(base, kicker, title, sub):
    d = ImageDraw.Draw(base)
    fk, ft, fs = F(26), F(56), F(28)
    d.text((64, 96), kicker.upper(), font=fk, fill=AMBER + (255,))
    d.rectangle([64, 134, 64 + d.textlength(kicker.upper(), font=fk), 138], fill=AMBER + (255,))
    d.text((64, 168), title, font=ft, fill=WHITE + (255,))
    d.text((64, 244), sub, font=fs, fill=GREY + (255,))

# ---------- hero: recording panel ----------
def panel(base, shot, prog, box, url, kb=1.10):
    x, y, w, h = box
    bar = 52
    card = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0,0,w,h], radius=20, fill=(20,24,44,255))
    d.rounded_rectangle([0,0,w,bar], radius=20, fill=(30,36,62,255))
    d.rectangle([0,bar-20,w,bar], fill=(30,36,62,255))
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([16+i*22,17,30+i*22,31], fill=c+(255,))
    d.rounded_rectangle([96,12,w-14,bar-12], radius=11, fill=(16,20,38,255))
    f = F(21)
    d.text(((w+96)/2 - d.textlength(url,font=f)/2, 18), url, font=f, fill=(150,156,182,255))
    cw, ch = w-4, h-bar-2
    z = 1.0 + (kb-1.0)*ease(prog)
    sw, sh = int(shot.width/z), int(shot.height/z)
    ox = (shot.width-sw)//2; oy = (shot.height-sh)//2
    im = shot.crop((ox,oy,ox+sw,oy+sh)).resize((cw,ch), Image.LANCZOS)
    card.paste(im,(2,bar+1))
    m = Image.new("L",(w,h),0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,w,h], radius=20, fill=255)
    card.putalpha(m)
    base.alpha_composite(card,(x,y))

# ---------- hero: animated data rows ----------
def data_rows(base, rows, prog, box, y0=None):
    x, y, w, h = box
    d = ImageDraw.Draw(base)
    rowh = h // max(1, len(rows))
    for i, r in enumerate(rows):
        appear = min(1.0, max(0.0, (prog - i*0.10) / 0.30))
        if appear <= 0: continue
        ry = y + i*rowh
        sl = int((1-ease(appear))*50)
        col = r.get("col", WHITE)
        # label
        fl = F(34)
        d.text((x+sl, ry+12), r["label"], font=fl, fill=col+(int(255*appear),))
        # value counting
        fv = F(40)
        vtxt = r["value"]
        if r.get("num") is not None:
            cp = min(1.0, max(0.0,(prog - i*0.10 - 0.15)/0.55))
            v = r["num"] if cp>=0.98 else int(r["num"]*ease(cp))
            vtxt = f"{v:,}" + r.get("suffix","")
        vw = d.textlength(vtxt, font=fv)
        d.text((x+w-vw-sl, ry+8), vtxt, font=fv, fill=col+(int(255*appear),))
        # bar
        bw = int((w-20) * min(1.0, r.get("frac",0.8)) * ease(appear))
        d.rounded_rectangle([x+sl, ry+rowh-22, x+sl+bw, ry+rowh-12], radius=5,
                            fill=r.get("bcol", ORANGE)+(int(230*appear),))
        if r.get("strike") and appear > 0.5:
            d.line([(x, ry+28), (x+w, ry+28)], fill=RED+(220,), width=5)

# ---------- caption + callout ----------
def caption(base, t1, t2, prog, y):
    d = ImageDraw.Draw(base)
    def fit(txt, s):
        while s > 26:
            f = F(s)
            if d.textlength(txt, font=f) <= W-128: return f
            s -= 3
        return F(26)
    f1, f2 = fit(t1, 74), fit(t2, 74)
    a1 = min(1.0, max(0.0, prog/0.25)); a2 = min(1.0, max(0.0, (prog-0.12)/0.25))
    d.text((64, y), t1, font=f1, fill=WHITE+(int(255*a1),))
    h1 = d.textbbox((0,0), t1, font=f1)[3]
    d.text((64, y+h1+6), t2, font=f2, fill=ORANGE+(int(255*a2),))
    uw = int(d.textlength(t2, font=f2)*min(1.0,prog/0.35))
    d.rectangle([64, y+h1+6+d.textbbox((0,0),t2,font=f2)[3]+14,
                 64+uw, y+h1+6+d.textbbox((0,0),t2,font=f2)[3]+22], fill=AMBER+(255,))

def callout(base, label, text, prog):
    d = ImageDraw.Draw(base)
    x, y, w, h = 64, 1560, W-128, 168
    a = int(255*min(1.0, max(0.0,(prog-0.2)/0.4)))
    if a <= 0: return
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x,y,x+w,y+h], radius=18, fill=(18,22,42,a))
    od.rounded_rectangle([x,y,x+w,y+h], radius=18, outline=(58,66,104,a), width=2)
    base.alpha_composite(ov)
    d.text((x+22, y+16), label.upper(), font=F(22), fill=AMBER+(a,))
    f = F(27)
    words = text.split(); line=""; yy=y+52
    for wd in words:
        t=(line+" "+wd).strip()
        if d.textlength(t,font=f)<=w-44: line=t
        else:
            d.text((x+22,yy),line,font=f,fill=(214,218,236,a)); yy+=34; line=wd
    if line: d.text((x+22,yy),line,font=f,fill=(214,218,236,a))

def footer(base, src, idx, t):
    d = ImageDraw.Draw(base)
    d.text((64, 1786), src, font=F(22), fill=(96,102,128,255))
    d.rectangle([0,H-8,W,H], fill=(26,30,52,255))
    d.rectangle([0,H-8,int(W*t/TOTAL),H], fill=ORANGE+(255,))
    for i in range(len(BEATS)):
        x = 64+i*17
        d.rectangle([x,H-36,x+10,H-30], fill=(ORANGE+(255,)) if i<=idx else ((52,58,88,255)))

# ---------- beat plan ----------
PLAN = {
 "B1":  dict(hero="panel", rec=8.0,  ghost="0",  kicker="free tier",  title="No server. No account.", sub="Cloudflare Workers Playground", call=("hook","Kisi bhi API ko browser mein test karo, bina server khareede."), src="developers.cloudflare.com/workers/playground · checked 24 Nov 2026"),
 "B2":  dict(hero="rows",  ghost="1", kicker="the setup you skip", title="What you normally need", sub="the usual local path", call=("context","Chhota web app banate ho? Pehle poora setup karna padta hai."), src="developers.cloudflare.com/workers/get-started/guide · checked 24 Nov 2026",
            rows=[dict(label="Node.js install", value="step 1", frac=.55, col=RED, strike=True, bcol=RED),
                  dict(label="npm / wrangler setup", value="step 2", frac=.72, col=RED, strike=True, bcol=RED),
                  dict(label="Deploy to test", value="step 3", frac=.88, col=RED, strike=True, bcol=RED)]),
 "B3":  dict(hero="panel", rec=10.6, ghost="2", kicker="free tier", title="Cloudflare Workers Playground", sub="account banaye bina, code likho", call=("value","Playground kholo, code likho, live preview dekho. Koi sign-in nahi."), src="workers.cloudflare.com/playground · checked 24 Nov 2026"),
 "B4":  dict(hero="rows",  ghost="3", kicker="before vs now", title="Pehle deploy, ab preview", sub="same second", call=("value","Pehle project setup aur deploy karna padta tha. Ab editor aur preview saath chalte hain."), src="workers.cloudflare.com/playground · checked 24 Nov 2026",
            rows=[dict(label="Pehle: setup + deploy", value="minutes", frac=.9, col=RED, bcol=RED),
                  dict(label="Ab: editor + preview", value="live", frac=.35, col=TEAL, bcol=TEAL)]),
 "B5":  dict(hero="panel", rec=18.6, ghost="4", kicker="live", title="Editor aur preview saath", sub="ek hi screen par", call=("value","Code likho, output wahin dekho."), src="workers.cloudflare.com/playground · checked 24 Nov 2026"),
 "B6":  dict(hero="panel", rec=21.8, ghost="5", kicker="live", title="Apna response likho", sub="Hello World badlo", call=("value","Hello World badlo, apna response likho, output dekho."), src="workers.cloudflare.com/playground · checked 24 Nov 2026"),
 "B7":  dict(hero="panel", rec=25.6, ghost="6", kicker="http", title="Request bhi bhejo", sub="HTTP tab se", call=("value","HTTP tab se request bhejo, response wahin dikhega."), src="workers.cloudflare.com/playground · checked 24 Nov 2026"),
 "B8":  dict(hero="panel", rec=26.4, ghost="7", kicker="proof", title="Maine khud check kiya", sub="official limits page", call=("proof","Ye number maine khud Cloudflare ke official page par dekhe."), src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026"),
 "B9":  dict(hero="rows",  ghost="8", kicker="proof · verified today", title="Free plan ki limit", sub="Workers Free", call=("proof","Free plan mein 1,00,000 requests roz. Midnight UTC par reset."), src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026",
            rows=[dict(label="Requests / day", num=100000, frac=.92, col=WHITE, bcol=TEAL),
                  dict(label="Paid plan", value="no limit", frac=1.0, col=GREY, bcol=(70,80,110))]),
 "B10": dict(hero="rows",  ghost="9", kicker="proof · verified today", title="Har request ko CPU", sub="Workers Free", call=("proof","Har request ko 10 millisecond CPU milta hai. Average Worker sirf 2.2 ms leta hai."), src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026",
            rows=[dict(label="CPU / request", num=10, suffix=" ms", frac=.30, col=WHITE, bcol=AMBER),
                  dict(label="Average Worker", value="2.2 ms", frac=.12, col=GREY, bcol=(70,80,110))]),
 "B11": dict(hero="rows",  ghost="10", kicker="the catch", title="Ek kami bhi hai", sub="honest", call=("catch","Kami: Playground sirf Chrome aur Firefox desktop par chalta hai."), src="developers.cloudflare.com/workers/playground · checked 24 Nov 2026",
            rows=[dict(label="Chrome / Firefox desktop", value="works", frac=.85, col=TEAL, bcol=TEAL),
                  dict(label="Mobile browser", value="not for this", frac=.30, col=RED, bcol=RED)]),
 "B12": dict(hero="rows",  ghost="11", kicker="the catch", title="Deploy ke liye account", sub="test karne ke liye nahi", call=("catch","Test karne ke liye account nahi chahiye. Deploy karne ke liye chahiye."), src="developers.cloudflare.com/workers/get-started/guide · checked 24 Nov 2026",
            rows=[dict(label="Test in playground", value="no account", frac=.25, col=TEAL, bcol=TEAL),
                  dict(label="Deploy to edge", value="account", frac=.70, col=AMBER, bcol=AMBER)]),
 "B13": dict(hero="panel", rec=6.0,  ghost="12", kicker="next", title="Aage kya", sub="deploy jab chaho", call=("next","Deploy karna ho to account banao. Test ke liye zaroorat nahi."), src="workers.cloudflare.com/playground · checked 24 Nov 2026"),
 "B14": dict(hero="panel", rec=8.6,  ghost="13", kicker="link", title="Link description mein", sub="workers.cloudflare.com/playground", call=("cta","Poora link description mein hai — workers.cloudflare.com/playground"), src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026"),
}

def frame(t):
    idx = len(BEATS)-1
    for i,b in enumerate(BEATS):
        if b["s"] <= t < b["e"]: idx=i; break
    b = BEATS[idx]; P = PLAN.get(b["id"], PLAN["B1"])
    local = t - b["s"]; blen = max(0.05, b["e"]-b["s"]); prog = min(1.0, local/blen)

    img = background(t, (46, 22, 8)).convert("RGBA")
    ghost(img, P["ghost"], prog)
    header(img, P["kicker"], P["title"], P["sub"])

    if P["hero"] == "panel":
        shot = rf(int((P["rec"] + local) * 30))
        panel(img, shot, prog, (64, 420, W-128, 900), "workers.cloudflare.com/playground")
    else:
        data_rows(img, P["rows"], prog, (64, 470, W-128, 380))

    caption(img, b["t1"], b["t2"], prog, 1300)
    callout(img, P["call"][0], P["call"][1], prog)
    footer(img, P["src"], idx, t)
    return img.convert("RGB")

def main():
    n = int(round(TOTAL*FPS)); print(n, "frames", flush=True)
    cmd = ["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
           "-r",str(FPS),"-i","-","-i","voice.wav","-i","channel-bgm.mp3",
           "-filter_complex",
           "[1:a]volume=1.0[v];[2:a]volume=0.13,atrim=0:42.1,afade=t=out:st=38.5:d=3.5[bg];"
           "[v][bg]amix=inputs=2:duration=first:dropout_transition=0[mix];"
           "[mix]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map","0:v","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","20",
           "-pix_fmt","yuv420p","-movflags","+faststart","-c:a","aac","-b:a","192k",
           "-shortest","video3.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 250 == 0: print(" ", i, flush=True)
    p.stdin.close(); p.wait(); print("exit", p.returncode, flush=True)
    for tt,nm in ((1.2,"a"),(4.0,"b"),(12.0,"c"),(28.0,"d"),(35.0,"e"),(41.0,"f")):
        frame(tt).save(f"chk_{nm}.png")
    frame(27.8).save("thumb3.png")
    print("done", flush=True)

main()
