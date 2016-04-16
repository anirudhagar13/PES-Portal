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
def navbar_functions(request , e = {}):
	clubs = Club.objects.all()
	extradict  = e.copy()
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
		dict1 = request.POST
		if dict1.get("logout"):
			#logout
			request.session["usn"] = None
			request.session["club_id"] = None
			user = None
		
		#signup form contains email field
		elif dict1.get("email"):		
			#signup
			try:
				username = dict1["username"]	
				usn = dict1["usn"]	
				email = dict1["email"]
				mobile = dict1["mobile"]
				dept = dict1["dept"]
				sem = dict1["sem"]
				password1 = dict1["password1"]
				dob = dict1["dob"]
				#two entries are made:  One in Django User table for authentication purpose
				#						Other in Signup table of our DB for recording user data
				new_user = User.objects.create_user(username=usn,password=password1)
				new_user.save()
				Signup.objects.create(name=username, email=email, usn=usn, dept=dept, phone=mobile, sem=sem, dob=dob)		
			except IntegrityError as e:
				#user exists
				extradict.update({"INTEGRITY_ERROR":True,"clubs":clubs})
				return extradict
		elif dict1.get("userusn"):
			#lost password
			usn = dict1["userusn"]
			try:
				if Signup.objects.get(usn=usn):
					msg = "You can reset your password here \n" + "http://localhost:8000/welcomepage/reset"
					subject = "PES Times Password sent"
					f_mail = settings.EMAIL_HOST_USER
					s_mail = [Signup.objects.get(usn=usn).email]
					send_mail(subject, msg , f_mail , s_mail, fail_silently=False)
					extradict.update({"MAIL_SENT":True,"clubs":clubs})
					return extradict
			except:
				extradict.update({"NO_USER":True,"clubs":clubs})
				return extradict
				
		elif dict1.get("password"):
			#login
			usn = dict1["usn"];
			password = dict1["password"];
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
				extradict.update({"PROBLEM_LOGGING":True,"clubs":clubs})
				return extradict
		
	try:
		extradict.update({"CLUBID":request.session["club_id"],"LOGGED":user, "PROBLEM_LOGGING": False,"clubs":clubs})
		return extradict
	except:
		extradict.update({"CLUBID":None,"LOGGED":user, "PROBLEM_LOGGING": False,"clubs":clubs})
		return extradict
'''
This function renders the newsfeed page
It manages the signup, login, logout functionality and sets appropriate session variables
'''
@csrf_exempt
def render_newsfeed(request):
	# set data to be sent to templates

	events = Event.objects.all()
	
	return render(request, "welcomepage/newsfeed.html", navbar_functions(request, {"events":events}))
	
	
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
	club_id = request.GET.get("club_id")
	event = Event.objects.get(event_id=event_id , club_id = club_id)
	comments = Comments.objects.filter(event_id=event_id)
	names = list()
	for each_comment in range( len(comments) ):
		names.append((Signup.objects.get(usn=comments[each_comment].usn)).name)
	comment_list = list()
	for i in range(len(names)):
		comment_list.append({"name":names[i],"comments":comments[i]})
	if usn:
		isLoggedIn = 'true'
	else:
		isLoggedIn = 'false'
	#print comment_list
	return render(request, "welcomepage/event.html",navbar_functions(request, {"event":event,"isLoggedIn":isLoggedIn,"comment_list":comment_list}))

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
			return render(request, "welcomepage/reset.html", navbar_functions(request, {"events":events,"NO_USER":True} ))
	return render(request, "welcomepage/reset.html",navbar_functions(request, {"events":events}) )

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
		print("***********",eventid,clubid)
		required_fields = Event.objects.get(event_id=eventid,club_id=clubid).requirements
		required_fields = eval(required_fields)
		print("**********",required_fields)
		default_params = {"usn":usn,"name":"","email":"","phone":None,"dept":"","sem":""}
		for required in required_fields:
			if required == "name":
				default_params["name"] = str(user.name)
			elif required == "email":
				default_params["email"] = str(user.email)
			elif required == "phone":
				default_params["phone"] = int(user.phone)
			elif required == "dept":
				default_params["dept"] = str(user.dept)
			elif required == "sem":
				default_params["sem"] = str(user.sem)
			else:
				pass
		
		print("******",default_params)
		try:
			Register.objects.create(club_id = clubid,event_id = eventid,usn = usn,name = default_params["name"],email = default_params["email"],phone = default_params["phone"],dept = default_params["dept"],sem = default_params["sem"])
			#new_registration.save()
			return HttpResponse("Congrats, you have been registered!")
		except IntegrityError as e:
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