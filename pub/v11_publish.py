import os, json, sys, requests

K = os.environ["CK"]
URL = "https://connect.composio.dev/mcp"
H = {"Authorization": f"Bearer {K}", "Content-Type": "application/json",
     "Accept": "application/json, text/event-stream"}
s = requests.Session()

def parse(t):
    out = []
    for line in t.splitlines():
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    return out

r = s.post(URL, headers=H, json={"jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
               "clientInfo": {"name": "p", "version": "1"}}}, timeout=60)
sid = r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
H2 = dict(H)
if sid: H2["Mcp-Session-Id"] = sid
s.post(URL, headers=H2, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, timeout=30)
_rid = [3000]

def call(name, args, to=300):
    _rid[0] += 1; rid = _rid[0]
    r = s.post(URL, headers=H2, json={"jsonrpc": "2.0", "id": rid, "method": "tools/call",
               "params": {"name": name, "arguments": args}}, timeout=to)
    r.encoding = "utf-8"
    for m in parse(r.text):
        if m.get("id") == rid: return m
    return {"raw": r.text[:400]}

def txt(m): return "".join(c.get("text", "") for c in (m.get("result") or {}).get("content", []))

def gql(query, variables=None):
    body = {"query": query}
    if variables: body["variables"] = variables
    m = call("COMPOSIO_PROXY_EXECUTE", {"toolkit_slug": "buffer", "endpoint": "",
                                        "method": "POST", "body": body})
    t = txt(m)
    try:
        d = json.loads(t)
        return d.get("data", {}).get("data", {}), t
    except Exception:
        return None, t

VIDEO = "https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1/2026-11-25-github-push-protection-FINAL.mp4"
DUE = "2026-11-26T10:00:00+05:30"
OLD_YT = "6b06fff3a2969125d5314695"   # first YouTube post: bullet chars came out garbled

TITLE = "Your API Key Is Public: GitHub Push Protection Explained #Shorts"

DESC = """One hardcoded API key in a public repo is readable by anyone who opens that file.
GitHub Push Protection stops the push before the secret ever reaches the repository.

- It blocks supported secrets at push time, not after the leak
- 532 partner patterns, and 465 of them are covered by push protection
- What it misses: only a subset is blocked, and a public-repo push over 50 MB is skipped
- The fix that always works: keep keys in environment variables, never in git

Source: docs.github.com - checked 25 Nov 2026

Push protection guide: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
What it scans and what it skips: https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope
All supported patterns: https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns

github push protection, api key leak, github secret scanning, hardcoded api key,
github security settings, env file, environment variables, git security,
github tricks, code security basics

#Shorts #GitHub #CyberSecurity #ApiSecurity"""

IG = """Ek hardcoded API key public repo mein - jo bhi file kholega, padh lega.
GitHub Push Protection push ko wahin rok deta hai, repo tak pahunchne se pehle.

- Supported secret push ke waqt hi block hota hai, leak ke baad nahi
- 532 partner patterns, unme se 465 push protection se cover
- Kami: sirf ek subset block hota hai, aur public repo mein 50 MB se bada push skip
- Pakka fix: keys environment variables mein, git mein kabhi nahi

Source: docs.github.com - checked 25 Nov 2026
Guide: https://docs.github.com/en/code-security/concepts/secret-security/push-protection

github push protection, api key leak, github secret scanning, hardcoded api key,
github security settings, env file, environment variables, git security,
github tricks, code security basics

#Shorts #GitHub #CyberSecurity #ApiSecurity #CodingTips #DevTips"""

FB = IG

IG_STORY = """API key git mein? Push Protection on karo.
https://docs.github.com/en/code-security/concepts/secret-security/push-protection

#Shorts #GitHub #CyberSecurity"""

FB_STORY = IG_STORY

FIRST_COMMENT = ("Which file in your repo would leak a key first - .env, config.js, "
                 "or something else? Tell me below.")

MUT = """mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id } }
    ... on MutationError { message }
  }
}"""

DEL = """mutation Del($id: ID!) {
  deletePost(id: $id) {
    __typename
    ... on PostActionSuccess { post { id } }
    ... on MutationError { message }
  }
}"""

def clean(d):
    return {k: v for k, v in d.items() if v != "" and v is not None}

def build(channel, text, meta_key, meta):
    inp = {
        "channelId": channel, "text": text,
        "assets": [{"video": {"url": VIDEO}}],
        "metadata": {meta_key: clean(meta)},
        "mode": "customScheduled", "dueAt": DUE,
        "schedulingType": "automatic", "needsApproval": False, "aiAssisted": True,
    }
    return inp

def post(label, inp):
    d, raw = gql(MUT, {"input": inp})
    print(f"\n##### {label} #####")
    print(json.dumps(d, ensure_ascii=False)[:900] if d else raw[:900])
    ok = bool(d) and d.get("data", {}).get("createPost", {}).get("__typename") == "PostActionSuccess"
    print("RESULT:", "PASS" if ok else "FAIL")
    return ok

def delete(label, pid):
    d, raw = gql(DEL, {"id": pid})
    print(f"\n##### DELETE {label} #####")
    print(json.dumps(d, ensure_ascii=False)[:600] if d else raw[:600])
    ok = bool(d) and d.get("data", {}).get("deletePost", {}).get("__typename") == "PostActionSuccess"
    print("RESULT:", "PASS" if ok else "FAIL")
    return ok

ONLY = sys.argv[1] if len(sys.argv) > 1 else "all"
def want(n): return ONLY in ("all", n)

if want("yt"):
    if delete("old YOUTUBE", OLD_YT):
        post("1 YOUTUBE", build("6afe91afece6dfde5f19c312", DESC, "youtube", {
            "title": TITLE, "categoryId": "28", "privacy": "public",
            "madeForKids": False, "notifySubscribers": True,
            "license": "youtube", "embeddable": True, "isAiGenerated": True}))
    else:
        print("!! old YouTube post not deleted - NOT creating a second one")

if want("igr"):
    post("2 INSTAGRAM REEL", build("6afe9396ece6dfde5f19f9c4", IG, "instagram", {
        "type": "reel", "shouldShareToFeed": True, "isAiGenerated": True,
        "firstComment": FIRST_COMMENT}))

if want("igs"):
    post("3 INSTAGRAM STORY", build("6afe9396ece6dfde5f19f9c4", IG_STORY, "instagram", {
        "type": "story", "shouldShareToFeed": False, "isAiGenerated": True}))

if want("fbr"):
    post("4 FACEBOOK REEL", build("6afe93c6ece6dfde5f19ffb9", FB, "facebook", {
        "type": "reel"}))

if want("fbs"):
    post("5 FACEBOOK STORY", build("6afe93c6ece6dfde5f19ffb9", FB_STORY, "facebook", {
        "type": "story"}))
