import json, os, urllib.request
CK=os.environ["CK"]; U="https://connect.composio.dev/mcp"
def post(b):
    r=urllib.request.Request(U,data=json.dumps(b).encode(),method="POST",
      headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Authorization":"Bearer "+CK})
    raw=urllib.request.urlopen(r,timeout=180).read().decode("utf-8","ignore")
    o=[]
    for l in raw.split("\n"):
        if l.startswith("data: "):
            try:o.append(json.loads(l[6:]))
            except:pass
    return o[-1] if o else {}
post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"r","version":"1"}}})
def ex(tools,_id=[10]):
    _id[0]+=1
    r=post({"jsonrpc":"2.0","id":_id[0],"method":"tools/call","params":{"name":"COMPOSIO_MULTI_EXECUTE_TOOL","arguments":{"tools":tools}}})
    try: return json.loads(r["result"]["content"][0]["text"])
    except Exception: return r
ctx = ex([{"tool_slug":"BUFFER_GET_ACCOUNT_CONTEXT","arguments":{}}])
print("=== BUFFER ACCOUNT CONTEXT ===")
print(json.dumps(ctx)[:3000])
# try to pull org id
org=None
try:
    d=ctx["data"]["results"][0]["response"]["data"]
    s=json.dumps(d)
    import re
    m=re.findall(r'"organization[^"]*id"\s*:\s*"([^"]+)"', s) or re.findall(r'"id"\s*:\s*"(org[^"]+)"', s)
    if m: org=m[0]
    else:
        m2=re.findall(r'"id"\s*:\s*"([A-Za-z0-9_\-]{6,})"', s)
        org=m2[0] if m2 else None
except Exception as e:
    print("parse err", e)
print("ORG:", org)
if org:
    p=ex([{"tool_slug":"BUFFER_LIST_POSTS","arguments":{"organization_id":org,"page_size":50}}])
    print("\n=== BUFFER POSTS ===")
    print(json.dumps(p)[:3000])
