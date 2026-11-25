import os, json, sys, requests

sys.argv = [sys.argv[0], "none"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_publish as V

gql = V.gql
IDS = ["6b0700b958090bfccaf4463f", "6b07008c8b7db026c8b5bc3d", "6b07004d3b698826fdcf04b4",
       "6b07004efe6e607e49d4c2ae", "6b07004ffe6e607e49d4c34d"]

d, raw = gql('{ a: __type(name:"PostsInput"){ inputFields{ name type{ name kind ofType{name} } } }'
             '  b: __type(name:"Post"){ fields{ name } } }')
print("PostsInput:", json.dumps(d, ensure_ascii=False)[:700] if d else raw[:400])

post_fields = []
try:
    post_fields = [f["name"] for f in d["data"]["b"]["fields"]]
except Exception:
    pass
print("Post fields:", post_fields)

sel = [f for f in ("id", "dueAt", "status", "channelId", "sentAt", "scheduledAt") if f in post_fields]
print("using:", sel)

if "posts" in ("posts",) and sel:
    q = 'query($input: PostsInput!){ posts(input: $input){ edges { node { %s } } } }' % " ".join(sel)
    for body in ({"organizationId": "6afe914c34b70aac8c250902", "first": 20},
                 {"first": 20}):
        r, rawr = gql(q, {"input": body})
        print("\nposts", list(body), "->", json.dumps(r, ensure_ascii=False)[:1800] if r else rawr[:600])
        if r and "errors" not in r:
            break

if "post" in post_fields or True:
    q2 = 'query($input: PostInput!){ post(input: $input){ %s } }' % " ".join(sel) if sel else None
    if q2:
        for pid in IDS:
            r, rawr = gql(q2, {"input": {"id": pid}})
            print(pid, "->", json.dumps(r, ensure_ascii=False)[:300] if r else rawr[:300])
