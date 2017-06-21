# from __future__ import absolute_import
#
# from itdtool.celeryapp import app
# # from lxml import etree
# # import xmltodict
# import sys
# # from passlib.hash import md5_crypt
# from django.conf import settings
#
#
#
# # @app.task
# def get_query_params_id(id):
#
#     from itdtool.models import QueryParameters
#     query_parameters = QueryParameters.objects.filter(id=id)
#     # print "get_query_params_id "+ str(id)
#     # print "result " + str(query_parameters)
#     for query_parameter in query_parameters:
#         result = {
#             "id": query_parameter.id,
#             "description": query_parameter.description,
#             "sources": query_parameter.sources,
#             "location": query_parameter.location,
#             "start_date": query_parameter.start_date,
#             "end_date": query_parameter.end_date,
#             "inference": query_parameter.inference,
#             "questions": query_parameter.questions
#         }
#
#
#     # print("retrieve query_parameter by id" + str(result))
#
#     return result
#
#
# # @app.task
# def delete_query_params_id(id):
#
#     query_deleted = QueryParameters.objects.filter(id=id)[0]
#     res = query_deleted.delete()
#
#     return res
#
#
# # @app.task
# def add_query_params(description, sources, location, start_date, end_date, inference, questions):
#
#     # description = models.TextField()
#     # sources = models.CharField(max_length=30) #["Twitter", "Google", "Youtube"]
#     # location = models.CharField(max_length=30)  # ["Athens", "Rome", "Madrid"]
#     # start_date = models.DateTimeField()  # starting time period to search
#     # end_date = models.DateTimeField()  # ending time period to search
#     # inference = models.BooleanField()
#     # questions = models.BooleanField()
#
#     query_parameters = QueryParameters(description=description, sources=sources,location=location,
#                                        start_date=start_date, end_date=end_date, inference=inference,
#                                        questions=questions)
#     query_parameters.save()
#     print "saved:" + str(query_parameters)
#
#     return query_parameters
#
#
# # @app.task
# def get_all_query_params():
#
#     query_parameters_all = QueryParameters.objects.all()
#     print query_parameters_all
#     results = []
#
#     for query_parameter in query_parameters_all:
#         print("retrieve all query_parameter " + str(query_parameter))
#         d = {"id": query_parameter.id,
#             "description": query_parameter.description,
#              "sources": query_parameter.sources,
#              "location": query_parameter.location,
#              "start_date": query_parameter.start_date,
#              "end_date": query_parameter.end_date,
#              "inference": query_parameter.inference,
#              "questions": query_parameter.questions}
#         results.append(d)
#     return results
#
