import os

import requests
import tweepy


class Thread():
    def __init__(self, initial):
        # markdown-it-attrs for class attributes
        # https://stackoverflow.com/a/39214987
        self.text = f"{self.parse(initial)} {{.first}}\n\n---\n\n"

    @classmethod
    def parse(cls, status):
        full_text = status["full_text"]
        entities = status["entities"]
        ex_entities = status.get("extended_entities", {})

        # download and replace images url by markdown
        for m in [_m for _m in ex_entities.get("media", []) if _m["type"] == "photo"]:
            r = requests.get(m["media_url_https"])
            r.raise_for_status()
            image_path = f"images/{m['id']}.jpg"
            with open(f"files/{image_path}", "wb") as ofile:
                ofile.write(r.content)
            if m["url"] in full_text:
                full_text = full_text.replace(m["url"], f"![]({image_path})")
            else:
                full_text += f" ![]({image_path})"

        # replace urls with originals and markdown
        for url in entities["urls"]:
            true_url = url["expanded_url"]
            full_text = full_text.replace(url["url"], f"[{true_url}]({true_url})")

        return full_text

    def add(self, status):
        # FIXME: handle last tweet
        self.text += f"{self.parse(status)}\n\n---\n\n"


def return_api():
    auth = tweepy.AppAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
    # we don't need anything not public _a priori_
    # auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
    return tweepy.API(auth)


def unthread(url):
    tweet_id = url.split("?")[0].split("/")[-1]
    output_file = os.path.abspath("files/{}.md".format(tweet_id))
    api = return_api()
    try:
        # TODO:
        # - mutualize with dig
        # - remove image pics urls (use media[0].indices[0])
        # - download images (use media[type=photo][media_url_https])
        # - handle external urls (use urls[].expanded_url.!startswith('twitter.com') && urls[].url for replace)
        #   -use metadata parser in v2
        # - handle tweet links (use urls[].expanded_url.startswith('twitter.com') and use embed)
        # - handle mentions and hashtags
        topLevelTweet = api.get_status(tweet_id, tweet_mode="extended")._json
        print("topLevelTweet", topLevelTweet)
    except:
        raise Exception("Error finding tweet: {}".format(tweet_id))
    thread = Thread(topLevelTweet)
    uid = topLevelTweet["user"]["id"]

    def dig(tweet_id):
        for page in tweepy.Cursor(api.user_timeline, id=uid, since_id=tweet_id, tweet_mode="extended").pages():
            nextTweet = [item._json for item in page if item._json["in_reply_to_status_id_str"] == tweet_id]
            if nextTweet:
                print("next", nextTweet)
                thread.add(nextTweet[0])
                dig(nextTweet[0]["id_str"])

    dig(tweet_id)
    with open(output_file, "w+") as f:
        f.write(thread.text)
    print(f"{output_file}\n{thread.text}")
    return output_file
