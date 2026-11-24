import os, json, requests, time
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
H={"Authorization":f"Bearer {K}","Content-Type":"application/json","Accept":"application/json, text/event-stream"}
s=requests.Session()
def parse(t):
    out=[]
    for line in t.splitlines():
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    return out
r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize",
 "params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=60)
sid=r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
H2=dict(H)
if sid: H2["Mcp-Session-Id"]=sid
s.post(URL,headers=H2,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
_rid=[2000]
def call(name,args,to=300):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:400]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))

PROMPT = (
 "Describe this video so vividly that a person who cannot see it can picture every second in their head. "
 "Write like this example: 'Dark clouds have gathered. Rain is falling slowly. A child is walking through it.' "
 "Go in time order. Cover the whole video in blocks of two to three seconds. "
 "For every block say: what is on the screen in plain pictures; what is moving and how it moves; "
 "what appears or disappears; any words on screen and where they sit; and the colours you actually see. "
 "Write flowing sentences, one paragraph per time block, each starting with its timestamps. "
 "Do not summarise. Do not skip the small movements. "
 "Never use technical words like motion graphics, transition, asset, composition, frame or overlay. "
 "Describe only what a child would notice."
)

VIDEOS = [
 ("gpu_character", "https://drive.usercontent.google.com/download?id=12D81Tx5I0DjbJI0nqi8Vh5HjmFsDP6eQ&export=download&confirm=t"),
 ("ai_dashboard",  "https://drive.usercontent.google.com/download?id=1YkhoBXu9ZUtzlmNedHe4heai-hpsehc8&export=download&confirm=t"),
]

for name, url in VIDEOS:
    print(f"\n########## {name} ##########", flush=True)
    # stage
    up = s.post(URL, headers=H2, json={"jsonrpc":"2.0","id":900+hash(name)%90,"method":"tools/call",
        "params":{"name":"COMPOSIO_MULTI_EXECUTE_TOOL","arguments":{"memory":{},"tools":[{"tool_slug":"COMPOSIO_PROXY_EXECUTE","arguments":{}}]}}}, timeout=30)
    m = call("COMPOSIO_MULTI_EXECUTE_TOOL", {"memory":{},"tools":[{"tool_slug":"COMPOSIO_PROXY_EXECUTE","arguments":{}}]}, to=30)
    # real: use TwelveLabs through the composio proxy is not available; use the TL key path below
    break

# --- direct TwelveLabs (api.twelvelabs.io is reachable from the runner) ---
TLK = os.environ["TLK"]
TB = "https://api.twelvelabs.io/v1.3"
TH = {"x-api-key": TLK}

for name, url in VIDEOS:
    print(f"\n########## {name} ##########", flush=True)
    a = requests.post(f"{TB}/assets", headers=TH, timeout=300,
        files={"method": (None,"url"), "url": (None,url), "filename": (None,f"{name}.mp4")})
    print("asset", a.status_code, a.text[:200], flush=True)
    if a.status_code not in (200,201):
        continue
    aid = a.json().get("_id")
    for _ in range(60):
        g = requests.get(f"{TB}/assets/{aid}", headers=TH, timeout=60)
        st = g.json().get("status")
        print("  status:", st, flush=True)
        if st == "ready": break
        if st == "failed": break
        time.sleep(6)
    if st != "ready":
        print("  not ready, skipping", flush=True); continue
    an = requests.post(f"{TB}/analyze", headers={**TH,"Content-Type":"application/json"},
        json={"video":{"type":"asset_id","asset_id":aid},"prompt":PROMPT,
              "temperature":0.1,"stream":False}, timeout=600)
    print("analyze", an.status_code, flush=True)
    try:
        out = an.json().get("data") or an.text
    except Exception:
        out = an.text
    open(f"DESC-{name}.md","w",encoding="utf-8").write(f"# {name}\n\nURL: {url}\n\n{out}\n")
    print(str(out)[:1200], flush=True)
print("done")
