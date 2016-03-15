from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.

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
	own_form = models.URLField(null = True,blank = True)
	poster = models.ImageField(upload_to="./tester/static",null=True,blank=True)
	requirements = models.CharField(max_length=100,null = True, blank = True)
	timestamp = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.club_id

	class Meta:
		unique_together = ('club_id','event_id')

class Register(models.Model):
	club_id = models.CharField(max_length = 120,default="")
	event_id = models.IntegerField()
	usn = models.CharField(max_length=10)
	name = models.CharField(max_length=120,null=True)
	email = models.EmailField(default = "abc@xyz.com",null=True)
	phone_no = models.IntegerField(null=True)
	branch = models.CharField(max_length=3,null=True)
	sem = models.CharField(max_length=2,null=True)

	def __str__(self):
		return self.club_id

	class Meta:
		unique_together = ('event_id','usn','club_id')


branch_choice = (("CSE","Computer Engineering"),
				("ISE","Information Engineering"),
				("ME","Mechanical Engineering"),
				("ECE","Electronics Engineering"),
				("EEE","Electrical Engineering"),
				("TE","Telecom Engineering"),
				("BT","Bio-Technology"),
				("CV","Civil Engineering"))

sem_choice = (("1","I"),
			("2","II"),
			("3","III"),
			("4","IV"),
			("5","V"),
			("6","VI"),
			("7","VII"),
			("8","VIII"))




class Signup(models.Model):
	usn = models.CharField(max_length=10,primary_key=True)
	password = models.CharField(max_length=10)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone_no = models.IntegerField()
	D_O_B = models.DateField()
	branch = models.CharField(max_length=3,choices=branch_choice)
	sem = models.CharField(max_length=1,choices=sem_choice)
	club_id = models.CharField(max_length=10,null=True,blank=True)




