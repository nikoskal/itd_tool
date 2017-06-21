from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from rest.views import views_gtrends, views_queryparams, views_twitter, views_combined



urlpatterns = [

    #################################################
    # basic configuration
    #################################################

    url(r'^combined/$', views_combined.get_combined),
    url(r'^twitter-trends/(?P<place_id>[a-zA-Z0-9_]+)/$', views_twitter.get_trends_location),
    url(r'^google-trends/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.related_kws),
    url(r'^google-cat-suggestions/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.cat_suggestions),
    url(r'^google-related-queries/(?P<keyword>[a-zA-Z0-9_]+)/$', views_gtrends.related_queries),
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
