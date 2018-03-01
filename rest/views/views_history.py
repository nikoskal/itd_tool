from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import HttpResponse
from itdtool import account_repo
import pandas as pd
from validate_ip import valid_ip
from validate_user import valid_user
from itdtool.tasks.history_task import get_all_history, get_history_item, delete_history
import json
import xlsxwriter




@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def history(request, format=None):
    """
    Retrieve all history

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        # print "retrieve histroy"
        hist_asynch = get_all_history.delay()
        hist_list = hist_asynch.get()
        # print("in1")
        # print "retrieve hist_list " + str(hist_list)
        return Response(hist_list, status=status.HTTP_200_OK)



@api_view(['GET', 'DELETE'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def history_id(request, history_id, format=None):
    """
    Retrieve history items for specific id

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        print "retrieve histroy item "

        hist_asynch = get_history_item.delay(history_id)
        # hist_asynch = get_all_history.delay()
        hist_list = hist_asynch.get()
        print "retrieve one hist_list " + str(hist_list)
        # results = {"history"+queryid};
        return Response(hist_list, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        print "DELETE histroy item "

        hist_asynch = delete_history.delay(history_id)
        # hist_asynch = get_all_history.delay()
        delete_result = hist_asynch.get()
        print "delete one hist " + str(delete_result)
        # results = {"history"+queryid};
        return Response(delete_result, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def history_export_id(request, history_id, format=None):
    """
       Export history to excel

    """
    if request.method == 'GET':
        print "export history item" + str(history_id)
        hist_asynch = get_history_item.delay(history_id)
        hist_data = hist_asynch.get()
        print "1"
        print hist_data['results']
        id = hist_data['id']
        keyword = hist_data['keyword']
        filename = keyword +"_"+str(id) +"_results.xlsx"
        print filename

        workbook = xlsxwriter.Workbook(filename)
        ws_query_details = workbook.add_worksheet('query_details')
        ws_related_queries_top = workbook.add_worksheet('related_terms_top')
        ws_related_queries_rising = workbook.add_worksheet('related_terms_rising')
        ws_time_interest = workbook.add_worksheet('time_interest')
        ws_volume = workbook.add_worksheet('volume')
        ws_region = workbook.add_worksheet('region')
        ws_autocomplete = workbook.add_worksheet('autocomplete')
        ws_twitter_gender = workbook.add_worksheet('twitter_gender')
        ws_twitter_sentiment = workbook.add_worksheet('twitter_sentiment')
        ws_popular_tweets = workbook.add_worksheet('popular_tweets')

        results_exp = hist_data['results']
        # writing to query details

        ws_query_details.write(0, 0, "Query description")
        ws_query_details.write(0, 1, hist_data['query_desc'])
        ws_query_details.write(1, 0, "Date of execution")
        ws_query_details.write(1, 1, hist_data['execution_date'])
        ws_query_details.write(2, 0, "Executed by")
        ws_query_details.write(2, 1, hist_data['user_name'])
        ws_query_details.write(3, 0, "Keyword investigated")
        ws_query_details.write(3, 1, hist_data['keyword'])

        # top
        top_list = results_exp['related_queries_list']['top']
        row_t = 0
        col_t = 0
        for top in top_list:
            ws_related_queries_top.write(row_t, col_t, top['query'])
            ws_related_queries_top.write(row_t, col_t + 1, top['value'])
            row_t += 1

        # rising
        rising_list = results_exp['related_queries_list']['rising']
        row_r = 0
        col_r = 0
        for rising in rising_list:
            ws_related_queries_rising.write(row_r, col_r, rising['query'])
            ws_related_queries_rising.write(row_r, col_r + 1, rising['value'])
            row_r += 1

        # ws_time_interest
        time_interest_list = results_exp['time_interest_list']
        row_i = 0
        col_i = 0
        for time_interest in time_interest_list:
            ws_time_interest.write(row_i,col_i,time_interest['date'] )
            ws_time_interest.write(row_i, col_i+1, time_interest['interest'])
            row_i += 1

        volume_list = results_exp['volume_list']
        row_v = 0
        col_v = 0
        for volume in volume_list:
            ws_volume.write(row_v, col_v, volume['year'])
            ws_volume.write(row_v, col_v + 1, volume['month'])
            ws_volume.write(row_v, col_v + 2, volume['count'])
            row_v += 1

        interest_over_region_list = results_exp['interest_over_region']
        row_int = 0
        col_int = 0
        for interest_over_region in interest_over_region_list:
            ws_region.write(row_int, col_int, interest_over_region['region'])
            ws_region.write(row_int, col_int + 1, interest_over_region['interest'])
            row_int += 1

        autocomplete_list = results_exp['autocomplete']
        row_aut = 0
        col_aut = 0
        for autocomplete in autocomplete_list:
            ws_autocomplete.write(row_aut, col_aut, autocomplete['question'])
            for question in autocomplete['result']:
                ws_autocomplete.write(row_aut+1, col_aut + 1, question)
                row_aut += 1

        # ws_twitter_gender
        row_g = 0
        col_g = 0

        ws_twitter_gender.write(row_g, col_g, "estimation of male gender for relevant tweets")
        ws_twitter_gender.write(row_g, col_g + 1, results_exp['tweets']['tweet_gender_prob']['male'])
        ws_twitter_gender.write(row_g+1, col_g , "confidence of estimation for male ")
        ws_twitter_gender.write(row_g+1, col_g + 1, results_exp['tweets']['tweet_gender_prob']['male_conf'])

        ws_twitter_gender.write(row_g+2, col_g, "estimation of female gender for relevant tweets")
        ws_twitter_gender.write(row_g+2, col_g + 1, results_exp['tweets']['tweet_gender_prob']['female'])
        ws_twitter_gender.write(row_g + 3, col_g, "confidence of estimation for female")
        ws_twitter_gender.write(row_g + 3, col_g + 1, results_exp['tweets']['tweet_gender_prob']['female_conf'])

        ws_twitter_gender.write(row_g+4, col_g, "percentage of unknown")
        ws_twitter_gender.write(row_g+4, col_g + 1, results_exp['tweets']['tweet_gender_prob']['unknown'])

        ws_twitter_gender.write(row_g + 5, col_g, "total tweets processed")
        ws_twitter_gender.write(row_g + 5, col_g + 1, results_exp['tweets']['tweet_gender_prob']['total_records'])


        # ws_twitter_sentiment
        row_s = 0
        col_s = 0

        ws_twitter_sentiment.write(row_s, col_s, "number of tweets classified as positive")
        ws_twitter_sentiment.write(row_s, col_s + 1, results_exp['tweets']['twitter_sentiment_top_result']['total_tweets_positive'])

        ws_twitter_sentiment.write(row_s+1, col_s, "number of tweets classified as negative")
        ws_twitter_sentiment.write(row_s+1, col_s + 1,
                                   results_exp['tweets']['twitter_sentiment_top_result']['total_tweets_negative'])

        ws_twitter_sentiment.write(row_s + 2, col_s, "number of tweets classified as neutral")
        ws_twitter_sentiment.write(row_s + 2, col_s + 1,
                                   results_exp['tweets']['twitter_sentiment_top_result']['total_tweets_neutral'])

        ws_twitter_sentiment.write(row_s + 3, col_s, "polarisation of positive tweets ,min=0, max=1")
        ws_twitter_sentiment.write(row_s + 3, col_s + 1,
                                   results_exp['tweets']['twitter_sentiment_top_result']['average_score_pos'])

        ws_twitter_sentiment.write(row_s + 4, col_s, "polarisation of negative tweets ,min=0, max=-1")
        ws_twitter_sentiment.write(row_s + 4, col_s + 1,
                                   results_exp['tweets']['twitter_sentiment_top_result']['average_score_neg'])

        # ws_popular_tweets
        row_p = 0
        col_p = 0
        poptweet_list = results_exp['tweets']['popular_tweets']
        ws_popular_tweets.write(0, 0, "id")
        ws_popular_tweets.write(0, 1, "user")
        ws_popular_tweets.write(0, 2, "created")
        ws_popular_tweets.write(0, 3, "retweets")
        ws_popular_tweets.write(0, 4, "likes")
        ws_popular_tweets.write(0, 5, "text")
        row_p = 1
        for poptweet in poptweet_list:
            ws_popular_tweets.write(row_p, 0, poptweet['id'])
            ws_popular_tweets.write(row_p, 1, poptweet['user'])
            ws_popular_tweets.write(row_p, 2, poptweet['created'])
            ws_popular_tweets.write(row_p, 3, poptweet['retweets'])
            ws_popular_tweets.write(row_p, 4, poptweet['favs'])
            ws_popular_tweets.write(row_p, 5, poptweet['text'])
            row_p += 1

        workbook.close()
        file = open(filename, 'rb')
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response