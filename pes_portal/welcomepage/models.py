from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.
class Club(models.Model):
	club_id = models.CharField(primary_key=True, max_length=10)
	club_name = models.CharField(max_length=100)
	objective = models.CharField(null = True,max_length=1000,default="objective")
	members = models.CharField(null = True,max_length=1000)
	fb_link = models.CharField(null = True,max_length=100)
	twitter_link = models.CharField(null = True,max_length=100)

	def __str__(self):
		return str(self.club_id)

class Signup(models.Model):
	usn = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=100)
	dept = models.CharField(max_length=50)
	email = models.EmailField(default = "abc@xyz.com",null=True)
	dob = models.DateField(null=True)
	phone = models.BigIntegerField(null=True)
	sem = models.IntegerField(null=True)
	club_id = models.ForeignKey(Club, default=None, null=True)

	def __str__(self):
		return str(self.usn)

class Event(models.Model):
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
	timestamp = models.DateTimeField(default = timezone.now)
	club_id = models.ForeignKey(Club, default=None)
	
	def __str__(self):
		return str(self.event_id)

	class Meta:
		unique_together = ('club_id','event_id')


