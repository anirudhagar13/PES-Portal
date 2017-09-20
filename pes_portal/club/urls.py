from django.conf.urls import include, url
from club import views
from club.models import *
from django.conf.urls.static import static

urlpatterns = [url(r'', views.clubname,),
]

'''
cname=club.objects.all()
for i in cname:								#generating urls for only those clubs which are present in db
	x = str(i.club_id)
	urlpatterns.append(url(r"^club/cl000"+ x +"/", views.clubname,))	#appending each club_name which are in db to list "urlpatterns"



eid=Event.objects.all()
for i in eid:								#generating urls for only those clubs which are present in db
	x = str(i.event_id)
	urlpatterns.append(url(r"^event/ev000"+ x +"/", views.event,))	#appending each club_name which are in db to list "urlpatterns"
'''