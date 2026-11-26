"""
analytics/fetch.py — YouTube / Instagram / Facebook ka asli data laane wali script.

Kaam:
  1. Composio MCP se baat (runner se — sandbox se 502 aata hai)
  2. Instagram: user info -> media list -> per-media insights
  3. Facebook: pages -> posts -> per-post insights
  4. YouTube: channel videos -> video details (statistics)
  5. Sab kuch analytics/data/ me JSON me

Kya NAHI karta: publish nahi karta, delete nahi karta, purani file nahi chhoota.
Tools COMPOSIO_MULTI_EXECUTE_TOOL se chalte hain (individual tool name MCP par
expose nahi hote — pehle run me yahi galti pakdi gayi).
"""
import os, json, sys, datetime, traceback
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
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
     "Accept": "application/json, text/event-stream"}
_mid = [200]

def _parse(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    if not out:
        try: out.append(json.loads(text))
        except Exception: pass
    return out

def init():
    if not KEY:
        log("FATAL: COMPOSIO_KEY khaali hai")
        sys.exit(1)
    log("key length:", len(KEY))
    r = S.post(URL, headers=H, json={"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "gk-analytics", "version": "1"}}}, timeout=90)
    log("init HTTP", r.status_code)
    sid = r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"] = sid
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
    return {"__error__": {"message": r.text[:400]}, "__http__": r.status_code}

def text_of(res):
    if "__error__" in res:
        return json.dumps({"error": str(res["__error__"])[:400]})
    return "\n".join(c.get("text", "") for c in (res.get("content") or []) if c.get("type") == "text")

def deep(d, keys=("data", "response")):
    cur = d
    for _ in range(5):
        if isinstance(cur, dict):
            if "successful" in cur:
                if cur.get("successful") is False:
                    return {"__fail__": str(cur.get("error"))[:300]}
                cur = cur.get("data")
                continue
            if set(cur.keys()) == {"data"}:
                cur = cur["data"]; continue
            if set(cur.keys()) == {"response"}:
                cur = cur["response"]; continue
        break
    return cur

def run_tools(pairs):
    """pairs = [(slug, args), ...] -> {slug: unwrapped result}"""
    res = rpc("tools/call", {"name": "COMPOSIO_MULTI_EXECUTE_TOOL",
                             "arguments": {"tools": [{"tool_slug": s, "arguments": a} for s, a in pairs]}})
    txt = text_of(res)
    try:
        j = json.loads(txt)
    except Exception:
        log("multi_execute raw:", txt[:300])
        return {s: {"__error__": txt[:300]} for s, _ in pairs}
    out = {}
    for item in (((j.get("data") or {}).get("results")) or []):
        slug = item.get("tool_slug") or pairs[(item.get("index") or 0)][0]
        resp = item.get("response") or {}
        out[slug] = deep(resp) if not item.get("error") else {"__error__": str(item.get("error"))[:300]}
        if item.get("error"):
            log("  !", slug, str(item.get("error"))[:160])
    for s, _ in pairs:
        out.setdefault(s, {"__error__": "no result"})
    return out

# ------------------------- Instagram -------------------------
IG_METRICS_FULL = ["reach", "likes", "comments", "saved", "shares", "total_interactions",
                   "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "views", "plays"]
IG_METRICS_MIN = ["reach", "likes", "comments", "saved", "shares", "total_interactions"]

def instagram():
    out = {"user": None, "media": [], "rows": []}
    r = run_tools([("INSTAGRAM_GET_USER_INFO",
                    {"ig_user_id": "me",
                     "fields": "id,user_id,username,name,account_type,followers_count,follows_count,media_count,biography"})])
    user = r.get("INSTAGRAM_GET_USER_INFO")
    out["user"] = user
    log("IG user:", json.dumps(user)[:400])

    ig_id = None
    if isinstance(user, dict):
        ig_id = user.get("id") or user.get("user_id") or user.get("ig_user_id")
    log("IG id:", ig_id)

    media = []
    for args in ({"ig_user_id": ig_id or "me", "limit": 25},
                 {"ig_user_id": ig_id or "me", "fields": "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count"}):
        rr = run_tools([("INSTAGRAM_GET_IG_USER_MEDIA", args)])
        d = rr.get("INSTAGRAM_GET_IG_USER_MEDIA")
        lst = d.get("data") if isinstance(d, dict) else d
        if isinstance(lst, list) and lst:
            media = lst
            log("IG media:", len(media), "via", list(args))
            break
        log("IG media try", list(args), "->", json.dumps(d)[:200])
    out["media"] = media

    for m in media[:20]:
        if not isinstance(m, dict): continue
        mid = m.get("id")
        if not mid: continue
        row = {"id": mid, "type": m.get("media_type"), "product": m.get("media_product_type"),
               "at": m.get("timestamp"), "link": m.get("permalink"),
               "caption": (m.get("caption") or "")[:150],
               "likes": m.get("like_count"), "comments": m.get("comments_count")}
        got = None
        for metrics in (IG_METRICS_FULL, IG_METRICS_MIN):
            rr = run_tools([("INSTAGRAM_GET_IG_MEDIA_INSIGHTS", {"ig_media_id": mid, "metric": metrics})])
            d = rr.get("INSTAGRAM_GET_IG_MEDIA_INSIGHTS")
            if d and not (isinstance(d, dict) and ("__error__" in d or "__fail__" in d)):
                got = d
                break
        row["insights"] = got
        out["rows"].append(row)
        log("IG insights", mid, "->", json.dumps(got)[:220])
    return out

# ------------------------- Facebook -------------------------
FB_FIELDS = ("id,message,created_time,permalink_url,full_picture,"
             "shares,reactions.summary(total_count),comments.summary(total_count),"
             "insights.metric(post_impressions,post_impressions_unique,"
             "post_video_avg_time_watched,post_video_view_time,post_clicks,post_reactions_by_type_total)")

def facebook():
    out = {"pages": [], "rows": []}
    rr = run_tools([("FACEBOOK_LIST_MANAGED_PAGES", {"limit": 25, "fields": "id,name,category,fan_count,followers_count,link"})])
    d = rr.get("FACEBOOK_LIST_MANAGED_PAGES")
    pages = d.get("data") if isinstance(d, dict) else d
    if isinstance(pages, list):
        out["pages"] = [{"id": p.get("id"), "name": p.get("name"),
                         "category": p.get("category"), "fans": p.get("fan_count"),
                         "followers": p.get("followers_count")} for p in pages if isinstance(p, dict)]
    log("FB pages:", json.dumps(out["pages"])[:400])

    for p in out["pages"][:3]:
        pid = p.get("id")
        rr = run_tools([("FACEBOOK_GET_PAGE_POSTS", {"page_id": pid, "limit": 20, "fields": FB_FIELDS})])
        d = rr.get("FACEBOOK_GET_PAGE_POSTS")
        posts = d.get("data") if isinstance(d, dict) else d
        if not isinstance(posts, list) or not posts:
            log("FB posts for", pid, "->", json.dumps(d)[:220])
            continue
        for post in posts[:20]:
            if not isinstance(post, dict): continue
            ins = None
            pi = post.get("insights")
            if isinstance(pi, dict):
                ins = pi.get("data") or pi
            out["rows"].append({
                "page": p.get("name"), "post_id": post.get("id"),
                "at": post.get("created_time"), "link": post.get("permalink_url"),
                "message": (post.get("message") or "")[:160],
                "likes": ((post.get("reactions") or {}).get("summary") or {}).get("total_count"),
                "comments": ((post.get("comments") or {}).get("summary") or {}).get("total_count"),
                "shares": (post.get("shares") or {}).get("count"),
                "insights": ins,
            })
            log("FB post", post.get("id"), "insights:", json.dumps(ins)[:200])
    return out

# ------------------------- YouTube -------------------------
def youtube():
    out = {"channel_videos": None, "videos": [], "note": ""}
    rr = run_tools([("YOUTUBE_LIST_CHANNEL_VIDEOS", {"mine": True, "maxResults": 25, "part": "snippet,statistics"})])
    d = rr.get("YOUTUBE_LIST_CHANNEL_VIDEOS")
    out["channel_videos"] = d
    log("YT channel videos:", json.dumps(d)[:400])

    items = []
    if isinstance(d, dict):
        items = d.get("items") or (d.get("data") or {}).get("items") or []
    ids = [((i.get("contentDetails") or {}).get("videoId") or i.get("id")) for i in items if isinstance(i, dict)]
    ids = [i for i in ids if i]
    if ids:
        rr = run_tools([("YOUTUBE_GET_VIDEO_DETAILS_BATCH", {"id": ids[:50], "parts": ["snippet", "statistics", "contentDetails"]})])
        out["videos"] = rr.get("YOUTUBE_GET_VIDEO_DETAILS_BATCH")
        log("YT details:", json.dumps(out["videos"])[:400])
    else:
        out["note"] = "channel video list khaali ya 403 — upar ka jawab dekho"
    return out

def main():
    started = datetime.datetime.utcnow().isoformat() + "Z"
    status = init()
    log("started", started)

    tl = rpc("tools/list", {})
    log("tools available:", len([t for t in (tl.get("tools") or [])]))

    schemas = {}
    slugs = ["INSTAGRAM_GET_USER_INFO", "INSTAGRAM_GET_IG_USER_MEDIA",
             "INSTAGRAM_GET_IG_MEDIA_INSIGHTS", "FACEBOOK_LIST_MANAGED_PAGES",
             "FACEBOOK_GET_PAGE_POSTS", "YOUTUBE_LIST_CHANNEL_VIDEOS",
             "YOUTUBE_GET_VIDEO_DETAILS_BATCH"]
    res = rpc("tools/call", {"name": "COMPOSIO_GET_TOOL_SCHEMAS", "arguments": {"tool_slugs": slugs}})
    txt = text_of(res)
    try:
        schemas = json.loads(txt)
    except Exception:
        schemas = {"raw": txt[:3000]}
    json.dump(schemas, open(os.path.join(OUT, "schemas.json"), "w"), ensure_ascii=False, indent=1)
    log("schemas saved")

    result = {"run_at": started, "http_init": status}
    for name, fn in (("instagram", instagram), ("facebook", facebook), ("youtube", youtube)):
        try:
            result[name] = fn()
        except Exception as e:
            result[name] = {"error": str(e), "trace": traceback.format_exc()[-1000:]}
            log(name, "EXCEPTION", str(e)[:300])

    day = datetime.date.today().isoformat()
    payload = {"run_at": started, "key_len": len(KEY), "data": result}
    json.dump(payload, open(os.path.join(OUT, "latest.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(payload, open(os.path.join(OUT, f"{day}.json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, "RUN.txt"), "w").write("\n".join(LOG) + "\n")
    log("DONE")

if __name__ == "__main__":
    main()
