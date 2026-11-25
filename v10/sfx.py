import re, os, urllib.request, json
os.makedirs("sfx", exist_ok=True)
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
def get(u):
    r=urllib.request.Request(u, headers=UA)
    return urllib.request.urlopen(r, timeout=60).read()

pages = {
 "whoosh":"https://mixkit.co/free-sound-effects/whoosh/",
 "transition":"https://mixkit.co/free-sound-effects/transition/",
 "click":"https://mixkit.co/free-sound-effects/click/",
 "pop":"https://mixkit.co/free-sound-effects/pop/",
}
found={}
for k,u in pages.items():
    try:
        h=get(u).decode("utf-8","ignore")
        urls=re.findall(r'https://assets\.mixkit\.co/active_storage/sfx/[0-9]+/[0-9]+-preview\.mp3', h)
        urls=list(dict.fromkeys(urls))
        found[k]=urls[:6]
        print(k, len(urls), urls[:3])
    except Exception as e:
        print(k,"ERR",str(e)[:100])

os.makedirs("sfx", exist_ok=True)
taken=[]
for k,urls in found.items():
    for i,u in enumerate(urls[:2]):
        try:
            d=get(u)
            p=f"sfx/{k}_{i}.mp3"
            open(p,"wb").write(d)
            taken.append((p,len(d)))
        except Exception as e:
            print("dl fail",u,str(e)[:60])
print(json.dumps(taken, indent=1))
