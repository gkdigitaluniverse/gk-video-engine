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

print("=== 1. Check Connections (dropbox, instagram, facebook, youtube, buffer) ===")
for tk in ("dropbox", "instagram", "facebook", "youtube", "buffer"):
    res = unwrap(call("COMPOSIO_MANAGE_CONNECTIONS", {"toolkits": [{"name": tk, "action": "list"}]}))
    info = (res.get("data") or {}).get("results", {}).get(tk, {}) if isinstance(res, dict) else res
    print(f"{tk}: status={info.get('status') if isinstance(info, dict) else info}")
    if isinstance(info, dict) and info.get("accounts"):
        for a in info["accounts"]:
            print(f"  account id={a.get('id')} status={a.get('status')} user_info={a.get('user_info')}")

print("\n=== 2. Search Dropbox tools ===")
srch = unwrap(call("COMPOSIO_SEARCH_TOOLS", {
    "queries": [{"use_case": "list files in dropbox folder and read file contents", "known_fields": ""}]
}))
print(json.dumps(srch, ensure_ascii=False)[:2500])

print("\n=== 3. Proxy list /gkhackter on Dropbox API ===")
def dbx_rpc(endpoint, body):
    return unwrap(call("COMPOSIO_PROXY_EXECUTE", {
        "toolkit_slug": "dropbox",
        "endpoint": endpoint,
        "method": "POST",
        "body": body,
    }))

for path in ("/gkhackter", "/gkhackter/incoming", "/gkhackter/done", "/gkhackter/logs"):
    print(f"\n--- LIST {path} ---")
    res = dbx_rpc("https://api.dropboxapi.com/2/files/list_folder", {"path": path, "recursive": False})
    if isinstance(res, dict) and res.get("successful") and isinstance(res.get("data"), dict):
        d = res["data"]
        entries = d.get("entries") or (d.get("response_data") or {}).get("entries")
        if entries is not None:
            for e in entries:
                print(f"  [{e.get('.tag')}] {e.get('path_display')} (size={e.get('size', '-')}, modified={e.get('server_modified', '-')})")
        else:
            print(json.dumps(res, ensure_ascii=False)[:1500])
    else:
        print(json.dumps(res, ensure_ascii=False)[:1500])

print("\n=== 4. Download tools.md & LEDGER.md from /gkhackter/ via Dropbox content API ===")
for fpath in ("/gkhackter/tools.md", "/gkhackter/LEDGER.md", "/gkhackter/0-STRUCTURE.md"):
    print(f"\n--- READ {fpath} ---")
    res = unwrap(call("COMPOSIO_PROXY_EXECUTE", {
        "toolkit_slug": "dropbox",
        "endpoint": "https://content.dropboxapi.com/2/files/download",
        "method": "POST",
        "headers": {"Dropbox-API-Arg": json.dumps({"path": fpath})},
    }))
    print(json.dumps(res, ensure_ascii=False)[:3000])
