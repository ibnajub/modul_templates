from django import forms

from myapp.models import Product, Buy, ReturnConfirmation, SiteUser
# from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.conf import settings

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'quantity']

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.get('disabled_fields')
        if disabled_fields is not None:
            del kwargs['disabled_fields']
        super().__init__(*args, **kwargs)
        if disabled_fields:
            for field in self.fields:
                self.fields[field].disabled = True


class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = ['product', 'site_user', 'quantity','summ', 'created_at']

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.get('disabled_fields')
        if disabled_fields is not None:
            del kwargs['disabled_fields']
        super().__init__(*args, **kwargs)
        if disabled_fields:
            for field in self.fields:
                self.fields[field].disabled = True


class ReturnConfirmationForm(forms.ModelForm):
    class Meta:
        model = ReturnConfirmation
        fields = ['buy', 'site_user', 'created_at']

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.get('disabled_fields')
        if disabled_fields is not None:
            del kwargs['disabled_fields']
        super().__init__(*args, **kwargs)
        if disabled_fields:
            for field in self.fields:
                self.fields[field].disabled = True



class MyRegisterForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
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
        fields = ['username', 'password1', 'password2', 'money']

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
        user.money = settings.USER_MONEY
        if commit:
            user.save()
        return user