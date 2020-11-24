import tweepy
import formula_parser
import subprocess

consumer_key = "voB62BfaL1HmxeX3WB4B1trbS"
consumer_secret = "LncVSXgm8TKDXio9mhBhXtvjhr9iZkjwiPV6fq7E2JUviuHj3k"

access_token = "879000066945667072-Tt1SPFpiaWkGtPwXbWu0uwru9mLOabq"
access_token_secret = "ex0PFRbbcKFDaLHhOcYG908cHPhyuGfhS44DagRz4UPfd"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

mathslogicbot_id = '2871456406'

def get_timeline(user_id):
  return tweepy.Cursor(
    api.user_timeline,
    user_id = user_id,
    tweet_mode='extended',
  ).items()

parser = formula_parser.FormulaParser()


for tweet in get_timeline(mathslogicbot_id):
# tweet_text = get_timeline(mathslogicbot_id).next().full_text
    tweet_text = tweet.full_text
    print("Parse:")
    print(tweet_text)
    parsed_formula = str(parser.parse(tweet_text))
    print(parsed_formula)
    proved = subprocess.check_output(["./Main", parsed_formula])
    print(proved.decode('utf-8'))
