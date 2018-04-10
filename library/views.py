from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm, ProfileForm, ProfileAddForm, AddCopiesForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Profile, Document, ReturnList, Copy
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime
from .functions import *

class IndexView(TemplateView):
	template_name = 'library/index.html'

	@method_decorator(login_required(login_url='/library/login/'))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
		print(Notifications.objects.filter(user=self.request.user))
		context['notifications'] = Notifications.objects.filter(user=self.request.user)
		return context

class LoginView(FormView):
	template_name = 'library/login.html'
	form_class = UserLoginForm
	success_url = '/'

	def form_valid(self, form):
		data = form.cleaned_data
		username = data['username']
		password = data['password']
		user = authenticate(username=username, password=password)
		if user is None:
			return render(self.request, 'library/login.html', {'form':form, 'error':'Invalid login!'})
		login(self.request, user)
		return super().form_valid(form)

class SignupView(FormView):
	template_name = 'library/signup.html'
	form_class = UserForm
	success_url = '/'

	def form_valid(self, form):
		username = self.request.POST['username']
		password = self.request.POST['password']
		if User.objects.filter(username=username).exists():
			return render(self.request, template_name, {'error':'Username already exists!', 'form':form})
		user = User.objects.create_user(username=username, password=password)
		login(self.request, user)
		return super().form_valid(form)

class ManagePatronsViews(ListView):
	model = User
	context_object_name = 'patron_list'
	queryset = User.objects.all()
	template_name = 'library/patrons.html'

def queue_view(request, **kwargs):
	queue = get_priority_queue(Document.objects.get(id=kwargs.get('id')))
	return render(request, 'library/queue.html', {'queue':queue})

class ManageDocumentsViews(ListView):
	model = Document
	template_name = 'library/documents.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		return Document.objects.all()

def patron(request, id):
	return render(request, 'library/patron.html', {'user':User.objects.get(id=id)})

def patron_edit(request, **kwargs):
	if request.method == "POST":
		user_form = PatronEditForm(data=request.POST, instance=User.objects.get(id=kwargs.get('id')))
		profile_form = ProfileForm(data=request.POST, instance=Profile.objects.get(id=kwargs.get('id')))
		if user_form.is_valid():
			if profile_form.is_valid():
				user = user_form.save()
				data = profile_form.cleaned_data
				user.profile.phone_number = data['phone_number']
				user.profile.adress = data['adress']
				user.profile.patron_type = data['patron_type']
				user.save()
				return HttpResponseRedirect('/library/manage/patrons/')
	else:
		user_form = PatronEditForm()
		profile_form = ProfileForm()
	return render(request, 'library/patron_edit.html', {'user_form':user_form, 'profile_form':profile_form})

def patron_delete(request, **kwargs):
	user = User.objects.get(id=kwargs.get('id'))
	user.delete()
	return HttpResponseRedirect('/library/manage/patrons/')

def patron_add(request):
	if request.method == "POST":
		user_form = PatronAddForm(data=request.POST)
		profile_form = ProfileAddForm(data=request.POST)
		if user_form.is_valid():
			if profile_form.is_valid():
				user = user_form.save()
				data = profile_form.cleaned_data
				user.profile.phone_number = data['phone_number']
				user.profile.adress = data['adress']
				user.set_password(user_form.cleaned_data['password'])
				user.save()
				return HttpResponseRedirect('/library/manage/patrons/')
	else:
		user_form = PatronAddForm()
		profile_form = ProfileAddForm()
	return render(request, 'library/add_patron.html', {'user_form':user_form, 'profile_form':profile_form})

def document(request, id):
	return render(request, 'library/document.html', {'document':Document.objects.get(id=id), 'copies':Document.objects.get(id=id).copy_set.count()}) 

class DocumentAddView(FormView):
	form_class = DocumentAddForm
	template_name = 'library/add_document.html'
	success_url = '/library/manage/documents/'

	def form_valid(self, form):
		title = self.request.POST['title']
		published_date = self.request.POST['published_date']
		document_type = self.request.POST['document_type']
		authors = self.request.POST['authors']
		copies = self.request.POST['copies']
		best_seller = self.request.POST['best_seller']	
		document = Document.objects.create(title=title, published_date=published_date, document_type=document_type, authors=authors)
		for i in range(int(copies)):
			Copy.objects.create(document=document, user=None, overdue_date=None)
		document.save()
		return super().form_valid(form)

