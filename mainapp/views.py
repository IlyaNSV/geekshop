from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from django.urls import re_path
from django.views.generic import TemplateView, DetailView

from adminapp.views import PageTitleMixin
from mainapp.models import ProductCategory, Product

date = datetime.now()


# def index(request):
#     context = {
#         'page_title': 'Главная',
#         'year': date.year,
#     }
#     return render(request, 'mainapp/index.html', context)

class IndexView(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['year'] = date.year
        context['page_title'] = 'Главная'
        return context


# def contacts(request):
#     context = {
#         'page_title': 'Контакты',
#         'year': date.year,
#     }
#     return render(request, 'mainapp/contacts.html', context)

class ContactsView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['year'] = date.year
        context['page_title'] = 'Контакты'
        return context


# def products(request):
#     products = Product.objects.filter(is_active=True)
#
#     context = {
#         'page_title': 'Каталог',
#         'products': products,
#         'year': date.year,
#     }
#
#     return render(request, 'mainapp/products.html', context)


def category_products(request, pk, page=1):
    if pk == '0':
        category = {'pk': 0, 'name': 'Все'}
        products = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        pass
        products = category.product_set.filter(is_active=True)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'каталог',
        'products': products,
        'category': category,
    }
    return render(request, 'mainapp/category_products.html', context)


# def product_page(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'page_title': 'каталог',
#         'category': product.category,
#         'product': product,
#     }
#
#     return render(request, 'mainapp/product_detail.html', context)

class ProductDetailView(DetailView, PageTitleMixin, ):
    model = Product
    pk_url_kwarg = 'pk'


def product_detail_async(request, pk):
    if request.is_ajax():
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({
                'product_price': product.price,
            })
        except Exception as e:
            return JsonResponse({
                    'error': str(e),
                })
