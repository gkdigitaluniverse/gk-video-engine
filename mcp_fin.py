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
_rid=[500]
def call(name,args,to=240):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:300]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
def ex(label, slug, args, to=240):
    m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":slug,"arguments":args}],"memory":{}},to)
    t=txt(m); ok='"error_count":0' in t
    print(f"\n##### {label} -> {'PASS' if ok else 'FAIL'} #####")
    print(t[:1100]); return t, ok

print("===== does a Facebook VIDEO upload tool exist? =====")
m=call("COMPOSIO_SEARCH_TOOLS",{"queries":[{"use_case":"upload a video file to a facebook page as a video post"}]},2)
t=txt(m)
try:
    d=json.loads(t)
    for res in d.get("data",{}).get("results",[]):
        print("  primary:", res.get("primary_tool_slugs"))
        print("  related:", res.get("related_tool_slugs"))
except Exception: print(t[:600])

ex("IG media (permalink)","INSTAGRAM_GET_IG_MEDIA",{"ig_media_id":"18147730507590066"})
ex("IG comments on new reel","INSTAGRAM_GET_IG_MEDIA_COMMENTS",{"ig_media_id":"18147730507590066"})
ex("FB read my post","FACEBOOK_GET_POST",{"post_id":"1270080059532814_122122021401511062"})
ex("FB comments on post","FACEBOOK_GET_COMMENTS",{"object_id":"1270080059532814_122122021401511062"})
