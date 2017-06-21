# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from itdtool.tasks.history_task import retrieve_actions_ls, retrieve_actions_name, retrieve_actions_ls_name, \
#     retrieve_actions_date
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
# from rest_framework import status
# from validate_ip import valid_ip
# from validate_user import valid_user
#
#
# @api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def history_ls(request, lsname, format=None):
#     """
#     get all user actions on specified LS
#     """
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     try:
#         service_user = User.objects.get(username=request.user)
#     except User.DoesNotExist:
#         # service_user = None
#         return Response("unknown user:"+request.user, status=status.HTTP_400_BAD_REQUEST)
#
#     if valid_user(service_user, lsname) is False:
#         return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#                         status=status.HTTP_401_UNAUTHORIZED)
#
#     print("retrieve all actions view")
#     actions_list = []
#     if request.method == 'GET':
#         actions_list = retrieve_actions_ls.delay(lsname)
#
#     return Response(actions_list.get())
#
#
# @api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def history_ls_name(request, lsname, username, format=None):
#     """
#     get all user actions on specified LS for specified user
#     """
#     actions_list = []
#
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#     try:
#         service_user = User.objects.get(username=request.user)
#     except User.DoesNotExist:
#         # service_user = None
#         return Response("unknown user:"+request.user, status=status.HTTP_400_BAD_REQUEST)
#
#     if valid_user(service_user, lsname) is False:
#         return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#                         status=status.HTTP_401_UNAUTHORIZED)
#
#     if request.method == 'GET':
#         actions_list = retrieve_actions_ls_name.delay(lsname, username)
#
#     return Response(actions_list.get())
#
#
# @api_view(['GET'])
# @authentication_classes((TokenAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def history_ls_name_date(request, lsname, username, start, end, format=None):
#     """
#     get all user actions on specified LS for specified user for the spec time period
#     input date with 3 comma digits, indicating year,month,day e.g.
#
#     """
#     ip_address = request.META['REMOTE_ADDR']
#     if valid_ip(ip_address) is False:
#         return Response("Not authorised client IP", status=status.HTTP_401_UNAUTHORIZED)
#
#     try:
#         service_user = User.objects.get(username=request.user)
#     except User.DoesNotExist:
#         # service_user = None
#         return Response("unknown user:"+request.user, status=status.HTTP_400_BAD_REQUEST)
#
#     if valid_user(service_user, lsname) is False:
#         return Response("User:"+str(service_user)+" is not authorised to manage LS:"+str(lsname),
#                         status=status.HTTP_401_UNAUTHORIZED)
#
#     actions_list = []
#     if request.method == 'GET':
#         actions_list = retrieve_actions_date.delay(username, lsname, start, end)
#     return Response(actions_list.get())
