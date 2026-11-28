import os, json, requests

K = os.environ["CK"]
URL = "https://connect.composio.dev/mcp"
H = {
    "Authorization": f"Bearer {K}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
s = requests.Session()

def parse(t):
    out = []
    for line in t.splitlines():
        if line.startswith("data:"):
            try:
                out.append(json.loads(line[5:].strip()))
            except Exception:
                pass
    return out

r = s.post(URL, headers=H, json={
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "gk-probe", "version": "1"}}
}, timeout=60)
sid = r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
H2 = dict(H)
if sid:
    H2["Mcp-Session-Id"] = sid
s.post(URL, headers=H2, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, timeout=30)

rid_counter = [10]
def call(name, args):
    rid_counter[0] += 1
    rid = rid_counter[0]
    r = s.post(URL, headers=H2, json={
        "jsonrpc": "2.0", "id": rid, "method": "tools/call",
        "params": {"name": name, "arguments": args}
    }, timeout=120)
    for m in parse(r.text):
        if m.get("id") == rid:
            return m
    return {"raw": r.text[:2000], "status": r.status_code}

def unwrap(m):
    try:
        txt = m["result"]["content"][0]["text"]
        return json.loads(txt)
    except Exception:
        return m

def dbx_rpc(endpoint, body):
    return unwrap(call("COMPOSIO_PROXY_EXECUTE", {
        "toolkit_slug": "dropbox",
        "endpoint": endpoint,
        "method": "POST",
        "body": body,
    }))

print("=== FULL RECURSIVE TREE OF /gkhackter ===")
all_entries = []
res = dbx_rpc("https://api.dropboxapi.com/2/files/list_folder", {"path": "/gkhackter", "recursive": True})
d = ((res.get("data") or {}).get("data") or {})
all_entries.extend(d.get("entries", []))
while d.get("has_more") and d.get("cursor"):
    res = dbx_rpc("https://api.dropboxapi.com/2/files/list_folder/continue", {"cursor": d["cursor"]})
    d = ((res.get("data") or {}).get("data") or {})
    all_entries.extend(d.get("entries", []))

for e in sorted(all_entries, key=lambda x: x.get("path_display", "")):
    tag = e.get(".tag")
    sz = e.get("size", "-")
    mod = (e.get("server_modified") or "-")[:16]
    print(f"[{tag:6}] {e.get('path_display')}  ({sz} bytes, {mod})")

def read_text_file(path, max_chars=4000):
    res = dbx_rpc("https://api.dropboxapi.com/2/files/get_temporary_link", {"path": path})
    link = ((res.get("data") or {}).get("data") or {}).get("link")
    if not link:
        return f"ERROR getting link: {json.dumps(res)[:400]}"
    resp = requests.get(link, timeout=60)
    return resp.text[:max_chars]

print("\n=== READ /gkhackter/tools.md ===")
print(read_text_file("/gkhackter/tools.md", 6000))

# Also check if there's any new incoming package or Hacker-Series README/index
md_files = [e["path_display"] for e in all_entries if e.get(".tag") == "file" and e["path_display"].endswith(".md")]
hs_files = [p for p in md_files if "/Hacker-Series/" in p][:5]
if hs_files:
    print("\n=== SAMPLE /gkhackter/Hacker-Series/ FILES ===")
    for p in hs_files:
        print(f"\n--- {p} ---")
        print(read_text_file(p, 1200))

# Check latest incoming handoff.md
handoffs = sorted([p for p in md_files if p.endswith("/handoff.md")])
if handoffs:
    print("\n=== LATEST INCOMING HANDOFFS ===")
    for p in handoffs[-2:]:
        print(f"\n--- {p} ---")
        print(read_text_file(p, 1500))
