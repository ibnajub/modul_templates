from django.contrib import admin

from myapp.models import SiteUser, Product, Buy, ReturnСonfirmation

admin.site.register(SiteUser)
admin.site.register(Product)
admin.site.register(Buy)
admin.site.register(ReturnСonfirmation)
