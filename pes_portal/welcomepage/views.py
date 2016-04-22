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
from django.views.decorators.cache import never_cache
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
			request.session["username"] = dict1["username"]	
			request.session["usn"] = dict1["usn"]	
			request.session["email"] = dict1["email"]
			request.session["mobile"] = dict1["mobile"]
			request.session["dept"] = dict1["dept"]
			request.session["sem"] = dict1["sem"]
			request.session["password1"] = dict1["password1"]
			request.session["dob"] = dict1["dob"]
			
			try:
				user = User.objects.get(username = usn)
			except:
				key = get_random_string(length = 8)
				request.session["key"] = key
				msg = "This is your key: " + key
				subject = "PES Times key sent"
				f_mail = settings.EMAIL_HOST_USER
				s_mail = [dict1["email"]]
				send_mail(subject, msg , f_mail , s_mail, fail_silently=False)
				extradict.update({"KEY_SENT":True,"clubs":clubs})
				return extradict
			else:
				#user exists
				extradict.update({"INTEGRITY_ERROR":True,"clubs":clubs})
				return extradict
			
		elif dict1.get("key"):
			#print(key,dict1.get("key"),"***************")
			if dict1.get("key") == request.session["key"]:
				#two entries are made:  One in Django User table for authentication purpose
				#						Other in Signup table of our DB for recording user data
				new_user = User.objects.create_user(username=request.session["usn"],password=request.session["password1"])
				new_user.save()
				Signup.objects.create(name=request.session["username"], email=request.session["email"], usn=request.session["usn"], dept=request.session["dept"], phone=request.session["mobile"], sem=request.session["sem"], dob=request.session["dob"])
				request.session["key"] = None
				request.session["username"] = None	
				request.session["usn"] = None
				request.session["email"] = None
				request.session["mobile"] = None
				request.session["dept"] = None
				request.session["sem"] = None
				request.session["password1"] = None
				request.session["dob"] = None
			else:
				extradict.update({"WRONG_KEY":True,"clubs":clubs})
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
@never_cache
def render_newsfeed(request):
	# set data to be sent to templates

	events = Event.objects.all().order_by("id").reverse()
	
	paginator = Paginator(events,4)

	page=request.GET.get('page')
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)

	return render(request, "welcomepage/newsfeed.html", navbar_functions(request, {"events":data}))
	
	
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
	try:
		reg = Register.objects.get(usn = usn , club_id = club_id , event_id = event_id)
	except:
		reg = None
	event = Event.objects.get(event_id=event_id , club_id = club_id)
	comments = Comments.objects.filter(event_id=event_id , club_id = club_id)
	club = Club.objects.get(club_id = club_id)
	names = list()
	for each_comment in range( len(comments) ):
		names.append((Signup.objects.get(usn=comments[each_comment].usn)).name)
	comment_list = list()
	for i in range(len(names)):
		comment_list.append({"name":names[i],"comments":comments[i]})
	
	return render(request, "welcomepage/event.html",navbar_functions(request, {"event":event,"comment_list":comment_list,"club":club,"registered":reg}))

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
		club_id = parameters.get("clubid")
		new_comment = Comments(usn=usn,event_id=eventid,club_id = club_id, comment=comment,creat_date=timezone.now())
		try:
			new_comment.save()			
			return HttpResponse((Signup.objects.get(usn=usn)).name)
		except:
			return HttpResponse("Oops! Something is wrong!")

@register.filter
def get_item_value(dictionary,key):
	return dictionary.get(key)