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
def call(name,args,rid,to=300):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:900]}
def txt(m):
    return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))

# A. list my videos
m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":"YOUTUBE_LIST_CHANNEL_VIDEOS",
   "arguments":{"mine":True,"maxResults":5}}]},10)
print("=== A. my channel videos ===")
print(txt(m)[:1200]); print()

# B. real upload, PRIVATE, using the platform s3key
S3=os.environ.get("S3KEY","")
args={"title":"craft anything — test upload, will be deleted",
      "description":"Private test upload to verify the pipeline. Safe to delete.",
      "categoryId":"28","privacyStatus":"private",
      "tags":["test"],
      "videoFile":{"name":"craft-anything.mp4","mimetype":"video/mp4","s3key":S3}}
m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":"YOUTUBE_MULTIPART_UPLOAD_VIDEO",
   "arguments":args}]},11,to=300)
print("=== B. UPLOAD (private) with s3key ===")
print("s3key:", S3)
print(txt(m)[:2000])
