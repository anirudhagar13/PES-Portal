from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import User
from tester.models import Signup,Seller
import random
import string
class Command(BaseCommand):
	
	def handle(self,n_signups=50,*args,**options):
		n_signups = int(n_signups)
		start_usn = "1pi13cs"
		names = ["prafful","parikshit","rohan","manisha","romasha","neha","smitha","sharath","nagasundar","niket","anirudh"]
		for x in range(n_signups):

			""" create new signup """
			usn = start_usn + str(x)
			name = names[int(random.uniform(0,len(names)-1))]
			dept = "CSE"
			sem = 6
			phone=random.uniform(944870000,9999999999)
			email = name +"@gmail.com"

			new_signup = Signup(
				usn = usn,
				name = name,
				dept = dept,
				sem = sem,
				phone = phone,
				email = email,
				)
			new_signup.save()

			"""make entry into user table"""
			User.objects.create_user(username=usn,password="password")

			"""create entry into Seller table"""

			subjects = ["Discrete Math","ADA","Data Structures","Algorithms","Python","Unix System Programming"
			,"Operating Systems","Computer Networks"]
			book_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(10))
			subject = subjects[int(random.uniform(0,len(subjects)-1))]
			seller_id = Signup.objects.get(usn=usn)

			new_seller = Seller(
				book_name = book_name,
				subject = subject,
				seller_id = seller_id
				)
			new_seller.save()

		#print "Done!"
