# import string
# from random import random
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import ListView, CreateView

from myapp.models import Product, SiteUser


# class Index(View):
#     http_method_names = ['get', ]
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'index.html')

class IndexProduct(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'


# class RegisterDefUser(CreateView):
#     form_class = UserCreationForm
#     template_name = 'register.html'
#     success_url = '/'

# class RegisterView(View):
#     User = get_user_model()
#     def get(self,request):
#         form = UserCreationForm()
#         render(request, 'register.html', {'form': form, })
#     def post(self,request):
#
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         render(request, 'register.html', {'form': form, })

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = '/'
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Дополнительные действия после успешной регистрации пользователя
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_model'] = SiteUser
            # get_user_model()
        return kwargs

    
class Login(LoginView):
    # https://ccbv.co.uk/projects/Django/4.1/django.contrib.auth.views/LoginView/
    success_url = '/'
    template_name = 'login.html'
    def get_success_url(self):
        return self.success_url
class LogOut(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'
    
    
    