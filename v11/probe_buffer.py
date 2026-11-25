import os, json, requests
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
def init():
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=90)
    sid=r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"]=sid
    s.post(URL,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
def call(tool,args,mid=[10]):
    mid[0]+=1
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":mid[0],"method":"tools/call","params":{"name":tool,"arguments":args}},timeout=280)
    for m in parse(r.text):
        if m.get("id")==mid[0]:
            for c in ((m.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return r.text[:400]
init()
for t in ["PostType","PostTypeFacebook","ShareMode","SchedulingType","InstagramGeolocationInput"]:
    q='query { __type(name: "%s") { name kind enumValues { name description } inputFields { name description } } }' % t
    out=call("COMPOSIO_PROXY_EXECUTE",{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}})
    try:
        j=json.loads(out); d=j["data"]["data"]["data"]["__type"]
        print(f"===== {t} =====")
        if d.get("enumValues"):
            for e in d["enumValues"]: print("  ", e["name"], "-", (e.get("description") or "")[:90])
        elif d.get("inputFields"):
            for f in d["inputFields"]: print("  ", f["name"], "-", (f.get("description") or "")[:90])
        else: print("  (none)")
    except Exception as e:
        print(f"===== {t} ===== parse err", out[:200])
