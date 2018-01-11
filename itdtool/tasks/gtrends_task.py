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
import json
import pprint
import requests

# from itdtool.requests import TrendReq
from pytrends.request import TrendReq


@app.task
def get_autocomplete(keyword):

    # http://suggestqueries.google.com/complete/search?client=firefox&q=is%20vettel
    results = []
    # print("get_autocomplete questions")

    url = "http://suggestqueries.google.com/complete/search?client=firefox&q=is%20"+keyword
    # print url
    isresponse = requests.get(url)
    jisres = isresponse.json()

    # print jisres
    jisres_reduced = jisres[1]
    # print jisres_reduced

    isresult = {"isresult":jisres_reduced}
    results.append(isresult)

    url = "http://suggestqueries.google.com/complete/search?client=firefox&q=did%20" + keyword
    # print url
    #
    didresponse = requests.get(url)
    jdidres = didresponse.json()
    # print jdidres
    jdidres_reduced = jdidres[1]
    didresult = {"didresult": jdidres_reduced}
    results.append(didresult)

    return results


@app.task
def get_gtrends(keyword, location, category, start_date, end_date ):

    pytrend = TrendReq()
    # keyword = "Blockchain"
    # keyword = "edward snowden"
    # keyword = "war terror"
    kw_list = [keyword]
    category = ""

    if location == 'none':
        location = ''
    # loc = str(location)
    print "location "+location
    timeframe = ''

    #  correct date format 2014-01-01T00:00:00
    if (len(start_date) == 19) and (len(end_date) == 19):
        timeframe = start_date[:-9]+" "+end_date[:-9]

    # '2016-12-14 2017-01-25'
    print timeframe

    pytrend.build_payload(kw_list, cat=category, timeframe=timeframe, geo=location)
    # pytrend.build_payload(kw_list,  timeframe=timeframe, geo=location)

    # region interest
    region_interest_df = pytrend.interest_by_region()
    region_interest = region_interest_df[keyword]
    region_result = []
    for region in region_interest.keys():
        d = {"region": region,
             "interest": region_interest_df[keyword][region]}
        region_result.append(d)

    # related_queries
    try:
        print("------")
        related_queries_dict = pytrend.related_queries()
        rising_df = related_queries_dict[keyword]['rising']
        top_df = related_queries_dict[keyword]['top']
        related_queries = {
            'rising': rising_df.to_dict(orient='record'),
            'top': top_df.to_dict(orient='record')
        }
    except:
        related_queries = {
            'rising': "",
            'top': ""
        }

    #time_interest
    interest_over_time_df = pytrend.interest_over_time()

    interest_over_time_temp = {
        'interest_over_time': interest_over_time_df.to_dict()
    }

    values = interest_over_time_temp['interest_over_time'][keyword]

    interest_over_time = {}
    keyword_result = []

    for timestamp in values:
        # print 'timestamp '+ str(timestamp)
        date_string = timestamp.strftime('%Y-%m-%d')
        # print 'value ' + str(values[timestamp])

        d = {"date":date_string,
             "interest": values[timestamp]}
        # print 'd = ' + str(d)
        keyword_result.append(d)

    interest_over_time[keyword] = keyword_result

    results = {"related_queries_list": related_queries,
               "time_interest_list": interest_over_time[keyword],
               "interest_over_region": region_result,
               }

    return results


@app.task
def get_region_interest(keyword, category, google_username, google_password):

    path = ""
    pytrend = TrendReq()
    # pytrend = TrendReq(google_username, google_password, hl='en-US',  custom_useragent='ITD script')

    kw_list = [keyword]
    pytrend.build_payload(kw_list, cat=category)
    # pytrend.build_payload(kw_list=['obama', 'trump'])

    region_interest_df = pytrend.interest_by_region()

    # print 'printing region_interest_df '
    # pprint.pprint(region_interest_df)
    # print 'printing region_interest_df keys '
    # pprint.pprint(region_interest_df.keys())

    region_interest = region_interest_df[keyword]
    # print 'printing region_interest_df keyword '
    # pprint.pprint(region_interest)

    # print 'printing region_interest_df keys '
    # pprint.pprint(region_interest.keys)

    interest_over_region = {}
    keyword_result = []

    for region in region_interest.keys():
        # print region

        d = {"region":region,
             "interest": region_interest_df[keyword][region]}
        # print d
        keyword_result.append(d)

    # interest_over_region[keyword] = keyword_result

    # print 'printing interest_over_region '
    # pprint.pprint(keyword_result)

    return keyword_result



