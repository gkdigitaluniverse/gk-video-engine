import os, json, requests
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
ORPHANS=["6b0846691e13bd67eef3087f","6b08466ba9607f7555829b06","6b08466eee9d307b372d90de","6b084670b2044ab9dfaf261b"]
H={"Authorization":f"Bearer {K}","Content-Type":"application/json","Accept":"application/json, text/event-stream"}
s=requests.Session()
def blobs(t):
    out=[]
    for line in t.splitlines():
        line=line.strip()
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    if not out:
        try: out.append(json.loads(t))
        except Exception: pass
    return out
def init():
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=90)
    sid=r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"]=sid
    s.post(URL,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
M=[10]
def gql(q):
    M[0]+=1; my=M[0]
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":my,"method":"tools/call","params":{"name":"COMPOSIO_PROXY_EXECUTE","arguments":{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}}}},timeout=280)
    for b in blobs(r.text):
        if b.get("id")==my:
            for c in ((b.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return ""
def d3(o):
    try: return json.loads(o)["data"]["data"]["data"]
    except Exception: return None

init()
for pid in ORPHANS:
    out=gql('mutation { deletePost(input: {id: "%s"}) { __typename ... on MutationError { message } } }' % pid)
    print(f"DEL {pid}: {'OK' if 'DeletePostSuccess' in out else 'FAIL'} {out[:150]}")

# final state
d=d3(gql('query { posts(first: 100, input: {organizationId: "6afe914c34b70aac8c250902"}) { edges { node { id dueAt status channelService } } } }'))
if d and isinstance(d.get("posts"),dict):
    print("\nFINAL SCHEDULED:")
    from datetime import datetime, timedelta, timezone
    IST=timezone(timedelta(hours=5,minutes=30))
    rows=[]
    for e in d["posts"]["edges"]:
        n=e["node"]
        if n.get("status") in ("scheduled","sending"):
            dt=datetime.fromisoformat(n["dueAt"].replace("Z","+00:00")).astimezone(IST)
            rows.append((dt.strftime("%Y-%m-%d %H:%M"), n["channelService"], n["id"]))
    for r in sorted(rows): print("  ", *r)
