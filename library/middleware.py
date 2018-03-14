from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if not request.user.is_authenticated and request.path != '/library/login/' and request.path != '/library/sign-up/':
            return HttpResponseRedirect('/library/login/')

        # Code to be executed for each request/response after
        # the view is called.

        return response
