from flask import Flask, make_response
from feedgen.feed import FeedGenerator
import json

app = Flask(__name__)

with open("video_list.json") as f:
    video_list = json.load(f)


@app.route("/")
def hello_world():
    return "Hello, World! See /feed.rss for contents"


@app.route("/feed.rss")
def feed():
    fg = FeedGenerator()
    fg.title("Old HGC videos")
    fg.link("https://www.youtube.com/c/heroesesports/videos")
    fg.description("Replaying old HGC videos over time")

    for video in video_list:
        fe = fg.add_entry()
        fe.title(video["title"])
        fe.link(video["href"])
        fe.description(video["description"])
        fe.pubDate(video("publishedAt"))

    response = make_response(fg.rss_str())

    response.headers.set("Content-Type", "application/rss+xml")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
