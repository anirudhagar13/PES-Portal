from django.shortcuts import render
from forms import *
from .models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def event(request):
	cid = str(request).split("create/")[1][:-2]							#For auto filling of club-id in event creation
	itr = Event.objects.filter(club_id=cid).order_by('-id')				#Cannot have auto-generated event_id as repeated event entries are possilble
	if not itr:															#So Retrieving eid of last event to help admin
		eid = 1;
	else:
		eid = itr[0].event_id								
	form = Eventform(request.POST)										#Function to handle and put event creation form in database
	if form.is_valid():													#Checks If form properly filled		
		form.save()
		form = Eventform()
		itr = Event.objects.filter(club_id=cid).order_by('-id')				#Cannot have auto-generated event_id as repeated event entries are possilble
		if not itr:															#So Retrieving eid of last event to help admin
			eid = 1;
		else:
			eid = itr[0].event_id
		return render(request,"tester/forms.html",{'fill_cid':cid,'fill_eid':eid,'form':form})

	return render(request,"tester/forms.html",{'fill_cid':cid,'fill_eid':eid,'form':form})			#Redirects to Event Creation template

def del_event(cid,num):													#Function to delete checked events by club-admin
	ls = list(map(int,str(num).split(',')[:-1]))						#Getting list of entries checked
	itr = Event.objects.filter(club_id=cid).order_by('id')				#Getting all tuples from event	
	for i in ls:
		#print(itr[i].event_name)
		Register.objects.filter(event_id = itr[i].event_id).delete()	#Also deleting all registrations done for the event	
		itr[i].delete()

def del_reg(cid,eid,num):												#Function to delete checked registrations by club-admin
	ls = list(map(int,str(num).split(',')[:-1]))
	itr = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')	#Getting ordered registration entries for that event
	for i in ls:	
		#print(i,itr[i].name)
		itr[i].delete()

def show(request):														#Function to redirect to all events list hosted by passed club
	cid = str(request).split("event/")[1][:-2]
	checkbox = Tuple_no(request.POST)									#Hidden form to get list of checked boxes for deletion
	forms = Event.objects.filter(club_id=cid).order_by('id')	
	if checkbox.is_valid():
		checked = checkbox.cleaned_data.get("rows")
		del_event(cid,checked)											#Calling function to delete checked events
		checked = Tuple_no()
		forms = Event.objects.filter(club_id=cid).order_by('id')	
		return render(request, 'tester/show.html', {'check':checkbox,'form': forms})

	return render(request, 'tester/show.html', {'check':checkbox,'form': forms})	#Rendering event list template

def reg(request):
	ls = str(request).split("register/")[1][:-2].split('$')				#deriving info from URL
	cid = ls[0]
	eid = int(ls[1])
	checkbox = Tuple_no(request.POST)									#Function to redirect to all registrations list for passed event
	name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 	#if no entry of event_id in event gives index out of
	forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')	#Getting ordered registration list
	if checkbox.is_valid():
		checked = checkbox.cleaned_data.get("rows")
		del_reg(cid,eid,checked)										#Calling checked registrations method
		checked = Tuple_no()
		name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 
		forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
		return render(request, 'tester/show2.html', {'name':name,'check':checkbox,'form': forms})

	return render(request, 'tester/show2.html', {'name':name,'check':checkbox,'form': forms})	#rendering registration list template

def filt(a,b,c):														#Function to filter event requirements set by club-admin													
	pick = Signup.objects.filter(usn=a)
	pick2 = Event.objects.filter(club_id=c).filter(event_id=b)
	req = str(pick2[0].requirements)									#Getting and segregating info from event requirements
	req = req[1:-1].replace("u'","").replace("'","").replace(" ","")	#To process and extract unicode strings
	ls = req.split(",")
	put_reg(pick,ls,c,b)

def put_reg(sgnup,ls,cid,eid):											#Function to put decided info of registered user in registration table
	d = {"usn":sgnup[0].usn,"name":"","email":"","phone_no":"","branch":"","sem":""}
	ls1 = ["name", "email","phone_no","branch","sem"]
	for i in d.keys():													#To check which of info during signup is required for event registration
		if i in ls:
			index = ls1.index(i)
			if index == 0:
				d[i] = str(sgnup[0].name)
			elif index == 1:
				d[i] = str(sgnup[0].email)
			elif index == 2:
				d[i] = str(sgnup[0].phone_no)
			elif index == 3:
				d[i] = str(sgnup[0].branch)
			elif index == 4:
				d[i] = str(sgnup[0].sem)
			else:
				d[i] = None

	Register.objects.create(club_id=cid,event_id=eid,					#Creating a registration entry
							usn = d["usn"],name=d["name"],
							email=d["email"],phone_no=d["phone_no"],
							branch=d["branch"],sem=d["sem"])


def one_click_reg(request):												#Function to inact one click registrations
	one_click = Registry(request.POST)
	if one_click.is_valid():
		usn = one_click.cleaned_data.get("usn")							#Inputting three basic info 
		eid = one_click.cleaned_data.get("eid")
		cid = one_click.cleaned_data.get("cid")
		filt(usn,eid,cid)												#Calling function to register entered USN
		one_click = Registry()
		return render(request,"tester/one_click.html",{'form':one_click})
	return render(request,"tester/one_click.html",{'form':one_click})

def main_admin(request):												#To redirect to main-template
	cid = str(request).split("tester/")[1][:-2]							#deriving info from URL
	return render(request,"tester/main_admin.html",{'fill_cid':cid})

def prom(request):														#To redirect to promotion page
	cid = str(request).split("promote/")[1][:-2]						#Get club_id from URL
	forms = Event.objects.filter(club_id=cid).order_by('id')	
	return render(request,"tester/event_prom.html",{'fill_cid':cid,'form':forms})

def click_prom(request):												#To redirect to promotion choice page
	ls = str(request).split("click_prom/")[1][:-2].split('$')			#deriving info from URL
	cid = ls[0]
	eid = int(ls[1])
	hidden = Tuple_no(request.POST)													#Hidden Form to see if button clicked or not
	name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 	#if no entry of event_id in event gives index out of
	forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
	if hidden.is_valid():
		url = 'https://localhost/event/%s'%(eid)
		msg = "Upcoming Event : %s is on the verge.\nPlease Click the link : %s"%(name,url)
		subject = "PES Times Upcoming Events"
		f_mail = settings.EMAIL_HOST_USER
		s_mail = ["senddjango@gmail.com"]
		'''for(i in forms):
			s_mail.append(forms[i].email)'''
		send_mail(subject,msg, f_mail , s_mail, fail_silently=False)			#Sending Mail
		hidden = Tuple_no()
		name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name
		forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
		return render(request, 'tester/click_prom.html', {'hide':hidden})

	return render(request, 'tester/click_prom.html', {'hide':hidden})