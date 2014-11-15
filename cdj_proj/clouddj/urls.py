from django.conf.urls import patterns, include,url


urlpatterns = [
    #social urls
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^register$', 'clouddj.social_views.register', name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        'clouddj.social_views.confirm_registration', name='confirm'),
    url(r'^$', 'clouddj.social_views.home', name='home'),
    url(r'^search$', 'clouddj.social_views.stream', name='search'),
    url(r'^stream$', 'clouddj.social_views.stream', name='stream'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/cdj_proj/accounts/password_reset/mailed/'}, name="password_reset"),
    url(r'^accounts/password_reset/mailed/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': 'accounts/password_reset/complete/'}),
    url(r'^accounts/password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm', name="password_reset_confirm"),
    url(r'^password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete', name="password_reset_complete"),

    url(r'^add-comment$', 'clouddj.social_views.add_comment', name='add_comment'),
    url(r'^rate/(?P<id>\d+)/$', 'clouddj.social_views.rate'),

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
    url(r'^record/(?P<song_id>\d+)/$', 'clouddj.music_views.record', name='record'),

]
