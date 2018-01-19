from tweepy import OAuthHandler
from tweepy import API
import tweepy

def get_tw_trends_term(term):
    result = []
    # print "starting"


    # TWITTER_KEY "Qe0uB9vqRPJC4t3XUGnNt7uW0"
    # TWITTER_SECRET "O018Ae3LCbw2jNe4Dqy4LgxZKnIdoxWJ9DtmgJ2RBzYBgUbvwi"
    # TWITTER_ACCESS_TOKEN "2340983450 - LunqxRWQeA7gtDQNtdk4BY7WpMLztOQiXiZQXo3"
    # TWITTER_ACCESS_TOKEN_SECRET "3UefP7CaWOy6PXOJIG3VjBdbOCdgR1zm96zldUVNFcdP4"



    twitter_key = 'Qe0uB9vqRPJC4t3XUGnNt7uW0'
    twitter_secret = 'O018Ae3LCbw2jNe4Dqy4LgxZKnIdoxWJ9DtmgJ2RBzYBgUbvwi'
    twitter_access_token = '2340983450 - LunqxRWQeA7gtDQNtdk4BY7WpMLztOQiXiZQXo3'
    twitter_access_token_secret = '3UefP7CaWOy6PXOJIG3VjBdbOCdgR1zm96zldUVNFcdP4'

    try:
        auth = OAuthHandler(twitter_key, twitter_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    except AttributeError:
        print "No twitter keys are set, please set TWITTER_KEY parameters attribute in settings!!"
        return False

    print "auth"
    print auth


    api = API(auth)
    trends1 = api.trends_place(1)

    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    # put all the names together with a ' ' separating them
    trendsName = '\n '.join(names)
    print(trendsName)


    print trends1


    # Also note that the search results at twitter.com may return historical results
    # while the Search API usually only serves tweets from the past week.- Twitter documentation.

    cricTweet = tweepy.Cursor(api.search, q="#" + term).items(350)

    print "cricTweet"
    print str(tweepy.Cursor(api.search, q="#" + term))

    print "loop"

    for tweet in cricTweet:
        # print tweet.created_at, tweet.text, tweet.lang

        # print tweet.user.name
        name = tweet.user.name
        print name
        if "RT @" not in tweet.text:
            if (tweet.retweet_count > 5) or (tweet.favorite_count > 5):
                tweet = {
                    "user": name,
                    "text": tweet.text,
                    "favs": tweet.favorite_count,
                    "retweets": tweet.retweet_count,
                    "created": tweet.created_at}
                result.append(tweet)

    # print "finished"
    # print result
    # print len(result)
    return result


    # n_docs is the total n. of tweets
    p_t = {}
    p_t_com = defaultdict(lambda: defaultdict(int))

    for term, n in count_stop_single.items():
        p_t[term] = n / n_docs
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs


get_tw_trends_term("snowden")