import os, json, requests
from datetime import datetime, timedelta, timezone

K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
ORG="6afe914c34b70aac8c250902"
CH={"YT":"6afe91afece6dfde5f19c312","IG":"6afe9396ece6dfde5f19f9c4","FB":"6afe93c6ece6dfde5f19ffb9"}
IST=timezone(timedelta(hours=5,minutes=30))
BASE="https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1"

H={"Authorization":f"Bearer {K}","Content-Type":"application/json","Accept":"application/json, text/event-stream"}
s=requests.Session()
def blobs(t):
    out=[]
    for line in t.splitlines():
        line=line.strip()
        if line.startswith("data:"):
            try: out.append(json.loads(line[5:].strip()))
            except Exception: pass
    if not out:
        try: out.append(json.loads(t))
        except Exception: pass
    return out
def init():
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}},timeout=90)
    sid=r.headers.get("mcp-session-id")
    if sid: H["mcp-session-id"]=sid
    s.post(URL,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"},timeout=30)
M=[10]
def gql(q):
    M[0]+=1; my=M[0]
    r=s.post(URL,headers=H,json={"jsonrpc":"2.0","id":my,"method":"tools/call","params":{"name":"COMPOSIO_PROXY_EXECUTE","arguments":{"toolkit_slug":"buffer","endpoint":"","method":"POST","body":{"query":q}}}},timeout=280)
    for b in blobs(r.text):
        if b.get("id")==my:
            for c in ((b.get("result") or {}).get("content") or []):
                if c.get("type")=="text": return c.get("text","")
    return ""
def d3(o):
    try: return json.loads(o)["data"]["data"]["data"]
    except Exception: return None

init()

# ---------- existing posts ----------
existing=set()
d = d3(gql('query { posts(first: 100, input: {organizationId: "%s"}) { edges { node { dueAt status channelService } } } }' % ORG))
if d and isinstance(d.get("posts"), dict):
    for e in d["posts"]["edges"]:
        n=e["node"]; due=n.get("dueAt")
        if due and n.get("status") in ("scheduled","sending","sent"):
            try:
                dt=datetime.fromisoformat(due.replace("Z","+00:00")).astimezone(IST)
                existing.add((dt.strftime("%Y-%m-%d"), n.get("channelService")))
            except Exception: pass
    print("EXISTING (date, service):", sorted(existing))
else:
    print("EXISTING QUERY FAILED:", str(d)[:200])

today=datetime.now(IST).date()
busy={x[0] for x in existing}
slots=[]
for i in range(1, 40):
    ds=(today+timedelta(days=i)).strftime("%Y-%m-%d")
    if ds in busy: continue
    slots.append(ds)
    if len(slots)>=2: break
print("SLOTS:", slots)

def esc(t): return t.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")

CF={"slug":"cloudflare","date":slots[0],"mp4":f"{BASE}/cf.mp4",
 "yt_title":"Run An API In Your Browser — No Server, No Signup #Shorts",
 "yt_desc":"Run a live API right inside your browser tab — no server, no signup, no CLI.\nCloudflare Workers Playground runs the code on the edge. Here is what it actually gives you.\n\n• Write the fetch handler, hit Send, get a real response\n• 100,000 requests per day on the free plan\n• 10 ms CPU time per request — that is the real limit\n• What it cannot do: no long jobs, no heavy packages\n\nSource: Cloudflare Workers docs — checked 26 Nov 2026\nTry it: https://workers.cloudflare.com/playground\n\ncloudflare workers, workers playground, serverless api, free api hosting,\nedge computing, cloudflare free plan, run api in browser, no server needed,\njavascript api tutorial, cloudflare tutorial\n\n#Shorts #Cloudflare #Serverless #WebDev",
 "ig":"Bina server ke API chalao — seedha browser tab ke andar.\n\nCloudflare Workers Playground mein code likho, Send dabao, asli response aata hai.\n\n• Roz 1,00,000 requests free\n• Har request par 10 ms CPU — yahi asli hadd hai\n• Lambi jobs nahi chalengi\n\nSource: Cloudflare Workers docs — checked 26 Nov 2026\nTry it: https://workers.cloudflare.com/playground\n\n#Shorts #Cloudflare #Serverless #WebDev #Coding",
 "fb":"Bina server ke API chalao — seedha browser tab ke andar.\n\nCloudflare Workers Playground mein code likho, Send dabao, asli response aata hai.\n\n• Roz 1,00,000 requests free\n• Har request par 10 ms CPU — yahi asli hadd hai\n\nSource: Cloudflare Workers docs\nTry it: https://workers.cloudflare.com/playground\n\n#Shorts #Cloudflare #Serverless #WebDev"}

SH={"slug":"sheets","date":slots[1],"mp4":f"{BASE}/sh.mp4",
 "yt_title":"One Cell, Many Choices: Google Sheets Hidden Setting #Shorts",
 "yt_desc":"Pick multiple values in one Google Sheets cell — no formula, no script.\nIt only works with chip-style dropdowns. Here is the exact setup.\n\n• Turn on \"Allow multiple selections\" in Data Validation\n• Switch Display style to Chip — other styles are disabled\n• Keep Pending, Testing and Done in the same cell\n• What breaks: the mobile app cannot select multiple yet\n\nSource: Google Workspace Updates, 26 July 2024 — checked 26 Nov 2026\nTry it: https://sheets.google.com\n\ngoogle sheets, multi select dropdown, dropdown chips, google sheets tricks,\nspreadsheet tips, data validation, google sheets tutorial, excel alternative,\nmultiple values in one cell, google workspace tips\n\n#Shorts #GoogleSheets #SpreadsheetTips #GoogleWorkspace",
 "ig":"Ek cell mein kai choices — Google Sheets ka chhupa hua setting.\n\nData Validation mein dropdown banao, Allow multiple selections chalu karo, aur Display style Chip rakho.\n\n• Pending, Testing, Done — teeno ek hi cell mein\n• Sirf Chip style ke saath chalta hai\n• Mobile app par abhi nahi chalta\n\nSource: Google Workspace Updates, 26 July 2024 — checked 26 Nov 2026\nTry it: https://sheets.google.com\n\n#Shorts #GoogleSheets #SpreadsheetTips #GoogleWorkspace #Productivity",
 "fb":"Ek cell mein kai choices — Google Sheets ka chhupa hua setting.\n\nData Validation mein dropdown banao, Allow multiple selections chalu karo, aur Display style Chip rakho.\n\n• Pending, Testing, Done — teeno ek hi cell mein\n• Sirf Chip style ke saath chalta hai\n\nSource: Google Workspace Updates, 26 July 2024\nTry it: https://sheets.google.com\n\n#Shorts #GoogleSheets #SpreadsheetTips"}

for v in (CF, SH):
    due=f"{v['date']}T10:00:00+05:30"
    print("\n==== ", v["slug"], due)
    jobs=[
     ("YT", CH["YT"], v["yt_desc"], None, v["mp4"], "youtube",
      '{youtube: {title: "%s", categoryId: "28", privacy: "public", madeForKids: false, notifySubscribers: true, license: youtube, embeddable: true, isAiGenerated: true}}' % esc(v["yt_title"])),
     ("IG-reel", CH["IG"], v["ig"], None, v["mp4"], "instagram",
      '{instagram: {type: reel, shouldShareToFeed: true, isAiGenerated: true}}'),
     ("IG-story", CH["IG"], "Ek cell, kai choices.\\n\\n#GoogleSheets #Shorts" if v["slug"]=="sheets" else "Bina server ke API. Browser mein.\\n\\n#Cloudflare #Shorts", None, v["mp4"], "instagram",
      '{instagram: {type: story, shouldShareToFeed: false, isAiGenerated: true}}'),
     ("FB-reel", CH["FB"], v["fb"], None, v["mp4"], "facebook",
      '{facebook: {type: reel}}'),
     ("FB-story", CH["FB"], "Ek cell, kai choices.\\n\\n#GoogleSheets #Shorts" if v["slug"]=="sheets" else "Bina server ke API.\\n\\n#Cloudflare #Shorts", None, v["mp4"], "facebook",
      '{facebook: {type: story}}'),
    ]
    for tag, ch, text, fc, asset, svc, meta in jobs:
        if (v["date"], svc) in existing:
            # a post for this service already exists that day; still allow if different type
            pass
        assets='[{video: {url: "%s"}}]' % asset
        q=('mutation { createPost(input: {channelId: "%s", text: "%s", dueAt: "%s", mode: customScheduled, '
           'schedulingType: automatic, needsApproval: false, aiAssisted: true, assets: %s, metadata: %s}) '
           '{ __typename ... on PostActionSuccess { post { id dueAt status channelService } } '
           '... on MutationError { message } ... on InvalidInputError { message } } }') % (ch, esc(text), due, assets, meta)
        out=gql(q)
        ok='"PostActionSuccess"' in out
        print(f"  {tag:9} {'OK ' if ok else 'FAIL'} {out[:200]}")