def document_edit(request, **kwargs):
	if request.method == "POST":
		form = DocumentAddForm(data=request.POST, instance=Document.objects.get(id=kwargs.get('id')))
		if form.is_valid():
			edit_document(Document.objects.get(id=kwargs.get('id')), request.POST)
			form.save()
			return HttpResponseRedirect('/library/manage/documents/')
	else:
		form = DocumentAddForm()
	return render(request, 'library/document_edit.html', {'form':form})

def document_delete(request, **kwargs):
	delete_document(Document.objects.get(id=kwargs.get('id')))
	return HttpResponseRedirect('/library/manage/documents/')

class DocumentsView(ListView):
	model = Copy
	template_name = 'library/my_documents.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		return_list = ReturnList.objects.filter(user=self.request.user)
		print(Copy.objects.filter(Q(user=self.request.user)))
		return Copy.objects.filter(Q(user=self.request.user) & ~Q(document__id__in=[d.document.id for d in return_list])) # check

def my_document(request, id):
	return render(request, 'library/my_document.html', {'document':Document.objects.get(id=id), 'copy':Copy.objects.get(user=request.user,document=Document.objects.get(id=id))}) # check

def document_return(request, **kwargs):
	return_book(request.user, Document.objects.get(id=kwargs.get('id')))
	return HttpResponseRedirect('/library/documents/') # check

class DocumentsCheckOutView(ListView):
	model = Document
	template_name = 'library/check_out.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		return_list = ReturnList.objects.filter(user=self.request.user)
		owned_copies_docs = Copy.objects.filter(user=self.request.user)
		return Document.objects.all().filter(~Q(id__in=[d.document.id for d in owned_copies_docs]) & ~Q(id__in=[d.document.id for d in return_list]))

def document_check_out(request, **kwargs):
	document = Document.objects.get(id=kwargs.get('id'))
	check_out_a_book(request.user, document, datetime.date.today())
	return HttpResponseRedirect('/') # check

class DocumentsReturnView(ListView):
	model = ReturnList
	template_name = 'library/return_list.html' # check the template
	context_object_name = 'return_list'
	queryset = ReturnList.objects.all()

def document_lreturn(request, **kwargs):
	librarian_accept_return(ReturnList.objects.get(id=kwargs.get('id')))
	return HttpResponseRedirect('/library/manage/return/')

class OverdueDocumentsView(ListView):
	model = Copy
	template_name = 'library/overdue_documents.html'
	context_object_name = 'overdue_documents'
	def get_queryset(self):
		return Copy.objects.filter(~Q(overdue_date=None) & Q(overdue_date__lte=datetime.date.today()))

def mycard(request):
	update_fines(request.user)
	return render(request, 'library/mycard.html', {'user':request.user})

class PatronsCheckedView(ListView):
	model = User
	template_name = 'library/checked_patrons.html'
	context_object_name = 'checked_patrons'
	def get_queryset(self):
		return User.objects.filter(copy__in=Copy.objects.filter(Q(document=Document.objects.filter(id=self.kwargs.get('id'))) & ~Q(user=None)))
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['overdue_date'] = Copy.objects.filter(Q(document=Document.objects.filter(id=self.kwargs.get('id'))) & ~Q(user=None)).values_list('overdue_date')
		return data #check

def overdue_copy(request, **kwargs):
	cp = Copy.objects.get(id=kwargs.get('id'))
	return render(request, 'library/overdue_copy.html', {'copy':cp})

def document_renew(request, **kwargs):
	copy = Copy.objects.get(document=document, user=request.user)
	if not copy.renewed:
		renew(request.user, Document.objects.get(id=kwargs.get('id')))
		return render(request, 'library/my_document.html', {'document':Document.objects.get(id=kwargs.get('id')), 'copy':Copy.objects.get(user=request.user,document=Document.objects.get(id=kwargs.get('id')))})
	else:
		return render(request, 'library/my_document.html', {'document':Document.objects.get(id=kwargs.get('id')), 'copy':Copy.objects.get(user=request.user,document=Document.objects.get(id=kwargs.get('id'))), 'error':'You have already renewed this item.'})

def add_copies_view(request, **kwargs):
	if request.method == "POST":
		form = AddCopiesForm(data=request.POST)
		if form.is_valid():
			add_copies(Document.objects.get(id=kwargs.get('id')), int(request.POST['amount']))
			return HttpResponseRedirect('/library/manage/documents/')
	else:
		form = AddCopiesForm()
	return render(request, 'library/add_copies.html', {'form':form})