from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from rest.views import views_gtrends, views_queryparams, views_twitter, views_combined, views_adwords



urlpatterns = [

    #################################################
    # basic configuration
    #################################################

    # integrated query
    url(r'^integrated/$', views_combined.get_combined),

    # adwords
    url(r'^google-adwords/(?P<keywd>[a-zA-Z0-9_]+)/location/(?P<loc_name>[a-zA-Z0-9_]+)$', views_adwords.keywords_volume),

    # twitter
    url(r'^twitter-trends/(?P<place_id>[a-zA-Z0-9_]+)/$', views_twitter.get_trends_location),

    # google trends
    url(r'^gtrends-region/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.over_region),
    url(r'^gtrends-time/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.over_time),
    url(r'^gtrends-time-list/k1/(?P<keyword1>[a-zA-Z0-9_]+)/k2/(?P<keyword2>[a-zA-Z0-9_]+)$',
        views_gtrends.over_time_list),
    url(r'^gtrends-keywords/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.related_kws),
    # url(r'^google-cat-suggestions/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.cat_suggestions),
    url(r'^google-related-queries/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.related_queries),

    # query params
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
