from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm, ProfileForm, ProfileAddForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Profile, Document, ReturnList
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime

class IndexView(TemplateView):
	template_name = 'library/index.html'

	@method_decorator(login_required(login_url='/library/login/'))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
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

class ManageDocumentsViews(ListView):
	model = Document
	template_name = 'library/documents.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		disabled = ReturnList.objects.values_list('document')
		if disabled.count() == 0:
			return Document.objects.all()
		else:
			return Document.objects.filter(~Q(disabled))

def patron(request, id):
	print(DocumentAddForm().as_p())
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
				user.save()
				return HttpResponseRedirect('/library/manage/patrons/')
	else:
		user_form = PatronEditForm()
		profile_form = ProfileForm()
	return render(request, 'library/add_patron.html', {'user_form':user_form, 'profile_form':profile_form})

def document(request, id):
	return render(request, 'library/document.html', {'document':Document.objects.get(id=id)})

class DocumentAddView(FormView):
	form_class = DocumentAddForm
	template_name = 'library/add_document.html'
	success_url = '/library/manage/documents/'

	def form_valid(self, form):
		title = self.request.POST['title']
		published_date = self.request.POST['published_date']
		document_type = self.request.POST['document_type']
		document = Document.objects.create(title=title, published_date=published_date, document_type=document_type)
		return super().form_valid(form)

def document_edit(request, **kwargs):
	if request.method == "POST":
		form = DocumentAddForm(data=request.POST, instance=Document.objects.get(id=kwargs.get('id')))
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/library/manage/documents/')
	else:
		form = DocumentAddForm()
	return render(request, 'library/document_edit.html', {'form':form})

def document_delete(request, **kwargs):
	document = Document.objects.get(id=kwargs.get('id'))
	document.delete()
	return HttpResponseRedirect('/library/manage/documents/')

class DocumentsView(ListView):
	model = Document
	template_name = 'library/my_documents.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		return Document.objects.filter(user=self.request.user)

def my_document(request, id):
	return render(request, 'library/my_document.html', {'document':Document.objects.get(id=id)})

def document_return(request, **kwargs):
	document = Document.objects.get(id=kwargs.get('id'))
	return_list = ReturnList.objects.create(user=request.user, document=document)
	document.user = None
	document.to_return = True
	document.save()
	return HttpResponseRedirect('/library/documents/')

class DocumentsCheckOutView(ListView):
	model = Document
	template_name = 'library/check_out.html'
	context_object_name = 'document_list'
	def get_queryset(self):
		return Document.objects.filter(~Q(user=self.request.user) & Q(to_return=False))

def document_check_out(request, **kwargs):
	document = Document.objects.get(id=kwargs.get('id'))
	document.user = request.user
	document.save()
	return HttpResponseRedirect('/')

class DocumentsReturnView(ListView):
	model = ReturnList
	template_name = 'library/return_list.html'
	context_object_name = 'return_list'
	queryset = ReturnList.objects.all()

def document_lreturn(request, **kwargs):
	__request = ReturnList.objects.get(id=kwargs.get('id'))
	document = __request.document
	__request.delete()
	document.to_return = False
	document.save()
	return HttpResponseRedirect('/library/manage/return/')

class OverdueDocumentsView(ListView):
	model = Document
	template_name = 'library/overdue_documents.html'
	context_object_name = 'overdue_documents'
	def get_queryset(self):
		return Document.objects.filter(~Q(overdue_date=None) & Q(overdue_date__lte=datetime.date.today()))

def mycard(request):
	return render(request, 'library/mycard.html', {'user':request.user})