# How to post to all three platforms (verified 2026-11-24)

## Buffer channel IDs
| platform | channel id | note |
|---|---|---|
| YouTube | `6afe91afece6dfde5f19c312` | publish |
| Instagram | `6afe9396ece6dfde5f19f9c4` | publish + engage |
| Facebook | `6afe93c6ece6dfde5f19ffb9` | publish |
| organization | `6afe914c34b70aac8c250902` | |

## YouTube video post — WORKS via Buffer GraphQL
Composio tool `BUFFER_PUBLISH_POSTS` is text-only and YouTube rejects it
("YouTube posts require a video, a title, a category").
So call Buffer's GraphQL directly through `COMPOSIO_PROXY_EXECUTE`.

```
tool: COMPOSIO_PROXY_EXECUTE
toolkit_slug: buffer
endpoint: ""            # empty = Buffer GraphQL API
method: POST
body: { query, variables }
```

Mutation:
```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id text } }
    ... on MutationError { message }
  }
}
```

Variables:
```json
{"input": {
  "channelId": "6afe91afece6dfde5f19c312",
  "text": "caption / description",
  "assets": [{"video": {"url": "https://.../file.mp4"}}],
  "metadata": {"youtube": {
     "title": "...", "categoryId": "28", "privacy": "private",
     "madeForKids": false, "notifySubscribers": false }},
  "mode": "addToQueue",
  "schedulingType": "automatic",
  "needsApproval": false
}}
```

- `mode`: `addToQueue` | `customScheduled` (+ `dueAt`) | `shareNext` | `shareNow`
- `privacy`: `private` | `public` | `unlisted`
- `categoryId`: 28 = Science & Technology, 27 = Education, 22 = People & Blogs
- Verified result: `PostActionSuccess`, post id `6b05423ff1f04351232d803d`

## THE ONE RULE THAT MATTERS: the video URL
Buffer fetches the file itself. The URL must be plainly public.

- Dropbox temporary link → **FAILED**: "Video could not be read from its URL."
- GitHub release asset URL → **WORKED**:
  `https://github.com/<owner>/<repo>/releases/download/<tag>/<file>.mp4`

So the pipeline must publish the finished mp4 as a GitHub release asset first,
then hand that URL to Buffer.

## Direct platform posting (no Buffer)
- Instagram reel: `INSTAGRAM_POST_IG_USER_MEDIA` (media_type REELS, video_url)
  → `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` (creation_id). VERIFIED, 50 posts/day.
- Facebook video: `FACEBOOK_CREATE_VIDEO_POST` with `file_url`. VERIFIED.
- Facebook text: `FACEBOOK_CREATE_POST` with `page_id` + `message`. VERIFIED.

## Known broken
- YouTube direct via Composio: 403 on channel read, shared Google quota exhausted,
  no working file staging. Do not use.
- `BUFFER_LIST_POSTS` returns empty. Do not rely on it for verification.
- `INSTAGRAM_GET_IG_MEDIA` requests fields Instagram rejects. Posting works, reading
  that one detail does not.
