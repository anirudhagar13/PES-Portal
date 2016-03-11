from django.shortcuts import render
from forms import *
from .models import *
from django.utils import timezone
# Create your views here.

def event(request):
	form = Eventform(request.POST)
	if form.is_valid():
		form.save()
		form = Eventform()
		return render(request,"tester/forms.html",{'form':form})

	return render(request,"tester/forms.html",{'form':form}) 

def del_event(cid,num):
	ls = list(map(int,str(num).split(',')[:-1]))
	#print ls
	itr = Event.objects.filter(club_id=cid).order_by('id')
	for i in ls:
		#print(itr[i].event_name)
		Register.objects.filter(event_id = itr[i].event_id).delete()	
		itr[i].delete()

def del_reg(cid,eid,num):
	ls = list(map(int,str(num).split(',')[:-1]))
	#print ls
	itr = Register.objects.filter(club_id=cid).filter(event_id=eid).order_by('id')
	for i in ls:	
		itr[i].delete()

def show(request):
	cid = str(request).split("event/")[1][:-2]
	#print(cid)
	checkbox = Tuple_no(request.POST)
	forms = Event.objects.filter(club_id=cid)	
	if checkbox.is_valid():
		checked = checkbox.cleaned_data.get("rows")
		del_event(cid,checked)
		checked = Tuple_no()
		forms = Event.objects.filter(club_id=cid)	
		return render(request, 'tester/show.html', {'check':checkbox,'form': forms})

	return render(request, 'tester/show.html', {'check':checkbox,'form': forms})

def reg(request):
	ls = str(request).split("register/")[1][:-2].split('$')
	cid = ls[0]
	eid = int(ls[1])
	checkbox = Tuple_no(request.POST)
	name = Event.objects.filter(club_id=cid).filter(event_id=eid)[0].event_name #if no entry of event_id in event gives index out of
	forms = Register.objects.filter(club_id=cid).filter(event_id=eid)
	if checkbox.is_valid():
		checked = checkbox.cleaned_data.get("rows")
		del_reg(cid,eid,checked)
		checked = Tuple_no()
		forms = Register.objects.filter(club_id=cid).filter(event_id=eid)
		return render(request, 'tester/show2.html', {'check':checkbox,'form': forms})

	return render(request, 'tester/show2.html', {'name':name,'check':checkbox,'form': forms})

def filt(a,b,c):
	pick = Signup.objects.filter(usn=a)
	pick2 = Event.objects.filter(club_id=c).filter(event_id=b)
	req = str(pick2[0].requirements)
	req = req[1:-1].replace("u'","").replace("'","").replace(" ","")
	ls = req.split(",")
	put_reg(pick,ls,c,b)

def put_reg(sgnup,ls,cid,eid):
	d = {"usn":sgnup[0].usn,"name":"","email":"","phone_no":"","branch":"","sem":""}
	ls1 = ["name", "email","phone_no","branch","sem"]
	for i in d.keys():
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

	Register.objects.create(club_id=cid,event_id=eid,
							usn = d["usn"],name=d["name"],
							email=d["email"],phone_no=d["phone_no"],
							branch=d["branch"],sem=d["sem"])


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