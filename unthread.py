import os

import requests
import tweepy

from minicli import cli, run
from yaml import safe_load

DEST_PATH = "blog/threads"

from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader("templates"),
)
template = env.get_template('thread.md')


class Thread():

    def __init__(self, initial):
        self.tweets = []
        text, min_indice = self.parse(initial)
        # separate content from the other stuff to allow text as fallback title
        self.tweets.append(f"{text[:min_indice]}\n{text[min_indice:]}")

    def add(self, status):
        text, _ = self.parse(status)
        self.tweets.append(text)

    def parse(self, status):
        full_text = status["full_text"]
        entities = status["entities"]
        ex_entities = status.get("extended_entities", {})
        # minimum indice for extras (images, urls...)
        min_indice = 1000

        # download and replace images url by markdown
        for m in [_m for _m in ex_entities.get("media", []) if _m["type"] == "photo"]:
            min_indice = m["indices"][0] if m["indices"][0] < min_indice else min_indice
            r = requests.get(m["media_url_https"])
            r.raise_for_status()
            image_path = f"images/{m['id']}.jpg"
            with open(f"{DEST_PATH}/{image_path}", "wb") as ofile:
                ofile.write(r.content)
            if m["url"] in full_text:
                full_text = full_text.replace(m["url"], f"![](./{image_path})")
            else:
                full_text += f" ![](./{image_path})"

        # replace urls with originals and markdown
        for url in entities["urls"]:
            min_indice = url["indices"][0] if url["indices"][0] < min_indice else min_indice
            true_url = url["expanded_url"]
            full_text = full_text.replace(url["url"], f"[{true_url}]({true_url})")

        return full_text, min_indice

def return_api():
    auth = tweepy.AppAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
    # we don't need anything not public _a priori_
    # auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
    return tweepy.API(auth)


@cli
def process(url, title=None):
    """Unthread an URL (top tweet URL)
    :url: Top tweet URL to unthread

    # TODO:
    # - use metadata parser for external urls (card/embed)
    # - handle tweet links (use urls[].expanded_url.startswith('twitter.com') and use embed)
    # - handle mentions and hashtags
    """
    print(f"Handling {url}...")
    tweet_id = url.split("?")[0].split("/")[-1]
    output_file = os.path.abspath(f"{DEST_PATH}/{tweet_id}.md")
    api = return_api()
    try:
        topLevelTweet = api.get_status(tweet_id, tweet_mode="extended")._json
    except:
        raise Exception(f"Error finding tweet: {tweet_id}")
    thread = Thread(topLevelTweet)
    uid = topLevelTweet["user"]["id"]

    def dig(tweet_id):
        for page in tweepy.Cursor(api.user_timeline, id=uid, since_id=tweet_id, tweet_mode="extended").pages():
            nextTweet = [item._json for item in page if item._json["in_reply_to_status_id_str"] == tweet_id]
            if nextTweet:
                thread.add(nextTweet[0])
                dig(nextTweet[0]["id_str"])

    dig(tweet_id)
    with open(output_file, "w+") as f:
        f.write(template.render(title=title, thread=thread))


@cli
def bulk():
    with open("threads.yml") as ifile:
        config = safe_load(ifile)
        author = config["author"]
        for thread in config["threads"]:
            url = f"https://twitter.com/{author}/status/{thread['id']}"
            process(url, title=thread.get("title"))


if __name__ == "__main__":
    run()
