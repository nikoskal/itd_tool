from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from validate_ip import valid_ip


@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def user(request, format=None):
    """
    (POST): Users are created upon successful (federated) login, so no create user functionality is provided
    GET: Retrieve a list of users that are the administrators of the domain

    """
    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    try:
        service_user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        # service_user = None
        return Response("User is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # get academic entity from user name
        academic = service_user.last_name
        # get all users for the defined academic entity
        user_list = User.objects.all().filter(last_name=academic)

        result_list = []
        for user_item in user_list:
            result = {'username': user_item.username, 'name': user_item.first_name, 'email': user_item.email,
                      'domain': user_item.last_name, 'date_joined': user_item.date_joined}
            result_list.append(result)

        if result_list:
            return Response(result_list, status=status.HTTP_200_OK)
        else:
            return Response("user list not found", status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def username_mgmt(request, username, format=None):
    """
    GET: Retrieve details for one user
    DELETE: Delete specified user ..
    """

    ip_address = request.META['REMOTE_ADDR']
    print "delete/get ip_address:"+ip_address

    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
    # verify that token corresponds to a valid user
    try:
        service_user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response("User token is unknown :"+request.user, status=status.HTTP_400_BAD_REQUEST)

    # verify that username exist
    try:
        user_name = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Username is unknown :"+str(username), status=status.HTTP_400_BAD_REQUEST)

    # verify that service_user has the rights to manage the username
    if user_name:
        # academic domain of service_user should be the same as the managed user
        user_domain = user_name.last_name
        user_domain_ = user_domain.replace(".", "_")
        service_user_domain = service_user.last_name
        service_user_domain_ = service_user_domain.replace(".", "_")

        if user_domain_ == service_user_domain_:
            print "permission granted"
        else:
            return Response("Not sufficient rights to perform this action for: "+username,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user_deleted = User.objects.get(username=username).delete()

        if user_deleted is None:
            return Response("user:"+username+" deleted", status=status.HTTP_200_OK)
        else:
            return Response("user:"+username+" not deleted", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # get academic entity from user name
        # get all users for the defined academic entity
        user_item = User.objects.get(username=username)
        result = {}
        if user_item:
            result = {'username': user_item.username, 'name': user_item.first_name, 'email': user_item.email,
                      'domain': user_item.last_name, 'date_joined': user_item.date_joined}
            return Response(result, status=status.HTTP_200_OK)

        if not result:
            return Response("user:"+username+" not found", status=status.HTTP_400_BAD_REQUEST)
