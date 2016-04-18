from django.shortcuts import render, HttpResponse
from tester.models import *
from .forms import *
from django.conf import settings
from welcomepage.views import navbar_functions

def clubname(request):
	club_id = request.GET.get("club_id")
	club = Club.objects.get(club_id=club_id)
	print("********************", club_id)
	event_list = Event.objects.filter(club_id=club_id).order_by("event_date").reverse()
	
	return render(request, 'club/club.html',navbar_functions(request, {'events' : event_list,'club':club}))

