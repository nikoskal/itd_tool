from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.gtrends_task import get_related_keywords, get_category_suggestions, get_related_queries,\
    get_time_interest, get_time_interest_list
from validate_ip import valid_ip
from validate_user import valid_user

google_username = account_repo.get_google_username()
google_password = account_repo.get_google_password()


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def related_queries(request, keyword, format=None):
    """
    Retrieve related queries

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)


    if request.method == 'GET':

        related_queries_asynch = get_related_queries.delay(keyword, google_username, google_password)
        # print "related_queries_asynch: "+ str(related_queries_asynch.get())
        print "eftasa edo"
        return Response(related_queries_asynch.get(), status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def cat_suggestions(request, keyword, format=None):
    """
    Retrieve category suggestions, get a list of categories that are related with the keyword 

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':

        suggestions_asynch = get_category_suggestions.delay(keyword, google_username, google_password)
        # print "trend_asynch: "+ trend_asynch
        return Response(suggestions_asynch.get(), status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def over_time(request, keyword, format=None):
    """
    Retrieve interest over time 
    Numbers represent search interest relative to the highest point on the 
    chart for the given region and time. A value of 100 is the peak popularity
    for the term. A value of 50 means that the term is half as popular. Likewise
    a score of 0 means the term was less than 1% as popular as the peak.
    if no timeframe is specified initial date is : 2012-07-01, until: today
    interest index / per week 

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
        kw_list = [keyword]
        trend_asynch = get_time_interest(kw_list, google_username, google_password)
        # print "trend_asynch: "+ trend_asynch
        return Response(trend_asynch, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def over_time_list(request, keyword1, keyword2, format=None):
    """
    Get interest for a specified time frame for the specified keywords 

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

    print str(keyword1)
    print str(keyword2)
    # kw_list = [keyword]
    if request.method == 'GET':
        kw_list = [keyword1, keyword2]
        related_kws_asynch = get_time_interest_list.delay(kw_list, google_username, google_password)
        print str('starting')
        return Response(related_kws_asynch.get(), status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def related_kws(request, keyword,  format=None):
    """
    Retrieve keywords

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

        related_kws_asynch = get_related_keywords.delay(keyword, google_username, google_password)
        return Response(related_kws_asynch.get(), status=status.HTTP_200_OK)