from tester.models import *
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand,CommandError
import random
import string
class Command(BaseCommand):
	
	def handle(self,*args,**options):
		#dept values are: eee cse ece civil ise me bt te
		#dob format: YYYY-MM-DD
		#sem values are: 1 2 3 4 5 6 7 8

		
		# clubs
		Club.objects.create()

		
		# to create users
		# to create club admins add extra field club_id="" while creating Signup object
		new_user = User.objects.create_user(username="1PI13CS099",password="ABC")
		new_user.save()
		Signup.objects.create(name="Neha M Kalibhat", email="neha.kalibhat@gmail.com", usn="1PI13CS099", dept="cse", phone="7829782761", sem="6", dob="1995-12-29")

	
		# events
		Event.objects.create()
		
		# books: fill Seller table
		Seller.objects.create()
		
		