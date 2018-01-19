from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.twitter_task import get_tw_trends, get_tw_term
from itdtool.tasks.gtrends_task import get_cat_suggestions, get_time_interest, get_region_interest, \
    get_related_queries,get_autocomplete

from validate_ip import valid_ip
from validate_user import valid_user
from itdtool.tasks.history_task import get_history
from celery import chain



google_username = account_repo.get_google_username()
google_password = account_repo.get_google_password()

@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def history(request, queryid, format=None):
    """
    Make integrated trends discovery

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        print "retrieve histroy per query id: " + queryid

        results = get_history(id)

        print "retrieve res " + results

        # results = {"history"+queryid};
        return Response(results, status=status.HTTP_200_OK)

