import json, os, urllib.request
CK=os.environ["CK"]; U="https://connect.composio.dev/mcp"
def post(b):
    r=urllib.request.Request(U,data=json.dumps(b).encode(),method="POST",
      headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Authorization":"Bearer "+CK})
    raw=urllib.request.urlopen(r,timeout=120).read().decode("utf-8","ignore")
    o=[]
    for l in raw.split("\n"):
        if l.startswith("data: "):
            try:o.append(json.loads(l[6:]))
            except:pass
    return o[-1] if o else {}
post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"r","version":"1"}}})
tl=post({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}})
names=[t["name"] for t in tl["result"]["tools"]]
print("TOOLS:", names)
# find executor
exe=[n for n in names if "EXECUTE" in n]
print("EXECUTOR:", exe)
if exe:
    r=post({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":exe[0],"arguments":{
        "tool_slug":"METRICOOL_MCP_GET_BRAND_SETTINGS","arguments":{}}}})
    print("BRAND:", json.dumps(r)[:1800])
