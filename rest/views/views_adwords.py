from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from itdtool import account_repo
from itdtool.tasks.adwords_task import get_keywords_volume
from validate_ip import valid_ip
from validate_user import valid_user

adwords_username = account_repo.get_adwords_username()
adwords_password = account_repo.get_adwords_password()


@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def keywords_volume(request, keywd, loc_name, format=None):
    """
    Retrieve keywords volume

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    print "in view:" + str(keywd)
    # keywd = "sebastian vettel"
    if request.method == 'GET':

        related_keywords_asynch = get_keywords_volume.delay(adwords_username,adwords_password, keywd, loc_name )
        return Response(related_keywords_asynch.get(), status=status.HTTP_200_OK)



@api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def keywords_volume_query_id(request, keywd, query_id, format=None):
    """
    Retrieve related queries

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    print "in view:" + str(keywd)

    if request.method == 'GET':

        related_keywords_asynch = get_keywords_volume.delay(adwords_username,adwords_password, keywd, loc_name )
        return Response(related_keywords_asynch.get(), status=status.HTTP_200_OK)
