import os, json, sys, requests

sys.argv = [sys.argv[0], "none"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_publish as V

gql = V.gql

d, raw = gql('{ __type(name: "DeletePostPayload") { kind fields { name type { name kind ofType { name kind } } } } }')
print("DeletePostPayload:", json.dumps(d, ensure_ascii=False)[:800] if d else raw[:800])

d2, raw2 = gql('{ __type(name: "Mutation") { fields { name args { name type { name kind ofType { name } } } } } }')
try:
    for f in d2["data"]["__type"]["fields"]:
        if "delete" in f["name"].lower():
            print("MUTATION:", json.dumps(f, ensure_ascii=False)[:400])
except Exception:
    print("mutation introspection failed", raw2[:300])

OLD = "6b06fff3a2969125d5314695"

CANDIDATES = [
    ("""mutation Del($input: DeletePostInput!) {
         deletePost(input: $input) { __typename }
       }""", {"input": {"id": OLD}}, "payload-typename"),
    ("""mutation Del($input: DeletePostInput!) {
         deletePost(input: $input) { post { id } }
       }""", {"input": {"id": OLD}}, "payload-post-id"),
]

deleted = False
for q, var, label in CANDIDATES:
    if deleted:
        break
    r, rawr = gql(q, var)
    print(f"\nTRY {label} ->", json.dumps(r, ensure_ascii=False)[:500] if r else rawr[:500])
    if r and "errors" not in r:
        deleted = True

print("deleted:", deleted)
if deleted:
    V.post("1 YOUTUBE (new)", V.build("6afe91afece6dfde5f19c312", V.DESC, "youtube", {
        "title": V.TITLE, "categoryId": "28", "privacy": "public",
        "madeForKids": False, "notifySubscribers": True,
        "license": "youtube", "embeddable": True, "isAiGenerated": True}))
else:
    print("!! still could not delete - YouTube post left as is")
