from django.shortcuts import render, HttpResponse
from tester.models import *
from .forms import *
from django.conf import settings
from welcomepage.views import navbar_functions

def clubname(request):
	club_id = request.GET.get("club_id")
	print("********************", club_id)
	curr_club_list = Club.objects.filter(club_id=club_id)
	event_list = Event.objects.filter(club_id=club_id)
	
	navfunc = navbar_functions(request)
	newdict = navfunc.copy()
	clubs = Club.objects.all()
	newdict.update({"clubs":clubs})
	
	all_dict = {'events' : event_list,'curr_club':curr_club_list}
	
	newdict.update(all_dict)
	return render(request, 'club/club.html',newdict)

