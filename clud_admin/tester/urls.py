from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^main/.*', views.main_admin, name='main_admin'),
	url(r'^click_prom/.*', views.click_prom, name='main_admin'),
	url(r'^create/.*', views.event, name='event'),
	url(r'^event/.*', views.show, name='show'),
	url(r'^register/.*', views.reg, name='reg'),
	url(r'^promote/.*', views.prom, name='reg'),
	url(r'^oneclick/.*', views.one_click_reg, name='one_click_reg'),
]