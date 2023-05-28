from django.contrib import messages
# from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
# from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from myapp.forms import MyRegisterForm, BuyForm, ProductForm
from myapp.models import Product, SiteUser, Buy, ReturnConfirmation
from mysite.settings import TIME_RETURN_LIMIT


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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
                queryset = queryset.order_by('-created_at')
            else:
                queryset = queryset.filter(site_user=self.request.user) \
                    .order_by('-created_at')
        else:
            queryset = None
        return queryset
    
    # def post(self, request, *args, **kwargs):
    # # create ReturnConfirmation
    # buy_id = int(request.POST.get('buy_id'))
    # with transaction.atomic():
    #     # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
    #     #     # select_for_update блокирует запись в таблице в транзакции
    #     obj_buy_blocked = Buy.objects.select_for_update().get(id=buy_id)
    #     return_confirmation_is = ReturnConfirmation.objects.filter(buy=obj_buy_blocked)
    #     if return_confirmation_is.exists():
    #         messages.error(self.request, "ReturnConfirmation already exist!")
    #         return redirect('returnconfirmationlist')
    #
    #     # блокировка уже существующего обьекта в транзакции
    #     #  для юзера нельзя применять только для обычных моделей
    #     # user_blocked = request.user.refresh_from_db(for_update=True)
    #     user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
    #     #  вернуть можно только в первые три минуты
    #     if timezone.now() > (obj_buy_blocked.created_at + timezone.timedelta(minutes=TIME_RETURN_LIMIT)):
    #         messages.error(self.request, "Return not allowed error, 3 minutes have passed!")
    #         return redirect('buylist')
    #
    #     return_confirmation_obj = ReturnConfirmation(buy=obj_buy_blocked, site_user=user_blocked)
    #     return_confirmation_obj.save()
    #     messages.success(self.request, "ReturnConfirmation saved SUCSESS!")
    #     return redirect('returnconfirmationlist')
    #
    # return redirect('buylist')


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
                queryset = queryset.order_by('-created_at')
            else:
                queryset = queryset.filter(site_user=self.request.user).order_by('-created_at')
        else:
            queryset = None
        return queryset
    
    # def post(self, request, *args, **kwargs):
    #     # подтверждение возврата
    #     return_id = int(request.POST.get('return_id'))
    #     submit_btn = request.POST.get('submit_btn')
    #     return_confirmation_obj = get_object_or_404(ReturnConfirmation, id=return_id)
    #     if submit_btn == 'Accept':
    #         with transaction.atomic():
    #             obj_buy_blocked = Buy.objects.select_for_update().get(id=return_confirmation_obj.buy.id)
    #             obj_product_blocked = Product.objects.select_for_update().get(id=obj_buy_blocked.product.id)
    #
    #             user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
    #
    #             user_blocked.money += obj_buy_blocked.summ
    #             user_blocked.save()
    #             obj_product_blocked.quantity += obj_buy_blocked.quantity
    #             obj_product_blocked.save()
    #
    #             return_confirmation_obj.delete()
    #             messages.success(self.request, "ReturnConfirmation Accepted success!")
    #
    #     elif submit_btn == 'Cancel':
    #         with transaction.atomic():
    #             return_confirmation_obj.delete()
    #             messages.success(self.request, "ReturnConfirmation Canceled success!")
    #
    #     return redirect('returnconfirmationlist')


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
            queryset = queryset.filter(Q(quantity__gt=0) & Q(title__icontains=query_search)).order_by('title')
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


class AddProductView(LoginRequiredMixin, AdminPassedMixin, CreateView):
    login_url = 'login/'
    template_name = 'add_product.html'
    model = Product
    # fields = ['title', 'content', 'img_url', 'price', 'quantity', ]
    success_url = reverse_lazy('index')
    form_class = ProductForm
    # def form_valid(self, form):
    #     pass


class ProductUpdateView(LoginRequiredMixin, AdminPassedMixin, UpdateView):
    model = Product
    login_url = 'login/'
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('index')
    # fields = ['title', 'content', 'img_url', 'price', 'quantity', ]
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
    
    # def post(self, request, *args, **kwargs):
    #
    #     id_product = int(request.POST.get('id'))
    #     quantity = int(request.POST.get('quantity'))
    #
    #     with transaction.atomic():
    #         # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
    #         # select_for_update блокирует запись в таблице в транзакции
    #         obj_product_blocked = Product.objects.select_for_update().get(id=id_product)
    #
    #         # блокировка уже существующего обьекта в транзакции
    #         #  для юзера нельзя применять только для обычных моделей
    #         # user_blocked = request.user.refresh_from_db(for_update=True)
    #         user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
    #
    #         summ = obj_product_blocked.price * quantity
    #         error = False
    #         if obj_product_blocked is None:
    #             messages.error(self.request, "Product not found!")
    #             error = True
    #         if quantity > obj_product_blocked.quantity or quantity < 1:
    #             messages.error(self.request, "Wrong quantity or product out of stock!")
    #             error = True
    #         if summ > user_blocked.money:
    #             messages.error(self.request, "Out of user money!")
    #             error = True
    #
    #         if error:
    #             return redirect('')
    #         buy_obj = Buy(product=obj_product_blocked, site_user=user_blocked, quantity=quantity,
    #                       summ=summ)
    #         buy_obj.save()
    #
    #         user_blocked.money -= summ
    #         user_blocked.save()
    #
    #         obj_product_blocked.quantity -= quantity
    #         obj_product_blocked.save()
    #
    #         # messages.success(self.request, "Количество должно быть больше нуля!")
    #         messages.success(self.request, "Baying SUCSESS!")
    #         return redirect('buylist')
    #
    #     return redirect('/')
    
    # return reverse_lazy('buylist')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['byform'] = BuyForm(initial={'product': self.object.id})
    #     # context['model2_objects'] = MyModel2.objects.all()
    #     return context


