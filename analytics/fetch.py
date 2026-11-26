"""
analytics/fetch.py — YouTube / Instagram / Facebook ka asli data laane wali script.

Kya karta hai:
  1. Composio MCP se baat karta hai (runner se, kyunki sandbox se 502 aata hai)
  2. Instagram: user info -> media list -> per-media insights
  3. Facebook: pages -> posts -> per-post insights
  4. YouTube: jo tools milte hain, unse koshish (channel-level 403 ho sakta hai)
  5. Sab kuch analytics/data/ me JSON ke roop me likhta hai

Kya NAHI karta: kuch publish nahi karta, kuch delete nahi karta,
repo ki koi purani file nahi chhoota.
"""
import os, json, sys, time, datetime, traceback
import requests

URL = "https://connect.composio.dev/mcp"
KEY = os.environ.get("COMPOSIO_KEY") or os.environ.get("CK") or ""
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)

LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)

S = requests.Session()
H = {
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
_mid = [100]

def _parse(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            try:
                out.append(json.loads(line[5:].strip()))
            except Exception:
                pass
    if not out:
        try:
            out.append(json.loads(text))
        except Exception:
            pass
    return out

def init():
    if not KEY:
        log("FATAL: COMPOSIO_KEY khaali hai (secret set nahi)")
        sys.exit(1)
    log("key length:", len(KEY))
    r = S.post(URL, headers=H, json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "gk-analytics", "version": "1"}}}, timeout=90)
    log("init HTTP", r.status_code)
    sid = r.headers.get("mcp-session-id")
    if sid:
        H["mcp-session-id"] = sid
    S.post(URL, headers=H, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, timeout=30)
    return r.status_code

def rpc(method, params, timeout=280):
    _mid[0] += 1
    mid = _mid[0]
    r = S.post(URL, headers=H, json={"jsonrpc": "2.0", "id": mid, "method": method, "params": params}, timeout=timeout)
    for m in _parse(r.text):
        if m.get("id") == mid:
            if "error" in m:
                return {"__error__": m["error"], "__http__": r.status_code}
            return m.get("result", {})
    return {"__error__": {"message": r.text[:500]}, "__http__": r.status_code}

def call(tool, args):
    """Ek tool chalao, text nikaalo, JSON me badlo. Kabhi crash nahi karta."""
    res = rpc("tools/call", {"name": tool, "arguments": args})
    if "__error__" in res:
        return {"ok": False, "error": str(res["__error__"])[:600]}
    texts = []
    for c in (res.get("content") or []):
        if c.get("type") == "text":
            texts.append(c.get("text", ""))
    raw = "\n".join(texts)
    try:
        return {"ok": True, "data": json.loads(raw)}
    except Exception:
        return {"ok": True, "text": raw[:4000]}

def unwrap(d):
    """Composio ka jawab aksar data.data.data me hota hai — jitna gehra ho utna khol do."""
    cur = d
    for _ in range(4):
        if isinstance(cur, dict):
            if "successful" in cur and "data" in cur:
                if cur.get("successful") is False:
                    return {"__fail__": str(cur)[:400]}
                cur = cur["data"]
                continue
            if "response" in cur and isinstance(cur["response"], dict):
                cur = cur["response"]
                continue
            if set(cur.keys()) == {"data"}:
                cur = cur["data"]
                continue
        break
    return cur

# ---------------- Instagram ----------------
def ig():
    out = {"user": None, "media": [], "insights": []}
    r = call("INSTAGRAM_GET_USER_INFO", {})
    out["user"] = unwrap(r.get("data")) if r.get("ok") else r
    log("IG user:", json.dumps(out["user"])[:300] if out["user"] else "FAIL")

    ig_id = None
    u = out["user"]
    if isinstance(u, dict):
        for k in ("id", "user_id", "ig_user_id"):
            if u.get(k):
                ig_id = u[k]
                break
    log("IG id:", ig_id)

    for args in ([{"ig_user_id": ig_id, "limit": 25}] if ig_id else []) + [{"limit": 25}, {}]:
        r = call("INSTAGRAM_GET_IG_MEDIA", args)
        d = unwrap(r.get("data")) if r.get("ok") else None
        if isinstance(d, dict) and (d.get("data") or d.get("media") or d.get("items")):
            out["media"] = d.get("data") or d.get("media") or d.get("items")
            log("IG media via", args, "->", len(out["media"]))
            break
        log("IG media try", args, "->", str(d or r)[:200])

    METRICS = "reach,plays,likes,comments,saved,shares,total_interactions,ig_reels_avg_watch_time,ig_reels_video_view_total_time,impressions"
    for m in out["media"][:15]:
        mid = m.get("id") if isinstance(m, dict) else None
        if not mid:
            continue
        row = {"media_id": mid, "caption": (m.get("caption") or "")[:120],
               "media_type": m.get("media_type"), "timestamp": m.get("timestamp"),
               "permalink": m.get("permalink"), "like_count": m.get("like_count"),
               "comments_count": m.get("comments_count")}
        got = None
        for args in ({"ig_media_id": mid, "metric": METRICS},
                     {"media_id": mid, "metric": METRICS},
                     {"ig_media_id": mid}):
            r = call("INSTAGRAM_GET_IG_MEDIA_INSIGHTS", args)
            d = unwrap(r.get("data")) if r.get("ok") else r
            if isinstance(d, (dict, list)) and "__fail__" not in str(d)[:20]:
                if "error" not in str(d)[:60].lower():
                    got = d
                    break
        row["insights"] = got
        out["insights"].append(row)
        log("IG insights", mid, "->", str(got)[:160])
    return out

