from __future__ import division
# import json
# import numpy as np
# import xlrd
# from neupy import algorithms, environment
# import math
import sys
import re
# import tweepy
import facepp
from facepp import API, File
import genderize
from genderize import Genderize
import string
from django.conf import settings


FACE_API_KEY = settings.FACE_API_KEY
FACE_API_SECRET = settings.FACE_API_SECRET
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

faceplusplus_api = API(FACE_API_KEY, FACE_API_SECRET, srv=api_server_international)

# Genderize Authentication
GENDERIZE_API_KEY = settings.GENDERIZE_API_KEY

# Face++ Detect API
def faceplusplus(image_url):
    if image_url == 'https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png':
        return 'unknown'
    try:
        res = faceplusplus_api.detect(image_url=image_url, return_attributes='gender')
        faces = res['faces']
        if not faces:
            return 'unknown'
        else:
            has_male = False
            has_female = False
            for face in faces:
                gender = face['attributes']['gender']['value']
                if gender == 'Male':
                    has_male = True
                else:
                    has_female = True
            if has_male and has_female:
                return 'unknown'
            elif has_male:
                return 'male'
            else:
                return 'female'
    except facepp.APIError as w:
        print w
        return 'error'
    except KeyError:
        print res
        return 'error'




# Genderize API
def genderize_function(name):
    # lowercase
    name = name.lower()
    regex = re.compile('[^a-z ]')
    # removal of all non-letters
    name = regex.sub('', name)
    # names = name.split()
    names = name.split()
    # print names

    try:
        for x in names:
            gen = Genderize(api_key=GENDERIZE_API_KEY).get([x])
            # print gen
            if gen[0]['gender'] != None:
                return (gen[0]['gender'], gen[0]['count'], gen[0]['probability'])
        return ('unknown', 'unknown', 'unknown')
    except genderize.GenderizeException:
        pass
        # book.save("liu_f_g1.xls")


# utility function to convert image to higher resolution
def hq_image(image_url):
    return string.replace(image_url, 'normal', '400x400')




# limit handler for Tweepy
# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             print 'Rate Limit Error'
#             time.sleep(15 * 60)
#         except tweepy.error.TweepError:
#             break





def predict_gender_average(tw_users_list):

    average_result = {}
    gendel_list_prob = []
    total_tweets_len = len(tw_users_list)
    print "total_tweets_len:::::::"
    print total_tweets_len

    for key  in tw_users_list:
        genderize_gender = "unknown"
        genderize_count = 0
        genderize_probability = 0.0
        val = tw_users_list[key]

        # ans = tweepy_function(x)
        # print "name, image url, color are: " + str(val)
        # print ans
        if val:
            # (name, image_url, theme_color) = ans
            name = val[0].encode('utf-8')
            image_url = val[1].encode('utf-8')
            print "----start-----"
            print "name " + str(name)
            # call Genderize based on name
            # (genderize_gender, genderize_count, genderize_probability) = genderize_function(name)

            try:
                (genderize_gender, genderize_count, genderize_probability) = genderize_function(name)
            except:
                print "!!!!Exception on Genderize utilisation"
                pass

            print genderize_gender, genderize_count, genderize_probability

            if genderize_gender != "unknown" and genderize_probability >= 0.7 and genderize_count >= 20:
                res = {'id': key,'name': name, 'gender': genderize_gender, 'probability': genderize_probability, 'inf': 'genderize'}
                gendel_list_prob.append(res)

            if genderize_gender == "unknown" or genderize_probability < 0.7 or genderize_count < 20:
                print "Calling Face++"
                print "image_url " + str(image_url)
                facepp_gender = faceplusplus(image_url)
                print facepp_gender
                if facepp_gender:
                    res = {'id': key, 'name': name, 'gender': facepp_gender, 'probability': 0.7, 'inf':'facepp'}
                    gendel_list_prob.append(res)



    print "--- finished"
    print gendel_list_prob
    total = len(gendel_list_prob)
    total_male, total_female, total_unk = 0, 0, 0
    total_probabilty_male, total_probabilty_female = 0.0, 0.0

    male_av, female_av, unk_av = 0.0, 0.0, 0.0
    male_conf, female_conf = 0.0, 0.0

    print total
    for entry in gendel_list_prob:
        print entry
        print entry['gender']

        if entry['gender'] == 'unknown':
            total_unk += 1
        if entry['gender'] == 'male':
            print "total_male"
            total_male += 1
            probabilty_male = entry['probability']
            print probabilty_male
            total_probabilty_male = total_probabilty_male + probabilty_male
            print total_probabilty_male

        if entry['gender'] == 'female':
            total_female += 1
            probabilty_female = entry['probability']
            total_probabilty_female = total_probabilty_female + probabilty_female
            print total_probabilty_female

    print "------------------"
    print "total_male:"+str(total_male)+",total_female:"+str(total_female)+", total_unk:"+str(total_unk)
    if total > 0:
        male_av = total_male / total
        female_av = total_female / total
        unk_av = total_unk / total

    if total_male > 0:
        male_conf = total_probabilty_male/total_male

    if total_female > 0:
        female_conf = total_probabilty_female / total_female

    result = {'male': format(male_av, '.2f'), 'female': format(female_av, '.2f'), 'unknown': format(unk_av, '.2f'),
              'male_conf': format(male_conf, '.2f'), 'female_conf': format(female_conf, '.2f'),
              'total_records': total_tweets_len}

    return result

