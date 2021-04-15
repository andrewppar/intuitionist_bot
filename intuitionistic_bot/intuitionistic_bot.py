import tweepy
import os 
from formula_parser import FormulaParser
import subprocess
import json
import logging


class IntuitionisticBot:
    """The class that tweets replies to mathslogicbot
    indicating whether the classical tautology that was
    tweeted is also an intuitionistic tautology.

    Attributes:
        mathslogic_bot_id: The twitter id of mathslogicbot
        consumer_key: The consumer key for the users twitter
            account which is read from config.json
        consumer_secret: The consumer secret for the users twitter
            account which is read from config.json
        access_token: The access toekn for the users twitter
            account which is read from config.json
        access_token_secret: The access token secret for the users twitter
            account which is read from config.json
        api: The tweepy.API that is generated from the above
            four attributes
        parser: An instance of FormulaParser for
            parsing formulas that are tweeted by
            mathslogicbot.
        """

    def __init__(self):
        self.mathslogic_bot_id = "2871456406" 
        self.repo_path = "/home/andrew/Documents/python/intuitionist_bot/"
        self.consumer_key: str = ""
        self.consumer_secret: str = ""
        self.access_token: str = ""
        self.access_token_secret: str = ""
        self.set_config()
        self.api = self.authorize()
        self.parser = FormulaParser()

    def set_config(self) -> None:
        """This function sets the consumer key,
        consumer secret, access token, and access token
        secret from a file called config.json that is
        located in the same directory as this file.

        Args:

        Returns:
        """ 
        config_path = os.path.join(self.repo_path, "intuitionistic_bot/config.json") 
        with open(config_path) as config_file:
            config = json.load(config_file)
            self.consumer_key = config["consumer_key"]
            self.consumer_secret = config["consumer_secret"]
            self.access_token = config["access_token"]
            self.access_token_secret = config["access_token_secret"]

    def authorize(self) -> tweepy.API:
        """This generates a tweepy.API from the
        four authorization token attributes.

        Args:

        Returns:
            An instance of tweepy.API that is used to interact
            with twitter.
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth)

    def logicbot_timeline(self) -> tweepy.Cursor:
        """This returns a tweepy.Cursor that contains
        the tweets from mathslogicbot

        Args:

        Returns:
            An instance of tweepy.Cursor
        """
        return tweepy.Cursor(
            self.api.user_timeline,
            user_id=self.mathslogic_bot_id,
            tweet_mode='extended',
            ).items()

    def listen(self) -> None:
        """Listens for tweets from mathslogicbot
        when it gets one, it tries to prove the
        tweeted formula.

        Args:

        Returns:
        """
        listener = MyStreamListener(self.mathslogic_bot_id, self)
        stream = tweepy.Stream(auth=self.api.auth, listener=listener)
        stream.filter(follow=[self.mathslogic_bot_id])

    def check_previous_tweet(self) -> None:
        """Gets the last formula that was tweeted by mathslogicbot
        and checks whether that formula is an intuitionistic
        tautology.

        Args:

        Returns:
        """
        tweet_log = os.path.join(self.repo_path, "tweet_log")

        if not os.path.exists(tweet_log):
            previous_tweet = "" 
        else:
            with open(tweet_log, 'r+') as previous_tweet_log:
                previous_tweet = previous_tweet_log.read()

        tweet = self.logicbot_timeline().next()
        if tweet.full_text == previous_tweet: 
            logging.info(f"{tweet.full_text} is the same as previous {previous_tweet}")
            print(f"{tweet.full_text} is the same as previous {previous_tweet}")
        else:
            self.check_tweet(tweet.full_text, tweet.id)
            with open(tweet_log, 'w+') as previous_tweet_log:
                previous_tweet_log.write(tweet.full_text)

    def check_tweet(self, tweet: str, tweet_id: str) -> None:
        """Checks whether a string represents an instance
        of an intuitionistic tautology. As a side effect it
        both prints and logs the formula, the parsed formula
        and whether or not it is a tautology.

        Args: 
            tweet: The text of the tweet that is being checked
            tweet_id: the id of the tweet that is being checked

        Returns:
        """
        logging.info(f"New Formula: {tweet}")
        parsed_formula = str(self.parser.parse(tweet))
        logging.info(f"Translation: {parsed_formula}")
        proved_byte = subprocess.check_output(["/home/andrew/.local/bin/IntuitionisticTheoremProver-exe", parsed_formula])
        proved = proved_byte.decode('utf-8') 
        self.reply_to_tweet(tweet_id, f"{tweet} {proved}")
        logging.info(f"{tweet} {proved}")

    def reply_to_tweet(self, tweet_id, reply):
        """
        Reply to a tweet.
        Return the reply's tweet object.
        """
        return self.api.update_status(
                                 status = reply,
                                 in_reply_to_status_id = tweet_id,
                                 auto_populate_reply_metadata = True
                                )



class MyStreamListener(tweepy.StreamListener):
    """A subclass of tweepy.StreamListener so that
    the IntuitionisticBot can listen for tweets.
    """

    def __init__(self, twitter_id: str, bot: IntuitionisticBot) -> None:
        super(MyStreamListener, self).__init__()
        self.id = twitter_id
        self.bot = bot

    def on_status(self, tweet):
        if tweet._json['user']['id'] == int(self.id):
            tweet_text = tweet.text 
            tweet_id = tweet.id
            self.bot.check_tweet(tweet_text, tweet_id)


if __name__ == '__main__':
    logging.basicConfig(filename='/home/andrew/Documents/python/intuitionist_bot/intuitionistic_bot.log', # noqa
                        filemode='a',
                        format='[%(asctime)s] %(message)s',
                        level=logging.INFO)
    bot = IntuitionisticBot()
    bot.check_previous_tweet()
