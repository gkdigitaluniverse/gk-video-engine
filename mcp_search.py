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
def call(name,args,rid):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=180)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:800]}
m=call("COMPOSIO_SEARCH_TOOLS",{"queries":[
  {"use_case":"upload a video to youtube with title description and tags"},
  {"use_case":"create an instagram post with image and caption"},
  {"use_case":"create a facebook page post with text and link"}]},7)
txt=""
for c in (m.get("result") or {}).get("content",[]):
    txt+=c.get("text","")
print(txt[:6000])
open("SEARCH.txt","w").write(txt)
