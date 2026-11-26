import os, json, requests
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
ORG="6afe914c34b70aac8c250902"
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
def gql(q, mid=[10]):
    mid[0]+=1
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":mid[0],"method":"tools/call","params":{"name":"COMPOSIO_PROXY_EXECUTE","arguments":{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}}}},timeout=280)
    for m in parse(r.text):
        if m.get("id")==mid[0]:
            for c in ((m.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return r.text[:300]
def inner(o):
    try: return json.loads(o)["data"]["data"]["data"]
    except Exception: return None

init()
q = 'query { posts(first: 100, input: {organizationId: "%s"}) { edges { node { id dueAt status channelId channelService text } } } }' % ORG
d = inner(gql(q))
if d and d.get("posts"):
    edges = d["posts"]["edges"]
    print("TOTAL POSTS:", len(edges))
    for e in edges:
        n = e["node"]
        print(f"  {str(n.get('dueAt')):26} {str(n.get('status')):12} {str(n.get('channelService')):10} {str(n.get('channelId'))[:20]:22} {(n.get('text') or '')[:40]}")
else:
    print("ERR/EMPTY:", json.dumps(d, ensure_ascii=False)[:600] if d else "no data")
