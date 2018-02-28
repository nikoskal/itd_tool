from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo

from validate_ip import valid_ip
from validate_user import valid_user
from itdtool.tasks.history_task import get_all_history, get_history_item, delete_history




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