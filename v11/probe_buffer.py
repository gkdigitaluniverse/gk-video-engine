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
def init():
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=90)
    sid=r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"]=sid
    s.post(URL,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
    return sid
def call(tool,args,mid=[10]):
    mid[0]+=1
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":mid[0],"method":"tools/call","params":{"name":tool,"arguments":args}},timeout=280)
    for m in parse(r.text):
        if m.get("id")==mid[0]:
            res=m.get("result",{})
            for c in (res.get("content") or []):
                if c.get("type")=="text":
                    return c.get("text","")
    return r.text[:500]

init()

# 1) walk the CreatePostInput type
q1 = """query { __type(name: "CreatePostInput") { inputFields { name description type { name kind ofType { name kind ofType { name kind } } } } } }"""
out = call("COMPOSIO_PROXY_EXECUTE", {"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q1}})
print("===== CreatePostInput =====")
print(out[:3000])

# 2) try the metadata types directly
for t in ["InstagramPostMetadataInput","FacebookPostMetadataInput","InstagramMetadataInput","FacebookMetadataInput","PostMetadataInput"]:
    q = 'query { __type(name: "%s") { name inputFields { name description type { name kind ofType { name kind } } } } }' % t
    out = call("COMPOSIO_PROXY_EXECUTE", {"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}})
    print(f"\n===== {t} =====")
    print(out[:2500])
