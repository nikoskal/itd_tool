from __future__ import absolute_import

from itdtool.celeryapp import app


# from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
# from tweepy import Stream
from tweepy import API
from itdtool import account_repo


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


#
#
# class StdOutListener(StreamListener):
#     """ A listener handles tweets that are received from the stream.
#     This is a basic listener that just prints received tweets to stdout.
#
#     """
#     def on_data(self, data):
#         print(data)
#         return True
#
#     def on_error(self, status):
#         print(status)
#
# if __name__ == '__main__':
#     l = StdOutListener()
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#
#     api = API(auth)
#
#     print(api.me().name)
#     # print(api.trends_available())
#     print(api.trends_place("946738"))
#
#
#     # stream = Stream(auth, l)
#     # stream.filter(track=['basketball'])



