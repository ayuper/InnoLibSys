from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm, ProfileForm, ProfileAddForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Profile, Document, ReturnList, Copy
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime

def check_out_a_book(user, document, date):
	available_copies = Copy.objects.filter(document=document, user=None).count()
	if available_copies > 0:
		copy = Copy.objects.filter(document=document, user=None).first()
		if user.profile.patron_type == 0 or user.profile.patron_type == 3 or user.profile.patron_type == 4:
			if document.document_type == 2:
				copy.overdue_date = date + datetime.timedelta(days=7)
			else:
				copy.overdue_date = date + datetime.timedelta(days=28)
		elif user.profile.patron_type == 1:
			if document.best_seller or document.document_type == 2:
				copy.overdue_date = date + datetime.timedelta(days=14)
			else:
				copy.overdue_date = date + datetime.timedelta(days=21)
		elif user.profile.patron_type == 2:
			copy.overdue_date = date + datetime.timedelta(days=7)
		copy.user = user
		copy.save()

def return_book(user, document):
	return_list = ReturnList.objects.create(user=user, document=document)
	Copy.objects.get(user=user, document=document).delete()


def get_dues(overdue, today):
	return max(0, (today-overdue).days)

def check_dues(user):
	user_copies = Copy.objects.filter(user=user)
	answer = []
	for i in range (user_copies.count()):
		#print(user.username)
		#print(user.profile.patron_type)
		#print(user_copies[i].overdue_date)
		#print(datetime.date.today())
		answer.append((user_copies[i].document, max(0, get_dues(user_copies[i].overdue_date, datetime.date.today()))))
	return answer

def check_fines(user):
	user_copies = Copy.objects.filter(user=user)
	answer = []
	for i in range (user_copies.count()):
		answer.append((max(0, get_dues(user_copies[i].overdue_date, datetime.date.today())), max(0, min(user_copies[i].document.price, get_dues(user_copies[i].overdue_date, datetime.date.today())*100))))
	return answer

def renew(user, document):
	copy = Copy.objects.get(user=user, document=document)
	if user.profile.patron_type == 0 or user.profile.patron_type == 3 or user.profile.patron_type == 4:
		if document.document_type == 2:
			copy.overdue_date = datetime.date.today() + datetime.timedelta(days=7)
		else:
			copy.overdue_date = datetime.date.today() + datetime.timedelta(days=28)
	elif user.profile.patron_type == 1:
		if document.best_seller or document.document_type == 2:
			copy.overdue_date = datetime.date.today() + datetime.timedelta(days=14)
		else:
			copy.overdue_date = datetime.date.today() + datetime.timedelta(days=21)
	elif user.profile.patron_type == 2:
		copy.overdue_date = datetime.date.today() + datetime.timedelta(days=7)
	copy.save()

def get_info(user):
	copies = Copy.objects.filter(user=user)
	answer = []
	for i in range(copies.count()):
		answer.append((copies[i].document, copies[i].overdue_date))
	return answer

def edit_document(document, data):
	copies = data['copies']
	Copy.objects.filter(document=document).delete()
	for i in range(int(copies)):
		Copy.objects.create(document=document, user=None, overdue_date=None)

def delete_document(document):
	Copy.objects.filter(document=document).delete()
	document.delete()

def librarian_accept_return(__request):
	document = __request.document
	cp = Copy.objects.get(document=document, user=__request.user)
	__request.delete()
	cp.user = None
	cp.save()

def update_fines(user):
	overdue_documents = Copy.objects.filter(~Q(overdue_date=None) & Q(overdue_date__lte=datetime.date.today()) & Q(user=user))
	current_fine = 0
	for i in range(overdue_documents.count()):
		current_fine += min((overdue_documents[i].overdue_date-datetime.date.today()).days*100, overdue_documents[i].document.price)
	user.profile.fine = current_fine
	user.save()