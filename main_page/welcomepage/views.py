from django.shortcuts import render
from .models import *

# Create your views here.
def newsfeed(request):
	events = Event.objects.all()
	clubs = Club.objects.all()
	return render(request, "welcomepage/newsfeed.html", {"events":events,"clubs":clubs})
	

def bootstrap(request):
	return render(request, "welcomepage/bootstrap.html")
	
