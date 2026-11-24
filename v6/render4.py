#!/usr/bin/env python3
"""gkhackter v4 — dense motion graphics. A different device in every beat."""
import os, json, math, subprocess, glob, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
NAVY   = (10, 14, 32)
WHITE  = (246, 247, 252)
GREY   = (140, 146, 170)
ORANGE = (255, 122, 48)
AMBER  = (255, 190, 70)
TEAL   = (60, 210, 180)
RED    = (255, 92, 92)
VIOLET = (150, 120, 255)

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
    if not RF: return Image.new("RGB",(1280,800),(20,24,44))
    i = max(0, min(len(RF)-1, i))
    if i not in _c:
        if len(_c) > 70: _c.clear()
        _c[i] = Image.open(RF[i]).convert("RGB")
    return _c[i]

def ease(x): return 1 - (1 - min(1.0, max(0.0, x))) ** 3
def ease_out(x):
    x = min(1.0, max(0.0, x)); return 1 - (1-x)**2
def back_out(x):
    x = min(1.0, max(0.0, x)); c1, c3 = 1.70158, 2.70158
    return 1 + c3*(x-1)**3 + c1*(x-1)**2

# ---------- background ----------
_glow = {}
def background(t, hue=ORANGE):
    g = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(g)
    for y in range(H):
        k = y/H
        d.line([(0,y),(W,y)], fill=(int(10+7*k), int(14+5*k), int(32-20*k)))
    key = hue
    if key not in _glow:
        gl = Image.new("RGB",(W,H),(0,0,0)); gd = ImageDraw.Draw(gl)
        gd.ellipse([-320,-520,W+320,820], fill=hue)
        _glow[key] = gl.filter(ImageFilter.GaussianBlur(190))
    g = Image.blend(g, _glow[key], 0.15)
    d = ImageDraw.Draw(g)
    off = int((t*14) % 64)
    for x in range(-64, W+64, 64): d.line([(x+off,0),(x+off,H)], fill=(25,31,56))
    for y in range(-64, H+64, 64): d.line([(0,y+off//2),(W,y+off//2)], fill=(23,29,52))
    return g

def ghost(base, txt, y=250, size=420, alpha=13):
    d = ImageDraw.Draw(base)
    f = F(size); w = d.textlength(txt, font=f)
    d.text(((W-w)/2, y), txt, font=f, fill=(alpha, alpha+6, alpha+26))

def orbit_shapes(base, t, n=5, seed=0):
    lay = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(lay)
    rnd = random.Random(seed)
    for i in range(n):
        cx = rnd.randint(80, W-80); cy = rnd.randint(150, 1400)
        r  = rnd.randint(40, 130)
        sp = rnd.uniform(0.4, 1.1); ph = rnd.uniform(0, 6.28)
        col = rnd.choice([ORANGE, AMBER, TEAL, VIOLET])
        x = cx + math.sin(t*sp+ph)*46
        y = cy + math.cos(t*sp*0.8+ph)*38
        a = 16 + int(10*(0.5+0.5*math.sin(t*1.6+ph)))
        if rnd.random() < 0.5:
            d.ellipse([x-r,y-r,x+r,y+r], outline=col+(a+22,), width=4)
        else:
            d.rounded_rectangle([x-r*0.7,y-r*0.7,x+r*0.7,y+r*0.7], radius=18,
                                outline=col+(a+22,), width=4)
    base.alpha_composite(lay)

# ---------- chrome ----------
def chapter_rail(base, idx, t, prog_total):
    d = ImageDraw.Draw(base)
    x = W - 34
    d.rounded_rectangle([x-3, 120, x+3, 1560], radius=6, fill=(30,36,62,255))
    n = len(BEATS); span = 1440
    hgt = int(span * prog_total)
    d.rounded_rectangle([x-3, 120, x+3, 120+hgt], radius=6, fill=ORANGE+(255,))
    for i in range(n):
        y = 120 + int(span*i/(n-1))
        c = ORANGE if i <= idx else (52,58,88)
        d.ellipse([x-7, y-7, x+7, y+7], fill=c+(255,))

def watermark(base):
    d = ImageDraw.Draw(base); f = F(26); s = "@gkhackter"
    d.text((W-90-d.textlength(s,font=f), 66), s, font=f, fill=(78,84,110,255))

def footer(base, src, t):
    d = ImageDraw.Draw(base)
    d.text((56, 1792), src, font=F(21), fill=(96,102,128,255))
    d.rectangle([0,H-7,W,H], fill=(26,30,52,255))
    d.rectangle([0,H-7,int(W*t/TOTAL),H], fill=ORANGE+(255,))

# ---------- header ----------
def header(base, kicker, title, sub):
    d = ImageDraw.Draw(base)
    fk, ft, fs = F(24), F(50), F(26)
    k = kicker.upper()
    d.text((56, 92), k, font=fk, fill=AMBER+(255,))
    d.rectangle([56, 126, 56+d.textlength(k,font=fk), 130], fill=AMBER+(255,))
    d.text((56, 156), title, font=ft, fill=WHITE+(255,))
    d.text((56, 222), sub, font=fs, fill=GREY+(255,))

# ---------- caption: karaoke word by word ----------
def karaoke(base, t1, t2, prog, y=1150):
    d = ImageDraw.Draw(base)
    def fit(txt, sz):
        while sz > 26:
            f = F(sz)
            if d.textlength(txt, font=f) <= W-150: return f
            sz -= 3
        return F(26)
    f1, f2 = fit(t1, 82), fit(t2, 82)
    words = [(w,0) for w in t1.split()] + [(w,1) for w in t2.split()]
    n = len(words)
    shown = int(prog * (n + 2))
    l1 = " ".join(w for i,(w,ln) in enumerate(words) if ln==0 and i < shown)
    l2 = " ".join(w for i,(w,ln) in enumerate(words) if ln==1 and i < shown)
    yy = y
    if l1:
        d.text((56, yy), l1, font=f1, fill=WHITE+(255,))
    h1 = d.textbbox((0,0), l1 or "Ag", font=f1)[3]
    yy2 = yy + (h1 + 12 if l1 else 0)
    if l2:
        d.text((56, yy2), l2, font=f2, fill=ORANGE+(255,))
    h2 = d.textbbox((0,0), l2 or "Ag", font=f2)[3] if l2 else 0
    uw = int((W-150) * min(1.0, max(0.0,(prog-0.55)/0.4)))
    if uw > 0:
        d.rectangle([56, yy2+h2+18, 56+uw, yy2+h2+28], fill=AMBER+(255,))

# ---------- devices ----------
def browser(base, shot, box, prog, url, kb=1.10):
    x,y,w,h = box; bar = 50
    card = Image.new("RGBA",(w,h),(0,0,0,0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle([0,0,w,h], radius=18, fill=(22,26,46,255))
    d.rounded_rectangle([0,0,w,bar], radius=18, fill=(32,38,64,255))
    d.rectangle([0,bar-18,w,bar], fill=(32,38,64,255))
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([14+i*21,16,28+i*21,30], fill=c+(255,))
    d.rounded_rectangle([92,10,w-12,bar-10], radius=10, fill=(18,22,40,255))
    f = F(20)
    d.text(((w+92)/2-d.textlength(url,font=f)/2, 16), url, font=f, fill=(150,156,182,255))
    cw, ch = w-4, h-bar-2
    z = 1.0+(kb-1.0)*ease(prog)
    sw, sh = int(shot.width/z), int(shot.height/z)
    ox, oy = (shot.width-sw)//2, (shot.height-sh)//2
    im = shot.crop((ox,oy,ox+sw,oy+sh)).resize((cw,ch), Image.LANCZOS)
    card.paste(im,(2,bar+1))
    m = Image.new("L",(w,h),0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,w,h], radius=18, fill=255)
    card.putalpha(m)
    base.alpha_composite(card,(x,y))

def bar_race(base, rows, prog, box):
    """Animated horizontal bar race with counting values and rank chips."""
    x,y,w,h = box
    pn = Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(pn).rounded_rectangle([x-20,y-26,x+w+20,y+h+16], radius=22, fill=(16,20,40,165))
    base.alpha_composite(pn)
    d = ImageDraw.Draw(base)
    rowh = h // max(1,len(rows))
    for i,r in enumerate(rows):
        ap = min(1.0, max(0.0,(prog - i*0.12)/0.32))
        if ap <= 0: continue
        ry = y + i*rowh
        sl = int((1-back_out(ap))*70)
        col = r.get("col", WHITE)
        d.rounded_rectangle([x+sl-14, ry+10, x+sl+34, ry+52], radius=10,
                            fill=(r.get("bcol",ORANGE) if i==0 else (70,78,110))+(230,))
        d.text((x+sl-2, ry+20), f"{i+1}", font=F(26), fill=(12,14,26,255))
        d.text((x+sl+52, ry+14), r["label"], font=F(32), fill=col+(255,))
        cp = min(1.0, max(0.0,(prog - i*0.10 - 0.08)/0.30))
        if r.get("num", 0) == 0:
            vtxt = r.get("suffix","").strip()
        else:
            v = r["num"] if cp >= 0.98 else int(r["num"]*ease(cp))
            vtxt = f"{v:,}"+r.get("suffix","")
        fv = F(34); vw = d.textlength(vtxt, font=fv)
        d.text((x+w-vw-sl, ry+12), vtxt, font=fv, fill=col+(255,))
        bw = int((w-20)*min(1.0,r.get("frac",0.8))*ease(ap))
        d.rounded_rectangle([x+sl, ry+rowh-32, x+sl+bw, ry+rowh-14], radius=8,
                            fill=r.get("bcol",ORANGE)+(235,))

def stickers(base, items, prog, t, y0=430):
    """Cards flying in from alternating sides."""
    d = ImageDraw.Draw(base)
    for i,it in enumerate(items):
        ap = min(1.0, max(0.0,(prog - i*0.13)/0.34))
        if ap <= 0: continue
        side = -1 if i%2==0 else 1
        dx = int(side * (1-back_out(ap)) * 260)
        yy = y0 + i*176
        col = it.get("col", RED)
        w = W-192
        x0 = min(W-56-w, max(56, 96 + dx))
        pn = Image.new("RGBA",(W,H),(0,0,0,0))
        pd = ImageDraw.Draw(pn)
        pd.rounded_rectangle([x0,yy,x0+w,yy+150], radius=20,
                             fill=(20,24,46,240), outline=col+(200,), width=3)
        base.alpha_composite(pn)
        d = ImageDraw.Draw(base)
        fl = F(34)
        while d.textlength(it["label"], font=fl) > w-200 and fl.size > 20:
            fl = F(fl.size-2)
        d.text((x0+22, yy+20), it["label"], font=fl, fill=col+(255,))
        if it.get("value"):
            fv = F(26); vw = d.textlength(it["value"], font=fv)
            d.text((x0+w-vw-20, yy+26), it["value"], font=fv, fill=(180,186,210,255))
        if it.get("strike") and ap > 0.6:
            lw = d.textlength(it["label"], font=fl)
            d.line([(x0+22, yy+44),(x0+22+lw, yy+44)], fill=RED+(235,), width=5)
        if it.get("bar") is not None:
            bw = int((w-44)*min(1.0,it["bar"])*ease(ap))
            d.rounded_rectangle([x0+22, yy+112, x0+22+bw, yy+130], radius=7,
                                fill=it.get("bcol",col)+(230,))

def chips(base, items, prog, y=1250):
    d = ImageDraw.Draw(base)
    x = 56
    for i, it in enumerate(items):
        ap = min(1.0, max(0.0,(prog - 0.20 - i*0.10)/0.28))
        if ap <= 0: continue
        f = F(24)
        tw = d.textlength(it[0], font=f)
        cw = int(tw + 44)
        sc = back_out(ap)
        hh = int(52*sc); yy = y + (52-hh)//2
        col = it[1]
        pn = Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(pn).rounded_rectangle([x, yy, x+cw, yy+hh], radius=14,
            fill=(20,24,46,235), outline=col+(200,), width=2)
        base.alpha_composite(pn)
        if ap > 0.6:
            d.text((x+22, y+13), it[0], font=f, fill=col+(255,))
        x += cw + 14
        if x > W - 180: break

def callout(base, label, text, prog, y=1420):
    d = ImageDraw.Draw(base); x,w,h = 56, W-112, 172
    a = int(255*min(1.0,max(0.0,(prog-0.15)/0.4)))
    if a <= 0: return
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x,y,x+w,y+h], radius=18, fill=(18,22,42,a))
    od.rounded_rectangle([x,y,x+w,y+h], radius=18, outline=(58,66,104,a), width=2)
    base.alpha_composite(ov)
    d.text((x+22,y+16), label.upper(), font=F(21), fill=AMBER+(a,))
    f = F(26); line=""; yy=y+50
    for wd in text.split():
        tt=(line+" "+wd).strip()
        if d.textlength(tt,font=f)<=w-44: line=tt
        else:
            d.text((x+22,yy),line,font=f,fill=(214,218,236,a)); yy+=33; line=wd
    if line: d.text((x+22,yy),line,font=f,fill=(214,218,236,a))

def bigword(base, txt, prog, y=560, size=210, col=WHITE):
    d = ImageDraw.Draw(base)
    f = F(size)
    while d.textlength(txt, font=f) > W-120 and size > 60:
        size -= 8; f = F(size)
    w = d.textlength(txt, font=f)
    sc = back_out(min(1.0, prog/0.35))
    if sc < 0.98:
        im = Image.new("RGBA",(int(w)+40,int(size*1.4)+40),(0,0,0,0))
        ImageDraw.Draw(im).text((20,20), txt, font=f, fill=col+(255,))
        im = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
        base.alpha_composite(im, (int((W-im.width)/2), int(y+(1-sc)*80)))
    else:
        d.text(((W-w)/2, y), txt, font=f, fill=col+(255,))
    return y + int(size*1.4)

# ---------- beat plan: a DIFFERENT device each beat ----------
PLAN = {
 "B1":  dict(chips=[("no server",TEAL),("no account",AMBER),("browser only",VIOLET)], dev="bigword", kicker="free tier", title="No server needed", sub="Cloudflare Workers Playground",
             big="TEST IN BROWSER", call=("hook","API ko browser mein test karo, bina server khareede."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="0"),
 "B2":  dict(chips=[("node.js",RED),("wrangler",RED),("deploy",RED)], dev="stickers", kicker="what you skip", title="The usual setup", sub="three steps before you see anything",
             call=("context","Chhota web app banate ho? Pehle ye teen step."),
             src="developers.cloudflare.com/workers/get-started/guide · checked 24 Nov 2026", ghost="1",
             items=[dict(label="Node.js install", value="step 1", col=RED, strike=True, bar=.55),
                    dict(label="npm + wrangler", value="step 2", col=RED, strike=True, bar=.72),
                    dict(label="Deploy to test", value="step 3", col=RED, strike=True, bar=.88)]),
 "B3":  dict(chips=[("account-free",TEAL),("live preview",AMBER),("1 click",TEAL)], dev="browser", kicker="free tier", title="Cloudflare Workers Playground", sub="no account, no install",
             rec=10.6, call=("value","Playground kholo, code likho, live preview dekho. Koi sign-in nahi."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="2"),
 "B4":  dict(chips=[("minutes",RED),("live",TEAL),("same screen",AMBER)], dev="stickers", kicker="before vs now", title="Setup gone, preview live", sub="same second",
             call=("value","Pehle project setup aur deploy. Ab editor aur preview saath."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="3",
             items=[dict(label="Pehle: setup + deploy", value="minutes", col=RED, bar=.92, bcol=RED),
                    dict(label="Ab: editor + preview", value="live", col=TEAL, bar=.28, bcol=TEAL)]),
 "B5":  dict(chips=[("editor",TEAL),("preview",AMBER),("side by side",VIOLET)], dev="browser", kicker="live", title="Editor aur preview saath", sub="ek hi screen par",
             rec=18.6, call=("value","Code likho, output wahin dekho."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="4"),
 "B6":  dict(chips=[("hello world",TEAL),("your response",AMBER),("instant",TEAL)], dev="browser", kicker="live", title="Apna response likho", sub="Hello World badlo",
             rec=21.8, call=("value","Hello World badlo, apna response likho, output dekho."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="5"),
 "B7":  dict(chips=[("HTTP tab",TEAL),("send request",AMBER),("see response",TEAL)], dev="stickers", kicker="http", title="Request bhi bhejo", sub="HTTP tab se",
             call=("value","HTTP tab se request bhejo, response wahin."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="6",
             items=[dict(label="GET /", value="200 OK", col=TEAL, bar=.30, bcol=TEAL),
                    dict(label="Response time", value="fast", col=TEAL, bar=.18, bcol=TEAL)]),
 "B8":  dict(chips=[("official docs",AMBER),("checked today",TEAL),("not a guess",VIOLET)], dev="browser", kicker="proof", title="Maine khud check kiya", sub="official limits page",
             rec=26.4, call=("proof","Ye number maine khud official page par dekhe."),
             src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026", ghost="7"),
 "B9":  dict(chips=[("100,000/day",TEAL),("midnight UTC",AMBER),("free plan",TEAL)], dev="race", kicker="proof · verified today", title="Free plan ki limit", sub="Workers Free vs Paid",
             call=("proof","Free plan mein 1,00,000 requests roz. Midnight UTC par reset."),
             src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026", ghost="100K",
             rows=[dict(label="Free / day", num=100000, col=WHITE, bcol=TEAL, frac=.62),
                   dict(label="Paid plan", num=0, suffix="  no limit", col=GREY, bcol=(80,88,124), frac=1.0)]),
 "B10": dict(chips=[("10 ms CPU",AMBER),("avg 2.2 ms",TEAL),("per request",VIOLET)], dev="race", kicker="proof · verified today", title="Har request ko CPU", sub="Workers Free",
             call=("proof","Har request ko 10 ms CPU. Average Worker sirf 2.2 ms leta hai."),
             src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026", ghost="10",
             rows=[dict(label="CPU / request", num=10, suffix=" ms", col=WHITE, bcol=AMBER, frac=.30),
                   dict(label="Average Worker", num=2, suffix=".2 ms", col=GREY, bcol=(80,88,124), frac=.10)]),
 "B11": dict(chips=[("chrome",TEAL),("firefox",TEAL),("desktop only",RED)], dev="stickers", kicker="the catch", title="Ek kami bhi hai", sub="honest",
             call=("catch","Playground sirf Chrome aur Firefox desktop par chalta hai."),
             src="developers.cloudflare.com/workers/playground · checked 24 Nov 2026", ghost="!",
             items=[dict(label="Chrome / Firefox", value="works", col=TEAL, bar=.85, bcol=TEAL),
                    dict(label="Mobile browser", value="not this", col=RED, bar=.25, bcol=RED)]),
 "B12": dict(chips=[("test: no account",TEAL),("deploy: account",AMBER),("your call",VIOLET)], dev="stickers", kicker="the catch", title="Deploy ke liye account", sub="test ke liye nahi",
             call=("catch","Test ke liye account nahi chahiye. Deploy ke liye chahiye."),
             src="developers.cloudflare.com/workers/get-started/guide · checked 24 Nov 2026", ghost="?",
             items=[dict(label="Test in playground", value="no account", col=TEAL, bar=.22, bcol=TEAL),
                    dict(label="Deploy to edge", value="account", col=AMBER, bar=.70, bcol=AMBER)]),
 "B13": dict(chips=[("deploy",AMBER),("edge network",TEAL),("when ready",VIOLET)], dev="browser", kicker="next", title="Aage kya", sub="deploy jab chaho",
             rec=6.0, call=("next","Deploy karna ho to account. Test ke liye zaroorat nahi."),
             src="workers.cloudflare.com/playground · checked 24 Nov 2026", ghost="13"),
 "B14": dict(chips=[("link below",AMBER),("workers.cloudflare.com",TEAL),("playground",VIOLET)], dev="bigword", kicker="link", title="Link description mein", sub="workers.cloudflare.com/playground",
             big="LINK IN DESCRIPTION", call=("cta","workers.cloudflare.com/playground"),
             src="developers.cloudflare.com/workers/platform/limits · checked 24 Nov 2026", ghost="14"),
}

def frame(t):
    idx = len(BEATS)-1
    for i,b in enumerate(BEATS):
        if b["s"] <= t < b["e"]: idx=i; break
    b = BEATS[idx]; P = PLAN.get(b["id"], PLAN["B1"])
    local = t-b["s"]; blen = max(0.05, b["e"]-b["s"]); prog = min(1.0, local/blen)

    img = background(t, P.get("hue", ORANGE)).convert("RGBA")
    ghost(img, P.get("ghost",""), y=300 if P["dev"]!="race" else 250)
    orbit_shapes(img, t, n=5, seed=idx)
    header(img, P["kicker"], P["title"], P["sub"])

    dev = P["dev"]
    if dev == "browser":
        browser(img, rf(int((P["rec"]+local)*30)), (56, 296, W-112, 716), prog,
                "workers.cloudflare.com/playground", kb=1.14)
    elif dev == "race":
        rows = P["rows"]; rh = 260
        top = 320 + max(0,(700 - rh*len(rows))//2)
        bar_race(img, rows, prog, (56, top, W-112, rh*len(rows)))
        pass
    elif dev == "stickers":
        items = P["items"]; ch, gap = 150, 26
        total = len(items)*ch + (len(items)-1)*gap
        top = 296 + max(0,(716 - total)//2)
        stickers(img, items, prog, t, y0=top)
    elif dev == "bigword":
        bigword(img, P["big"], prog, y=560, size=190)

    karaoke(img, b["t1"], b["t2"], prog, y=800)
    chips(img, P.get("chips", [("free tier",TEAL),("no account",AMBER),("browser only",VIOLET)]), prog, y=1180)
    callout(img, P["call"][0], P["call"][1], prog)
    watermark(img)
    chapter_rail(img, idx, t, t/TOTAL)
    footer(img, P["src"], t)
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
           "-shortest","video4.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 250 == 0: print(" ", i, flush=True)
    p.stdin.close(); p.wait(); print("exit", p.returncode, flush=True)
    for tt,nm in ((1.2,"a"),(4.0,"b"),(12.0,"c"),(20.0,"d"),(28.0,"e"),(35.0,"f"),(41.0,"g")):
        frame(tt).save(f"q_{nm}.png")
    frame(27.8).save("thumb4.png")
    print("done", flush=True)

main()
