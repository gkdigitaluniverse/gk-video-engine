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
def gql(q, mid=[10]):
    mid[0]+=1
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":mid[0],"method":"tools/call","params":{"name":"COMPOSIO_PROXY_EXECUTE","arguments":{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}}}},timeout=280)
    for m in parse(r.text):
        if m.get("id")==mid[0]:
            for c in ((m.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return r.text[:300]
def inner(out):
    try:
        j=json.loads(out); return j["data"]["data"]["data"]
    except Exception: return None

init()
# channels
d = inner(gql('query { channels { id name service } }'))
print("CHANNELS:", json.dumps(d, ensure_ascii=False)[:800] if d else "err")

# posts field args
d = inner(gql('query { __type(name: "Query") { fields { name args { name type { name kind ofType { name kind } } } } } }'))
if d:
    for f in d["__type"]["fields"]:
        if f["name"] == "posts":
            print("\nPOSTS ARGS:", json.dumps(f["args"], ensure_ascii=False)[:900])

# Post type fields
d = inner(gql('query { __type(name: "Post") { fields { name type { name kind ofType { name } } } } }'))
if d:
    print("\nPOST FIELDS:", [x["name"] for x in d["__type"]["fields"]][:40])
