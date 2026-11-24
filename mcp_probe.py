import os, json, requests, sys

K = os.environ["CK"]
URL = "https://connect.composio.dev/mcp"
H = {"Authorization": f"Bearer {K}", "Content-Type": "application/json",
     "Accept": "application/json, text/event-stream"}
s = requests.Session()

def parse(text):
    out = []
    for line in text.splitlines():
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    return out

# 1) initialize
r = s.post(URL, headers=H, json={"jsonrpc":"2.0","id":1,"method":"initialize",
    "params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}}, timeout=60)
sid = r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
print("init HTTP", r.status_code, "| session:", sid)
H2 = dict(H)
if sid: H2["Mcp-Session-Id"] = sid

# 2) initialized notification
s.post(URL, headers=H2, json={"jsonrpc":"2.0","method":"notifications/initialized"}, timeout=30)

# 3) tools/list
r = s.post(URL, headers=H2, json={"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}, timeout=60)
print("tools/list HTTP", r.status_code)
msgs = parse(r.text)
tools = []
for m in msgs:
    for t in (m.get("result") or {}).get("tools", []):
        tools.append(t)
print("TOOLS:", len(tools))
for t in tools:
    print(f"  - {t.get('name')}: {(t.get('description') or '')[:150]}")

json.dump([{"name":t.get("name"),"description":t.get("description"),
            "schema":t.get("inputSchema")} for t in tools],
          open("MCP-TOOLS.json","w"), indent=2, ensure_ascii=False)
print("\nSAVED MCP-TOOLS.json")
