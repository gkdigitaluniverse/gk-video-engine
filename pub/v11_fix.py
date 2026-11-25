import os, json, sys, requests

sys.argv = [sys.argv[0], "none"]   # stop v11_publish module-level blocks from running
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_publish as V

gql = V.gql

d, _ = gql('{ __type(name: "DeletePostInput") { inputFields { name type { name kind } } } }')
print("DeletePostInput:", json.dumps(d, ensure_ascii=False)[:600])

fields = []
try:
    fields = [f["name"] for f in d["data"]["__type"]["inputFields"]]
except Exception:
    pass
print("fields:", fields)

DEL = """mutation Del($input: DeletePostInput!) {
  deletePost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id } }
    ... on MutationError { message }
  }
}"""

OLD = "6b06fff3a2969125d5314695"
deleted = False
for key in ("id", "postId"):
    if key in fields:
        r, raw = gql(DEL, {"input": {key: OLD}})
        print("\nDELETE with", key, "->", json.dumps(r, ensure_ascii=False)[:500] if r else raw[:500])
        try:
            if r["data"]["deletePost"]["__typename"] == "PostActionSuccess":
                deleted = True
                break
        except Exception:
            pass

print("deleted:", deleted)
if not deleted:
    print("!! could not delete the old YouTube post - not creating a second one")
else:
    V.post("1 YOUTUBE (new)", V.build("6afe91afece6dfde5f19c312", V.DESC, "youtube", {
        "title": V.TITLE, "categoryId": "28", "privacy": "public",
        "madeForKids": False, "notifySubscribers": True,
        "license": "youtube", "embeddable": True, "isAiGenerated": True}))

V.post("2 INSTAGRAM REEL (no first comment)", V.build("6afe9396ece6dfde5f19f9c4", V.IG, "instagram", {
    "type": "reel", "shouldShareToFeed": True, "isAiGenerated": True}))
