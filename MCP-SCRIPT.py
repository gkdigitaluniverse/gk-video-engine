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
B="8098055"; F="2026-10-20T00:00:00+05:30"; T="2026-11-19T23:59:59+05:30"
def pull(ids):
    return {"tool_slug":"METRICOOL_MCP_GET_ANALYTICS_DATA_BY_METRICS",
            "arguments":{"brandId":B,"from":F,"to":T,"metrics":ids}}
res=ex([pull(["YTEV04","YTEV02","YTEV01"]), pull(["IGEV01"]), pull(["FBEV03"])])
print(json.dumps(res)[:4500])
