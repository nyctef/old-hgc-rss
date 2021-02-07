import requests
import json

hgc_uploads_playlist = "UUASdq716V77-Ixup3HZOZWQ"
# get api key from https://console.developers.google.com/apis/credentials?project=applied-mystery-117722&organizationId=0

with open("api_key.txt") as f:
    api_key = f.read()


results = []
next_page_token = ""
page = 0
while True:
    page += 1
    print(f"processing page {page}")
    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    response = requests.get(
        url,
        params={
            "playlistId": hgc_uploads_playlist,
            "part": "snippet",
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": api_key,
        },
    ).json()
    for item in response["items"]:
        snippet = item["snippet"]
        results.append(
            {
                "title": snippet["title"],
                "href": f"""https://www.youtube.com/watch?v={snippet['resourceId']['videoId']}""",
                "description": snippet["description"],
                "publishedAt": snippet["publishedAt"],
            }
        )
    try:
        next_page_token = response["nextPageToken"]
    except KeyError:
        # run out of pages to query, so let's stop
        break


with open("video_list.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)