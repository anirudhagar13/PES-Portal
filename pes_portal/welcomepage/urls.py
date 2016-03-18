from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^newsfeed', views.newsfeed, name='newsfeed'),
	url(r'^event/', views.render_event, name='event'),
	url(r'^club/$', views.render_club, name='club'),
]