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
_rid=[200]
def call(name,args,to=300):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:400]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
def ex(label, slug, args, to=300):
    m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":slug,"arguments":args}],"memory":{}},to)
    t=txt(m)
    ok='"error_count":0' in t
    print(f"\n##### {label} :: {slug} -> {'PASS' if ok else 'FAIL'} #####")
    print(t[:1500])
    return t, ok

IGID="29161770546783780"
ex("IG media list","INSTAGRAM_GET_IG_USER_MEDIA",{"ig_user_id":IGID,"limit":5})
ex("IG user info","INSTAGRAM_GET_USER_INFO",{})
ex("FB page posts","FACEBOOK_GET_PAGE_POSTS",{"page_id":"1270080059532814","limit":3})
ex("FB pages","FACEBOOK_LIST_MANAGED_PAGES",{})
# YouTube: does upload accept a public URL as the file reference?
ex("YT upload via public URL","YOUTUBE_MULTIPART_UPLOAD_VIDEO",{
   "title":"TEST ONLY delete me","description":"pipeline test",
   "categoryId":"28","privacyStatus":"private",
   "videoFile":{"name":"test.mp4","mimetype":"video/mp4",
     "s3key":"https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"}},to=300)
# YouTube connection detail
m=call("COMPOSIO_MANAGE_CONNECTIONS",{"toolkits":[{"name":"youtube","action":"list"}]})
print("\n##### YT connection detail #####")
print(txt(m)[:1200])
