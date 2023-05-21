from django.contrib import messages
# from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils import timezone
# from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from myapp.forms import MyRegisterForm, BuyForm
from myapp.models import Product, SiteUser, Buy, ReturnConfirmation
from mysite.settings import TIME_RETURN_LIMIT


class BuyListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    # ordering = ['-created_at']  # явно указать ордеринг
    paginate_by = 5
    model = Buy
    template_name = 'buy_list.html'
    
    # login_url = 'login/'
    # allow_empty = True  # разрешить ли отображение пустого списка
    # success_url = '/'
    def get_queryset(self):
        queryset = super().get_queryset()
        m_user = self.request.user
        
        if m_user.is_authenticated:
            if m_user.is_superuser:
                queryset = Buy.objects.all().order_by('-created_at')
            else:
                queryset = Buy.objects.filter(site_user=self.request.user)\
                    .order_by('-created_at')
        else:
            queryset = None
        return queryset
    
    def post(self, request, *args, **kwargs):
        # create ReturnConfirmation
        buy_id = int(request.POST.get('buy_id'))
        with transaction.atomic():
            # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
            #     # select_for_update блокирует запись в таблице в транзакции
            obj_buy_blocked = Buy.objects.select_for_update().get(id=buy_id)
            return_confirmation_is = ReturnConfirmation.objects.filter(buy = obj_buy_blocked)
            if return_confirmation_is.exists():
                messages.error(self.request, "ReturnConfirmation already exist!")
                return redirect('returnconfirmationlist')
                
            # блокировка уже существующего обьекта в транзакции
            #  для юзера нельзя применять только для обычных моделей
            # user_blocked = request.user.refresh_from_db(for_update=True)
            user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
            #  вернуть можно только в первые три минуты
            if timezone.now() > (obj_buy_blocked.created_at + timezone.timedelta(minutes=TIME_RETURN_LIMIT) ):
                messages.error(self.request, "Return not allowed error, 3 minutes have passed!")
                return redirect('buylist')
            
            return_confirmation_obj = ReturnConfirmation(buy=obj_buy_blocked, site_user=user_blocked)
            return_confirmation_obj.save()
            messages.success(self.request, "ReturnConfirmation saved SUCSESS!")
            return redirect('returnconfirmationlist')
        
        return redirect('buylist')


class ReturnConfirmationListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    paginate_by = 5
    model = ReturnConfirmation
    template_name = 'return_confirmation_list.html'
    # allow_empty = True  # разрешить ли отображение пустого списка
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        m_user = self.request.user
        if m_user.is_authenticated:
            if m_user.is_superuser:
                queryset = ReturnConfirmation.objects.all().order_by('-created_at')
            else:
                queryset = ReturnConfirmation.objects.filter(site_user=self.request.user).order_by('-created_at')
        else:
            queryset = None
        return queryset
    
    def post(self, request, *args, **kwargs):
        # подтверждение возврата
        return_id = int(request.POST.get('return_id'))
        submit_btn =  request.POST.get('submit_btn')
        return_confirmation_obj = get_object_or_404(ReturnConfirmation, id=return_id)
        if submit_btn == 'Accept':
            with transaction.atomic():
                obj_buy_blocked = Buy.objects.select_for_update().get(id = return_confirmation_obj.buy.id)
                obj_product_blocked = Product.objects.select_for_update().get(id=obj_buy_blocked.product.id)
                
                user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
                
                user_blocked.money += obj_buy_blocked.summ
                user_blocked.save()
                obj_product_blocked.quantity += obj_buy_blocked.quantity
                obj_product_blocked.save()
                
                return_confirmation_obj.delete()
                messages.success(self.request, "ReturnConfirmation Accepted success!")
            
        elif submit_btn == 'Cancel':
            with transaction.atomic():
                return_confirmation_obj.delete()
                messages.success(self.request, "ReturnConfirmation Canceled success!")
                
        return redirect('returnconfirmationlist')


class IndexProductView(ListView):
    paginate_by = 5
    model = Product
    template_name = 'index.html'
    # login_url = 'login/'
    # queryset = Product.objects.filter(quantity__gt=0)
    # allow_empty = True  # разрешить ли отображение пустого списка
    # ordering = None  # явно указать ордеринг
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_search = self.request.GET.get('query_search')
        if query_search:
            queryset = queryset.filter( Q(quantity__gt=0) & Q(title__icontains=query_search) ).order_by('title')
        else:
            queryset = queryset.filter(quantity__gt=0).order_by('title')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем GET-параметр 'query_search' в контекст шаблона для отображения что искали по кнопке поиска
        query_search = self.request.GET.get('query_search')
        if query_search:
            context['query_search'] = query_search
        return context
        



class AddProductView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    template_name = 'add_product.html'
    model = Product
    fields = ['title', 'content', 'img_url', 'price', 'quantity', ]
    success_url = '/'
    # form_class = MyRegisterForm
    # def form_valid(self, form):
    #     pass


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    login_url = 'login/'
    # form_class = MyModelForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('index')
    fields = ['title', 'content', 'img_url', 'price', 'quantity', ]
    # def form_valid(self, form):
    #     # Вызываем родительский метод form_valid() для сохранения изменений в базе данных
    #     response = super().form_valid(form)
    #     # Добавляем дополнительную логику обработки после сохранения изменений, если это необходимо
    #     return response


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    login_url = 'login/'
    template_name = 'product_detail.html'
    extra_context = {'byform': BuyForm(), }
    
    # success_url = reverse_lazy('buylist')
    # fields = ['title', 'content','img_url', 'price', 'quantity',]
    
    def post(self, request, *args, **kwargs):

        id_product = int(request.POST.get('id'))
        quantity = int(request.POST.get('quantity'))
        
        with transaction.atomic():
            # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
            # select_for_update блокирует запись в таблице в транзакции
            obj_product_blocked = Product.objects.select_for_update().get(id=id_product)
            
            # блокировка уже существующего обьекта в транзакции
            #  для юзера нельзя применять только для обычных моделей
            # user_blocked = request.user.refresh_from_db(for_update=True)
            user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
            
            summ = obj_product_blocked.price * quantity
            error = False
            if obj_product_blocked is None:
                messages.error(self.request, "Product not found!")
                error = True
            if quantity > obj_product_blocked.quantity or quantity < 1:
                messages.error(self.request, "Wrong quantity or product out of stock!")
                error = True
            if summ > user_blocked.money:
                messages.error(self.request, "Out of user money!")
                error = True
                
            if error:
                return redirect('')
            buy_obj = Buy(product=obj_product_blocked, site_user=user_blocked, quantity=quantity,
                          summ=summ)
            buy_obj.save()
            
            user_blocked.money -= summ
            user_blocked.save()
            
            obj_product_blocked.quantity -= quantity
            obj_product_blocked.save()
            
            # messages.success(self.request, "Количество должно быть больше нуля!")
            messages.success(self.request, "Baying SUCSESS!")
            return redirect('buylist')
        
        return redirect('/')
        
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
