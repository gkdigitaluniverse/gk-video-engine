import os, json, requests
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
VURL=os.environ["VURL"]; IURL=os.environ["IURL"]
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
_rid=[1500]
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
    t=txt(m); ok='"error_count":0' in t
    print(f"\n##### {label} -> {'PASS' if ok else 'FAIL'} #####"); print(t[:900]); return t, ok
def gql(label, query, variables=None):
    body={"query":query}
    if variables: body["variables"]=variables
    m=call("COMPOSIO_PROXY_EXECUTE",{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":body},to=300)
    t=txt(m)
    try:
        d=json.loads(t); print(f"\n##### {label} #####"); print(json.dumps(d.get("data",{}).get("data",{}), ensure_ascii=False)[:800]); return d
    except Exception:
        print(f"\n##### {label} RAW #####"); print(t[:600]); return None

CAP = ("Cloudflare Workers Playground: account banaye bina code likho, live preview dekho. "
       "Free plan mein 100,000 requests roz aur har request ko 10 ms CPU. "
       "Link: https://workers.cloudflare.com/playground")
TAGS = "#cloudflare #workers #webdevelopment #coding #hindi #techtips"

# 1) Instagram reel
t,ok = ex("IG reel container","INSTAGRAM_POST_IG_USER_MEDIA",{
  "ig_user_id":"29161770546783780","media_type":"REELS","video_url":VURL,
  "caption":CAP+"\n\n"+TAGS},to=300)
cid=None
try:
    d=json.loads(t); cid=d["data"]["results"][0]["response"]["data"]["id"]
except Exception: pass
print("IG container:", cid)
if cid:
    ex("IG publish","INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH",
       {"ig_user_id":"29161770546783780","creation_id":cid},to=300)

# 2) Facebook video
ex("FB video","FACEBOOK_CREATE_VIDEO_POST",{
  "page_id":"1270080059532814",
  "title":"Cloudflare Workers Playground",
  "description":CAP+"\n\n"+TAGS,
  "file_url":VURL},to=300)

# 3) YouTube via Buffer GraphQL
MUT = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id text } }
    ... on MutationError { message }
  }
}
"""
gql("YouTube via Buffer", MUT, {"input":{
  "channelId":"6afe91afece6dfde5f19c312",
  "text": CAP+"\n\n"+TAGS,
  "assets":[{"video":{"url":VURL}}],
  "metadata":{"youtube":{"title":"Bina server, browser mein API test karo",
                          "categoryId":"28","privacy":"public",
                          "madeForKids":False,"notifySubscribers":True}},
  "mode":"shareNow","schedulingType":"automatic","needsApproval":False}})
