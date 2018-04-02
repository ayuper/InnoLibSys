from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Profile, Document
from django.http import HttpResponseRedirect

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
	queryset = Document.objects.all()
	template_name = 'library/documents.html'

def patron(request, id):
	print(DocumentAddForm().as_p())
	return render(request, 'library/patron.html', {'user':User.objects.get(id=id)})

def patron_edit(request, **kwargs):
	if request.method == "POST":
		form = PatronEditForm(data=request.POST, instance=User.objects.get(id=kwargs.get('id')))
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/library/manage/patrons/')
	else:
		form = PatronEditForm()
	return render(request, 'library/patron_edit.html', {'form':form})

def patron_delete(request, **kwargs):
	user = User.objects.get(id=kwargs.get('id'))
	user.delete()
	return HttpResponseRedirect('/library/manage/patrons/')

class PatronAddView(FormView):
	form_class = PatronAddForm
	template_name = 'library/add_patron.html'
	success_url = '/library/manage/patrons/'

	def form_valid(self, form):
		username = self.request.POST['username']
		password = self.request.POST['password']
		first_name = self.request.POST['first_name']
		last_name = self.request.POST['last_name']
		user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
		return super().form_valid(form)

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