from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views
from rest.serializers import UserSerializer
from validate_ip import valid_ip


# noinspection PyUnusedLocal
@api_view(['GET', 'POST'])
def user_token(request, format=None):
    """
    Retrieve user's token based on the following attributes
    {
    "displayName": "John  Doe",
    "eduPersonPrincipalName": "johnDoe@ntua.gr",
    "eduPersonEntitlement": "admin",
    "schacHomeOrganization": "ntua.gr"
    }
    the value in schacHomeOrganization will be utilised for the Logical System's name
    user.first_name = display_name
    user.last_name = domain
    """

    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    print("get_user_token: Retrieve user's token based on provided credentials")
    # academicEntityList = {"ntua","uoa", "uoi"}

    if request.method == 'POST':
        display_name = request.data['displayName']
        username = request.data['eduPersonPrincipalName']
        role = request.data['eduPersonEntitlement']
        domain = request.data['schacHomeOrganization']
        # ip_addr = request.META['REMOTE_ADDR']

        if role != "admin":
            return Response("unnauthorised user", status=status.HTTP_401_UNAUTHORIZED)
        # create user if not exist
        # user = get_user_obj(username)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            # print "create LS admin :"+username +" academic domain:" + domain
            user = User.objects.create_user(username, email=username)
            # academic = AcademicEntityAdmin(user, domain = domain)
            user.first_name = display_name
            domain_ = domain.replace(".", "_")
            user.last_name = domain_
            user.save()
        # print "get token for:" + str(user)
        token = Token.objects.get_or_create(user_id=user.id)
        # print 'token:'+str(token)
        stringtoken = str(token)
        return Response({'token': stringtoken}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):

    ip_address = request.META['REMOTE_ADDR']
    if valid_ip(ip_address) is False:
        return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)

    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = User.objects.create_user(username, email, password)
    if user:
        return Response(user.username, status=status.HTTP_201_CREATED)
    else:
        return Response("user not created", status=status.HTTP_400_BAD_REQUEST)

