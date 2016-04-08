from django.shortcuts import render
from .forms import *
from .models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
'''
This function renders the form to create the event
'''
def event(request):
	cid = str(request).split("create/")[1][:-2]							#For auto filling of club-id in event creation
	itr = Event.objects.filter(club_id=cid).order_by('-id')				
	if not itr:															#Retrieving eid of last event to help admin
		eid = 1;
	else:
		eid = itr[0].event_id								
	form = Eventform(request.POST)										
	if form.is_valid():															
		form.save()
		form = Eventform()
		itr = Event.objects.filter(club_id=cid).order_by('-id')				
		if not itr:															
			eid = 1;
		else:
			eid = itr[0].event_id
		return render(request,"tester/forms.html",{'fill_cid':cid,'fill_eid':eid,'form':form})

	return render(request,"tester/forms.html",{'fill_cid':cid,'fill_eid':eid,'form':form})			
	
'''
This function deletes checked events by club-admin
'''
def del_event(cid,num):													
	ls = list(map(int,str(num).split(',')[:-1]))						
	itr = Event.objects.filter(club_id=cid).order_by('id')					
	for i in ls:
		Register.objects.filter(event_id = itr[i].event_id).delete()	#Also deleting all registrations done for the event	
		itr[i].delete()

'''
This function deletes checked registrations by club-admin
'''
def del_reg(cid,eid,num):												
	ls = list(map(int,str(num).split(',')[:-1]))
	itr = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')	
	for i in ls:	
		itr[i].delete()
		
'''
This function redirects the club-admin to all events list hosted by his/her club
'''
def show(request):														
	cid = str(request).split("event/")[1][:-2]
	checkbox = Tuple_no(request.POST)									
	forms = Event.objects.filter(club_id=cid).order_by('id')	
	if checkbox.is_valid():
		#deleting checked events
		checked = checkbox.cleaned_data.get("rows")
		del_event(cid,checked)											
		checked = Tuple_no()
		forms = Event.objects.filter(club_id=cid).order_by('id')	
		return render(request, 'tester/show.html', {'check':checkbox,'form': forms})

	return render(request, 'tester/show.html', {'check':checkbox,'form': forms})

'''
This function enables the admin to see all the registrations 
'''
def reg(request):
	ls = str(request).split("register/")[1][:-2].split('$')				
	cid = ls[0]
	eid = int(ls[1])
	checkbox = Tuple_no(request.POST)									#Function to redirect to all registrations list for passed event
	name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 	
	forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
	if checkbox.is_valid():
		#deleting checked registrations
		checked = checkbox.cleaned_data.get("rows")
		del_reg(cid,eid,checked)			
		checked = Tuple_no()
		name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 
		forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
		return render(request, 'tester/show2.html', {'name':name,'check':checkbox,'form': forms})

	return render(request, 'tester/show2.html', {'name':name,'check':checkbox,'form': forms})	#rendering registration list template

'''
This function filters event requirements as set by club-admin
'''
def filt(a,b,c):																											
	pick = Signup.objects.filter(usn=a)
	pick2 = Event.objects.filter(club_id=c).filter(event_id=b)
	req = str(pick2[0].requirements)									#Getting and segregating info from event requirements
	req = req[1:-1].replace("u'","").replace("'","").replace(" ","")	#To process and extract unicode strings
	ls = req.split(",")
	put_reg(pick,ls,c,b)

'''
This function puts desired info of registered user in registration table
'''
def put_reg(sgnup,ls,cid,eid):											
	d = {"usn":sgnup[0].usn,"name":"","email":"","phone":"","dept":"","sem":""}
	ls1 = ["name", "email","phone","dept","sem"]
	for i in d.keys():													#To check which of info during signup is required for event registration
		if i in ls:
			index = ls1.index(i)
			if index == 0:
				d[i] = str(sgnup[0].name)
			elif index == 1:
				d[i] = str(sgnup[0].email)
			elif index == 2:
				d[i] = str(sgnup[0].phone)
			elif index == 3:
				d[i] = str(sgnup[0].dept)
			elif index == 4:
				d[i] = str(sgnup[0].sem)
			else:
				d[i] = None

	Register.objects.create(club_id=cid,event_id=eid,					#Creating a registration entry
							usn = d["usn"],name=d["name"],
							email=d["email"],phone=d["phone"],
							dept=d["dept"],sem=d["sem"])

'''
This function performs one click registrations
'''
def one_click_reg(request):												
	one_click = Registry(request.POST)
	if one_click.is_valid():
		usn = one_click.cleaned_data.get("usn")						 
		eid = one_click.cleaned_data.get("eid")
		cid = one_click.cleaned_data.get("cid")
		filt(usn,eid,cid)											
		one_click = Registry()
		return render(request,"tester/one_click.html",{'form':one_click})
	return render(request,"tester/one_click.html",{'form':one_click})

'''
This function is used to redirect to main-template
'''
def main_admin(request):												
	cid = str(request).split("tester/")[1][:-2]							
	return render(request,"tester/main_admin.html",{'fill_cid':cid})

'''
This function is used to redirect to promotion page
'''
def prom(request):														
	cid = str(request).split("promote/")[1][:-2]						
	forms = Event.objects.filter(club_id=cid).order_by('id')	
	return render(request,"tester/event_prom.html",{'fill_cid':cid,'form':forms})

'''
This function is used to redirect to the promotion choice page
'''
def click_prom(request):												
	ls = str(request).split("click_prom/")[1][:-2].split('$')		
	cid = ls[0]
	eid = int(ls[1])
	hidden = Tuple_no(request.POST)													#Hidden Form to see if button clicked or not
	name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name 	
	forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
	if hidden.is_valid():
		url = 'https://localhost/event/%s'%(eid)
		msg = "Upcoming Event : %s is on the verge.\nPlease Click the link : %s"%(name,url)
		subject = "PES Times Upcoming Events"
		f_mail = settings.EMAIL_HOST_USER
		s_mail = ["senddjango@gmail.com"]
		send_mail(subject,msg, f_mail , s_mail, fail_silently=False)	
		hidden = Tuple_no()
		name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name
		forms = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
		return render(request, 'tester/click_prom.html', {'hide':hidden})

	return render(request, 'tester/click_prom.html', {'hide':hidden})