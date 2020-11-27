import tweepy
import formula_parser
import subprocess
import json
import logging

# Intuitionistic Bot

class IntuitionisticBot:

    def __init__(self):
        self.mathslogic_bot_id = "2871456406"
        self.consumer_key: str = ""
        self.consumer_secret: str = ""
        self.access_token: str = ""
        self.access_token_secret: str = "" 
        self.set_config()
        self.api = self.authorize()
        self.parser = formula_parser.FormulaParser() 

    def set_config(self) -> None:
        with open("config.json") as config_file:
            config = json.load(config_file)
            self.consumer_key = config["consumer_key"]
            self.consumer_secret = config["consumer_secret"]
            self.access_token = config["access_token"]
            self.access_token_secret = config["access_token_secret"]
            
    def authorize(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth) 

    def logicbot_timeline(self):
        return tweepy.Cursor(
            self.api.user_timeline,
            user_id = self.mathslogic_bot_id, 
            tweet_mode = 'extended',
            ).items()

    def listen(self) -> None:
        listener = MyStreamListener(self.mathslogic_bot_id, self)
        stream = tweepy.Stream(auth=self.api.auth, listener=listener)
        stream.filter(follow=[self.mathslogic_bot_id]) 

    def check_previous_tweet(self) -> None:
        tweet = self.logicbot_timeline().next()
        self.check_tweet(tweet.full_text)

    def check_tweet(self, tweet: str) -> None: 
        print(tweet)
        logging.info(f"New Formula: {tweet}")
        parsed_formula = str(self.parser.parse(tweet))
        print(parsed_formula)
        logging.info(f"Translation: {parsed_formula}")
        proved = subprocess.check_output(["./Main", parsed_formula])
        print(proved)
        logging.info(f"Result: {proved.decode('utf-8')}")


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, twitter_id: str, bot: IntuitionisticBot) -> None:
        super(MyStreamListener, self).__init__()
        self.id  = twitter_id
        self.bot = bot
    
    def on_status(self, tweet): 
        if tweet._json['user']['id'] == int(self.id):
            tweet_text = tweet.text
            self.bot.check_tweet(tweet_text)

if __name__ == '__main__': 
    logging.basicConfig(filename='intuitionistic_bot.log', 
                        filemode='a',
                        format='[%(asctime)s] %(message)s',
                        level=logging.INFO) 
    bot = IntuitionisticBot()
    bot.listen() 

