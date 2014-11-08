from django.conf.urls import url

urlpatterns = [
    #social urls
    url(r'^$', 'clouddj.social_views.home', name='home'),

    #music urls
    url(r'^upload$', 'clouddj.music_views.upload', name='upload')

]
