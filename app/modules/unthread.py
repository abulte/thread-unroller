import tweepy, sys, os



class Thread():
    def __init__(self, initial):
        self.text = "{}\n".format(initial)

    def add(self, text):
        self.text += "{}\n".format(text)


def return_api():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_KEY'), os.getenv('TWITTER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    return tweepy.API(auth)


def unthread(url):
    tweetId = url.split("?")[0].split('/')[-1]
    outputFile = os.path.abspath("files/{}.txt".format(tweetId))
    api = return_api()
    try:
        topLevelTweet = api.get_status(tweetId)._json
    except:
        print("Error finding tweet: {}".format(tweetId))
        sys.exit()
    thread = Thread(topLevelTweet['text'])
    uid = topLevelTweet['user']['id']

    def dig(tweetId):
        for page in tweepy.Cursor(api.user_timeline, id=uid, since_id = tweetId).pages():
            nextTweet = [item._json for item in page if item._json['in_reply_to_status_id_str'] == tweetId]
            if nextTweet: 
                thread.add(nextTweet[0]['text'])
                dig(nextTweet[0]['id_str'])
    
    dig(tweetId)
    with open(outputFile, "w+") as f:
        f.write(thread.text)
    print("{}\n{}".format(outputFile, thread.text))
    return outputFile