@app.task
def get_related_queries(keyword, category):

    path = ""
    pytrend = TrendReq()
    kw_list= [keyword]
    pytrend.build_payload(kw_list, cat=category)
    # pytrend.build_payload(kw_list=['obama', 'trump'])

    related_queries_dict = pytrend.related_queries()

    # print 'printing dictionary '
    # pprint.pprint(related_queries_dict)

    # print 'printing dictionary rising'
    rising_df = related_queries_dict[keyword]['rising']
    # pprint.pprint(rising_df)

    # print 'printing dictionary top'
    top_df = related_queries_dict[keyword]['top']
    # pprint.pprint(top_df)

    # print 'interest_over_time'
    related_queries = {
        'rising': rising_df.to_dict(orient='record'),
        'top': top_df.to_dict(orient='record')
    }
    # pprint.pprint(interest_over_time)
    # related_queries_json = json.dumps(related_queries_dict)

    return related_queries







@app.task
def get_related_queries(keyword, location, category):

    path = ""
    pytrend = TrendReq()
    kw_list= [keyword]
    # print "## get_related_queries  ##"
    print kw_list
    print location
    # category = 184
    print category

    pytrend.build_payload(kw_list, geo=location,  cat=category)
    # print "edo1"
    try:
        related_queries_dict = pytrend.related_queries()
        # print "edo2"
        rising_df = related_queries_dict[keyword]['rising']
        # pprint.pprint(rising_df)
        # print "edo3"
        # print 'printing dictionary top'
        top_df = related_queries_dict[keyword]['top']
        related_queries = {
            'rising': rising_df.to_dict(orient='record'),
            'top': top_df.to_dict(orient='record')
        }
    except:
        related_queries = {
            'rising': "",
            'top': ""
        }



    return related_queries


@app.task
def get_time_interest(keyword, location, category, google_username, google_password):

    # kw_list = ['snowden', 'obama']
    # kw_list = [keyword]
    print "key words :"
    print(keyword)
    kw_list = [keyword]

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    # pytrend = TrendReq(google_username, google_password, hl='en-US', geo=location, custom_useragent='ITD script')
    pytrend = TrendReq()
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend.build_payload(kw_list, cat=category)
    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()

    # uncomment for empty results
    # interest_over_time_df = " ".join(str(x) for x in kw_list) +":empty trends over time results"
    # print "interest_over_time_df" + str(interest_over_time_df)
    # print "interest_over_time_df json" + str(interest_over_time_df.to_json(orient = 'records'))

    # print 'printing interest_over_time_df keys '
    # pprint.pprint(interest_over_time_df.keys())

    interest_over_time_temp = {
        'interest_over_time': interest_over_time_df.to_dict()
    }

    # print 'printing interest_over_time dict '
    # pprint.pprint(interest_over_time_temp)

    values = interest_over_time_temp['interest_over_time'][keyword]

    # make timestamps strings
    # print 'iterate'

    interest_over_time = {}
    keyword_result = []

    for timestamp in values:
        # print 'timestamp '+ str(timestamp)
        date_string = timestamp.strftime('%Y-%m-%d')
        # print 'value ' + str(values[timestamp])

        d = {"date":date_string,
             "interest": values[timestamp]}
        # print 'd = ' + str(d)
        keyword_result.append(d)

    interest_over_time[keyword] = keyword_result

    # print 'interest_over_time final:'
    # pprint.pprint(interest_over_time)

    return interest_over_time


# data = {'list': [{'a':'1'}]}
# >>> data['list'].append({'b':'2'})
# >>> data
# {'list': [{'a': '1'}, {'b': '2'}]}


@app.task
def get_time_interest_list(kw_list,  google_username, google_password):

    # kw_list = ['snowden', 'obama']
    # kw_list = [keyword]
    print "key words :"
    print(kw_list)

    # uncomment for real results
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()
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
def get_cat_suggestions(kw_list_obj):

    # kw_list_obj = 'snowden'
    kw_list = [kw_list_obj]
    # kw_list = [kw_list_obj]
    print " get_cat_suggestions task key words :" +str(kw_list)

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    # pytrend = TrendReq(google_username, google_password, hl='en-US', custom_useragent='My Pytrends Script')
    pytrend = TrendReq()
    pytrend.build_payload(kw_list, timeframe='today 5-y')
    suggestions_dict = pytrend.suggestions(keyword = kw_list_obj)

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