class BuyProductView(LoginRequiredMixin, CreateView):
    model = Buy
    login_url = 'login/'
    # fields = ['quantity', 'product', ]
    success_url = reverse_lazy('buylist')
    form_class = BuyForm
    
    # def get_form_kwargs(self):
    #     # является методом, который возвращает словарь с аргументами для инициализации формы. Этот метод позволяет передать
    #     # дополнительные аргументы в конструктор формы при ее создании.
    #     # Часто используется для передачи контекста представления (например, объекта модели или других данных) в форму для
    #     # дальнейшего использования при инициализации или валидации данных.
    #     kwargs = super().get_form_kwargs()
    #     # kwargs.update({'request': self.request,'product_id': self.kwargs['product_id']})
    #     kwargs.update({
    #         'request': self.request
    #     })
    def form_valid(self, form):
        buy_obj = form.save(commit=False)
        # buy.summ = buy.price * buy.quantity
        # buy.save()
        # messages.success(self.request, "Продукт был успешно добавлен в вашу корзину.")
        
        # если брать из параметров URL  то
        # obj_product_blocked = Product.objects.select_for_update().get(pk= self.kwargs['id'])
        # Вар1
        # id_product = int(form.data.get('id'))
        # Вар2
        
        quantity = buy_obj.quantity
        #
        with transaction.atomic():
            try:
                id_product = int(self.request.POST.get('id'))
                # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
                # select_for_update блокирует запись в таблице в транзакции
                obj_product_blocked = Product.objects.select_for_update().get(id=id_product)
            except Product.DoesNotExist:
                messages.error(self.request, "Product not found!")
                return redirect('index')
            
            try:
                # блокировка уже существующего обьекта в транзакции
                #  для юзера нельзя применять только для обычных моделей
                # user_blocked = request.user.refresh_from_db(for_update=True)
                user_blocked = SiteUser.objects.select_for_update().get(id=self.request.user.id)
            except SiteUser.DoesNotExist:
                messages.error(self.request, "Error get user!")
                return redirect('index')
            
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
                return redirect('index')
            
            # buy_obj.quantity = quantity
            buy_obj.product = obj_product_blocked
            buy_obj.site_user = user_blocked
            buy_obj.summ = summ
            buy_obj.save()
            #
            user_blocked.money -= summ
            user_blocked.save()
            
            obj_product_blocked.quantity -= quantity
            obj_product_blocked.save()
            messages.success(self.request, "Baying SUCSESS!")
            return redirect('buylist')
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect('product_detail')
        # redirect(reverse('product_detail', kwargs={'slug': self.object.slug}))


class ReturnConfirmationView(LoginRequiredMixin, CreateView):
    model = ReturnConfirmation
    login_url = 'login/'
    # fields = ['quantity', 'product', ]
    success_url = reverse_lazy('returnconfirmationlist')
    # form_class = ReturnConfirmationForm
    fields = []
    
    def form_valid(self, form):
        return_confirmation_obj = form.save(commit=False)
        # create ReturnConfirmation
        
        with transaction.atomic():
            buy_id = self.request.POST.get('buy_id')
            return_confirmation_is = ReturnConfirmation.objects.filter(buy=buy_id)
            if return_confirmation_is.exists():
                messages.error(self.request, "ReturnConfirmation already exist!")
                return redirect('returnconfirmationlist')
            return_confirmation_obj.buy = Buy.objects.get(id=buy_id)
            return_confirmation_obj.site_user = SiteUser.objects.get(id=self.request.user.id)
            return_confirmation_obj.save()
            messages.success(self.request, "ReturnConfirmation saved SUCSESS!")
        return super().form_valid(form=form)
        # return redirect('buylist')
    # def form_invalid(self, form):
    #     return redirect('returnconfirmationlist')


class ReturnConfirmationCancelView(LoginRequiredMixin, AdminPassedMixin, DeleteView):
    model = ReturnConfirmation
    login_url = 'login/'
    success_url = reverse_lazy('returnconfirmationlist')
    
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #
    #     messages.success(self.request, "ReturnConfirmation Canceled success!")
    #     return HttpResponseRedirect(success_url)
    
    def form_valid(self, form):
        messages.success(self.request, "ReturnConfirmation Canceled success!")
        return super().form_valid(form)


class ReturnConfirmationAcceptView(LoginRequiredMixin, AdminPassedMixin, DeleteView):
    model = ReturnConfirmation
    login_url = 'login/'
    success_url = reverse_lazy('returnconfirmationlist')
    
    def form_valid(self, form):
        if self.object:
            with transaction.atomic():
                obj_buy_blocked = Buy.objects.select_for_update().get(id=self.object.buy.id)
                obj_product_blocked = Product.objects.select_for_update().get(id=obj_buy_blocked.product.id)
                user_blocked = SiteUser.objects.select_for_update().get(id=self.request.user.id)
                user_blocked.money += obj_buy_blocked.summ
                obj_product_blocked.quantity += obj_buy_blocked.quantity
                user_blocked.save()
                obj_product_blocked.save()
                obj_buy_blocked.delete()
                # self.object.delete()
        
        messages.success(self.request, "ReturnConfirmation Accepted success!")
        return super().form_valid(form)
        # return HttpResponseRedirect('returnconfirmationlist')
        # return reverse_lazy('returnconfirmationlist')


class UserRegisterView(CreateView):
    form_class = MyRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')
    
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
    success_url = reverse_lazy('index')
    template_name = 'login.html'
    
    def get_success_url(self):
        return self.success_url


class LogOut(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'
