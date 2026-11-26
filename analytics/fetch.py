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

def _walk(obj, acc, depth=0):
    """JSON ke andar chhupe hue saare 'text' payloads nikaalo (double-encoded bhi)."""
    if depth > 6:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                acc.append(v)
            else:
                _walk(v, acc, depth + 1)
    elif isinstance(obj, list):
        for i in obj:
            _walk(i, acc, depth + 1)
    elif isinstance(obj, str):
        t = obj.strip()
        if t[:1] in "{[":
            try:
                _walk(json.loads(t), acc, depth + 1)
            except Exception:
                pass

def harvest(raw):
    """SSE stream ya plain JSON — dono se payloads nikaal do."""
    acc = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            s2 = line[5:].strip()
            try:
                _walk(json.loads(s2), acc)
            except Exception:
                pass
    if not acc:
        try:
            _walk(json.loads(raw), acc)
        except Exception:
            pass
    if not acc:
        acc.append(raw[:4000])
    return acc

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
    return r.text

def text_of(raw):
    """Sabse bada payload — jo actual data hota hai."""
    ps = harvest(raw)
    ps.sort(key=len, reverse=True)
    return ps[0] if ps else ""

def _as_json(txt):
    try:
        return json.loads(txt)
    except Exception:
        return None

def deep(d):
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
    """pairs = [(slug, args)] -> {slug: unwrapped result}"""
    raw = rpc("tools/call", {"name": "COMPOSIO_MULTI_EXECUTE_TOOL",
                             "arguments": {"tools": [{"tool_slug": s, "arguments": a} for s, a in pairs]}})
    out = {}
    for txt in harvest(raw):
        j = _as_json(txt)
        if not isinstance(j, dict):
            continue
        results = ((j.get("data") or {}).get("results")) if isinstance(j.get("data"), dict) else None
        if not results and isinstance(j.get("results"), list):
            results = j["results"]
        if not isinstance(results, list):
            continue
        for item in results:
            if not isinstance(item, dict):
                continue
            slug = item.get("tool_slug")
            if not slug:
                idx = item.get("index")
                slug = pairs[idx][0] if isinstance(idx, int) and idx < len(pairs) else None
            if not slug:
                continue
            if item.get("error"):
                out[slug] = {"__error__": str(item.get("error"))[:300]}
                log("  !", slug, str(item.get("error"))[:150])
            else:
                out[slug] = deep(item.get("response") or {})
    for s2, _ in pairs:
        out.setdefault(s2, {"__error__": "no result"})
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
    cands = ["INSTAGRAM_GET_IG_USER_MEDIA", "INSTAGRAM_GET_USER_MEDIA",
             "INSTAGRAM_LIST_IG_MEDIA", "INSTAGRAM_GET_MEDIA_LIST",
             "INSTAGRAM_GET_IG_MEDIA_LIST"]
    for slug in cands:
        for args in ({"ig_user_id": ig_id or "me", "limit": 25},
                     {"ig_user_id": ig_id or "me", "fields": "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count"}):
            rr = run_tools([(slug, args)])
            d = rr.get(slug)
            lst = d.get("data") if isinstance(d, dict) else d
            if isinstance(lst, list) and lst:
                media = lst
                log("IG media:", len(media), "via", slug)
                break
            log("IG media try", slug, list(args), "->", json.dumps(d)[:160])
        if media:
            break
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
             "shares,reactions.summary(total_count),comments.summary(total_count)")
FB_METRICS = ["post_impressions", "post_impressions_unique", "post_engaged_users",
              "post_clicks", "post_video_avg_time_watched", "post_video_view_time"]

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
            if not ins:
                for mset in (FB_METRICS, FB_METRICS[:3], ["post_impressions"]):
                    rr2 = run_tools([("FACEBOOK_GET_GRAPH_OBJECT",
                                      {"object_id": post.get("id"),
                                       "fields": "insights.metric(" + ",".join(mset) + ")"})])
                    d2 = rr2.get("FACEBOOK_GET_GRAPH_OBJECT")
                    if d2 and not (isinstance(d2, dict) and ("__error__" in d2 or "__fail__" in d2)):
                        ins = d2
                        break
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
    d = None
    for slug in ("YOUTUBE_LIST_CHANNEL_VIDEOS", "YOUTUBE_GET_MY_CHANNEL",
                 "YOUTUBE_LIST_VIDEOS", "YOUTUBE_SEARCH_LIST"):
        for args in ({"mine": True, "maxResults": 25, "part": "snippet,statistics"},
                     {"channelId": "mine", "maxResults": 25, "part": "snippet,statistics"},
                     {"maxResults": 25, "part": "snippet,statistics"}):
            rr = run_tools([(slug, args)])
            cand = rr.get(slug)
            if cand and not (isinstance(cand, dict) and ("__error__" in cand or "__fail__" in cand)):
                d = cand
                log("YT via", slug, json.dumps(args)[:80])
                break
            log("YT try", slug, json.dumps(args)[:60], "->", json.dumps(cand)[:140])
        if d:
            break
    out["channel_videos"] = d
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

    tl = text_of(rpc("tools/list", {}))
    try:
        n_tools = len((json.loads(tl) or {}).get("tools") or [])
    except Exception:
        n_tools = -1
    log("tools available:", n_tools)

    schemas = {}
    slugs = ["INSTAGRAM_GET_USER_INFO", "INSTAGRAM_GET_IG_USER_MEDIA",
             "INSTAGRAM_GET_IG_MEDIA_INSIGHTS", "FACEBOOK_LIST_MANAGED_PAGES",
             "FACEBOOK_GET_PAGE_POSTS", "YOUTUBE_LIST_CHANNEL_VIDEOS",
             "YOUTUBE_GET_VIDEO_DETAILS_BATCH"]
    txt = text_of(rpc("tools/call", {"name": "COMPOSIO_GET_TOOL_SCHEMAS", "arguments": {"tool_slugs": slugs}}))
    try:
        schemas = json.loads(txt)
    except Exception:
        schemas = {"raw": txt[:3000]}
    json.dump(schemas, open(os.path.join(OUT, "schemas.json"), "w"), ensure_ascii=False, indent=1)
    log("schemas saved")
    probe = ["INSTAGRAM_GET_IG_USER_MEDIA", "INSTAGRAM_GET_USER_MEDIA", "INSTAGRAM_LIST_IG_MEDIA",
             "INSTAGRAM_GET_MEDIA_LIST", "INSTAGRAM_GET_USER_INSIGHTS", "INSTAGRAM_GET_ACCOUNT_INSIGHTS",
             "YOUTUBE_LIST_CHANNEL_VIDEOS", "YOUTUBE_GET_MY_CHANNEL", "YOUTUBE_LIST_VIDEOS",
             "YOUTUBE_SEARCH_LIST", "YOUTUBE_GET_CHANNEL_STATISTICS",
             "FACEBOOK_GET_PAGE_INSIGHTS", "FACEBOOK_GET_POST_INSIGHTS", "FACEBOOK_GET_PAGE_POSTS"]
    t2 = text_of(rpc("tools/call", {"name": "COMPOSIO_GET_TOOL_SCHEMAS", "arguments": {"tool_slugs": probe}}))
    try:
        pj = json.loads(t2)
    except Exception:
        pj = {"raw": t2[:2000]}
    json.dump(pj, open(os.path.join(OUT, "probe.json"), "w"), ensure_ascii=False, indent=1)
    ok = []
    ts = (pj.get("data") or {}).get("tool_schemas") or {}
    for k in probe:
        if k in ts:
            ok.append(k)
    log("EXISTS:", ",".join(ok))

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
