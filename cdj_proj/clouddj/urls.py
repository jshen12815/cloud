from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'clouddj.social_views.home', name='home'),
]
