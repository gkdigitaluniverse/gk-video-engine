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
_rid=[900]
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
    print(t[:1600]); return t, ok

print("=== is there ANY buffer tool with media/video? ===")
m=call("COMPOSIO_SEARCH_TOOLS",{"queries":[
 {"use_case":"buffer post with video or image attachment media upload"},
 {"use_case":"buffer youtube video upload publish"}]},2)
print(txt(m)[:2200])

YT="6afe91afece6dfde5f19c312"
ex("BUFFER -> YouTube channel, queue a text post","BUFFER_PUBLISH_POSTS",{
   "channel_ids":[YT],"text":"Buffer connectivity test - safe to delete",
   "delivery_mode":"add_to_queue"},to=200)
ex("BUFFER list posts","BUFFER_LIST_POSTS",{"organization_id":"6afe914c34b70aac8c250902","page_size":5},to=200)
