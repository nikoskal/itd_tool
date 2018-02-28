from __future__ import absolute_import

from itdtool.celeryapp import app
import re
from textblob import TextBlob
import pandas as pd
import math

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
def get_tweets_term(term, number_of_tweets):
    # get all tweets based on term
    auth = account_repo.get_twitter_auth()
    api = API(auth)
    # number_of_tweets = 100
    cricTweet = tweepy.Cursor(api.search, q=term, tweet_mode='extended', result_type='popular').items(number_of_tweets)
    return cricTweet


@app.task
def get_tw_gender(ans_list):
    gender_prob = predict_gender_average(ans_list)
    # results = {'tweet_gender_prob': gender_prob}
    return gender_prob



@app.task
def get_tw_sentiment(all_tweets):
    result = []

    total_sent_pol = 0
    counter = 0
    total_tweets_sentiment = []
    all_tweets_sent = []
    # all_tweets = []
    total_tweets_positive = 0
    total_tweets_negative = 0
    total_tweets_neutral = 0


    for tweet in all_tweets:
        tweet_sent = {}
        cleanedTweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", tweet["text"]).split())
        print "cleanedTweet:"
        print cleanedTweet

        analysis = TextBlob(cleanedTweet)
        tweet_sent["score"] = analysis.sentiment.polarity
        tweet_sent["text"] = tweet["text"]
        tweet_sent["retweets"] = tweet["retweets"]
        tweet_sent["user"] = tweet["user"]
        tweet_sent["created"] = tweet["created"]
        # classify polarity
        polarity = {}
        if analysis.sentiment.polarity > 0.1:
            polarity = 'Positive'
            # print "Positive RT"+ str(tweet.retweet_count)
            total_tweets_positive += 1
            total_tweets_positive += tweet["retweets"]
        if analysis.sentiment.polarity < -0.1:
            polarity = 'Negative'
            total_tweets_negative += 1
            total_tweets_negative += tweet["retweets"]
        if -0.1 <= analysis.sentiment.polarity <= 0.1:
            polarity = 'Neutral'
            total_tweets_neutral += 1
            total_tweets_neutral += tweet["retweets"]

        tweet_sent["sentiment"] = polarity
        all_tweets_sent.append(tweet_sent)

    df_total_tweets_sentiment = pd.DataFrame(all_tweets_sent)
    # print df_total_tweets_sentiment
    # print len(df_total_tweets_sentiment)
    average_score_pos, average_score_neg = 0.0, 0.0

    df_total_tweets_sentiment_pos = df_total_tweets_sentiment[df_total_tweets_sentiment.sentiment == 'Positive']
    total_score_pos = df_total_tweets_sentiment_pos['score'].sum()
    average_score_pos = total_score_pos/len(df_total_tweets_sentiment_pos)
    if math.isnan(average_score_pos):
        average_score_pos = 0.0

    df_total_tweets_sentiment_neg = df_total_tweets_sentiment[df_total_tweets_sentiment.sentiment == 'Negative']
    total_score_neg = df_total_tweets_sentiment_neg['score'].sum()
    average_score_neg = total_score_neg/len(df_total_tweets_sentiment_neg)
    if math.isnan(average_score_neg):
        average_score_neg = 0.0



    # print "+++++ all_tweets_sentiment sorted RT,score"
    df_sorted_positive = df_total_tweets_sentiment[df_total_tweets_sentiment.sentiment == 'Positive'].sort_values(
        by=['retweets', 'score'], ascending=['True', 'True'])

    # print df_sorted_positive
    # print "+++++ top possitive"
    # print df_sorted_positive.tail(5)

    df_sorted_negative = df_total_tweets_sentiment[df_total_tweets_sentiment.sentiment == 'Negative'].sort_values(
        by=['retweets', 'score'], ascending=['True', 'True'])
    # print "+++++ top negative"
    # print df_sorted_negative.tail(5)
    # print total_tweets_positive, total_tweets_negative, total_tweets_neutral

    top_positive = df_sorted_positive.tail(5).set_index('text').T.to_dict('list')
    top_negative = df_sorted_negative.tail(5).set_index('text').T.to_dict('list')

    # top_positive_5 = top_positive.tail(5)
    # top_negative_5 = top_negative.tail(5)

    print "top_positive_5"
    print top_positive

    print "top_negative_5"
    print top_negative

    print "Done"


    results_to_returns = {'total_tweets_positive': total_tweets_positive,
                          'total_tweets_negative': total_tweets_negative,
                          'total_tweets_neutral': total_tweets_neutral,
                          'top_positive': top_positive,
                          'top_negative': top_negative,
                          'average_score_pos':  format(average_score_pos, '.2f'),
                          'average_score_neg': format(average_score_neg, '.2f')}
    print results_to_returns

    return results_to_returns



@app.task
def get_tw_sentiment_term_fake(term):
    result = []

    print "inside FAKE twitter sentiment task term:" + term

    # for tweet in cricTweet:
    tweet_one = {}
    tweet_one["user"] = "nikos1"
    tweet_one["text"] = "obama is a fascinating person"
    tweet_one["favs"] = 10
    tweet_one["retweets"] = 5

    tweet_two = {}
    tweet_two["user"] = "nikos2"
    tweet_two["text"] = "obama is a bad guy"
    tweet_two["favs"] = 12
    tweet_two["retweets"] = 6

    tweet_three = {}
    tweet_three["user"] = "nikos3"
    tweet_three["text"] = "I don't care about obama"
    tweet_three["favs"] = 12
    tweet_three["retweets"] = 6

    tweet_four = {}
    tweet_four["user"] = "nikos4"
    tweet_four["text"] = "Who is obama?"
    tweet_four["favs"] = 12
    tweet_four["retweets"] = 6

    tweet_five = {}
    tweet_five["user"] = "nikos5"
    tweet_five["text"] = "I love obama"
    tweet_five["favs"] = 12
    tweet_five["retweets"] = 6

    tweet_six = {}
    tweet_six["user"] = "nikos6"
    tweet_six["text"] = "I love #obama"
    tweet_six["favs"] = 12
    tweet_six["retweets"] = 6

    # 'good', 'nice', 'great', 'awesome', 'outstanding',
    # 'fantastic', 'terrific', ':)', ':-)', 'like', 'love',

    result.append(tweet_one)
    result.append(tweet_two)

    result.append(tweet_three)
    result.append(tweet_four)
    result.append(tweet_five)
    result.append(tweet_six)

    return result



def hq_image(image_url):
    return string.replace(image_url, 'normal', '400x400')


