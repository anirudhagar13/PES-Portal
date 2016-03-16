from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.newsfeed, name='newsfeed'),
	url(r'^$', views.bootstrap, name='bootstrap'),
]