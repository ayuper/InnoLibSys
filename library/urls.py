from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('login/', views.LoginFormView.as_view()),
	path('sign-up/', views.RegisterFormView.as_view()),
	path('logout/', views.LogoutView.as_view()),
	path('main-page/', views.MainPageView.as_view()),
	path('', views.redirect_login)
]
