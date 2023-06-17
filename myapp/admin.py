from django.contrib import admin

from myapp.models import SiteUser, Product, Purchase, ReturnConfirmation

admin.site.register(SiteUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(ReturnConfirmation)
