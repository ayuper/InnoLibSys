from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		username = forms.CharField(label='Username', max_length=20)
		password = forms.CharField(label='Password', widget=forms.PasswordInput)

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('librarian',)

class PatronEditForm(forms.ModelForm):
	class Meta:
		model = User
		username = forms.CharField(label='Username', max_length=20)
		first_name = forms.CharField(label='First name', max_length=50)
		last_name = forms.CharField(label='Last name', max_length=50)
		fields = ['username', 'first_name', 'last_name']

class PatronAddForm(forms.ModelForm):
	class Meta:
		model = User
		username = forms.CharField(label='Username', max_length=20)
		first_name = forms.CharField(label='First name', max_length=50)
		last_name = forms.CharField(label='Last name', max_length=50)
		password = forms.CharField(label='Password', widget=forms.PasswordInput)
		fields = ['username', 'first_name', 'last_name', 'password']