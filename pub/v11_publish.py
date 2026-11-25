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
_rid = [2000]

def call(name, args, to=300):
    _rid[0] += 1; rid = _rid[0]
    r = s.post(URL, headers=H2, json={"jsonrpc": "2.0", "id": rid, "method": "tools/call",
               "params": {"name": name, "arguments": args}}, timeout=to)
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

def fields(type_name):
    d, _ = gql('{ __type(name: "%s") { inputFields { name } } }' % type_name)
    try: return [f["name"] for f in d["data"]["__type"]["inputFields"]]
    except Exception: return []

VIDEO = "https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1/2026-11-25-github-push-protection-FINAL.mp4"
THUMB = "https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1/2026-11-25-github-push-protection-thumbnail.png"
DUE = "2026-11-26T10:00:00+05:30"

TITLE = "Your API Key Is Public: GitHub Push Protection Explained #Shorts"

DESC = """One hardcoded API key in a public repo is readable by anyone who opens that file.
GitHub Push Protection stops the push before the secret ever reaches the repository.

• It blocks supported secrets at push time — not after the leak
• 532 partner patterns, and 465 of them are covered by push protection
• What it misses: only a subset is blocked, and a public-repo push over 50 MB is skipped
• The fix that always works: keep keys in environment variables, never in git

Source: docs.github.com — checked 25 Nov 2026

Push protection guide: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
What it scans and what it skips: https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope
All supported patterns: https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns

github push protection, api key leak, github secret scanning, hardcoded api key,
github security settings, env file, environment variables, git security,
github tricks, code security basics

#Shorts #GitHub #CyberSecurity #ApiSecurity"""

IG = """Ek hardcoded API key public repo mein — jo bhi file kholega, padh lega.
GitHub Push Protection push ko wahin rok deta hai, repo tak pahunchne se pehle.

• Supported secret push ke waqt hi block hota hai — leak ke baad nahi
• 532 partner patterns, unme se 465 push protection se cover
• Kami: sirf ek subset block hota hai, aur public repo mein 50 MB se bada push skip
• Pakka fix: keys environment variables mein, git mein kabhi nahi

Source: docs.github.com — checked 25 Nov 2026
Guide: https://docs.github.com/en/code-security/concepts/secret-security/push-protection

github push protection, api key leak, github secret scanning, hardcoded api key,
github security settings, env file, environment variables, git security,
github tricks, code security basics

#Shorts #GitHub #CyberSecurity #ApiSecurity #CodingTips #DevTips"""

FB = IG

IG_STORY = """API key git mein? Push Protection on karo.
https://docs.github.com/en/code-security/concepts/secret-security/push-protection

#Shorts #GitHub #CyberSecurity"""

FB_STORY = """API key git mein? Push protection on karo.
https://docs.github.com/en/code-security/concepts/secret-security/push-protection

#Shorts #GitHub #CyberSecurity"""

FIRST_COMMENT = ("Which file in your repo would leak a key first — .env, config.js, "
                 "or something else? Tell me below.")

MUT = """mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id text } }
    ... on MutationError { message }
  }
}"""

# ---------- discover the real schema ----------
cf = fields("CreatePostInput")
igf = fields("InstagramPostMetadataInput")
fbf = fields("FacebookPostMetadataInput")
print("CreatePostInput:", cf)
print("InstagramPostMetadataInput:", igf)
print("FacebookPostMetadataInput:", fbf)

def build(channel, text, meta_key, meta, asset="video"):
    inp = {
        "channelId": channel,
        "text": text,
        "assets": [{asset: {"url": VIDEO}}],
        "metadata": {meta_key: meta},
        "mode": "customScheduled",
        "dueAt": DUE,
        "schedulingType": "automatic",
        "needsApproval": False,
        "aiAssisted": True,
    }
    if cf:
        inp = {k: v for k, v in inp.items() if k in cf}
    allowed = {"youtube": None, "instagram": igf, "facebook": fbf}[meta_key]
    if allowed:
        meta = {k: v for k, v in meta.items() if k in allowed}
    inp["metadata"] = {meta_key: meta}
    return inp

def post(label, inp):
    d, raw = gql(MUT, {"input": inp})
    print(f"\n##### {label} #####")
    print(json.dumps(d, ensure_ascii=False)[:1200] if d else raw[:1200])
    ok = bool(d) and d.get("data", {}).get("createPost", {}).get("__typename") == "PostActionSuccess"
    print("RESULT:", "PASS" if ok else "FAIL")
    return ok

ONLY = sys.argv[1] if len(sys.argv) > 1 else "all"

def want(n): return ONLY in ("all", n)

if want("yt"):
    post("1 YOUTUBE", build("6afe91afece6dfde5f19c312", DESC, "youtube", {
        "title": TITLE, "categoryId": "28", "privacy": "public",
        "madeForKids": False, "notifySubscribers": True,
        "license": "youtube", "embeddable": True, "isAiGenerated": True}))

if want("igr"):
    post("2 INSTAGRAM REEL", build("6afe9396ece6dfde5f19f9c4", IG, "instagram", {
        "type": "reel", "shouldShareToFeed": True, "isAiGenerated": True,
        "firstComment": FIRST_COMMENT, "geolocation": ""}))

if want("igs"):
    post("3 INSTAGRAM STORY", build("6afe9396ece6dfde5f19f9c4", IG_STORY, "instagram", {
        "type": "story", "shouldShareToFeed": False, "isAiGenerated": True,
        "firstComment": "", "geolocation": ""}))

if want("fbr"):
    post("4 FACEBOOK REEL", build("6afe93c6ece6dfde5f19ffb9", FB, "facebook", {
        "type": "reel", "firstComment": "", "linkAttachment": ""}))

if want("fbs"):
    post("5 FACEBOOK STORY", build("6afe93c6ece6dfde5f19ffb9", FB_STORY, "facebook", {
        "type": "story", "firstComment": "", "linkAttachment": ""}))
