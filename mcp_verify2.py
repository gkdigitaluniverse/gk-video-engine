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
r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize",
 "params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=60)
sid=r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
H2=dict(H)
if sid: H2["Mcp-Session-Id"]=sid
s.post(URL,headers=H2,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
_rid=[1600]
def call(name,args,to=240):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:300]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
m=call("COMPOSIO_PROXY_EXECUTE",{"toolkit_slug":"buffer","endpoint":"","method":"POST",
  "body":{"query":'{ post(input:{id:"6b055b085e1f4df6a058d0f1"}){ id status sentAt externalLink } }'}},to=200)
print(txt(m)[:800])
