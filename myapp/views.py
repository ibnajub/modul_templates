# import string
# from random import random

from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView

from myapp.models import Product


# class Index(View):
#     http_method_names = ['get', ]
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'index.html')

class IndexProduct(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = '/'
    
class Login(LoginView):
    # https://ccbv.co.uk/projects/Django/4.1/django.contrib.auth.views/LoginView/
    success_url = '/'
    template_name = 'login.html'
    def get_success_url(self):
        return self.success_url
class LogOut(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'
    
    
    