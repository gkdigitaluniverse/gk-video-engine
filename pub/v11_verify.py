import os, json, sys, requests

sys.argv = [sys.argv[0], "none"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_publish as V

gql = V.gql
IDS = ["6b0700b958090bfccaf4463f", "6b07008c8b7db026c8b5bc3d", "6b07004d3b698826fdcf04b4",
       "6b07004efe6e607e49d4c2ae", "6b07004ffe6e607e49d4c34d"]

d, raw = gql('{ __type(name: "Query") { fields { name } } }')
names = []
try:
    names = [f["name"] for f in d["data"]["__type"]["fields"]]
except Exception:
    print("introspect fail", raw[:300])
print("Query fields with 'post':", [n for n in names if "ost" in n.lower()])

for cand in ("posts", "postsByChannel", "allPosts"):
    if cand not in names:
        continue
    q = '{ %s(first: 20) { edges { node { id dueAt status } } } }' % cand
    r, rawr = gql(q)
    print(f"\n{cand} ->", json.dumps(r, ensure_ascii=False)[:1500] if r else rawr[:600])
    break

# node(id:) style fallback
if "node" in names:
    for pid in IDS[:5]:
        q = 'query($id: ID!){ node(id: $id){ __typename } }'
        r, rawr = gql(q, {"id": pid})
        print(pid, "->", json.dumps(r, ensure_ascii=False)[:200] if r else rawr[:200])
