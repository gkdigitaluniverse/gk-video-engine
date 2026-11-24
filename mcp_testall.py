import os, json, requests, base64, subprocess, time
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
_rid=[100]
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
    ok=('"success_count":1' in t) or ('"successful":true' in t and '"error_count":1' not in t)
    print(f"\n##### {label} :: {slug} -> {'PASS' if ok else 'FAIL'} #####")
    print(t[:1200])
    return t, ok

# ---- make a tiny test video ----
subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=0x0A0A0C:s=360x640:d=4",
                "-vf","drawtext=text='TEST':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","t.mp4"],check=False)
if not os.path.exists("t.mp4"):
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=black:s=360x640:d=4",
                    "-c:v","libx264","-pix_fmt","yuv420p","t.mp4"],check=False)
sz=os.path.getsize("t.mp4")
print("test video bytes:", sz)
b64=base64.b64encode(open("t.mp4","rb").read()).decode()
print("base64 chars:", len(b64))

# ---- 1. stage the file through the Composio pipeline ----
t,ok=ex("STAGE FILE","BOLDSIGN_FILE_UPLOAD",
        {"file_name":"test.mp4","mimetype":"video/mp4","base64":b64},to=300)
key=None
try:
    d=json.loads(t)
    key=d["data"]["results"][0]["response"]["data"].get("key") or \
        d["data"]["results"][0]["response"]["data"].get("s3key") or \
        d["data"]["results"][0]["response"]["data"].get("file_key")
except Exception: pass
print("STAGED KEY:", key)

# ---- 2. YouTube upload PRIVATE ----
if key:
    t2,ok2=ex("YT UPLOAD private","YOUTUBE_MULTIPART_UPLOAD_VIDEO",{
        "title":"TEST ONLY - delete me","description":"pipeline test",
        "categoryId":"28","privacyStatus":"private","tags":["test"],
        "videoFile":{"name":"test.mp4","mimetype":"video/mp4","s3key":key}},to=300)
    vid=None
    try:
        d=json.loads(t2); vid=d["data"]["results"][0]["response"]["data"].get("id")
    except Exception: pass
    print("UPLOADED VIDEO ID:", vid)

# ---- 3. reads ----
ex("YT comments","YOUTUBE_LIST_COMMENT_THREADS2",
   {"videoId":"dQw4w9WgXcQ","part":"id,snippet","maxResults":2})
ex("YT channel mine","YOUTUBE_LIST_CHANNEL_VIDEOS",{"mine":True,"maxResults":5})
ex("IG media list","INSTAGRAM_GET_IG_USER_MEDIA",{"limit":5})
ex("IG limit","INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT",{})
ex("IG conversations","INSTAGRAM_LIST_ALL_CONVERSATIONS",{"limit":5})
ex("FB page posts","FACEBOOK_GET_PAGE_POSTS",{"page_id":"1270080059532814","limit":5})
