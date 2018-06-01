from __future__ import absolute_import

from itdtool.celeryapp import app


@app.task
def get_query_params_id(id):
    from itdtool.models import QueryParameters
    query_parameters = QueryParameters.objects.filter(id=id)
    # print "get_query_params_id "+ str(id)
    # print "result " + str(query_parameters)
    result = {
        "id": "",
        "description": "",
        "keywords": "",
        "google": "",
        "twitter": "",
        "youtube": "",
        "location": "",
        "start_date": "",
        "end_date": "",
        "inference": "",
        "questions": "",
        "category": "",
        "topic": "",
        "authid": ""
    }

    for query_parameter in query_parameters:
        result = {
            "id": query_parameter.id,
            "description": query_parameter.description,
            "keywords": query_parameter.keywords,
            "location": query_parameter.location,
            "start_date": query_parameter.start_date,
            "end_date": query_parameter.end_date,
            "inference": query_parameter.inference,
            "questions": query_parameter.questions,
            "google": query_parameter.google,
            "twitter":query_parameter.twitter,
            "youtube": query_parameter.youtube,
            "category": query_parameter.category,
            "topic": query_parameter.topic,
            "authid": query_parameter.authid
        }


    # print("retrieve query_parameter by id" + str(result))
    return result


@app.task
def delete_query_params_id(id):
    from itdtool.models import QueryParameters
    query_deleted = QueryParameters.objects.filter(id=id)[0]
    res = query_deleted.delete()

    return res


@app.task
def add_query_params(description, keywords, location, start_date, end_date, inference, questions,twitter, google,youtube,
                     category, topic, authid):
    from itdtool.models import QueryParameters
    # description = models.TextField()
    # sources = models.CharField(max_length=30) #["Twitter", "Google", "Youtube"]
    # location = models.CharField(max_length=30)  # ["Athens", "Rome", "Madrid"]
    # start_date = models.DateTimeField()  # starting time period to search
    # end_date = models.DateTimeField()  # ending time period to search
    # inference = models.BooleanField()
    # questions = models.BooleanField()

    query_parameters = QueryParameters(description=description, keywords=keywords, location=location,
                                       start_date=start_date, end_date=end_date, inference=inference,
                                       questions=questions,twitter=twitter, google=google,youtube=youtube,
                                       category=category,
                                       topic=topic, authid=authid)
    query_parameters.save()
    print "saved:" + str(query_parameters)

    return query_parameters


@app.task
def get_all_query_params():
    from itdtool.models import QueryParameters

    query_parameters_all_rev = QueryParameters.objects.all()
    # print query_parameters_all
    query_parameters_all = list(reversed(query_parameters_all_rev))
    results = []
    # print "saved:" + str(query_parameters)

    for query_parameter in query_parameters_all:
        print("retrieve all query_parameter " + str(query_parameter))
        d = {"id": query_parameter.id,
            "description": query_parameter.description,
             "keywords": query_parameter.keywords,
             "location": query_parameter.location,
             "start_date": query_parameter.start_date,
             "end_date": query_parameter.end_date,
             "inference": query_parameter.inference,
             "questions": query_parameter.questions,
             "google": query_parameter.google,
             "twitter":query_parameter.twitter,
             "youtube": query_parameter.youtube,
             "category": query_parameter.category,
             "topic": query_parameter.topic,
             "authid": query_parameter.authid
             }
        results.append(d)
    return results


@app.task
def get_all_query_params_authid(authid):
    from itdtool.models import QueryParameters

    query_parameters_all_rev = QueryParameters.objects.filter(authid=authid)
    # print query_parameters_all
    query_parameters_all = list(reversed(query_parameters_all_rev))
    results = []
    print "saved:" + str(query_parameters_all)

    for query_parameter in query_parameters_all:
        print("retrieve all query_parameter " + str(query_parameter))
        d = {"id": query_parameter.id,
            "description": query_parameter.description,
             "keywords": query_parameter.keywords,
             "location": query_parameter.location,
             "start_date": query_parameter.start_date,
             "end_date": query_parameter.end_date,
             "inference": query_parameter.inference,
             "questions": query_parameter.questions,
             "google": query_parameter.google,
             "twitter":query_parameter.twitter,
             "youtube": query_parameter.youtube,
             "category": query_parameter.category,
             "topic": query_parameter.topic,
             "authid": query_parameter.authid
             }
        results.append(d)
    return results

