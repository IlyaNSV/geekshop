from django.shortcuts import render, get_object_or_404
from datetime import datetime
from mainapp.models import ProductCategory, Product

date = datetime.now()

def get_basket(request):
    return request.user.is_authenticated and request.user.basket.all() or []

def index(request):
    context = {
        'page_title': 'Главная',
        'year': date.year,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)


def contacts(request):
    context = {
        'page_title': 'Контакты',
        'year': date.year,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/contacts.html', context)


def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'Каталог',
        'products': products,
        'year': date.year,
        'categories': categories,
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/products.html', context)


def category_products(request, pk):
    categories = ProductCategory.objects.all()
    if pk == '0':
        category = {'pk': 0, 'name': 'Все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        pass
        products = category.product_set.all()

    context = {
        'page_title': 'каталог',
        'categories': categories,
        'products' : products,
        'category' : category,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/category_products.html', context)
