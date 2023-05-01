from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# from django.utils import timezone
# from django.utils.translation import gettext as _


class SiteUser(AbstractUser):
    money = models.IntegerField()


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.TextField(max_length=10000, null=True)
    img_url = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()


class Buy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False, related_name='products')
    siteUser = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, null=False, related_name='buy_users')
    quantity = models.IntegerField()
    summ = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Return(models.Model):
    buy = models.ForeignKey(Buy, on_delete=models.DO_NOTHING, null=False, related_name='buy_returns')
    siteUser = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, null=False, related_name='return_users')
    created_at = models.DateTimeField(auto_now_add=True)
