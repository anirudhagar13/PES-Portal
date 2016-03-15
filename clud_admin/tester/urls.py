from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.event, name='event'),
	url(r'^event/.*', views.show, name='show'),
	url(r'^register/.*', views.reg, name='reg'),
	url(r'^oneclick/.*', views.one_click_reg, name='one_click_reg'),
]