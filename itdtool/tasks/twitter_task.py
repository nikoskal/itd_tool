from __future__ import absolute_import

from itdtool.celeryapp import app


# from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
# from tweepy import Stream
from tweepy import API
from itdtool import account_repo
import tweepy
from itdtool.tasks.gt_predictor import predict_gender_average
import string


@app.task
def get_tw_trends(place_id):

    auth = account_repo.get_twitter_auth()
    api = API(auth)
    trends1 = api.trends_place(place_id)

    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    # put all the names together with a ' ' separating them
    trendsName = '\n '.join(names)
    print(trendsName)

    return trendsName


@app.task
def get_tw_term(term, inference):

        # TODO: when searching for "woody allen" check also #Woody and #Allen

        result = []
        # print "starting"
        auth = account_repo.get_twitter_auth()
        api = API(auth)

        # Also note that the search results at twitter.com may return historical results
        # while the Search API usually only serves tweets from the past week.- Twitter documentation.
        total_items = 20

        cricTweet = tweepy.Cursor(api.search, q=term).items(total_items)

        # cricTweet2 = tweepy.Cursor(api.search, q="#" + term).items(total_items)


        print "retrieving  tweets --------- "
        popular_tweets = []
        tweeter_users_ids = []
        text_tweets = []
        # ans_list = [{id}:{name, image_url, theme_color}...]
        ans_list = {}
        for tweet in cricTweet:
                # print tweet.created_at, tweet.text, tweet.lang

                # print tweet.user.name
            # food["spam"] = "yes"
            image_url = hq_image(tweet.user.profile_image_url_https)
            theme_color = tweet.user.profile_link_color
            ans_list[tweet.user.id_str] = (tweet.user.name,image_url,theme_color, )

            # tweet_sent_text = {
            #         "user": tweet.user.name,
            #         "text": tweet.text}
            # text_tweets.append(tweet)

            if tweet.id_str not in tweeter_users_ids:
                tweeter_users_ids.append(tweet.user.id_str)

            if "RT @" not in tweet.text:
                if (tweet.retweet_count > 1) or (tweet.favorite_count > 1):
                    tweet = {
                            "id": tweet.user.id_str,
                            "user": tweet.user.name,
                            "text": tweet.text,
                            "favs": tweet.favorite_count,
                            "retweets": tweet.retweet_count,
                            "created": tweet.created_at}
                    popular_tweets.append(tweet)

        # print "sentiment analysis on tweets"
        # print len(text_tweets)
        # need to apply filters for bots that just search for trending topics and send spam tweets.
        # e.g. filter tweets and keep only one tweet per user

        # for text in text_tweets:
        #     print "#######start"
        #     print text
        #     print "-------end"


        print "unique ids:"
        print tweeter_users_ids

        if inference:
            print "predict_gender START "
            # predict_gender(tweeter_users_ids)
            print ans_list
            print len(ans_list)
            gender_prob = predict_gender_average(ans_list)

            print "predict_gender END "
        else:
            gender_prob = {}

        results = { 'popular_tweets': popular_tweets, 'tweet_gender_prob': gender_prob}

        return results


@app.task
def get_tw_sentiment_term(term):
    result = []
    # print "starting"
    auth = account_repo.get_twitter_auth()
    api = API(auth)

    # Also note that the search results at twitter.com may return historical results
    # while the Search API usually only serves tweets from the past week.- Twitter documentation.

    cricTweet = tweepy.Cursor(api.search, q="#" + term).items(100)

    # print "loop"

    for tweet in cricTweet:
        # print tweet.created_at, tweet.text, tweet.lang

        # print tweet.user.name
        # name = tweet.user.name
        # print name
        # print tweet.text
        # print "start"
        if "RT @" not in tweet.text:

            tweet = {
                "user": tweet.user.name,
                "text": tweet.text,
                "favs": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                "created": tweet.created_at}
            print "#######start"
            print tweet
            print "-------end"
            result.append(tweet)

    # print "finished"
    # print result
    # print len(result)
    return result



def hq_image(image_url):
    return string.replace(image_url, 'normal', '400x400')


