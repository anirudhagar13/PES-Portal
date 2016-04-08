from django.shortcuts import render
from tester.models import *
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
from django.core.mail import send_mail
from django.conf import settings
from django.template.defaulttags import register

# Create your views here.

'''
This function renders the newsfeed page
It manages the signup, login, logout functionality and sets appropriate session variables
'''
@csrf_exempt
def render_newsfeed(request):
	# set data to be sent to templates
	try:
		usn = request.session["usn"]
		clubid = request.session["club_id"]
	except:
		usn = None
		club_id = None
	try:
		user = Signup.objects.get(usn=usn)
	except:
		user = None
	
	events = Event.objects.all()
	clubs = Club.objects.all()
	
	if request.method=="POST":
		dict = request.POST
		if dict.get("logout"):
			#logout
			request.session["usn"] = None
			request.session["club_id"] = None
			user = None
		
		#signup form contains email field
		elif dict.get("email"):		
			#signup
			try:
				username = dict["username"]	
				usn = dict["usn"]	
				email = dict["email"]
				mobile = dict["mobile"]
				dept = dict["dept"]
				sem = int(dict["sem"])
				password1 = dict["password1"]
				#two entries are made:  One in Django User table for authentication purpose
				#						Other in Signup table of our DB for recording user data
				new_user = User.objects.create_user(username=usn,password=password1)
				new_user.save()
				Signup.objects.create(name=username, email=email, usn=usn, dept=dept, phone=mobile, sem=sem)		
			except IntegrityError as e:
				#user exists
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"INTEGRITY_ERROR":True})
		elif dict.get("userusn"):
			#lost password
			usn = dict["userusn"]
			try:
				if Signup.objects.get(usn=usn):
					msg = "You can reset your password here \n" + "http://localhost:8000/welcomepage/reset"
					subject = "PES Times Password sent"
					f_mail = settings.EMAIL_HOST_USER
					s_mail = [Signup.objects.get(usn=usn).email]
					send_mail(subject, msg , f_mail , s_mail, fail_silently=False)
					return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"MAIL_SENT":True})
			except:
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"NO_USER":True})
				
		else:
			#login
			usn = dict["usn"];
			password = dict["password"];
			log_user = authenticate(username=usn, password=password)
				
			if log_user:
				request.session["usn"] = usn
				user = Signup.objects.get(usn=usn)
				try:
					clubid = (Signup.objects.get(usn=usn).club_id).club_id
				except:
					clubid = None
				request.session["club_id"] = clubid
			else:
				#user not signed up
				return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"PROBLEM_LOGGING":True})
		
	try:
		return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"CLUBID":request.session["club_id"],
	"LOGGED":user, "PROBLEM_LOGGING": False})
	except:
		return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs,"CLUBID":None,
	"LOGGED":user, "PROBLEM_LOGGING": False})
'''
This function renders the Event page
'''
def render_event(request, template="event.html"):
	try:
		usn = request.session["usn"]
		admin_club = request.session["club_id"]
	except:
		usn = None
		admin_club = None
		
	event_id = request.GET.get("event_id")
	event = Event.objects.get(event_id=event_id)
	comments = Comments.objects.filter(event_id=event_id)
	names = list()
	for each_comment in comments:
		names.append((Signup.objects.get(usn=each_comment.usn)).name)
	comment_list = list()
	for i in range(len(names)):
		comment_list.append({"name":names[i],"comments":comments[i]})
	if usn:
		isLoggedIn = 'true'
	else:
		isLoggedIn = 'false'
	print comment_list
	return render(request, "welcomepage/event.html",{"event":event,"isLoggedIn":isLoggedIn,"comment_list":comment_list})

def render_reset(request):
	events = Event.objects.all()
	clubs = Club.objects.all()
	
	if request.method == "POST":
		dict = request.POST
		#Reset password
		usn = dict["usn"]
		password = dict["newpassword1"]
		try:
			user = User.objects.get(username=usn)
			user.set_password(password)
			user.save()
			return redirect("/welcomepage/newsfeed")
		except:
			return render(request, "welcomepage/reset.html", {"events":events,"clubs":clubs,"NO_USER":True})
	return render(request, "welcomepage/reset.html",{"events":events,"clubs":clubs})

#Takes care of One tap login
@csrf_exempt
def register_one_tap(request):

	#user is logged in for sure, no need to check for exceptions
	usn = request.session["usn"]
	user = Signup.objects.get(usn=usn)
	
	if request.method == "POST":
		parameters = request.POST
		eventid = parameters.get('eventid')
		clubid = parameters.get("clubid")
		new_registration = Register(club_id=clubid,event_id=eventid,usn=usn,name=user.name,email=user.email,phone=user.phone,dept=user.dept,sem=user.sem)
		try:
			new_registration.save()
			return HttpResponse("Congrats, you have been registered!")
		except:
			return HttpResponse("Sorry, cannot register again!")


#Saves comments of users
@csrf_exempt
def add_comment(request):
	#user is logged in for sure, no need to check for exceptions
	usn = request.session["usn"]
	user = Signup.objects.get(usn=usn)
	if request.method == "POST":
		parameters = request.POST
		eventid = parameters.get('eventid')
		comment = parameters.get('comment')
		new_comment = Comments(usn=usn,event_id=eventid,comment=comment,creat_date=timezone.now())
		try:
			new_comment.save()			
			return HttpResponse((Signup.objects.get(usn=usn)).name)
		except:
			return HttpResponse("Oops! Something is wrong!")

@register.filter
def get_item_value(dictionary,key):
	return dictionary.get(key)