from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from rest.views import views_gtrends, views_queryparams, views_twitter, views_combined, views_adwords, views_history


urlpatterns = [

    #################################################
    # basic configuration
    #################################################

    # history
    url(r'^history_authid/(?P<authid>[a-zA-Z0-9_%]+)/$', views_history.history_authid),
    url(r'^history/$', views_history.history),
    url(r'^history/(?P<history_id>[0-9_]+)/$', views_history.history_id),
    url(r'^history_export/(?P<history_id>[0-9_]+)/$', views_history.history_export_id),
    url(r'^discover_test/(?P<queryid>[0-9_]+)$', views_combined.discover_test),
    url(r'^discover_gender_test/(?P<keyword>[a-zA-Z0-9_ ]+)$', views_combined.discover_test_gender),
    # url(r'^sentiment_test/(?P<keyword>[a-zA-Z0-9_]+)$', views_combined.sentiment_test),

    # integrated query
    url(r'^discover/(?P<queryid>[0-9_]+)$', views_combined.discover),

    # adwords
    url(r'^google-adwords/(?P<keywd>[a-zA-Z0-9_ ]+)/location/(?P<loc_name>[a-zA-Z0-9_]+)$', views_adwords.keywords_volume),

    # twitter
    # url(r'^twitter-trends-location/(?P<place_id>[a-zA-Z0-9_]+)/$', views_twitter.get_trends_location),
    # url(r'^twitter-tweets-term/(?P<term>[a-zA-Z0-9_]+)/$', views_twitter.get_tweets_term),

    # autocomplete
    url(r'^autocomplete/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.autocomplete),

    # google trends
    # url(r'^gtrends-region/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.over_region),
    # url(r'^gtrends-time/(?P<keyword>[a-zA-Z0-9_]+)/location/(?P<location>[a-zA-Z0-9_]+)$', views_gtrends.over_time),
    # url(r'^gtrends-time-list/k1/(?P<keyword1>[a-zA-Z0-9_]+)/k2/(?P<keyword2>[a-zA-Z0-9_]+)$',
    #     views_gtrends.over_time_list),
    url(r'^gtrends-keyword-topic/(?P<keyword>[a-zA-Z0-9_ ]+)/$', views_gtrends.cat_suggestions),
    # url(r'^google-cat-suggestions/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.cat_suggestions),
    # url(r'^google-related-queries/(?P<keyword>[a-zA-Z0-9_%]+)/location/(?P<location>[a-zA-Z0-9_]+)/category/(?P<category>[a-zA-Z0-9_]+)$',
    #     views_gtrends.related_queries),
    # test gtrends calls

    url(r'^gtrends/(?P<keyword>[a-zA-Z0-9_%]+)/location/(?P<location>[a-zA-Z]+)/category/(?P<category>[a-zA-Z0-9_]+)$', views_gtrends.gtrends),
    # url(r'^gtrends-tests/$', views_gtrends.test),

    # query params
    url(r'^query_parameters_authid/(?P<authid>[a-zA-Z0-9_%]+)/$', views_queryparams.query_params_mgmt_authid),
    url(r'^query_parameters_authid/(?P<authid>[a-zA-Z0-9_%]+)/id/(?P<id>[0-9]+)$', views_queryparams.query_params_mgmt_authid_id),

    url(r'^query-parameters/$', views_queryparams.query_params_mgmt),
    url(r'^query-parameters/(?P<id>[0-9]+)/$', views_queryparams.query_params_mgmt_id),



    # GET /user
    # url(r'^user/$', views_user_mgmt.user),
    # DELETE ,GET /user/:username
    # url(r'^user/(?P<username>[a-zA-Z0-9.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views_user_mgmt.username_mgmt),


]
urlpatterns += [
   url(r'^api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
]

urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token),
    # url(r'^token/', views_auth.user_token),

]
urlpatterns = format_suffix_patterns(urlpatterns)
