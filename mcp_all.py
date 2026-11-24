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
def call(name,args,rid,to=240):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:600]}

QUERIES=[
 ("youtube upload video with title description tags privacy status thumbnail",1),
 ("youtube read comments on a video",2),
 ("youtube post a comment on a video and reply to a comment",3),
 ("youtube pin or moderate a comment on a video",4),
 ("youtube create a community post on the channel",5),
 ("instagram publish a reel video with caption",6),
 ("instagram read comments and reply to comments on a post",7),
 ("instagram send a direct message DM to a user",8),
 ("facebook page create a post with video or text",9),
 ("facebook page read comments and reply to comments",10),
 ("facebook page pin a post or comment",11),
]
alltools={}
for uc,idx in QUERIES:
    m=call("COMPOSIO_SEARCH_TOOLS",{"queries":[{"use_case":uc}]},idx)
    txt="".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
    print(f"===== Q{idx}: {uc} =====")
    try:
        d=json.loads(txt)
        for res in d.get("data",{}).get("results",[]):
            prim=res.get("primary_tool_slugs") or []
            rel=res.get("related_tool_slugs") or []
            print("  primary:", prim)
            print("  related:", rel)
            for sl in prim+rel:
                alltools.setdefault(sl,set()).add(uc[:40])
    except Exception as e:
        print("  parse fail:", txt[:200])
    print()
print("TOTAL UNIQUE TOOL SLUGS:", len(alltools))
for sl in sorted(alltools): print("  ", sl)
json.dump({k:list(v) for k,v in alltools.items()}, open("ALL-TOOLS.json","w"), indent=2)
