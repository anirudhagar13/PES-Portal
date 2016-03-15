from django import forms
from .models import Event
from django.utils import timezone
OPTIONS = (
			("name", "Name"),
			("email", "Email Id"),
			("phone_no", "Phone No"),
			("branch", "Branch"),
			("sem", "Sem"),
		)

class Eventform(forms.ModelForm):
	requirements = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple, choices = OPTIONS)
	class Meta:
		model = Event
		fields = ('club_id', 'event_id','event_name','event_date','venue',
        		'no_part','no_reg','contact_info','event_desc','requirements','poster','own_form')
		
class Tuple_no(forms.Form):
	rows = forms.CharField()

class Registry(forms.Form):
	usn = forms.CharField()
	cid = forms.CharField()
	eid = forms.IntegerField()
