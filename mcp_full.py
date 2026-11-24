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
def call(name,args,rid,to=240):
    r=s.post(URL,headers=H2,json={"jsonrpc":"2.0","id":rid,"method":"tools/call",
      "params":{"name":name,"arguments":args}},timeout=to)
    for m in parse(r.text):
        if m.get("id")==rid: return m
    return {"raw":r.text[:500]}
def txt(m): return "".join(c.get("text","") for c in (m.get("result") or {}).get("content",[]))
def run(label, slug, args, rid):
    m=call("COMPOSIO_MULTI_EXECUTE_TOOL",{"tools":[{"tool_slug":slug,"arguments":args}]},rid)
    t=txt(m)
    ok='"successful":true' in t and '"error_count":0' in t
    print(f"\n########## {label} :: {slug} -> {'PASS' if ok else 'FAIL'} ##########")
    print(t[:1400])
    return ok

# 1. how do I stage a file?
print("===== SEARCH: stage/upload a file for another tool =====")
m=call("COMPOSIO_SEARCH_TOOLS",{"queries":[{"use_case":"upload a local file into storage so another tool can use it as s3key"}]},2)
print(txt(m)[:2500])

# 2. schema of multi execute (file params?)
print("\n===== SCHEMA: COMPOSIO_MULTI_EXECUTE_TOOL =====")
m=call("COMPOSIO_GET_TOOL_SCHEMAS",{"tool_slugs":["COMPOSIO_MULTI_EXECUTE_TOOL"]},3)
print(txt(m)[:2500])
