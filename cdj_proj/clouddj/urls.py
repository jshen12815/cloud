from django.conf.urls import url

urlpatterns = [
    #social urls
    url(r'^login$', '', name='login'),
    url(r'^register$', '', name='register'),
    url(r'^$', 'clouddj.social_views.home', name='home'),
    url(r'^search$', '', name='search'),
    url(r'^stream$', '', name='stream'),

    #music urls
    url(r'^upload$', 'clouddj.music_views.upload', name='upload')

]
