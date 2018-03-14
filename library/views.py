from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/library/login/")

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/library/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "library/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.

class LoginFormView(FormView):
    #import pdb; pdb.set_trace()
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "library/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/library/main-page/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class MainPageView(View):
	def get(self, request):
		context = {'user':request.user}
		return render(request, 'library/index.html', context)

def redirect_login(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/library/login/")
	return HttpResponseRedirect("/library/main-page/")

class AuthRequiredMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_request(self, request):
		if not request.user.is_authenticated() and not request.path != '/library/sign-up/':
			return HttpResponseRedirect("/library/login/") # or http response
		return None
