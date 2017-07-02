from __future__ import absolute_import

from itdtool.celeryapp import app

from lxml import etree
import xmltodict
import sys
from passlib.hash import md5_crypt
from django.conf import settings
# import jinja2
# from itdtool.tasks.history_task import monitor_action
# from raven.contrib.django.raven_compat.models import client


from pytrends.request import TrendReq


@app.task
def get_related_queries(keyword, google_username, google_password):

    path = ""
    pytrend = TrendReq(google_username, google_password, custom_useragent='ITD script')
    pytrend.build_payload(keyword)
    # pytrend.build_payload(kw_list=['obama', 'trump'])
    print 'before Sth'
    related_queries_dict = pytrend.related_queries()
    print 'after Sth!!'
    for key, value in related_queries_dict.iteritems():
        print 'key q:' + str(key) +" "+ str(value)

    return related_queries_dict


@app.task
def get_category_suggestions(keyword,  google_username, google_password):

    path = ""
    pytrend = TrendReq(google_username, google_password, custom_useragent='ITD script')
    suggestions = pytrend.suggestions(keyword)

    return suggestions


@app.task
def get_time_interest(kw_list,  google_username, google_password):

    # kw_list = ['snowden', 'obama']
    # kw_list = [keyword]
    print "key words :"
    print(kw_list)

    # uncomment for real results
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq(google_username, google_password, custom_useragent='ITD script')
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend.build_payload(kw_list)
    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()

    # uncomment for empty results
    # interest_over_time_df = " ".join(str(x) for x in kw_list) +":empty trends over time results"
    print "interest_over_time_df" + str(interest_over_time_df)
    # print "interest_over_time_df json" + str(interest_over_time_df.to_json(orient = 'records'))
    demo = {
        'key': interest_over_time_df.to_dict(orient='record')
    }

    return demo



@app.task
def get_time_interest_list(kw_list,  google_username, google_password):

    # kw_list = ['snowden', 'obama']
    # kw_list = [keyword]
    print "key words :"
    print(kw_list)

    # uncomment for real results
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq(google_username, google_password, custom_useragent='ITD script')
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend.build_payload(kw_list)
    # Interest Over Time
    interest_over_time_list_df = pytrend.interest_over_time()

    # uncomment for empty results
    # interest_over_time_df = " ".join(str(x) for x in kw_list) +":empty trends over time results"
    print "interest_over_time_df" + str(interest_over_time_list_df)
    # print "interest_over_time_df json" + str(interest_over_time_df.to_json(orient = 'records'))
    print "interest_over_time_df dict" + str(interest_over_time_list_df.to_dict)

    demo = {
        'key': interest_over_time_list_df.to_dict(orient='record')
    }

    print 'dictionary ready'
    return demo


@app.task
def get_related_keywords(kw_list ,  google_username, google_password):


    # kw_list = ['snowden', 'obama']
    # kw_list = [keyword]
    print "task key words :" +str(kw_list)

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend.build_payload(kw_list)
    # Get Google Keyword Suggestions
    suggestions_dict = pytrend.suggestions(kw_list)

    # # uncomment for empty results
    # suggestions_dict = " ".join(str(x) for x in kw_list) +":empty suggested keyword results"
    print "suggestions_dict" +str(suggestions_dict)

    return suggestions_dict


## example code


# google_username = "GMAIL_USERNAME"
# google_password = "PASSWORD"
# path = "."
#
# terms = [
#     "Image Processing",
#     "Signal Processing",
#     "Computer Vision",
#     "Machine Learning",
#     "Information Retrieval",
#     "Data Mining"
# ]
# # connect to Google Trends API
# connector = pyGTrends(google_username, google_password)
#
#
# for label in terms:
#     print(label)
#     sys.stdout.flush()
#     #kw_string = '"{0}"'.format(keyword, base_keyword)
#     connector.request_report(label, geo="US", date="01/2014 96m")
#     # wait a random amount of time between requests to avoid bot detection
#     time.sleep(randint(5, 10))
#     # download file
#     connector.save_csv(path, label)
#
# for term in terms:
#     data = connector.get_suggestions(term)
#     pprint(data)