import os, json, requests
K=os.environ["CK"]; URL="https://connect.composio.dev/mcp"
ORG="6afe914c34b70aac8c250902"
CH={"YT":"6afe91afece6dfde5f19c312"}
BASE="https://github.com/gkdigitaluniverse/gk-video-engine/releases/download/run1"
ORPHANS=["6b0846691e13bd67eef3087f","6b08466ba9607f7555829b06","6b08466eee9d307b372d90de","6b084670b2044ab9dfaf261b"]
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
def esc(t): return t.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")

init()

# --- mutation fields for delete ---
d=d3(gql('query { __type(name: "Mutation") { fields { name } } }'))
print("MUTATIONS:", [f["name"] for f in d["__type"]["fields"]] if d else "err")

# --- YouTube posts, privacy/license as ENUM literals ---
CF_T="Run An API In Your Browser — No Server, No Signup #Shorts"
SH_T="One Cell, Many Choices: Google Sheets Hidden Setting #Shorts"
CF_D="Run a live API right inside your browser tab — no server, no signup, no CLI.\nCloudflare Workers Playground runs the code on the edge. Here is what it actually gives you.\n\n• Write the fetch handler, hit Send, get a real response\n• 100,000 requests per day on the free plan\n• 10 ms CPU time per request — that is the real limit\n• What it cannot do: no long jobs, no heavy packages\n\nSource: Cloudflare Workers docs — checked 26 Nov 2026\nTry it: https://workers.cloudflare.com/playground\n\ncloudflare workers, workers playground, serverless api, free api hosting,\nedge computing, cloudflare free plan, run api in browser, no server needed,\njavascript api tutorial, cloudflare tutorial\n\n#Shorts #Cloudflare #Serverless #WebDev"
SH_D="Pick multiple values in one Google Sheets cell — no formula, no script.\nIt only works with chip-style dropdowns. Here is the exact setup.\n\n• Turn on Allow multiple selections in Data Validation\n• Switch Display style to Chip — other styles are disabled\n• Keep Pending, Testing and Done in the same cell\n• What breaks: the mobile app cannot select multiple yet\n\nSource: Google Workspace Updates, 26 July 2024 — checked 26 Nov 2026\nTry it: https://sheets.google.com\n\ngoogle sheets, multi select dropdown, dropdown chips, google sheets tricks,\nspreadsheet tips, data validation, google sheets tutorial, excel alternative,\nmultiple values in one cell, google workspace tips\n\n#Shorts #GoogleSheets #SpreadsheetTips #GoogleWorkspace"

for title, desc, date, slug in [(CF_T,CF_D,"2026-11-29","cloudflare"),(SH_T,SH_D,"2026-11-30","sheets")]:
    due=f"{date}T10:00:00+05:30"
    meta='{youtube: {title: "%s", categoryId: "28", privacy: public, madeForKids: false, notifySubscribers: true, license: youtube, embeddable: true, isAiGenerated: true}}' % esc(title)
    q=('mutation { createPost(input: {channelId: "%s", text: "%s", dueAt: "%s", mode: customScheduled, '
       'schedulingType: automatic, needsApproval: false, aiAssisted: true, assets: [{video: {url: "%s/%s.mp4"}}], metadata: %s}) '
       '{ __typename ... on PostActionSuccess { post { id dueAt status channelService } } '
       '... on MutationError { message } ... on InvalidInputError { message } } }') % (CH["YT"], esc(desc), due, BASE, "cf" if slug=="cloudflare" else "sh", meta)
    out=gql(q)
    print(f"YT {slug} {date}: {'OK' if 'PostActionSuccess' in out else 'FAIL'} {out[:230]}")

# --- delete orphan stories ---
for pid in ORPHANS:
    out=gql('mutation { deletePost(input: {id: "%s"}) { __typename ... on DeletePostSuccess { post { id } } ... on MutationError { message } } }' % pid)
    print(f"DEL {pid}: {out[:180]}")
