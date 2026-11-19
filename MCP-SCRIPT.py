import json, os, urllib.request, datetime

CK = os.environ["CK"]; U = "https://connect.composio.dev/mcp"
def post(body):
    req = urllib.request.Request(U, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Authorization":"Bearer "+CK})
    raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8","ignore")
    out=[]
    for line in raw.split("\n"):
        if line.startswith("data: "):
            try: out.append(json.loads(line[6:]))
            except: pass
    return out[-1] if out else {}

post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"r","version":"1"}}})

def call(name, args, _id=[10]):
    _id[0]+=1
    r = post({"jsonrpc":"2.0","id":_id[0],"method":"tools/call","params":{"name":name,"arguments":args}})
    try:
        return json.loads(r["result"]["content"][0]["text"])
    except Exception:
        return r

print("=== BRAND SETTINGS ===")
bs = call("METRICOOL_MCP_GET_BRAND_SETTINGS", {})
print(json.dumps(bs)[:2500])

print("\n=== AVAILABLE METRICS ===")
for net in ["youtube","instagram","facebook"]:
    m = call("METRICOOL_MCP_GET_ANALYTICS_AVAILABLE_METRICS", {"network": net})
    s = json.dumps(m)
    print(net, "->", s[:900])

print("\n=== SCHEDULED POSTS ===")
sp = call("METRICOOL_MCP_GET_SCHEDULED_POSTS", {})
print(json.dumps(sp)[:1500])
