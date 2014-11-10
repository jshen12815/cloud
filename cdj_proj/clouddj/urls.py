from django.conf.urls import url


urlpatterns = [
    #social urls
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^register$', 'django.contrib.auth.views.login', name='register'),
    url(r'^$', 'clouddj.social_views.home', name='home'),
    url(r'^search$', 'django.contrib.auth.views.login', name='search'),
    url(r'^stream$', 'clouddj.social_views.stream', name='stream'),

    #music urls
    url(r'^upload$', 'clouddj.music_views.upload', name='upload'),
    url(r'^song/(?P<id>\d+)/$', 'clouddj.music_views.get_song', name='get_song'),
    url(r'^amplify/(?P<id>\d+)/$', 'clouddj.music_views.amplify', name='amplify'),
]
