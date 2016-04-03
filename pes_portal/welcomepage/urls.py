from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^newsfeed', views.render_newsfeed, name='newsfeed'),
	url(r'^event/', views.render_event, name='event'),
	url(r'^reset/$', views.render_reset, name='reset'),
]