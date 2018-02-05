from __future__ import absolute_import

from itdtool.celeryapp import app
from itdtool.models import HistoryModel
import json
import operator


@app.task
def get_all_history_user(user_id):
    history_objects = HistoryModel.objects.filter(user_id=user_id)
    # print "get_query_params_id "+ str(id)
    # print "result " + str(query_parameters)
    all_results = []
    for history in history_objects:
        one_result = {
            "id": history.id,
            "query_desc": history.query_desc,
            "query_id": history.query_id,
            "user_name": history.user_name,
            "execution_date": history.execution_date,
            "results": history.results,
            "keyword": history.keyword
        }
        all_results.append(one_result)

    ordered = sorted(all_results, key=operator.attrgetter('execution_date'))
    print "ordered " + str(ordered)

    reverse_ordered = list(reversed(ordered))
    print "reversed ordered " + str(reverse_ordered)

    return reverse_ordered


@app.task
def get_history_item(id):

    history_objects = HistoryModel.objects.filter(id=id)
    # print "get_query_params_id "+ str(id)
    # print "result " + str(query_parameters)
    one_result = {}
    for history in history_objects:
        json_results = json.loads(history.results)
        print 'json_results'
        print json_results

        one_result = {
            "id": history.id,
            "query_desc": history.query_desc,
            "query_id": history.query_id,
            "user_name": history.user_name,
            "execution_date": history.execution_date,
            "results": json_results,
            "keyword": history.keyword
        }

    return one_result


@app.task
def delete_history(id):
    print "delete history item "+ str(id)
    try:
        history_deleted = HistoryModel.objects.filter(id=id)[0]
        res = history_deleted.delete()
        print "deleted"
        print res
        res = True
    except IndexError:
        res = False

    return res


@app.task
def add_history(query_id, keyword, query_desc, user_name, results):

    print "saved user_name:" + str(user_name)
    print "saved query_id:" + str(query_id)
    print "saved results:" + str(results)

    history_parameters = HistoryModel(keyword=keyword, query_id=query_id, user_name=user_name, results=results,
                                      query_desc=query_desc)
    history_parameters.save()
    print "saved:"
    print "done:"
    # return history_parameters


@app.task
def get_all_history():

    history_all = HistoryModel.objects.all()
    reverse_ordered = list(reversed(history_all))
    results = []

    for history in reverse_ordered:
        print("retrieve all history: " + str(history))
        one_result = {
            "id": history.id,
            "query_desc": history.query_desc,
            "query_id": history.query_id,
            "user_name": history.user_name,
            "execution_date": history.execution_date,
            "results": history.results,
            "keyword": history.keyword
        }
        results.append(one_result)

    return results