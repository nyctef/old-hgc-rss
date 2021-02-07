from flask import Flask, make_response
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from collections import namedtuple
import json

app = Flask(__name__)


class Videos:
    @staticmethod
    def from_json(parsed_json):
        return [Video.from_json(x) for x in parsed_json]


class Video(namedtuple("Video", "title link description publishDate")):
    @staticmethod
    def from_json(parsed_json):
        publishDate = datetime.strptime(
            parsed_json["publishedAt"],
            "%Y-%m-%dT%H:%M:%SZ",
        ).replace(tzinfo=timezone.utc)

        return Video(
            parsed_json["title"],
            parsed_json["href"],
            parsed_json["description"],
            publishDate,
        )

    def adjust_date(self, delta):
        return Video(self.title, self.link, self.description, self.publishDate + delta)

    def is_in_future(self, today=datetime.now(timezone.utc)):
        return self.publishDate > today


with open("video_list.json", encoding="utf-8") as f:
    video_list = Videos.from_json(json.load(f))


@app.route("/")
def hello_world():
    return "Hello, World! See /feed.rss for contents"


def filter_videos(all_videos):
    hgc_2017_start = datetime(2017, 1, 17)
    replay_start = datetime(2021, 2, 7)
    date_diff = replay_start - hgc_2017_start

    adjusted_videos = [x.adjust_date(date_diff) for x in all_videos]
    no_future_videos = [x for x in adjusted_videos if not x.is_in_future()]
    return no_future_videos


@app.route("/feed.rss")
def feed():
    fg = FeedGenerator()
    fg.title("Old HGC videos")
    fg.link(href="https://www.youtube.com/c/heroesesports/videos")
    fg.description("Replaying old HGC videos over time")

    for video in filter_videos(video_list):
        fe = fg.add_entry()
        fe.title(video.title)
        fe.link(href=video.link)
        fe.description(video.description)
        fe.pubDate(video.publishDate)

    response = make_response(fg.rss_str(pretty=True))

    response.headers.set("Content-Type", "application/rss+xml")
    return response


if __name__ == "__main__":
    # dev builds run in flask with hot reloading
    # heroku uses gunicorn as specified by the Procfile
    app.run(host="0.0.0.0", use_reloader=True)
