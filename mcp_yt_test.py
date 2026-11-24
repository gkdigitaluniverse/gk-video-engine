import os, json, requests, time
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
def call(name,args,rid,to=300):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:900]}

# 1) schema of the upload tool
m=call("COMPOSIO_GET_TOOL_SCHEMAS",{"tool_slugs":["YOUTUBE_MULTIPART_UPLOAD_VIDEO"]},2)
print("=== SCHEMA ===")
for c in (m.get("result") or {}).get("content",[]):
    print(c.get("text","")[:2500])
print()

# 2) list my channel videos (read-only, proves connection)
m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":"YOUTUBE_LIST_CHANNEL_VIDEOS",
        "arguments":{"maxResults":5}}]},3)
print("=== LIST CHANNEL VIDEOS ===")
for c in (m.get("result") or {}).get("content",[]):
    print(c.get("text","")[:1500])
