# import string
# from random import random
from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from myapp.forms import MyRegisterForm
from myapp.models import Product, SiteUser, Buy, ReturnConfirmation


# class Index(View):
#     http_method_names = ['get', ]
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'index.html')

# class IndexProduct(LoginRequiredMixin, ListView):

class BuyList(LoginRequiredMixin, ListView):
    login_url = 'login/'
    paginate_by = 5
    model = Buy
    template_name = 'buy_list.html'
    # login_url = 'login/'
    allow_empty = True  # разрешить ли отображение пустого списка

    def get_queryset(self):
        queryset = super().get_queryset()
        m_user = self.request.user
        if m_user.is_authenticated:
            queryset = Buy.objects.filter(site_user=self.request.user)
        else:
            queryset = None
        return queryset


class ReturnConfirmationList(LoginRequiredMixin, ListView):
    login_url = 'login/'
    paginate_by = 5
    model = ReturnConfirmation
    template_name = 'return_confirmation_list.html'
    allow_empty = True  # разрешить ли отображение пустого списка
    def get_queryset(self):
        queryset = super().get_queryset()
        m_user = self.request.user
        if m_user.is_authenticated:
            queryset = ReturnConfirmation.objects.filter(site_user=self.request.user)
        else:
            queryset = None
        return queryset

class IndexProduct(ListView):
    paginate_by = 5
    # model = Product
    template_name = 'index.html'
    # login_url = 'login/'
    queryset = Product.objects.filter(quantity__gt =  0)
    allow_empty = True  # разрешить ли отображение пустого списка
    # ordering = None  # явно указать ордеринг

    def post(self):
        pass

class SearchProdictResults(ListView):
    model = Product
    template_name = 'index.html'
    # context_object_name = 'page_obj'
    paginate_by =6
    def get_queryset(self):
        queryset = super().get_queryset()
        query_search = self.request.GET.get('query_search')
        if query_search:
            queryset = queryset.filter(name__icontains=query_search)
        return queryset



class AddProduct(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    template_name = 'add_product.html'
    model = Product
    fields =  ['title', 'content','img_url', 'price', 'quantity', ]
    success_url = '/'
    # form_class = MyRegisterForm
    # def form_valid(self, form):
    #     pass

class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Product
    # form_class = MyModelForm
    queryset = Product.objects.filter(pk= 1)
    template_name = 'update_product.html'
    success_url = reverse_lazy('index')








class UserRegisterView(CreateView):
    form_class = MyRegisterForm
    template_name = 'register.html'
    success_url = '/'
    # success_url = reverse_lazy('login')

    # def get(self, request):
#         form = UserCreationForm()
#         render(request, 'register.html', {'form': form, })
#     def post(self,request):
#
#         form = MyRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         render(request, 'register.html', {'form': form, })

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # Дополнительные действия после успешной регистрации пользователя
    #     return response
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user_model'] = SiteUser
    #         # get_user_model()
    #     return kwargs


class Login(LoginView):
    # https://ccbv.co.uk/projects/Django/4.1/django.contrib.auth.views/LoginView/
    success_url = '/'
    template_name = 'login.html'
    def get_success_url(self):
        return self.success_url


class LogOut(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


