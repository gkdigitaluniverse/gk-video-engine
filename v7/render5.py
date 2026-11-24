#!/usr/bin/env python3
"""gkhackter v5 — L6 light-editorial cream. The craft-anything language."""
import os, json, math, subprocess, glob, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
CREAM   = (236, 236, 231)
PAPER   = (255, 255, 255)
INK     = (17, 17, 17)
DOT     = (214, 212, 204)
ORANGE  = (232, 85, 31)
ORANGE2 = (244, 138, 66)
MINT    = (168, 226, 192)
GREEN   = (34, 160, 90)
RED     = (210, 60, 45)
GREY    = (120, 120, 116)
CHROME  = (34, 36, 42)

BEATS = json.load(open("beats.json"))
TOTAL = BEATS[-1]["e"]
FDIR = "frames"

def F(sz, style="display"):
    paths = {
      "display": ["fonts/Anton-Regular.ttf", "fonts/ArchivoBlack-Regular.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
      "mono":    ["fonts/SpaceMono-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
      "bold":    ["fonts/ArchivoBlack-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    }[style]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

RF = sorted(glob.glob(f"{FDIR}/*.jpg"))
_c = {}
def rf(i):
    if not RF: return Image.new("RGB",(1280,800),(240,240,236))
    i = max(0, min(len(RF)-1, i))
    if i not in _c:
        if len(_c) > 70: _c.clear()
        _c[i] = Image.open(RF[i]).convert("RGB")
    return _c[i]

def ease(x): return 1-(1-min(1.0,max(0.0,x)))**3
def back_out(x):
    x = min(1.0,max(0.0,x)); c1,c3 = 1.70158, 2.70158
    return 1 + c3*(x-1)**3 + c1*(x-1)**2

# ---------- background: cream + dot grid + starbursts ----------
def background(t):
    g = Image.new("RGB",(W,H),CREAM)
    d = ImageDraw.Draw(g)
    off = int((t*7) % 38)
    for y in range(-38, H+38, 38):
        for x in range(-38, W+38, 38):
            d.ellipse([x+off-2, y+off//2-2, x+off+2, y+off//2+2], fill=DOT)
    return g

def starburst(d, cx, cy, r, col, spikes=11, seed=0, rot=0.0, alpha=255):
    rnd = random.Random(seed)
    pts = []
    for i in range(spikes*2):
        a = rot + i*math.pi/spikes
        rr = r*(1.0 if i%2==0 else rnd.uniform(0.42,0.60))
        pts.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr))
    d.polygon(pts, fill=col+(alpha,) if len(col)==3 else col)

def bursts(base, t, seed, spots):
    lay = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(lay)
    for i,(bx,by,br) in enumerate(spots):
        rot = t*0.25 + i*0.7
        sc = 1.0 + 0.06*math.sin(t*1.4+i)
        starburst(d, bx, by, br*sc, ORANGE, spikes=11, seed=seed*10+i, rot=rot, alpha=52)
    base.alpha_composite(lay)

def ghost_watermark(base):
    d = ImageDraw.Draw(base)
    f = F(58,"mono"); s = "gkhackter"
    w = d.textlength(s, font=f)
    d.text(((W-w)/2, H//2-30), s, font=f, fill=(226,224,216))

# ---------- headline: black caps + orange boxed words ----------
def headline(base, parts, prog, y=150, size=104, maxw=None):
    """parts = [(text, kind)] kind: 'ink' | 'box' | 'orange'"""
    d = ImageDraw.Draw(base)
    maxw = maxw or W-110
    # measure & wrap into lines
    lines, cur = [], []
    curw = 0
    space = 0
    def measure(txt, f):
        return d.textlength(txt, font=f)
    f = F(size,"display")
    while size > 40 and any(measure(p[0], F(size,"display")) > maxw for p in parts):
        size -= 6; f = F(size,"display")
    for txt, kind in parts:
        for word in txt.split():
            fw = measure(word+" ", f)
            if curw + fw > maxw and cur:
                lines.append(cur); cur = []; curw = 0
            cur.append((word, kind, fw)); curw += fw
    if cur: lines.append(cur)
    # draw
    lh = int(size*1.06)
    yy = y
    for li, line in enumerate(lines):
        ap = min(1.0, max(0.0,(prog - li*0.09)/0.26))
        if ap <= 0: continue
        sl = int((1-ease(ap))*46)
        x = 55 - sl
        for word, kind, fw in line:
            if kind == "box":
                d.rounded_rectangle([x-6, yy+2, x+fw-2, yy+lh-6], radius=8, fill=ORANGE+(255,))
                d.text((x, yy), word, font=f, fill=PAPER+(255,))
            elif kind == "orange":
                d.text((x, yy), word, font=f, fill=ORANGE+(255,))
            else:
                d.text((x, yy), word, font=f, fill=INK+(255,))
            x += fw
        yy += lh
    return yy

# ---------- cards ----------
def shadow_panel(size, radius=22, blur=26, op=52):
    w,h = size
    sh = Image.new("RGBA",(w+120,h+120),(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([60,70,w+60,h+60], radius=radius, fill=(0,0,0,op))
    return sh.filter(ImageFilter.GaussianBlur(blur))

def white_card(base, box, title=None, pill=None, pill_col=ORANGE, prog=1.0, drop=26):
    x,y,w,h = box
    sc = back_out(min(1.0, prog/0.3))
    if sc < 0.97:
        return
    base.alpha_composite(shadow_panel((w,h)), (x-60, y-60+drop))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x,y,x+w,y+h], radius=20, fill=PAPER+(255,), outline=(28,28,28,255), width=3)
    if title:
        d.rounded_rectangle([x,y,x+w,y+46], radius=20, fill=CHROME+(255,))
        d.rectangle([x,y+30,x+w,y+46], fill=CHROME+(255,))
        for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
            d.ellipse([x+16+i*22, y+16, x+30+i*22, y+30], fill=c+(255,))
        fm = F(21,"mono")
        d.text((x+92, y+13), title, font=fm, fill=(210,214,224,255))
    if pill:
        fp = F(20,"mono"); tw = d.textlength(pill, font=fp)
        d.rounded_rectangle([x+w-tw-38, y-14, x+w-10, y+26], radius=8, fill=pill_col+(255,))
        d.text((x+w-tw-24, y-8), pill, font=fp, fill=PAPER+(255,))
    return (x, y+(46 if title else 0), w, h-(46 if title else 0))

def screen_in(base, box, shot, kb=1.10, prog=0.0):
    x,y,w,h = box
    z = 1.0+(kb-1.0)*ease(prog)
    sw, sh = int(shot.width/z), int(shot.height/z)
    ox, oy = (shot.width-sw)//2, (shot.height-sh)//2
    im = shot.crop((ox,oy,ox+sw,oy+sh)).resize((w,h), Image.LANCZOS)
    base.paste(im, (x,y))

def chip(base, x, y, text, col=INK, bg=None, prog=1.0, fs=22):
    d = ImageDraw.Draw(base)
    f = F(fs,"mono"); tw = d.textlength(text, font=f)
    sc = back_out(min(1.0, prog/0.28))
    if sc < 0.9: return x
    w = int(tw+34); h = 40
    if bg:
        d.rounded_rectangle([x,y,x+w,y+h], radius=9, fill=bg+(255,))
    else:
        d.rounded_rectangle([x,y,x+w,y+h], radius=9, fill=PAPER+(255,), outline=col+(255,), width=2)
    d.text((x+17, y+9), text, font=f, fill=col+(255,))
    return x+w+12

def checkrow(base, box, label, value, prog, col=GREEN):
    x,y,w,h = box
    d = ImageDraw.Draw(base)
    base.alpha_composite(shadow_panel((w,h), radius=14, blur=18, op=40), (x-60,y-60))
    d.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=MINT+(255,), outline=(24,24,24,255), width=3)
    f = F(30,"bold")
    d.ellipse([x+18, y+h//2-17, x+52, y+h//2+17], fill=GREEN+(255,))
    d.text((x+28, y+h//2-13), "v", font=F(24,"bold"), fill=PAPER+(255,))
    d.text((x+68, y+h//2-19), label, font=f, fill=INK+(255,))
    fm = F(22,"mono"); vw = d.textlength(value, font=fm)
    d.text((x+w-vw-20, y+h//2-12), value, font=fm, fill=(30,90,60,255))

def bigstat(base, num, unit, prog, y, col=ORANGE):
    d = ImageDraw.Draw(base)
    f = F(230,"display")
    while d.textlength(num, font=f) > W-120 and f.size > 80:
        f = F(f.size-10,"display")
    sc = back_out(min(1.0, prog/0.34))
    if sc < 0.97:
        im = Image.new("RGBA",(int(d.textlength(num,font=f))+40, int(f.size*1.5)),(0,0,0,0))
        ImageDraw.Draw(im).text((10,0), num, font=f, fill=col+(255,))
        im = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
        base.alpha_composite(im, (int((W-im.width)/2), int(y+(1-sc)*60)))
    else:
        d.text(((W-d.textlength(num,font=f))/2, y), num, font=f, fill=col+(255,))
    if unit:
        fu = F(34,"mono"); uw = d.textlength(unit, font=fu)
        d.text(((W-uw)/2, y+int(f.size*1.02)), unit, font=fu, fill=INK+(255,))

def mono_top(base, text):
    d = ImageDraw.Draw(base)
    d.text((56, 56), text, font=F(22,"mono"), fill=(150,148,142,255))
    d.line([(56,92),(W-56,92)], fill=(206,204,196,255), width=2)

def progress(base, t, idx):
    d = ImageDraw.Draw(base)
    d.rectangle([0,H-10,W,H], fill=(220,218,210,255))
    d.rectangle([0,H-10,int(W*t/TOTAL),H], fill=ORANGE+(255,))
    n = len(BEATS)
    for i in range(n):
        x = 56+i*17
        d.rectangle([x,H-42,x+11,H-34], fill=ORANGE+(255,) if i<=idx else (200,198,190,255))

# ---------- beat plan ----------
PLAN = {
 "B1":  dict(top="(1) FREE TIER  /  CLOUDFLARE", hl=[("NO SERVER.","ink"),("NO ACCOUNT.","ink"),("TEST IN","box"),("BROWSER","orange")],
             dev="screen", rec=8.0, chips=[("PLAYGROUND","ORANGE"),("NO SIGN-IN","GREEN")]),
 "B2":  dict(top="(2) THE SETUP YOU SKIP", hl=[("3 STEPS","box"),("BEFORE YOU","ink"),("SEE ANYTHING","ink")],
             dev="checks", rows=[("Node.js install","STEP 1"),("npm + wrangler","STEP 2"),("Deploy to test","STEP 3")]),
 "B3":  dict(top="(3) FREE TIER  /  LIVE", hl=[("CLOUDFLARE","ink"),("WORKERS","box"),("PLAYGROUND","orange")],
             dev="screen", rec=10.6, chips=[("NO AUTH","GREEN"),("LIVE PREVIEW","ORANGE")]),
 "B4":  dict(top="(4) BEFORE vs NOW", hl=[("SETUP GONE.","ink"),("PREVIEW","box"),("LIVE","orange")],
             dev="checks", rows=[("Pehle: setup + deploy","MINUTES"),("Ab: editor + preview","LIVE")]),
 "B5":  dict(top="(5) LIVE  /  SIDE BY SIDE", hl=[("EDITOR +","ink"),("LIVE PREVIEW","box")],
             dev="screen", rec=18.6, chips=[("SIDE BY SIDE","ORANGE"),("INSTANT","GREEN")]),
 "B6":  dict(top="(6) LIVE  /  EDIT", hl=[("CHANGE","ink"),("HELLO WORLD","box")],
             dev="screen", rec=21.8, chips=[("YOUR RESPONSE","ORANGE"),("SEE OUTPUT","GREEN")]),
 "B7":  dict(top="(7) HTTP  /  REQUEST", hl=[("SEND AN","ink"),("HTTP REQUEST","box")],
             dev="checks", rows=[("GET /","200 OK"),("Response","FAST")]),
 "B8":  dict(top="(8) PROOF  /  I CHECKED MYSELF", hl=[("I CHECKED","box"),("THE DOCS","ink")],
             dev="screen", rec=26.4, chips=[("OFFICIAL PAGE","ORANGE"),("TODAY","GREEN")]),
 "B9":  dict(top="(9) PROOF  /  VERIFIED TODAY", hl=[("FREE PLAN","ink"),("REQUESTS","box")],
             dev="stat", num="100,000", unit="REQUESTS PER DAY  /  RESET MIDNIGHT UTC"),
 "B10": dict(top="(10) PROOF  /  VERIFIED TODAY", hl=[("CPU PER","ink"),("REQUEST","box")],
             dev="stat", num="10 ms", unit="AVERAGE WORKER USES 2.2 ms"),
 "B11": dict(top="(11) THE CATCH  /  HONEST", hl=[("ONE","ink"),("CATCH","box"),("IT'S HONEST","orange")],
             dev="checks", rows=[("Chrome / Firefox","WORKS"),("Mobile browser","NOT THIS")]),
 "B12": dict(top="(12) THE CATCH  /  DEPLOY", hl=[("TEST:","ink"),("NO ACCOUNT","box"),("DEPLOY:","ink"),("ACCOUNT","orange")],
             dev="checks", rows=[("Test in playground","NO ACCOUNT"),("Deploy to edge","ACCOUNT")]),
 "B13": dict(top="(13) NEXT  /  WHEN READY", hl=[("DEPLOY","box"),("WHEN YOU WANT","ink")],
             dev="screen", rec=6.0, chips=[("EDGE NETWORK","ORANGE"),("YOUR CALL","GREEN")]),
 "B14": dict(top="(14) LINK  /  DESCRIPTION", hl=[("LINK IN","ink"),("DESCRIPTION","box")],
             dev="url"),
}

BURSTS = [(120,180,95),(950,240,120),(140,760,70),(990,1180,90),(90,1520,110),(1000,620,80)]

def frame(t):
    idx = len(BEATS)-1
    for i,b in enumerate(BEATS):
        if b["s"] <= t < b["e"]: idx=i; break
    b = BEATS[idx]; P = PLAN.get(b["id"], PLAN["B1"])
    local = t-b["s"]; blen = max(0.05, b["e"]-b["s"]); prog = min(1.0, local/blen)

    img = background(t).convert("RGBA")
    bursts(img, t, idx, BURSTS)
    ghost_watermark(img)
    mono_top(img, P["top"])

    hy = headline(img, P["hl"], prog, y=130, size=100)

    dev = P["dev"]
    top = max(hy+40, 470)
    if dev == "screen":
        card = white_card(img, (66, top, W-132, 700), title="workers.cloudflare.com/playground",
                          pill="LIVE", prog=prog)
        if card: screen_in(img, card, rf(int((P["rec"]+local)*30)), kb=1.12, prog=prog)
        cx = 66
        for i,(ct,ck) in enumerate(P.get("chips",[])):
            cx = chip(img, cx, top+730, ct, col=(GREEN if ck=="GREEN" else ORANGE),
                      prog=max(0.0,prog-0.25-i*0.08))
    elif dev == "checks":
        rows = P["rows"]; yy = top
        for i,(lab,val) in enumerate(rows):
            ap = max(0.0, prog - 0.15 - i*0.12)
            if ap > 0:
                checkrow(img, (66, yy, W-132, 92), lab, val, ap)
            yy += 118
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([66, yy+18, W-132, yy+96], radius=14, fill=PAPER+(255,), outline=(28,28,28,255), width=3)
        d.text((90, yy+38), "The playground skips all of this.", font=F(30,"bold"), fill=INK+(255,))
    elif dev == "stat":
        bigstat(img, P["num"], P["unit"], prog, y=top+40)
        d = ImageDraw.Draw(img)
        cy = top+430
        for i,(lab,val) in enumerate([("Verified at","developers.cloudflare.com"),("Checked","24 Nov 2026")]):
            yy = cy+i*86
            d.rounded_rectangle([66,yy,W-132,yy+70], radius=12, fill=PAPER+(255,), outline=(28,28,28,255), width=3)
            d.text((88,yy+16), lab, font=F(26,"mono"), fill=GREY+(255,))
            vw = d.textlength(val, font=F(26,"mono"))
            d.text((W-88-vw, yy+16), val, font=F(26,"mono"), fill=INK+(255,))
    elif dev == "url":
        d = ImageDraw.Draw(img)
        yy = top+40
        base.alpha_composite(shadow_panel((W-160, 120), radius=18, blur=22, op=44), (50, yy-60))
        d.rounded_rectangle([66, yy, W-66, yy+120], radius=18, fill=INK+(255,))
        u = "workers.cloudflare.com/playground"
        f = F(34,"mono"); uw = d.textlength(u, font=f)
        while uw > W-160 and f.size > 18:
            f = F(f.size-2,"mono"); uw = d.textlength(u, font=f)
        d.text(((W-uw)/2, yy+42), u, font=f, fill=PAPER+(255,))
        cx = 66
        for i,(ct,ck) in enumerate([("FREE TIER","GREEN"),("NO ACCOUNT","ORANGE"),("BROWSER ONLY","INK")]):
            cx = chip(img, cx, yy+160, ct, col=ck if ck!="INK" else INK,
                      prog=max(0.0,prog-0.2-i*0.08))

    progress(img, t, idx)
    return img.convert("RGB")

def main():
    n = int(round(TOTAL*FPS)); print(n, "frames", flush=True)
    cmd = ["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
           "-r",str(FPS),"-i","-","-i","voice.wav","-i","channel-bgm.mp3",
           "-filter_complex",
           "[1:a]volume=1.0[v];[2:a]volume=0.13,atrim=0:42.1,afade=t=out:st=38.5:d=3.5[bg];"
           "[v][bg]amix=inputs=2:duration=first:dropout_transition=0[mix];"
           "[mix]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map","0:v","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","19",
           "-pix_fmt","yuv420p","-movflags","+faststart","-c:a","aac","-b:a","192k",
           "-shortest","video5.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 250 == 0: print(" ", i, flush=True)
    p.stdin.close(); p.wait(); print("exit", p.returncode, flush=True)
    for tt,nm in ((1.2,"a"),(4.0,"b"),(12.0,"c"),(20.0,"d"),(28.0,"e"),(35.0,"f"),(41.0,"g")):
        frame(tt).save(f"z_{nm}.png")
    frame(28.2).save("thumb5.png")
    print("done", flush=True)

main()
