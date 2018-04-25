from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm, ProfileForm, ProfileAddForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime
import operator

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
		Log.objects.create(user=user, message="Patron " + user.username + " has checked out a document " + document.title, date=datetime.date.today())

	else:
		queue = DocumentQueue()
		if not DocumentQueue.objects.filter(document=document).exists():
			queue = DocumentQueue.objects.create(document=document)
			queue.users.add(user)
		else:
			queue = DocumentQueue.objects.get(document=document)
			if not DocumentQueue.objects.filter(users__in=[user]).count():
				queue.users.add(user)
		queue.save()

def get_priority_queue(document):
	result = []
	if DocumentQueue.objects.filter(document=document).exists():
		queue = DocumentQueue.objects.get(document=document)
		result = []
		priorities = [1, 0, 3, 2, 4]
		for user in queue.users.all():
			result.append((priorities[user.profile.patron_type], user))
		result.sort(key=operator.itemgetter(0))
	return result

def return_book(user, document):
	return_list = ReturnList.objects.create(user=user, document=document)
	Copy.objects.get(user=user, document=document).delete()
	Log.objects.create(user=user, message="Patron " + user.username + " has requested a document " + document.title + " to return", date=datetime.date.today())


def get_dues(overdue, today):
	return max(0, (today-overdue).days)

def check_dues(user):
	user_copies = Copy.objects.filter(user=user)
	answer = []
	for i in range (user_copies.count()):
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
	Log.objects.create(user=user, message="Patron " + user.username + " has renewed a document " + document.title, date=datetime.date.today())
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

def edit_document(user, document, data):
	copies = data['copies']
	Copy.objects.filter(document=document).delete()
	Log.objects.create(user=user, message="Librarian " + user.username + " has edited document " + document.title, date=datetime.date.today())
	for i in range(int(copies)):
		Copy.objects.create(document=document, user=None, overdue_date=None)

def delete_document(user, document):
	Copy.objects.filter(document=document).delete()
	Log.objects.create(user=user, message="Librarian " + user.username + " has deleted a document " + document.title, date=datetime.date.today())
	document.delete()

def delete_all_objects():
	Copy.objects.all().delete()
	Document.objects.all().delete()
	User.objects.all().delete()

def create_document(user, document, copies):
	if user.profile.priv2:
		Log.objects.create(user=user, message="Librarian " + user.username + " has created " + str(copies) + " of a document " + document.title, date=datetime.date.today())
		document = Document.objects.create(document_type=document.document_type, published_date=document.published_date, title=document.title, to_return=document.to_return, best_seller=document.best_seller, authors=document.authors, price=document.price, outstanding_request=document.outstanding_request, keywords=document.keywords)
		add_copies(user, document, copies)
		return document

def create_patron(user, patron):
	if user.profile.priv2:
		new_patron = User.objects.create_user(username=patron.username, password=patron.password)
		new_patron.profile.patron_type = patron.profile.patron_type
		new_patron.profile.librarian = False
		new_patron.profile.phone_number = patron.profile.phone_number
		new_patron.profile.adress = patron.profile.adress
		new_patron.save()
		Log.objects.create(user=user, message="Librarian " + user.username + " has created patron " + patron.username, date=datetime.date.today())
		return new_patron

def librarian_accept_return(user, __request):
	document = __request.document
	cp = Copy.objects.get(document=document, user=__request.user)
	__request.delete()
	Log.objects.create(user=user, message="Librarian " + user.username + " has accepter a return request from " + __request.user.username, date=datetime.date.today())
	cp.user = None
	cp.save()

def update_fines(user):
	overdue_documents = Copy.objects.filter(~Q(overdue_date=None) & Q(overdue_date__lte=datetime.date.today()) & Q(user=user))
	current_fine = 0
	for i in range(overdue_documents.count()):
		current_fine += min((overdue_documents[i].overdue_date-datetime.date.today()).days*100, overdue_documents[i].document.price)
	user.profile.fine = current_fine
	user.save()

def add_copies(user, document, amount):
	if user.profile.priv2:
		available_copies = Copy.objects.filter(document=document, user=None).count()
		Log.objects.create(user=user, message="Librarian " + user.username + " added " + str(amount) + " copies for document " + document.title, date=datetime.date.today())
		if not available_copies:
			queue = get_priority_queue(document)
			if queue is not None and len(queue) != 0:
				first_user = queue[0][1]
				date = datetime.date.today()
				message = "There's a new copy of document \"" + document.title + "\" and you can check it out."
				notify(first_user, Notifications(message=message, date=date, new_copy=True))
		for i in range(amount):
			Copy.objects.create(document=document, user=None)

def notify(user, notification):
	Notifications.objects.create(user=user, message=notification.message, date=notification.date, new_copy=notification.new_copy)

def outstanding_request(user, document):
	if user.profile.priv3:
		if not document.outstanding_request:
			document.outstanding_request = True
			document.save()
			owned_copies = Copy.objects.filter(Q(document=document) & ~Q(user=None))
			Log.objects.create(user=user, message="Librarian " + user.username + " made an outstanding request for document " + document.title, date=datetime.date.today())
			for copy in owned_copies:
				owner = copy.user
				date = datetime.date.today()
				message = "Librarian made an outstanding request for document \"" + document.title + "\", you must return it back as soon as possible!"
				notify(owner, Notifications(message=message, date=date, new_copy=False))
			queue = get_priority_queue(document)
			if queue is not None:
				for user in queue:
					date = datetime.date.today()
					message = "You have left the queue for document \"" + document.title + "\" due to an outstanding request."
					notify(user[1], Notifications(message=message, date=date, new_copy=False))
				DocumentQueue.objects.get(document=document).delete()

def create_admin(username, password):
	if not Profile.objects.filter(~Q(admin=False)).count():
		user = User.objects.create_user(username=username, password=password)
		user.profile.admin = True
		user.save()
		return user

def admin_create_librarian(admin, username, password, priv1, priv2, priv3):
	user = User.objects.create_user(username, password)
	user.profile.librarian = True
	user.profile.priv1 = priv1
	user.profile.priv2 = priv2
	user.profile.priv3 = priv3
	user.save()
	Log.objects.create(user=user, message="Admin " + admin.username + " has created librarian " + username, date=datetime.date.today())
	return user

def search_query(user, type, query):
	if type == 0:
		return Document.objects.filter(keywords__contains=query)
	else:
		return Document.objects.filter(title__contains=query)