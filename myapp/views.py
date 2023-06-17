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

# from django.utils import timezone
from datetime import datetime

# from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from myapp.forms import MyRegisterForm, PurchaseForm, ProductForm
from myapp.models import Product, SiteUser, Purchase, ReturnConfirmation
from mysite.settings import TIME_RETURN_LIMIT


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class PurchaseListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    # ordering = ['-created_at']  # явно указать ордеринг
    paginate_by = 5
    model = Purchase
    template_name = 'purchase_list.html'
    
    # login_url = 'login/'
    # allow_empty = True  # разрешить ли отображение пустого списка
    # success_url = '/'
    def get_queryset(self):
        queryset = super().get_queryset()
        m_user = self.request.user
        
        if m_user.is_superuser:
            queryset = queryset.order_by('-created_at')
        elif m_user.is_authenticated:
            queryset = queryset.filter(site_user=self.request.user) \
                .order_by('-created_at')
        else:
            queryset = None
        return queryset
    
    # def post(self, request, *args, **kwargs):
    # # create ReturnConfirmation
    # purchase_id = int(request.POST.get('purchase_id'))
    # with transaction.atomic():
    #     # obj_product_blocked =  get_object_or_404( Product.objects.select_for_update().get(id =  id_product))
    #     #     # select_for_update блокирует запись в таблице в транзакции
    #     obj_purchase_blocked = Purchase.objects.select_for_update().get(id=purchase_id)
    #     return_confirmation_is = ReturnConfirmation.objects.filter(purchase=obj_purchase_blocked)
    #     if return_confirmation_is.exists():
    #         messages.error(self.request, "ReturnConfirmation already exist!")
    #         return redirect('returnconfirmationlist')
    #
    #     # блокировка уже существующего обьекта в транзакции
    #     #  для юзера нельзя применять только для обычных моделей
    #     # user_blocked = request.user.refresh_from_db(for_update=True)
    #     user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
    #     #  вернуть можно только в первые три минуты
    #     if timezone.now() > (obj_purchase_blocked.created_at + timezone.timedelta(minutes=TIME_RETURN_LIMIT)):
    #         messages.error(self.request, "Return not allowed error, 3 minutes have passed!")
    #         return redirect('purchaselist')
    #
    #     return_confirmation_obj = ReturnConfirmation(purchase=obj_purchase_blocked, site_user=user_blocked)
    #     return_confirmation_obj.save()
    #     messages.success(self.request, "ReturnConfirmation saved SUCSESS!")
    #     return redirect('returnconfirmationlist')
    #
    # return redirect('purchaselist')


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
    #             obj_purchase_blocked = Purchase.objects.select_for_update().get(id=return_confirmation_obj.purchase.id)
    #             obj_product_blocked = Product.objects.select_for_update().get(id=obj_purchase_blocked.product.id)
    #
    #             user_blocked = SiteUser.objects.select_for_update().get(id=request.user.id)
    #
    #             user_blocked.money += obj_purchase_blocked.summ
    #             user_blocked.save()
    #             obj_product_blocked.quantity += obj_purchase_blocked.quantity
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
    ordering = 'title'  # явно указать ордеринг
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_search = self.request.GET.get('query_search')
        queryset = queryset.filter(quantity__gt=0)
        if query_search:
            # queryset = queryset.filter(Q(quantity__gt=0) & Q(title__icontains=query_search)).order_by('title')
            queryset = queryset.filter(quantity__gt=0, title__icontains=query_search)
        
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
    extra_context = {'byform': PurchaseForm(), }
    
    # success_url = reverse_lazy('purchaselist')
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
    #         purchase_obj = Purchase(product=obj_product_blocked, site_user=user_blocked, quantity=quantity,
    #                       summ=summ)
    #         purchase_obj.save()
    #
    #         user_blocked.money -= summ
    #         user_blocked.save()
    #
    #         obj_product_blocked.quantity -= quantity
    #         obj_product_blocked.save()
    #
    #         # messages.success(self.request, "Количество должно быть больше нуля!")
    #         messages.success(self.request, "Baying SUCSESS!")
    #         return redirect('purchaselist')
    #
    #     return redirect('/')
    
    # return reverse_lazy('purchaselist')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['byform'] = PurchaseForm(initial={'product': self.object.id})
    #     # context['model2_objects'] = MyModel2.objects.all()
    #     return context


class PurchaseProductView(LoginRequiredMixin, CreateView):
    model = Purchase
    login_url = 'login/'
    # fields = ['quantity', 'product', ]
    success_url = reverse_lazy('purchaselist')
    form_class = PurchaseForm
    
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
        purchase_obj = form.save(commit=False)
        # purchase.summ = purchase.price * purchase.quantity
        # purchase.save()
        # messages.success(self.request, "Продукт был успешно добавлен в вашу корзину.")
        
        # если брать из параметров URL  то
        # obj_product_blocked = Product.objects.select_for_update().get(pk= self.kwargs['id'])
        # Вар1
        # id_product = int(form.data.get('id'))
        # Вар2
        
        quantity = purchase_obj.quantity
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
            
            # purchase_obj.quantity = quantity
            purchase_obj.product = obj_product_blocked
            purchase_obj.site_user = user_blocked
            purchase_obj.summ = summ
            purchase_obj.save()
            #
            user_blocked.money -= summ
            user_blocked.save()
            
            obj_product_blocked.quantity -= quantity
            obj_product_blocked.save()
            messages.success(self.request, "Baying SUCSESS!")
            return redirect('purchaselist')
        
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
            purchase_id = self.request.POST.get('purchase_id')
            return_confirmation_is = ReturnConfirmation.objects.filter(purchase=purchase_id)
            if return_confirmation_is.exists():
                messages.error(self.request, "ReturnConfirmation already exist!")
                return redirect('returnconfirmationlist')
            return_confirmation_obj.purchase = Purchase.objects.get(id=purchase_id)
            # timezone.now() время сервера UTC отстает от моего на 3 часа
            # if timezone.now() > (
            if datetime.now() > (
                    return_confirmation_obj.purchase.created_at + datetime.timedelta(minutes=TIME_RETURN_LIMIT)):
                messages.error(self.request, f"Return not allowed error, 3 minutes have passed! {datetime.now()}")
                return redirect('purchaselist')
            return_confirmation_obj.site_user = SiteUser.objects.get(id=self.request.user.id)
            return_confirmation_obj.save()
            messages.success(self.request, "ReturnConfirmation saved SUCSESS!")
        return super().form_valid(form=form)
        # return redirect('purchaselist')
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
                obj_purchase_blocked = Purchase.objects.select_for_update().get(id=self.object.purchase.id)
                obj_product_blocked = Product.objects.select_for_update().get(id=obj_purchase_blocked.product.id)
                user_blocked = SiteUser.objects.select_for_update().get(id=self.request.user.id)
                user_blocked.money += obj_purchase_blocked.summ
                obj_product_blocked.quantity += obj_purchase_blocked.quantity
                user_blocked.save()
                obj_product_blocked.save()
                obj_purchase_blocked.delete()
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
