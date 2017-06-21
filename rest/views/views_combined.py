from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.twitter_task import get_tw_trends
from itdtool.tasks.gtrends_task import get_related_keywords
from validate_ip import valid_ip
from validate_user import valid_user

from celery import chain


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def get_combined(request, format=None):
    """
    Make sequencial calls 

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        place_id = 721943

        # res = chain(twitter_trends_location_asynch = get_tw_trends.delay(place_id), get_related_keywords)()
        # res.get()

        twitter_trends_location_asynch = get_tw_trends.delay(place_id)
        suggested_kws_asynch = get_related_keywords.delay("obama")


        twitt_results = str(twitter_trends_location_asynch.get())
        print "twitter_trends_location_asynch: " + twitt_results

        kws_result = str(suggested_kws_asynch)
        print "suggested_kws_asynch: " + kws_result

        concat = 'twitter:' + twitt_results+ " gtrends:"+kws_result

        return Response(concat, status=status.HTTP_200_OK)

