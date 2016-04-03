from django.shortcuts import render, HttpResponse
from tester.models import *
from .forms import *
from django.conf import settings

def index(request):
	club_list = club.objects.order_by('club_id')
	event_list = Event.objects.all()
	all_dict = {'categories':club_list,'events' : event_list}

	return render(request, 'club/index.html', all_dict)

def clubname(request):
	club_id = request.GET.get("club_id")
	print("********************", club_id)
	curr_club_list = Club.objects.filter(club_id=club_id)
	event_list = Event.objects.filter(club_id=club_id)
	member_list = Member.objects.filter(club_id=club_id)
	all_dict = {'members':member_list,'events' : event_list,'curr_club':curr_club_list}
	return render(request, 'club/club.html',all_dict,)
	'''
	cid = str(request).split("/")[3][5:]
	curr_club_list = club.objects.filter(club_id=cid)
	member_list = member.objects.filter(club_id=cid)
	print(member_list)
	event_list = Event.objects.filter(club_id=cid)
	all_dict = {'members':member_list,'events' : event_list,'curr_club':curr_club_list}
	return render(request, 'club/club.html',all_dict,)
	'''

def event(request):
	eid = str(request).split("/")[3][5:]
	curr_event_list = Event.objects.filter(event_id=eid)
	event_dict = {'events' : curr_event_list}
	return render(request, 'club/event.html',event_dict,)


def boots(request):
	return render(request, 'club/boots.html',)


