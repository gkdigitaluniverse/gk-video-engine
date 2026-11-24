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
def call(name,args,rid,to=180):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:500]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))

tests=[
 ("YOUTUBE_GET_VIDEO_DETAILS_BATCH",{"videoIds":["dQw4w9WgXcQ"]},20),
 ("YOUTUBE_LIST_COMMENT_THREADS2",{"videoId":"dQw4w9WgXcQ","maxResults":2},21),
 ("YOUTUBE_LIST_VIDEO_CATEGORIES",{"regionCode":"IN"},22),
 ("INSTAGRAM_GET_USER_INFO",{},23),
 ("FACEBOOK_LIST_MANAGED_PAGES",{},24),
]
for slug,args,rid in tests:
    m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":slug,"arguments":args}]},rid)
    t=txt(m)
    ok='"successful":true' in t
    print(f"===== {slug} -> {'OK' if ok else 'FAIL'} =====")
    print(t[:700])
    print()
