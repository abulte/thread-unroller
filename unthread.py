import tweepy, sys, os, dotenv
dotenv.load_dotenv()


class Thread():
    def __init__(self, initial):
        self.text = "{}\n".format(initial)

    def add(self, text):
        self.text += "{}\n".format(text)


def return_api():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_KEY'), os.getenv('TWITTER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    return tweepy.API(auth)


def run():
    if len(sys.argv) == 3:
        tweetId,outputFile = sys.argv[1].split("?")[0].split('/')[-1], sys.argv[2]
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
    
    else:
        print("ErrorParsingArguments:\tpython unthread.py <tweet-link> <output-txt-file>")


if __name__ == "__main__":
    run()