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
    url(r'^fade_out/(?P<song_id>\d+)/$', 'clouddj.music_views.fade_out', name='fade_out'),
    url(r'^fade_in/(?P<song_id>\d+)/$', 'clouddj.music_views.fade_in', name='fade_in'),
    url(r'^slice/(?P<song_id>\d+)/$', 'clouddj.music_views.slice', name='slice'),
    url(r'^repeat/(?P<song_id>\d+)/$', 'clouddj.music_views.repeat', name='repeat'),
    url(r'^reverse/(?P<song_id>\d+)/$', 'clouddj.music_views.reverse', name='reverse'),
    url(r'^amplify/(?P<song_id>\d+)/$', 'clouddj.music_views.amplify', name='amplify'),
    url(r'^speedup/(?P<song_id>\d+)/$', 'clouddj.music_views.speedup', name='speedup'),
    url(r'^filter/(?P<song_id>\d+)/$', 'clouddj.music_views.x_filter', name='filter'),
    url(r'^undo/(?P<song_id>\d+)/$', 'clouddj.music_views.undo', name='undo'),
    url(r'^save/(?P<song_id>\d+)/$', 'clouddj.music_views.save_song', name='save_song'),


]
