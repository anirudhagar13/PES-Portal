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
def navbar_functions(request):
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
				dob = dict["dob"]
				#two entries are made:  One in Django User table for authentication purpose
				#						Other in Signup table of our DB for recording user data
				new_user = User.objects.create_user(username=usn,password=password1)
				new_user.save()
				Signup.objects.create(name=username, email=email, usn=usn, dept=dept, phone=mobile, sem=sem, dob=dob)		
			except IntegrityError as e:
				#user exists
				return {"INTEGRITY_ERROR":True}
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
					return {"MAIL_SENT":True}
			except:
				return {"NO_USER":True}
				
		elif dict.get("password"):
			#login
			usn = dict["usn"];
			password = dict["password"];
			log_user = authenticate(username=usn, password=password)
				
			if log_user:
				request.session["usn"] = usn
				user = Signup.objects.get(usn=usn)
				try:
					clubid = (Signup.objects.get(usn=usn).club_id)
					
				except:
					clubid = None
				request.session["club_id"] = clubid
			else:
				#user not signed up
				return {"PROBLEM_LOGGING":True}
		
	try:
		return {"CLUBID":request.session["club_id"],"LOGGED":user, "PROBLEM_LOGGING": False}
	except:
		return {"CLUBID":None,"LOGGED":user, "PROBLEM_LOGGING": False}

'''
This function renders the newsfeed page
It manages the signup, login, logout functionality and sets appropriate session variables
'''
@csrf_exempt
def render_newsfeed(request):
	# set data to be sent to templates

	events = Event.objects.all()
	clubs = Club.objects.all()
	
	navfunc = navbar_functions(request)
	newdict = navfunc.copy()
	newdict.update({"events":events,"clubs":clubs})
	return render(request, "welcomepage/newsfeed.html", newdict)
	
	
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
	
	clubs = Club.objects.all()
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
	#print comment_list
	navfunc = navbar_functions(request)
	newdict = navfunc.copy()
	newdict.update({"event":event,"isLoggedIn":isLoggedIn,"comment_list":comment_list,"clubs":clubs})
	return render(request, "welcomepage/event.html",newdict)

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
		required_fields = Event.objects.get(event_id=eventid,club_id=clubid).requirements
		required_fields = eval(required_fields)
		default_params = {"usn":usn,"name":"","email":"","phone":"","dept":"","sem":""}
		for required in required_fields:
			if required == "name":
				default_params["name"] = str(user.name)
			elif required == "email":
				default_params["email"] = str(user.email)
			elif required == "phone":
				default_params["phone"] = str(user.phone)
			elif required == "dept":
				default_params["dept"] = str(user.dept)
			elif required == "sem":
				default_params["sem"] = str(user.sem)
			else:
				pass
		
		new_registration = Register(club_id=clubid,event_id=eventid,usn=usn,name=default_params["name"],email=default_params["email"],phone=default_params["phone"],dept=default_params["dept"],sem=default_params["sem"])
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