# ---------------- Facebook ----------------
def fb():
    out = {"pages": [], "posts": [], "insights": []}
    r = call("FACEBOOK_LIST_MANAGED_PAGES", {})
    d = unwrap(r.get("data")) if r.get("ok") else r
    pages = (d or {}).get("data") if isinstance(d, dict) else d
    if isinstance(pages, list):
        out["pages"] = [{"id": p.get("id"), "name": p.get("name")} for p in pages]
    log("FB pages:", out["pages"])

    for p in out["pages"][:3]:
        pid = p.get("id")
        posts = None
        for args in ({"page_id": pid, "limit": 25}, {"id": pid, "limit": 25}):
            r = call("FACEBOOK_GET_PAGE_POSTS", args)
            d = unwrap(r.get("data")) if r.get("ok") else r
            lst = (d or {}).get("data") if isinstance(d, dict) else d
            if isinstance(lst, list) and lst:
                posts = lst
                break
            log("FB posts try", args, "->", str(d or r)[:200])
        if not posts:
            continue
        for post in posts[:15]:
            row = {"page": p.get("name"), "post_id": post.get("id"),
                   "created": post.get("created_time"),
                   "message": (post.get("message") or "")[:160],
                   "permalink": post.get("permalink_url"),
                   "likes": ((post.get("reactions") or {}).get("summary") or {}).get("total_count") if isinstance(post.get("reactions"), dict) else None,
                   "comments": ((post.get("comments") or {}).get("summary") or {}).get("total_count") if isinstance(post.get("comments"), dict) else None}
            got = None
            for args in (
                {"object_id": post.get("id"), "edge": "insights",
                 "fields": "post_impressions,post_impressions_unique,post_video_avg_time_watched,post_video_view_time,post_clicks,post_reactions_by_type_total"},
                {"node_id": post.get("id"), "edge": "insights",
                 "params": {"metric": "post_impressions,post_impressions_unique,post_video_avg_time_watched"}},
            ):
                r = call("FACEBOOK_GET_GRAPH_OBJECT", args)
                d = unwrap(r.get("data")) if r.get("ok") else r
                if d and "error" not in str(d)[:60].lower() and "__fail__" not in str(d)[:20]:
                    got = d
                    break
            row["insights"] = got
            out["insights"].append(row)
            out["posts"].append(row)
            log("FB insights", post.get("id"), "->", str(got)[:160])
    return out

# ---------------- YouTube ----------------
def yt():
    out = {"channel": None, "videos": [], "note": ""}
    r = call("YOUTUBE_GET_VIDEO_DETAILS_BATCH", {"video_ids": [], "part": "snippet,statistics"})
    out["probe"] = str(r)[:300]
    out["note"] = ("Channel-level data pehle 403 de raha tha (scope). "
                   "Video IDs ke bina channel ki list nahi mil sakti — "
                   "isliye yahan sirf note hai, koi anka nahi.")
    log("YT probe:", out["probe"][:200])
    return out

def main():
    started = datetime.datetime.utcnow().isoformat() + "Z"
    status = init()
    log("started", started)

    tools = rpc("tools/list", {})
    names = [t.get("name") for t in (tools.get("tools") or [])]
    log("tools available:", len(names))

    schemas = {}
    for slug in ["INSTAGRAM_GET_USER_INFO", "INSTAGRAM_GET_IG_MEDIA",
                 "INSTAGRAM_GET_IG_MEDIA_INSIGHTS", "FACEBOOK_LIST_MANAGED_PAGES",
                 "FACEBOOK_GET_PAGE_POSTS", "FACEBOOK_GET_GRAPH_OBJECT",
                 "YOUTUBE_GET_VIDEO_DETAILS_BATCH"]:
        r = rpc("tools/call", {"name": "COMPOSIO_GET_TOOL_SCHEMAS", "arguments": {"tool_slugs": [slug]}})
        txt = "".join(c.get("text", "") for c in (r.get("content") or []) if c.get("type") == "text")
        try:
            schemas[slug] = json.loads(txt)
        except Exception:
            schemas[slug] = txt[:1500]
    json.dump(schemas, open(os.path.join(OUT, "schemas.json"), "w"), ensure_ascii=False, indent=1)
    log("schemas saved")

    result = {"run_at": started, "http_init": status}
    for name, fn in (("instagram", ig), ("facebook", fb), ("youtube", yt)):
        try:
            result[name] = fn()
        except Exception as e:
            result[name] = {"error": str(e), "trace": traceback.format_exc()[-1200:]}
            log(name, "EXCEPTION", str(e)[:300])

    day = datetime.date.today().isoformat()
    payload = {"run_at": started, "key_len": len(KEY), "data": result}
    json.dump(payload, open(os.path.join(OUT, "latest.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(payload, open(os.path.join(OUT, f"{day}.json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, "RUN.txt"), "w").write("\n".join(LOG) + "\n")
    log("DONE — files written")

if __name__ == "__main__":
    main()
