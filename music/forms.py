from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	
	'''The Django Meta class is a special thing 
	through out Django which is used to transfer 
	information about the model or other object to the 
	Django framework; rather than using subclassing 
	(which might have been another option
	but significantly more complex to implementing).'''
	class Meta:
	    model = User
	    fields = ('username','email','password')

