from django.contrib import admin
from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.index, name='index'),
    path('', mainapp.IndexView.as_view(), name='index'),
    # path('products/', mainapp.products, name='products'),

    re_path(r'^category/(?P<pk>\d+)/products/$',
            mainapp.category_products, name='category_products'),

    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/$',
            mainapp.category_products, name='category_products_pagination'),

    re_path(r'^product/(?P<pk>\d+)/$',
            mainapp.product_page, name='product_page'),

    # re_path(r'^product/(?P<pk>\d+)/$',
    #         mainapp.ProductDetailView.as_view(), name='product_page'),

    re_path(r'^product/detail/(?P<pk>\d+)/async/$',
            mainapp.product_detail_async),

    # path('contacts/', mainapp.contacts, name='contacts'),
    path('contacts/', mainapp.ContactsView.as_view(), name='contacts'),
]
