from adwords_client import RestClient

from itdtool.celeryapp import app


@app.task
def get_keywords_volume(adwords_username, adwords_password, keywd, loc_name ):
    # client = RestClient("login", "password")

    print "keyword:" + str(keywd)
    print "loc_name:" + str(loc_name)
    print "adwords_username:" + str(adwords_username)
    print "adwords_password:" + str(adwords_password)

    client = RestClient(adwords_username, adwords_password)

    keywords_list = [
        dict(
            language="en",
            loc_name_canonical=loc_name,
            key=keywd
        ),
        # dict(
        #     language="en",
        #     loc_id=2840,
        #     key="assange"
        # ),
        # dict(
        #     language="en",
        #     loc_name_canonical="United States",
        #     key="whistleblower"
        # )
    ]
    #
    response = client.post("/v2/kwrd_sv", dict(data=keywords_list))
    if response["status"] == "error":
        print("error. Code: %d Message: %s" % (response["error"]["code"], response["error"]["message"]))
    else:
        print(response["results"])
    # response = 'foo'

    return response


