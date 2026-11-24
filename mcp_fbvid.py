import os, json, requests
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
VURL=os.environ["VURL"]
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
_rid=[600]
def call(name,args,to=300):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:300]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
def ex(label, slug, args, to=300):
    m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":slug,"arguments":args}],"memory":{}},to)
    t=txt(m); ok='"error_count":0' in t
    print(f"\n##### {label} -> {'PASS' if ok else 'FAIL'} #####")
    print(t[:1400]); return t, ok

print("=== FACEBOOK_CREATE_VIDEO_POST schema ===")
m=call("COMPOSIO_GET_TOOL_SCHEMAS",{"tool_slugs":["FACEBOOK_CREATE_VIDEO_POST"]},3)
print(txt(m)[:1800])

ex("FB VIDEO post","FACEBOOK_CREATE_VIDEO_POST",{
  "page_id":"1270080059532814",
  "description":"Pipeline test video - safe to delete.",
  "video_url":VURL},to=300)
ex("FB page videos","FACEBOOK_GET_PAGE_VIDEOS",{"page_id":"1270080059532814","limit":3})
