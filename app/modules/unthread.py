import os

import tweepy


class Thread():
    def __init__(self, initial):
        self.text = f"{initial}\n"

    def add(self, text):
        self.text += f"{text}\n"


def return_api():
    auth = tweepy.AppAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
    # auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
    return tweepy.API(auth)


def unthread(url):
    tweet_id = url.split("?")[0].split("/")[-1]
    output_file = os.path.abspath("files/{}.md".format(tweet_id))
    api = return_api()
    try:
        topLevelTweet = api.get_status(tweet_id, tweet_mode="extended")._json
    except:
        raise Exception("Error finding tweet: {}".format(tweet_id))
    thread = Thread(topLevelTweet["full_text"])
    uid = topLevelTweet["user"]["id"]

    def dig(tweet_id):
        for page in tweepy.Cursor(api.user_timeline, id=uid, since_id = tweet_id, tweet_mode="extended").pages():
            nextTweet = [item._json for item in page if item._json["in_reply_to_status_id_str"] == tweet_id]
            if nextTweet:
                print("next", nextTweet)
                thread.add(nextTweet[0]["full_text"])
                dig(nextTweet[0]["id_str"])

    dig(tweet_id)
    with open(output_file, "w+") as f:
        f.write(thread.text)
    print("{output_file}\n{hread.text}")
    return output_file
