from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.twitter_task import get_tw_trends, get_tw_trends_term
from itdtool.tasks.gtrends_task import get_cat_suggestions, get_autocomplete, get_gtrends

from validate_ip import valid_ip
from validate_user import valid_user
from itdtool.tasks.query_params_task import get_query_params_id
from celery import chain
from itdtool.tasks.adwords_task import get_keywords_volume


google_username = account_repo.get_google_username()
google_password = account_repo.get_google_password()

@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def discover(request, queryid, format=None):
    """
    Make integrated trends discovery

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        print "integrated trends discovery query id: " + queryid

        results = {}

        # query_param = get_query_params_id.delay(id)
        query_param = get_query_params_id(queryid)
        print "query params:"
        print query_param

        keyword = query_param['keywords']
        location = query_param['location']
        category = query_param['category']
        youtube = query_param['youtube']
        twitter = query_param['twitter']
        google = query_param['google']
        start_date = query_param['start_date']
        end_date = query_param['end_date']


        print "query_param keyword: " + keyword

        get_gtrends_asynch = get_gtrends.delay(keyword, location, category, start_date, end_date)
        trends_results = get_gtrends_asynch.get()

        print "## Retrieving get_related_queries ##"
        related_queries_result_list = trends_results['related_queries_list']
        print "## Retrieving time based interest ##"
        time_interest_kw_dic = trends_results['time_interest_list']
        print "## Retrieving region based interest ##"
        region_interest_kw_dic = trends_results['interest_over_region']



        # retrieve autocomplete questions
        print "## Retrieving autocomplete ##"
        autocomplete_asynch = get_autocomplete.delay(keyword)
        print "Retrieving autocomplete - finished"

        ## Retrieving adwords volume ##
        print "## Retrieving adwords volume ## for " +keyword
        volume_list = []

        # Uncomment this !!!
        adwords_username = account_repo.get_adwords_username()
        adwords_password = account_repo.get_adwords_password()

        keywords_volume_asynch = get_keywords_volume.delay(adwords_username, adwords_password, keyword, location)
        volume_dic = keywords_volume_asynch.get()

        try:
            for x in range(0, len(volume_dic)):
                volume = {
                    "count": volume_dic[x]['count'],
                    "year": volume_dic[x]['year'],
                    "month": volume_dic[x]['month']
                }
                volume_list.append(volume)
        except TypeError:
            volume_list.append("none")
        # Until here !!!


        # volume_list = [{'count': 450000, 'month': 8, 'year': 2017}, {'count': 673000, 'month': 7, 'year': 2017},
        #  {'count': 450000, 'month': 6, 'year': 2017}, {'count': 550000, 'month': 5, 'year': 2017},
        #  {'count': 673000, 'month': 4, 'year': 2017}, {'count': 823000, 'month': 3, 'year': 2017},
        #  {'count': 1000000, 'month': 2, 'year': 2017}, {'count': 1830000, 'month': 1, 'year': 2017},
        #  {'count': 2240000, 'month': 12, 'year': 2016}, {'count': 2240000, 'month': 11, 'year': 2016},
        #  {'count': 1830000, 'month': 10, 'year': 2016}, {'count': 3350000, 'month': 9, 'year': 2016}]

        print "Retrieving adwords volume - finished"


        print "## Retrieving twitter data ##"

        if twitter:
            try:
                response_asynch = get_tw_trends_term.delay(keyword)
                twitter_result = response_asynch.get()
            except :
                twitter_result = [{"text": "too many twitter calls"}]
        else:
            twitter_result = {}
        print "Retrieving twitter data - finished"


        ## integrate results ##
        results = {"related_queries_list": related_queries_result_list,
                   # "related_queries_list_youtube": related_queries_youtube_result_list,
                   "volume_list": volume_list,
                   "time_interest_list": time_interest_kw_dic,
                   "interest_over_region": region_interest_kw_dic,
                   "autocomplete": autocomplete_asynch.get(),
                   "tweets": twitter_result
                   }

        print "results:"
        print results

        return Response(results, status=status.HTTP_200_OK)

# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def get_combined(request, format=None):
#     """
#     Make sequencial calls
#
#     """
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#         place_id = 721943
#
#         # res = chain(twitter_trends_location_asynch = get_tw_trends.delay(place_id), get_related_keywords)()
#         # res.get()
#
#         twitter_trends_location_asynch = get_tw_trends.delay(place_id)
#         suggested_kws_asynch = get_related_keywords.delay("obama")
#
#
#         twitt_results = str(twitter_trends_location_asynch.get())
#         print "twitter_trends_location_asynch: " + twitt_results
#
#         kws_result = str(suggested_kws_asynch)
#         print "suggested_kws_asynch: " + kws_result
#
#         concat = 'twitter:' + twitt_results+ " gtrends:"+kws_result
#
#         return Response(concat, status=status.HTTP_200_OK)

