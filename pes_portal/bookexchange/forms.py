from django import forms

from tester.models import Seller

class UploadBookForm(forms.ModelForm):

	class Meta:
		model = Seller
		fields = ('book_name','subject',)
		widgets = {
            'book_name': forms.TextInput(attrs={'class': 'w3-input w3-animate-input','style':'width:135px'}),
            'subject': forms.TextInput(attrs={'class': 'w3-input w3-animate-input','style':'width:135px'}),

        }