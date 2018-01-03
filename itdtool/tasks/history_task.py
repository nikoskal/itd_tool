from __future__ import absolute_import

from itdtool.celeryapp import app

from itdtool import account_repo



@app.task
def get_history(id):

    print id
    result = "ffooo"

    return result
