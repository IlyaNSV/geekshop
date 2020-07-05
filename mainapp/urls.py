from django.contrib import admin
from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/', mainapp.products, name='products'),

    re_path(r'category/(?P<pk>\d+)/products',
            mainapp.category_products, name='category_products'),

    re_path(r'^product/(?P<pk>\d+)/S',
            mainapp.product_page, name='product_page'),

    path('contacts/', mainapp.contacts, name='contacts'),
]
