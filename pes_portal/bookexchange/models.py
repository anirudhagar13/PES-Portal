from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''Temporary - not required post integration'''
class Student(models.Model):
	Usn =  models.CharField(max_length=10, primary_key=True)

class Seller(models.Model):
	book_name = models.CharField(max_length=50)
	seller_id = models.ForeignKey(Student)
	subject = models.CharField(max_length=50)
	

	class Meta:
		unique_together = (("book_name","seller_id"),)


class Pending_transactions(models.Model):
	buyer_id = models.ForeignKey(Student)
	seller = models.ForeignKey(Seller,default=None)

	class Meta:
		unique_together = (("buyer_id","seller"))