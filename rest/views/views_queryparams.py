from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from itdtool import account_repo
# from rest.serializers import UserSerializer
# from itdtool.tasks.basic_trends_task import get_google_trends_task, get_google_keywords_task
# from itdtool.tasks.basic_trends_task import  get_google_keywords_task
from itdtool.tasks.query_params_task import add_query_params, get_all_query_params, get_query_params_id, \
    delete_query_params_id
from django.conf import settings
from validate_ip import valid_ip
from validate_user import valid_user


@api_view(['DELETE','GET', 'POST'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def query_params_mgmt_id(request, id, format=None):
    """
    Manage "Query Parameters" by id

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

    if request.method == 'DELETE':
        print "delete query_params by id in view "
        deletion_status = delete_query_params_id(id)
        print "deletion_status:" + str(deletion_status)


        # if deletion_status:
        #     return Response("query param deleted:" + id, status=status.HTTP_200_OK)
        # else:
        #     return Response("query param not deleted:" + id, status=status.HTTP_400_BAD_REQUEST)
        return Response("query param deleted:" + id, status=status.HTTP_200_OK)


    if request.method == 'GET':
        print "get query_params by id in view "
        query_param = get_query_params_id.delay(id)
        print "query_param:"+str(query_param)

        return Response(query_param.get(), status=status.HTTP_200_OK)




@api_view(['GET', 'POST', 'DELETE'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def query_params_mgmt(request, format=None):
    """
    Manage "Query Parameters"

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


 # use the following json in order to add new query parameters
 # {
 #   "description" : "My Mediterranean Capitals Research",
	# "sources": "Twitter",
	# "location": "Athens",
	# "start_date": "1-1-2010",
	# "end_date": "1-1-2012",
	# "inference": true,
 #    "questions": true
 #    }

    if request.method == 'POST':
        print "create query_params_mgmt "
        description = request.data['description']
        keywords = request.data['keywords']
        location = request.data['location']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        inference = request.data['inference']
        questions = request.data['questions']
        twitter = request.data['twitter']
        google = request.data['google']
        category = request.data['category']
        topic = request.data['topic']
        youtube = request.data['youtube']

        print category
        print topic
        print keywords

        new_params = add_query_params(description, keywords, location, start_date,
                                      end_date, inference, questions, twitter, google,youtube,
                                      category, topic)
        print 'new_params:'+ str(new_params)

        return Response(True, status=status.HTTP_200_OK)

    if request.method == 'GET':
        print "get get_all_query_params in view "
        all_params = get_all_query_params.delay()
        print all_params

        return Response(all_params.get(), status=status.HTTP_200_OK)


