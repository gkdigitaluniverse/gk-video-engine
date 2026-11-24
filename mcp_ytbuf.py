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
_rid=[1300]
def call(name,args,to=300):
    _rid[0]+=1; rid=_rid[0]
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:300]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
def gql(label, query, variables=None):
    body={"query":query}
    if variables: body["variables"]=variables
    m=call("COMPOSIO_PROXY_EXECUTE",{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":body},to=300)
    t=txt(m)
    try:
        d=json.loads(t); inner=d.get("data",{}).get("data",{})
        print(f"\n##### {label} #####"); print(json.dumps(inner, ensure_ascii=False)[:2200]); return inner
    except Exception:
        print(f"\n##### {label} RAW #####"); print(t[:1000]); return None

gql("VideoAssetInput + YoutubePrivacy", """
{ a: __type(name:"VideoAssetInput"){inputFields{name description type{name kind}}} b: __type(name:"YoutubePrivacy"){enumValues{name}} }
""")

YT="6afe91afece6dfde5f19c312"
MUT = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id text } }
    ... on MutationError { message }
  }
}
"""
vars_ = {"input": {
  "channelId": YT,
  "text": "Pipeline test via Buffer — safe to delete.",
  "assets": [{"video": {"url": VURL}}],
  "metadata": {"youtube": {"title": "TEST ONLY - delete me", "categoryId": "28",
                            "privacy": "private", "madeForKids": False,
                            "notifySubscribers": False}},
  "mode": "addToQueue",
  "schedulingType": "automatic",
  "needsApproval": False
}}
gql("createPost -> YouTube", MUT, vars_)
