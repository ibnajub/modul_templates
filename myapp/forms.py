from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError

from myapp.models import Product, Purchase, ReturnConfirmation, SiteUser
# from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.conf import settings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['title', 'content', 'img_url', 'price', 'quantity', ]
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price should be more then 0')
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError('Quantity should be more then 1')
        return quantity


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity', ]
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError('Quantity should be more then 1')
        return quantity
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super.__init__(*args, **kwargs)
    
    #     disabled_fields = kwargs.get('disabled_fields')
    #     if disabled_fields is not None:
    #         del kwargs['disabled_fields']
    #     super().__init__(*args, **kwargs)
    #     if disabled_fields:
    #         for field in self.fields:
    #             self.fields[field].disabled = True
    
    # def clean(self):
    #     cleaned_data = super.clean()
    #     if cleaned_data.get('quantity') < 1:
    #         self.add_error(None,'Cannot order < 1 product')
    #         messages.error(self.request, "Wrong quantity or product out of stock!")
    #     quantity = cleaned_data.get('quantity')
    #     try:
    #         id_product = int(self.request.POST.get('id'))


# class ReturnConfirmationForm(forms.ModelForm):
#     class Meta:
#         model = ReturnConfirmation
#         fields = ['purchase']
#
#     def clean(self):
#         return super().clean()


class MyRegisterForm(forms.ModelForm):
    # """
    # A form that creates a user, with no privileges, from the given username and
    # password.
    # """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match.111"),
    }
    # money = forms.CharField(label="mys",
    #                         widget=forms.TextInput(attrs={'readonly': 'readonly'}) )
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))
    
    class Meta:
        model = SiteUser
        fields = ['username', 'password1', 'password2']
        # fields = ['username', ]
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # user.is_superuser = True
        # user.is_staff = True
        user.set_password(self.cleaned_data["password1"])
        # user.set_password(self.cleaned_data["password"])
        user.money = settings.USER_MONEY
        if commit:
            user.save()
        return user
