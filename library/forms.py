from django import forms
from django.contrib.auth.models import User
from .models import Profile, Document

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
	class Meta:
		type_options = (
			(0, "Instructor (Faculty)"),
			(1, "Student"),
			(2, "Visiting Professor"),
			(3, "TA (Faculty)"),
			(4, "Professor (Faculty)")
		)
		model = Profile
		patron_type = forms.ChoiceField(
			widget=forms.Select(choices=type_options),
			required=True,
			label='Type') 
		fields = ['patron_type', 'phone_number', 'adress']

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

class ProfileAddForm(forms.ModelForm):
	class Meta:
		type_options = (
			(0, "Faculty"),
			(1, "Student"),
			(2, "Visiting Professor"),
		)
		model = Profile
		patron_type = forms.ChoiceField(
			widget=forms.Select(choices=type_options),
			required=True,
			label='Type') 
		fields = ['patron_type', 'phone_number', 'adress']

class DocumentAddForm(forms.ModelForm):
	class Meta:
		type_options = (
			(0, "Book"),
			(1, "Article"),
			(2, "Audio-Video Material"),
		)
		model = Document
		document_type = forms.ChoiceField(
			widget=forms.Select(choices=type_options),
			required=True,
			label='Type')
		widgets = {
			'published_date': forms.DateInput(attrs={'class':'datepicker'}),
		}
		fields = ['published_date', 'document_type', 'title', 'authors', 'best_seller']
	copies = forms.IntegerField()
	title = forms.CharField(max_length=100)

class AddCopiesForm(forms.Form):
	amount = forms.IntegerField()