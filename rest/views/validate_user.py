from django.conf import settings


def valid_user(user, ls_name):
    """
    " check if user is allowed to configure the logical system defined by ls_name
    """

    print "@@@@@@ user:" + str(user)
    print "@@@@@@ ls_name:" + str(ls_name)
    user_domain = user.last_name
    user_domain_ = user_domain.replace(".", "_")

    if user_domain_ in ls_name:
        return True
    else:
        return False
