from django import forms

from myapp.models import Product, Buy, ReturnСonfirmation


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'content', 'price','quantity']
    
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
        fields = ['product', 'siteUser', 'quantity,summ', 'created_at']
    
    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.get('disabled_fields')
        if disabled_fields is not None:
            del kwargs['disabled_fields']
        super().__init__(*args, **kwargs)
        if disabled_fields:
            for field in self.fields:
                self.fields[field].disabled = True


class ReturnСonfirmationForm(forms.ModelForm):
    class Meta:
        model = ReturnСonfirmation
        fields = ['buy', 'siteUser', 'quantity,summ', 'created_at']
    
    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.get('disabled_fields')
        if disabled_fields is not None:
            del kwargs['disabled_fields']
        super().__init__(*args, **kwargs)
        if disabled_fields:
            for field in self.fields:
                self.fields[field].disabled = True

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

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
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            # дать права юзера права
            
            user.save()
            
        return user