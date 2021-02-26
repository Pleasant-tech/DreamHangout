from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields =['username','email','password1','password2']

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user','name','value']
		labels = {
	        'age':'',
	        'gender':'',
	        'state':'',
	        'country':'',
	        'bio':'',
	        'profile_pic':'',
        }
		

		

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','email']
		labels = {
	        'username':'',
	        'email':'',
        }


class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )