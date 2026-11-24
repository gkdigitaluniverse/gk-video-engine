import os, json, requests

K = os.environ["CK"]
URL = "https://connect.composio.dev/mcp"
H = {"Authorization": f"Bearer {K}", "Content-Type": "application/json",
     "Accept": "application/json, text/event-stream"}
s = requests.Session()

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

def call(name, args, rid):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
        "params":{"name":name,"arguments":args}},timeout=120)
    txt=r.text
    for m in parse(txt):
        if m.get("id")==rid:
            return m
    return {"raw":txt[:1500]}

for tk in ("instagram","facebook","youtube","youtube_content","gmail"):
    m=call("COMPOSIO_MANAGE_CONNECTIONS",{"toolkits":[{"name":tk,"action":"list"}]},10+hash(tk)%50)
    print(f"===== {tk} =====")
    print(json.dumps(m, ensure_ascii=False)[:900])
    print()
