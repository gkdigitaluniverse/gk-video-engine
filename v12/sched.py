import os, json, requests
from datetime import datetime, timedelta, timezone

K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
ORG="6afe914c34b70aac8c250902"
CH={"YT":"6afe91afece6dfde5f19c312","IG":"6afe9396ece6dfde5f19f9c4","FB":"6afe93c6ece6dfde5f19ffb9"}
IST=timezone(timedelta(hours=5,minutes=30))
BASE="https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1"

H={"Authorization":f"Bearer {K}","Content-Type":"application/json","Accept":"application/json, text/event-stream"}
s=requests.Session()
def parse(t):
    out=[]
    for line in t.splitlines():
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    return out
def init():
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=90)
    sid=r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"]=sid
    s.post(URL,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
M=[10]
def gql(q):
    M[0]+=1
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":M[0],"method":"tools/call","params":{"name":"COMPOSIO_PROXY_EXECUTE","arguments":{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}}}},timeout=280)
    for m in parse(r.text):
        if m.get("id")==M[0]:
            for c in ((m.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return r.text[:400]
def d3(o):
    try: return json.loads(o)["data"]["data"]["data"]
    except Exception: return None

init()

# ---------- 1. what is already scheduled ----------
used=set()
raw = gql('query { posts(first: 100, input: {organizationId: "%s"}) { edges { node { dueAt status channelService text } } } }' % ORG)
d = d3(raw)
if d and isinstance(d.get("posts"), dict):
    for e in d["posts"]["edges"]:
        n=e["node"]; due=n.get("dueAt")
        if due:
            try:
                dt=datetime.fromisoformat(due.replace("Z","+00:00")).astimezone(IST)
                used.add(dt.strftime("%Y-%m-%d"))
            except Exception: pass
    print("BUFFER POSTS FOUND:", len(d["posts"]["edges"]))
else:
    print("BUFFER POSTS QUERY FAILED — raw:", raw[:600])

print("DATES ALREADY USED:", sorted(used) if used else "none / unknown")

# ---------- 2. pick free 10:00 slots ----------
today=datetime.now(IST).date()
slots=[]
for i in range(1, 40):
    day=today+timedelta(days=i)
    ds=day.strftime("%Y-%m-%d")
    if ds in used: continue
    slots.append(ds)
    if len(slots)>=2: break
print("CHOSEN SLOTS:", slots)

# ---------- 3. content ----------
V=[{
 "slug":"cloudflare-playground-demo",
 "date":slots[0],
 "mp4":f"{BASE}/cf.mp4","png":f"{BASE}/cf.png",
 "yt_title":"Run An API In Your Browser — No Server, No Signup #Shorts",
 "yt_desc":"""Run a live API right inside your browser tab — no server, no signup, no CLI.
Cloudflare Workers Playground runs the code on the edge. Here is what it actually gives you.

• Write the fetch handler, hit Send, get a real response
• 100,000 requests per day on the free plan
• 10 ms CPU time per request — that is the real limit
• What it cannot do: no long jobs, no heavy packages

Source: Cloudflare Workers docs — checked 26 Nov 2026
Try it: https://workers.cloudflare.com/playground

cloudflare workers, workers playground, serverless api, free api hosting,
edge computing, cloudflare free plan, run api in browser, no server needed,
javascript api tutorial, cloudflare tutorial

#Shorts #Cloudflare #Serverless #WebDev""",
 "ig":"Bina server ke API chalao — seedha browser tab ke andar.\n\nCloudflare Workers Playground mein code likho, Send dabao, asli response aata hai.\n\n• Roz 1,00,000 requests free\n• Har request par 10 ms CPU — yahi asli hadd hai\n• Lambi jobs nahi chalengi\n\nSource: Cloudflare Workers docs — checked 26 Nov 2026\nTry it: https://workers.cloudflare.com/playground\n\n#Shorts #Cloudflare #Serverless #WebDev #Coding",
 "fb":"Bina server ke API chalao — seedha browser tab ke andar.\n\nCloudflare Workers Playground mein code likho, Send dabao, asli response aata hai.\n\n• Roz 1,00,000 requests free\n• Har request par 10 ms CPU — yahi asli hadd hai\n\nSource: Cloudflare Workers docs\nTry it: https://workers.cloudflare.com/playground\n\n#Shorts #Cloudflare #Serverless #WebDev",
 "first":"Kis API ko browser mein chalana chahoge? Batao.",
},{
 "slug":"google-sheets-multi-select",
 "date":slots[1],
 "mp4":f"{BASE}/sh.mp4","png":f"{BASE}/sh.png",
 "yt_title":"One Cell, Many Choices: Google Sheets Hidden Setting #Shorts",
 "yt_desc":"""Pick multiple values in one Google Sheets cell — no formula, no script.
It only works with chip-style dropdowns. Here is the exact setup.

• Turn on "Allow multiple selections" in Data Validation
• Switch Display style to Chip — other styles are disabled
• Keep Pending, Testing and Done in the same cell
• What breaks: the mobile app cannot select multiple yet

Source: Google Workspace Updates, 26 July 2024 — checked 26 Nov 2026
Try it: https://sheets.google.com

google sheets, multi select dropdown, dropdown chips, google sheets tricks,
spreadsheet tips, data validation, google sheets tutorial, excel alternative,
multiple values in one cell, google workspace tips

#Shorts #GoogleSheets #SpreadsheetTips #GoogleWorkspace""",
 "ig":"Ek cell mein kai choices — Google Sheets ka chhupa hua setting.\n\nData Validation mein dropdown banao, Allow multiple selections chalu karo, aur Display style Chip rakho.\n\n• Pending, Testing, Done — teeno ek hi cell mein\n• Sirf Chip style ke saath chalta hai\n• Mobile app par abhi nahi chalta\n\nSource: Google Workspace Updates, 26 July 2024 — checked 26 Nov 2026\nTry it: https://sheets.google.com\n\n#Shorts #GoogleSheets #SpreadsheetTips #GoogleWorkspace #Productivity",
 "fb":"Ek cell mein kai choices — Google Sheets ka chhupa hua setting.\n\nData Validation mein dropdown banao, Allow multiple selections chalu karo, aur Display style Chip rakho.\n\n• Pending, Testing, Done — teeno ek hi cell mein\n• Sirf Chip style ke saath chalta hai\n\nSource: Google Workspace Updates, 26 July 2024\nTry it: https://sheets.google.com\n\n#Shorts #GoogleSheets #SpreadsheetTips",
 "first":"Kis cell mein istemal karoge? Neeche batao.",
}]

def esc(t): return t.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")

def mk(v, date):
    due=f"{date}T10:00:00+05:30"
    jobs=[]
    # YouTube
    yt_meta=('{youtube: {title: "%s", categoryId: "28", privacy: "public", madeForKids: false, '
             'notifySubscribers: true, license: "youtube", embeddable: true, isAiGenerated: true}}') % esc(v["yt_title"])
    jobs.append(("YT", CH["YT"], v["yt_desc"], yt_meta, None))
    # IG reel
    jobs.append(("IG-reel", CH["IG"], v["ig"],
        '{instagram: {type: reel, shouldShareToFeed: true, isAiGenerated: true, firstComment: "%s"}}' % esc(v["first"]), v["mp4"]))
    # IG story
    jobs.append(("IG-story", CH["IG"], "Ek cell, kai choices. Google Sheets mein.\\n\\n#GoogleSheets #Shorts" if "sheets" in v["slug"] else "Bina server ke API. Browser mein.\\n\\n#Cloudflare #Shorts",
        '{instagram: {type: story, shouldShareToFeed: false, isAiGenerated: true}}', v["mp4"]))
    # FB reel
    jobs.append(("FB-reel", CH["FB"], v["fb"],
        '{facebook: {type: reel, firstComment: "%s"}}' % esc(v["first"]), v["mp4"]))
    # FB story
    jobs.append(("FB-story", CH["FB"], "Ek cell, kai choices.\\n\\n#GoogleSheets #Shorts" if "sheets" in v["slug"] else "Bina server ke API.\\n\\n#Cloudflare #Shorts",
        '{facebook: {type: story}}', v["mp4"]))
    return due, jobs

for v in V:
    due, jobs = mk(v, v["date"])
    print("\n==== ", v["slug"], "->", due)
    for tag, ch, text, meta, asset in jobs:
        assets = '[{video: {url: "%s"}}]' % asset if asset else "[]"
        q = ('mutation { createPost(input: {channelId: "%s", text: "%s", dueAt: "%s", mode: customScheduled, '
             'schedulingType: automatic, needsApproval: false, aiAssisted: true, assets: %s, metadata: %s}) '
             '{ __typename ... on PostActionSuccess { post { id dueAt status channelService } } '
             '... on MutationError { message } } }') % (ch, esc(text), due, assets, meta)
        out = gql(q)
        ok = '"id"' in out and 'errors' not in out[:200]
        print(f"  {tag:9} {'OK' if ok else 'FAIL'}  {out[:230]}")
