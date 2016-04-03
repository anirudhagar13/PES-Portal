from django import forms
from tester.models import *
from django.utils import timezone
class ClubForm(forms.ModelForm):
	class Meta:
		model = Club
		fields = ('club_id','club_name', 'contact_info', 'objective', 'description', 'created_on')

class StudentForm(forms.ModelForm):
	class Meta:
		model = Signup
		fields = ('usn', 'name', 'email','phone_no', 'D_O_B', 'branch', 'sem' ,'club_id')

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ('club_id', 'usn')

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ('event_id', 'event_name', 'event_date', 'venue', 'no_part', 'no_reg', 'contact_info', 'event_desc', 'requirements', 'own_form', 'timestamp' ,'club_id')
	
	
