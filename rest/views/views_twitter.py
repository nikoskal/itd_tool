from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.twitter_task import get_tw_trends, get_tw_trends_term
from validate_ip import valid_ip
from validate_user import valid_user
import requests




@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def get_trends_location(request, place_id, format=None):
    """
    Retrieve twitter trends for specified location

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        twitter_trends_location_asynch = get_tw_trends.delay(place_id)
        # print "related_queries_asynch: " + str(twitter_trends_location_asynch.get())
        return Response(twitter_trends_location_asynch.get(), status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def get_tweets_term(request, term, format=None):
    """
    Retrieve twitter trends for specific term

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        response_asynch = get_tw_trends_term.delay(term)
        return Response(response_asynch.get(), status=status.HTTP_200_OK)

