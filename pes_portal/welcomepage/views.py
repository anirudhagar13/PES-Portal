from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils import timezone


# Create your views here.

@csrf_exempt
def newsfeed(request, template = "newsfeed.html"):
	events = Event.objects.all()
	clubs = Club.objects.all()
	integrity_problem = False
	clubid = None
	if request.method=="POST":
		dict = request.POST
		if not request.POST.get("email"):
			#login
			usn = dict["usn"];
			password = dict["password"];
			user = authenticate(username=usn, password=password)
			
			if user:
				request.session["usn"] = usn
				u = Signup.objects.get(usn=usn)
				clubid = (Signup.objects.get(usn=usn).club_id).club_id
				request.session["club_id"] = clubid
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"CLUBID":clubid,"LOGGED":u})
			else:
				NOT_SIGNED_UP = True
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"CLUBID":clubid,"LOGGED":None})
			
		else:
			#signup
			try:
				username = dict["username"]	
				usn = dict["usn"]	
				email = dict["email"]
				mobile = dict["mobile"]
				dept = dict["dept"]
				sem = int(dict["sem"])
				password1 = dict["password1"]
				user = User.objects.create_user(username=usn,password=password1)
				user.save()
				Signup.objects.create(name=username, usn=usn, dept=dept, phone=mobile, sem=sem)
			except IntegrityError as e:
				integrity_problem = True
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs})
				
	return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"CLUBID":clubid,"LOGGED":None})
	

def render_event(request, template="event.html"):
	#u = request.session["usn"]
	#c = request.session["club_id"]
	
	event_id = request.GET.get("event_id")
	event = Event.objects.get(event_id=event_id)
	
	return render(request, "welcomepage/event.html",{"event":event})
	
def render_club(request):
	#u = request.session["usn"]
	#c = request.session["club_id"]
	
	clubid = request.GET.get("club_id")
	club = Club.objects.get(club_id=clubid)
	nowtime = timezone.now
	upcomingevents = Event.objects.get(club_id=clubid)
	recentevents = Event.objects.get(club_id=clubid)
	return render(request, "welcomepage/club.html",{"club":club,"upcomingevents":upcomingevents,"recentevents":recentevents})
