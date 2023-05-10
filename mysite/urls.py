"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path

from myapp.views import IndexProduct, Login, LogOut, UserRegisterView, BuyList, ReturnConfirmationList, AddProduct, \
    ProductUpdate, SearchProdictResults, ProductDetail\
    # , BuyProduct
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', IndexProduct.as_view(), name='index'),
    path('addproduct/', AddProduct.as_view(), name='addproduct'),
    path('search_prodict_results/', SearchProdictResults.as_view(), name='search_prodict_results'),
    path('update_product/<slug:slug>/', ProductUpdate.as_view(), name='update_product'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    # path('buy_product/', BuyProduct.as_view(), name='buy_product'),
    path('buylist/', BuyList.as_view(), name='buylist'),
    path('returnconfirmationlist', ReturnConfirmationList.as_view(), name='returnconfirmationlist'),
    path('login/', Login.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('logout/', LogOut.as_view(), name='logout'),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)