from django.conf.urls import patterns, include,url


urlpatterns = [
    # social urls
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^edit-profile$', 'clouddj.social_views.edit_profile', name='edit-profile'),
    url(r'^profile/(?P<id>\w+)$', 'clouddj.social_views.profile', name="profile"),
    url(r'^follow/(?P<id>\w+)$', 'clouddj.social_views.follow', name="follow"),
    url(r'^register$', 'clouddj.social_views.register', name='register'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        'clouddj.social_views.confirm_registration', name='confirm'),
    url(r'^$', 'clouddj.social_views.home', name='home'),
    url(r'^search$', 'clouddj.social_views.search', name='search'),
    url(r'^stream$', 'clouddj.social_views.stream', name='stream'),
    url(r'^explore$', 'clouddj.social_views.explore', name='explore'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/clouddj/accounts/password_reset/mailed/'}, name="password_reset"),
    url(r'^accounts/password_reset/mailed/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': 'accounts/password_reset/complete/'}),
    url(r'^accounts/password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm', name="password_reset_confirm"),
    url(r'^password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete', name="password_reset_complete"),

    url(r'^add-comment/(?P<id>\d+)$', 'clouddj.social_views.add_comment', name='add_comment'),
    url(r'^rate/(?P<id>\d+)$', 'clouddj.social_views.rate', name='rate'),
    url(r'^post_photo/(?P<id>\d+)$', 'clouddj.social_views.get_post_photo', name='post_photo'),
    url(r'^add-post/(?P<id>\d+)$', 'clouddj.social_views.add_post', name='add_post'),
    url(r'^delete-post/(?P<id>\d+)$', 'clouddj.social_views.delete_post', name='delete_post'),
    url(r'^like/(?P<id>\d+)$', 'clouddj.social_views.like', name='like'),

    # competition urls
    url(r'^create-competition$', 'clouddj.social_views.create_competition', name='create_competition'),
    url(r'^edit-competition/(?P<id>\d+)$', 'clouddj.social_views.edit_competition', name='edit_competition'),
    url(r'^competition/(?P<id>\d+)$', 'clouddj.social_views.competition', name='competition'),
    url(r'^join-competition/(?P<id>\d+)$', 'clouddj.social_views.join_competition', name='join_competition'),
    url(r'^list-competitions$', 'clouddj.social_views.list_competitions', name='list_competitions'),

    # music urls
    url(r'^studio/(?P<proj_id>\d+)/$', 'clouddj.music_views.studio', name='studio'),
    url(r'^studio$', 'clouddj.music_views.studio', name='studio'),
    url(r'^upload$', 'clouddj.music_views.upload', name='upload'),
    url(r'^song/(?P<id>\d+)/$', 'clouddj.music_views.get_song', name='get_song'),
    url(r'^fade_out/(?P<song_id>\d+)/$', 'clouddj.music_views.fade_out', name='fade_out'),
    url(r'^fade_in/(?P<song_id>\d+)/$', 'clouddj.music_views.fade_in', name='fade_in'),
    url(r'^slice/(?P<song_id>\d+)/$', 'clouddj.music_views.slice', name='slice'),
    url(r'^repeat/(?P<song_id>\d+)/$', 'clouddj.music_views.repeat', name='repeat'),
    url(r'^echo/(?P<song_id>\d+)/$', 'clouddj.music_views.echo', name='echo'),
    url(r'^reverse/(?P<song_id>\d+)/$', 'clouddj.music_views.reverse', name='reverse'),
    url(r'^amplify/(?P<song_id>\d+)/$', 'clouddj.music_views.amplify', name='amplify'),
    url(r'^tempo/(?P<song_id>\d+)/$', 'clouddj.music_views.tempo', name='tempo'),
    url(r'^filter/(?P<song_id>\d+)/$', 'clouddj.music_views.x_filter', name='filter'),
    url(r'^bass/(?P<song_id>\d+)/$', 'clouddj.music_views.bass', name='bass'),
    url(r'^treble/(?P<song_id>\d+)/$', 'clouddj.music_views.treble', name='treble'),
    url(r'^undo/(?P<song_id>\d+)/$', 'clouddj.music_views.undo', name='undo'),
    url(r'^save/(?P<song_id>\d+)/$', 'clouddj.music_views.save_song', name='save_song'),
    url(r'^undo_all/(?P<song_id>\d+)/$', 'clouddj.music_views.undo_all', name='undo_all'),
    url(r'^delete/(?P<song_id>\d+)/$', 'clouddj.music_views.delete', name='delete'),
    url(r'^record/(?P<song_id>\d+)/$', 'clouddj.music_views.record', name='record'),
    url(r'^speed/(?P<song_id>\d+)/$', 'clouddj.music_views.speed', name='speed'),   

]
