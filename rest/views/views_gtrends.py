from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.gtrends_task import get_cat_suggestions, get_autocomplete, get_gtrends
from validate_ip import valid_ip
from validate_user import valid_user

google_username = account_repo.get_google_username()
google_password = account_repo.get_google_password()



# if location 'none' defaults to wordwide
# categories -->
# Movies: 34
# News : 16
# Real Estate: 29

@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def gtrends(request, keyword, location, category, format=None):
    """
    Retrieve interest for one term
    Numbers represent search interest relative to the highest point on the
    chart for the given region and time. A value of 100 is the peak popularity
    for the term. A value of 50 means that the term is half as popular. Likewise
    a score of 0 means the term was less than 1% as popular as the peak.
    if no timeframe is specified initial date is : 2012-07-01, until: today
    interest index / per week.
    """

    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    # try:
    #     service_user = User.objects.get(username=request.user)
    # except User.DoesNotExist:
    #     # service_user = None
    #     return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)
    #
    # if valid_user(service_user, lsname) is False:
    #     return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
    #

    if request.method == 'GET':
        print keyword, location, category
        get_gtrends_asynch = get_gtrends.delay(keyword, location, category)
        print "get_gtrends_asynch: " + str(get_gtrends_asynch.get())
        return Response(get_gtrends_asynch.get(), status=status.HTTP_200_OK)




#
#
# @api_view(['GET'])
# def test(request, format=None):
#
#     if request.method == 'GET':
#         keyword = 'snowden'
#         location = 'GB'
#         category = 0
#         print "start testing for "+ str(keyword)
#         #1
#         print "test: get_related_queries "
#         related_queries_asynch = get_related_queries.delay(keyword, location, category)
#         print "related_queries_asynch: " + str(related_queries_asynch.get())
#         #2
#         print "test: get_cat_suggestions: "
#         cat_suggestions_asynch = get_cat_suggestions.delay(keyword)
#         print "cat_suggestions_asynch: " + str(cat_suggestions_asynch.get())
#         #3
#         print "test: get_time_interest: "
#         time_interest_asynch = get_time_interest.delay(keyword, location, google_username, google_password)
#         time_interest_kw_dic = time_interest_asynch.get()
#         print "time_interest_asynch: " + str(time_interest_kw_dic.get())
#         #4
#         print "test: get_region_interest: "
#         region_interest_kw_asynch = get_region_interest.delay(keyword, category, google_username, google_password)
#         print "time_interest_asynch: " + str(region_interest_kw_asynch.get())
#         #5
#         print "test: get_autocomplete: "
#         autocomplete_asynch = get_autocomplete.delay(keyword)
#         print "autocomplete_asynch: " + str(autocomplete_asynch.get())
#         #
#         print "Finished testing"
#
#         results = {"1related_queries_list": related_queries_asynch.get(),
#                    "2cat_suggestions": cat_suggestions_asynch.get(),
#                    "3time_interest_list": time_interest_kw_dic[keyword],
#                    "4interest_over_region": region_interest_kw_asynch.get(),
#                    "5autocomplete": autocomplete_asynch.get(),
#                    }
#
#         return Response(results, status=status.HTTP_200_OK)



@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def autocomplete(request, keyword, format=None):
    """
    Get autocomplete questions...
    :param request:
    :param keyword:
    :param format:
    :return:
    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':

        autocomplete_asynch = get_autocomplete.delay(keyword)
        # print "trend_asynch: "+ trend_asynch
        return Response(autocomplete_asynch.get(), status=status.HTTP_200_OK)


# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def over_region(request, keyword, format=None):
#     """
#     Retrieve interest over region for one term
#     Numbers represent search interest relative to the highest point on the
#     chart for the given region and time. A value of 100 is the peak popularity
#     for the term. A value of 50 means that the term is half as popular. Likewise
#     a score of 0 means the term was less than 1% as popular as the peak.
#     if no timeframe is specified initial date is : 2012-07-01, until: today
#     interest index / per week
#
#     """
#
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     # try:
#     #     service_user = User.objects.get(username=request.user)
#     # except User.DoesNotExist:
#     #     # service_user = None
#     #     return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # if valid_user(service_user, lsname) is False:
#     #     return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#     #                     status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#         # kw_list = [keyword]
#         trend_asynch = get_region_interest.delay(keyword, google_username, google_password)
#         # print "trend_asynch: "+ trend_asynch
#         return Response(trend_asynch.get(), status=status.HTTP_200_OK)
#

# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def related_queries(request, keyword, location, category, format=None):
#     """
#     Retrieve related queries (rising and top)
#
#     """
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#         print "1 .related_queries_asynch: "+ str(keyword)
#         related_queries_asynch = get_related_queries.delay(keyword, location, category, google_username, google_password)
#         # print "related_queries_asynch: "+ str(related_queries_asynch.get())
#
#         return Response(related_queries_asynch.get(), status=status.HTTP_200_OK)


# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def cat_suggestions(request, keyword, format=None):
#     """
#     Retrieve category suggestions, get a list of categories that are related with the keyword
#
#     """
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#
#         suggestions_asynch = get_category_suggestions.delay(keyword, google_username, google_password)
#         # print "trend_asynch: "+ trend_asynch
#         return Response(suggestions_asynch.get(), status=status.HTTP_200_OK)


# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def over_time(request, keyword, location, format=None):
#     """
#     Retrieve interest over time for one term
#     Numbers represent search interest relative to the highest point on the
#     chart for the given region and time. A value of 100 is the peak popularity
#     for the term. A value of 50 means that the term is half as popular. Likewise
#     a score of 0 means the term was less than 1% as popular as the peak.
#     if no timeframe is specified initial date is : 2012-07-01, until: today
#     interest index / per week
#
#     """
#
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     # try:
#     #     service_user = User.objects.get(username=request.user)
#     # except User.DoesNotExist:
#     #     # service_user = None
#     #     return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # if valid_user(service_user, lsname) is False:
#     #     return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#     #                     status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#         # kw_list = [keyword]
#         trend_asynch = get_time_interest.delay(keyword, location, google_username, google_password)
#         # print "trend_asynch: "+ trend_asynch
#         return Response(trend_asynch.get(), status=status.HTTP_200_OK)


# @api_view(['GET'])
# # @authentication_classes((TokenAuthentication, BasicAuthentication))
# # @permission_classes((IsAuthenticated,))
# def over_time_list(request, keyword1, keyword2, format=None):
#     """
#     Get interest for a specified time frame for the specified keyword list
#
#     """
#
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     # try:
#     #     service_user = User.objects.get(username=request.user)
#     # except User.DoesNotExist:
#     #     # service_user = None
#     #     return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # if valid_user(service_user, lsname) is False:
#     #     return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#     #                     status=status.HTTP_401_UNAUTHORIZED)
#
#     print str(keyword1)
#     print str(keyword2)
#     # kw_list = [keyword]
#     if request.method == 'GET':
#         kw_list = [keyword1, keyword2]
#         related_kws_asynch = get_time_interest_list.delay(kw_list, google_username, google_password)
#         print str('starting')
#         return Response(related_kws_asynch.get(), status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def cat_suggestions(request, keyword,  format=None):
    """
    Retrieve related keywords

    """

    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    # try:
    #     service_user = User.objects.get(username=request.user)
    # except User.DoesNotExist:
    #     # service_user = None
    #     return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)
    #
    # if valid_user(service_user, lsname) is False:
    #     return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
    #                     status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        cat_suggestions_asynch = get_cat_suggestions.delay(keyword)
        return Response(cat_suggestions_asynch.get(), status=status.HTTP_200_OK)