from django.core.validators import MinValueValidator
from django.utils import timezone

from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# from django.utils import timezone
# from django.utils.translation import gettext as _


class SiteUser(AbstractUser):
    money = models.PositiveIntegerField()
    
    # def save(self, **kwargs):
    #     self.money = 10000
    #     super().save(**kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.TextField(max_length=10000, null=True)
    img_url = models.ImageField()
    price = models.IntegerField()
    quantity = models.PositiveIntegerField()
    # slug = models.SlugField(max_length=50, null=True, unique=True, db_index=True)
    slug = models.SlugField(unique=True)
    
    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)
    
    def __str__(self):
        return "Title: {}; quantity: {}; price:{}".format(self.title, self.quantity, self.price)


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name='product_purchases')
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=False, related_name='user_purchases')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    summ = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.created_at = timezone.now()
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return "product: {}; siteUser: {}; quantity:{}".format(self.product, self.site_user, self.quantity)


class ReturnConfirmation(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, null=False, related_name='returns_purchases')
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=False, related_name='return_users')
    created_at = models.DateTimeField(default=timezone.now)

    # def save(self, **kwargs):
    #     self.created_at = timezone.now()
    #     super().save(**kwargs)

    def __str__(self):
        return "purchase: {}; created_at:{}".format(self.purchase, self.created_at)

    # если подтвержден возврат то удалить покупку, вернуть количество товару, удалить возрват
    # если отклонен возврат то удалить обьект возврата
