from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


branch_choice = (("CSE","Computer Engineering"),
				("ISE","Information Engineering"),
				("ME","Mechanical Engineering"),
				("ECE","Electronics Engineering"),
				("EEE","Electrical Engineering"),
				("TE","Telecom Engineering"),
				("BT","Bio-Technology"),
				("CV","Civil Engineering"))

designation_choice = (("Admin","Admin"),
				("Cultural Secretary","Cultural Secretary"),
				("Event Manager","Event Manager"),
				("Other","Other"))

sem_choice = (("1","I"),
			("2","II"),
			("3","III"),
			("4","IV"),
			("5","V"),
			("6","VI"),
			("7","VII"),
			("8","VIII"))
			
# Create your models here.

class Club(models.Model):
	club_id = models.CharField(max_length = 120,primary_key=True)
	club_name = models.CharField(max_length = 120,null = True)
	contact_info = models.IntegerField(null = True)
	objective = models.TextField(null = True)
	description = models.TextField(null = True)
	created_on = models.DateTimeField(default = timezone.now)
	class Meta:
		unique_together = ('club_id',)
	def __str__ (self):
		return self.club_name

class Signup(models.Model):
	usn = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=100)
	dept = models.CharField(max_length=50,null=True)
	email = models.EmailField(default = "abc@xyz.com",null=True)
	dob = models.DateField(null=True)
	phone = models.BigIntegerField(null=True)
	sem = models.IntegerField(null=True)
	club_id = models.CharField(max_length=10,null=True,blank=True)

	def __str__(self):
		return str(self.usn)
'''

class Signup(models.Model):
	usn = models.CharField(max_length=10,primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone_no = models.IntegerField()
	D_O_B = models.DateField(null=True)
	branch = models.CharField(max_length=3,choices=branch_choice,null=True)
	sem = models.CharField(max_length=1,choices=sem_choice)
	club_id = models.CharField(max_length=10,null=True,blank=True)

	def __str__(self):
		return str(self.usn)
'''

'''
class Member(models.Model):
	club_id = models.ForeignKey(Club, db_column = "club_id")
	usn = models.ForeignKey(Signup, db_column = "usn")
	designation = models.CharField(max_length=50,choices=designation_choice,null = True)
	class Meta:
		unique_together = ('club_id','usn')
'''	
	
#Cannot Make club_id foreign due to `forbidden csrf error` while form posting
class Event(models.Model):
	club_id = models.CharField(max_length = 120)
	event_id = models.IntegerField()
	event_name = models.CharField(max_length = 120)
	event_date = models.DateTimeField(default = "")
	venue = models.CharField(max_length = 120,null=True)
	no_part = models.IntegerField()
	no_reg = models.IntegerField(null = True,blank = True)
	contact_info = models.TextField(null = False,default="")
	event_desc = models.TextField(null = True)
	requirements = models.TextField(null = True,blank = True)
	own_form = models.URLField(null = True,blank = True)
	poster = models.ImageField(upload_to="./tester/static",null=True,blank=True)
	timestamp = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return str(self.event_id)

	class Meta:
		unique_together = ('club_id','event_id')

class Register(models.Model):
	club_id = models.CharField(max_length = 120,default="")
	event_id = models.IntegerField()
	usn = models.CharField(max_length=10)
	name = models.CharField(max_length=120,null=True)
	email = models.EmailField(default = "abc@xyz.com",null=True)
	phone = models.BigIntegerField(null=True)
	dept = models.CharField(max_length=50,null=True)
	sem = models.CharField(max_length=2,null=True)

	def __str__(self):
		return self.club_id

	class Meta:
		unique_together = ('event_id','usn','club_id')


class Seller(models.Model):
	book_name = models.CharField(max_length=50)
	seller_id = models.ForeignKey(Signup)
	subject = models.CharField(max_length=50)
	

	class Meta:
		unique_together = (("book_name","seller_id"),)


class Pending_transactions(models.Model):
	buyer_id = models.ForeignKey(Signup)
	seller = models.ForeignKey(Seller,default=None)
	book_name = models.CharField(max_length=50)
	class Meta:
		unique_together = (("buyer_id","seller","book_name"))
		
class Comments(models.Model):

	usn = models.CharField(max_length=10)
	event_id = models.IntegerField()
	comment = models.CharField(max_length=100000000000000)
	creat_date = models.DateTimeField('date published')

	class Meta:
		unique_together =(("usn","creat_date"))