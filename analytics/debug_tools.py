"""analytics/debug_tools.py — sirf jaanch: meta tools ka schema aur raw jawab dekhna.
Kuch nahi badalta, sirf data/debug.json likhta hai.
"""
import os, json
from fetch import init, rpc, text_of, OUT

def main():
    init()
    out = {}

    # 1. meta tools ke schema
    res = rpc("tools/call", {"name": "COMPOSIO_GET_TOOL_SCHEMAS",
                             "arguments": {"tool_slugs": ["COMPOSIO_SEARCH_TOOLS", "COMPOSIO_MULTI_EXECUTE_TOOL"]}})
    try:
        out["meta_schemas"] = json.loads(text_of(res))
    except Exception:
        out["meta_schemas"] = text_of(res)[:3000]

    # 2. search ke alag-alag arg shapes
    shapes = [
        {"queries": [{"use_case": "list my instagram media and reels insights"}]},
        {"query": "list my instagram media and reels insights"},
        {"use_case": "list my instagram media and reels insights"},
    ]
    out["search"] = []
    for sh in shapes:
        r = rpc("tools/call", {"name": "COMPOSIO_SEARCH_TOOLS", "arguments": sh})
        out["search"].append({"args": sh, "raw": text_of(r)[:2500]})

    # 3. raw multi-execute — IG media list
    r = rpc("tools/call", {"name": "COMPOSIO_MULTI_EXECUTE_TOOL", "arguments": {"tools": [
        {"tool_slug": "INSTAGRAM_GET_IG_USER_MEDIA", "arguments": {"ig_user_id": "me", "limit": 25}},
        {"tool_slug": "FACEBOOK_GET_PAGE_POSTS", "arguments": {"page_id": "1270080059532814", "limit": 10}},
    ]}})
    out["multi_raw"] = text_of(r)[:4000]

    json.dump(out, open(os.path.join(OUT, "debug.json"), "w"), ensure_ascii=False, indent=1)
    print("debug written")

if __name__ == "__main__":
    main()
