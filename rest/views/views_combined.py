from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.twitter_task import get_tw_trends, get_tw_trends_term
from itdtool.tasks.gtrends_task import get_cat_suggestions, get_time_interest, get_region_interest, \
    get_related_queries,get_autocomplete

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

        results = {};

        # query_param = get_query_params_id.delay(id)
        query_param = get_query_params_id(queryid)
        print "query params:"
        print query_param

        keyword = query_param['keywords']
        location = query_param['location']
        category = query_param['category']
        youtube = query_param['youtube']
        twitter =  query_param['twitter']


        # retrieve autocomplete questions
        print "## Retrieving autocomplete ##"
        autocomplete_asynch = get_autocomplete.delay(keyword)
        print "Retrieving autocomplete - finished"
        # TODO change this to related queries not categories !!!
        ## Retrieving suggested Keywords ##
        # print "## Retrieving suggested Keywords ##"
        # suggested_kws_asynch = get_cat_suggestions.delay(keyword, google_username, google_password)
        # kws_result = str(suggested_kws_asynch.get())
        # print "suggested_kws_asynch: " + kws_result
        # kws_dic = suggested_kws_asynch.get()
        # related_kwd_list = []
        #
        # # print len(kws_dic)
        #
        # for x in range(0, len(kws_dic)):
        #     related_kwd = {
        #         "type": kws_dic[x]['type'],
        #         "mid": kws_dic[x]['mid'],
        #         "title": kws_dic[x]['title']
        #     }
        #     related_kwd_list.append(related_kwd)
        # print "related_kwd_list"
        # print related_kwd_list
        # kwds reply ready ##

        print "## Retrieving get_related_queries ##"

        related_queries_asynch = get_related_queries.delay(keyword, location, category, google_username, google_password)
        related_queries_result_list = related_queries_asynch.get()

        print "Retrieving get_related_queries - finished"
        # print related_queries_result_list


        # print "## Retrieving get_related_queries for youtube ##"
        # related_queries_youtube_result_list = {}
        # if youtube:
        #     related_queries_youtube_asynch = get_related_queries.delay(keyword, location, category, True, google_username, google_password)
        #     related_queries_youtube_result_list = related_queries_youtube_asynch.get()
        #     print related_queries_youtube_result_list


        # for x in range(0, len(kws_dic)):
        #     related_kwd = {
        #         "type": kws_dic[x]['type'],
        #         "mid": kws_dic[x]['mid'],
        #         "title": kws_dic[x]['title']
        #     }
        #     related_kwd_list.append(related_kwd)
        # print "related_kwd_list"
        # print related_kwd_list


        ## Retrieving time based interest on Keyword ##
        print "## Retrieving time based interest ##"
        time_interest_kw_asynch = get_time_interest.delay(keyword, location, category, google_username, google_password)
        time_interest_kw_dic = time_interest_kw_asynch.get()
        # print "!!!!!time_interest_kw_dic_result: "
        # print time_interest_kw_dic[keyword]
        # time based interest reply ready ##
        print "Retrieving time based interest - finished"

        ## Retrieving region based interest on Keyword ##
        print "## Retrieving region based interest ##"
        region_interest_kw_asynch = get_region_interest.delay(keyword, category, google_username, google_password)
        region_interest_kw_dic = region_interest_kw_asynch.get()
        print "Retrieving region based interest - finished"

        ## Retrieving adwords volume ##
        print "## Retrieving adwords volume ##"
        # Uncomment this !!!
        adwords_username = account_repo.get_adwords_username()
        adwords_password = account_repo.get_adwords_password()

        keywords_volume_asynch = get_keywords_volume.delay(adwords_username, adwords_password, keyword, location)
        volume_dic = keywords_volume_asynch.get()

        volume_list = []
        for x in range(0, len(volume_dic)):
            volume = {
                "count": volume_dic[x]['count'],
                "year": volume_dic[x]['year'],
                "month": volume_dic[x]['month']
            }
            volume_list.append(volume)
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
            except:
                twitter_result = [{"text": "too many twitter calls"}]
        else:
            twitter_result = {}
        print "Retrieving twitter data - finished"


        ## integrate results ##
        results = {"related_queries_list": related_queries_result_list,
                   # "related_queries_list_youtube": related_queries_youtube_result_list,
                   "volume_list": volume_list,
                   "time_interest_list": time_interest_kw_dic[keyword],
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

