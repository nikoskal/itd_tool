from django.conf import settings
from tweepy import OAuthHandler


def get_google_username():
    try:
        google_username = settings.GOOGLE_USERNAME
    except AttributeError:
        print "No Google username is set, please set GOOGLE_USERNAME attribute in settings!!"
        return False

    return google_username


def get_google_password():
    try:
        google_password = settings.GOOGLE_PASSWORD
    except AttributeError:
        print "No Google username is set, please set GOOGLE_PASSWORD attribute in settings!!"
        return False

    return google_password


def get_twitter_auth():
    try:
        twitter_key = settings.TWITTER_KEY
        twitter_secret = settings.TWITTER_SECRET
        twitter_access_token = settings.TWITTER_ACCESS_TOKEN
        twitter_access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        auth = OAuthHandler(twitter_key, twitter_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    except AttributeError:
        print "No twitter keys are set, please set TWITTER_KEY parameters attribute in settings!!"
        return False

    return auth


def get_adwords_username():
    try:
        adwords_username = settings.ADWORDS_USERNAME
    except AttributeError:
        print "No Adwords username is set, please set ADWORDS_USERNAME attribute in settings!!"
        return False

    return adwords_username


def get_adwords_password():
    try:
        adwords_password = settings.ADWORDS_PASSWORD
    except AttributeError:
        print "No Adwords password is set, please set ADWORDS_PASSWORD attribute in settings!!"
        return False

    return adwords_password
