from django.utils import timezone

from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# from django.utils import timezone
# from django.utils.translation import gettext as _


class SiteUser(AbstractUser):
    money = models.IntegerField()
    
    # def save(self, **kwargs):
    #     self.money = 10000
    #     super().save(**kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.TextField(max_length=10000, null=True)
    img_url = models.ImageField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    slug = models.SlugField(max_length=50, null=True, unique=True, db_index=True)
    
    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)
    
    def __str__(self):
        return "Title: {}; quantity: {}; price:{}".format(self.title, self.quantity, self.price)


class Buy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name='products')
    siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=False, related_name='buy_users')
    quantity = models.IntegerField()
    summ = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.created_at = timezone.now()
    #     return super().save(*args, **kwargs)
    
    def __str__(self):
        return "product: {}; siteUser: {}; quantity:{}".format(self.product, self.siteUser, self.quantity)


class ReturnConfirmation(models.Model):
    buy = models.OneToOneField(Buy, on_delete=models.CASCADE, null=False, related_name='buy_returns')
    siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=False, related_name='return_users')
    created_at = models.DateTimeField(default=timezone.now)
    
    # def save(self, **kwargs):
    #     self.created_at = timezone.now()
    #     super().save(**kwargs)
    
    def __str__(self):
        return "buy: {}; created_at:{}".format(self.buy, self.created_at)
    
    # если подтвержден возврат то удалить покупку, вернуть количество товару, удалить возрват
    # если отклонен возврат то удалить обьект возврата
