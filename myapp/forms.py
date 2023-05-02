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
