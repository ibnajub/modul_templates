# import string
# from random import random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from myapp.forms import MyRegisterForm, BuyForm
from myapp.models import Product, SiteUser, Buy, ReturnConfirmation


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

    # def post(self):
    
    
    def get(self, request, *args, **kwargs):
        
        return  super().get(request)

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
    model = Product
    login_url = 'login/'
    # form_class = MyModelForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('index')
    fields = ['title', 'content','img_url', 'price', 'quantity',]
    # def form_valid(self, form):
    #     # Вызываем родительский метод form_valid() для сохранения изменений в базе данных
    #     response = super().form_valid(form)
    #     # Добавляем дополнительную логику обработки после сохранения изменений, если это необходимо
    #     return response
class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    login_url = 'login/'
    template_name = 'product_detail.html'
    extra_context = {'byform': BuyForm(),}
    # success_url = reverse_lazy('buylist')
    # fields = ['title', 'content','img_url', 'price', 'quantity',]


    
    def post(self, request, *args, **kwargs):
        #     return buy_product(self,request)
        # def buy_product(self,request):
        
        # self.object = self.get_object()
        # context = self.get_context_data(object=self.object)
        # return self.render_to_response(context)
        id_product = int(request.POST.get('id'))
        quantity = int(request.POST.get('quantity'))
        
        with transaction.atomic():
            # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
            # select_for_update блокирует запись в таблице в транзакции
            obj_product_blocked =   Product.objects.select_for_update().get(id =  id_product)
            
            # блокировка уже существующего обьекта в транзакции
            #  для юзера нельзя применять только для обычных моделей
            # user_blocked = request.user.refresh_from_db(for_update=True)
            
            user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
            
            summ = obj_product_blocked.price * quantity
            error = False
            if not obj_product_blocked:
                messages.ERROR(self.request, "Product not found!")
                error = True
            if quantity >= obj_product_blocked.quantity or quantity < 1:
                messages.ERROR(self.request, "Wrong quantity or product out of stock!")
                error = True
            if summ > user_blocked.money:
                messages.ERROR(self.request, "Out of user money!")
                error = True
            if error:
                return redirect('')
            buy_obj = Buy(product = obj_product_blocked, site_user = user_blocked, quantity = quantity,
                          summ = summ)
            buy_obj.save()
            
            user_blocked.money -= summ
            user_blocked.save()
            
            obj_product_blocked.quantity -= quantity
            obj_product_blocked.save()
            
            # messages.success(self.request, "Количество должно быть больше нуля!")
            messages.success(self.request, "Baying SUCSESS!")
            return redirect('buylist')
        
        return redirect('')
        
        # return reverse_lazy('buylist')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['byform'] = BuyForm(initial={'product': self.object.id})
    #     # context['model2_objects'] = MyModel2.objects.all()
    #     return context






# class BuyProduct(LoginRequiredMixin, CreateView):
#     model = Buy
#     login_url = 'login/'
#     fields = ['quantity','product',  ]
#     success_url = reverse_lazy('buylist')
#     form_class = BuyForm
#
#     def form_valid(self, form):
#         buy = form.save(commit=False)
#         buy.summ = buy.price * buy.quantity
#         buy.save()
#         messages.success(self.request, "Продукт был успешно добавлен в вашу корзину.")
#         return super().form_valid(form)
#     def get(self, request, *args, **kwargs):
#         messages.add_message(request, messages.INFO, 'Hello world.')
#
#         # form = self.form_class()
#         # return render(request, 'my_buy_form.html', {'form': form})
#         return reverse_lazy('buylist')




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


