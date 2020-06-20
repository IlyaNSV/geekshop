from django.shortcuts import render
from datetime import datetime
from mainapp.models import ProductCategory , Product

date = datetime.now()

def index(request):
    context = {
        'page_title': 'Главная',
        'year':date.year,
    }
    return render(request, 'mainapp/index.html', context)


def contacts(request):
    context = {
        'page_title': 'Контакты',
        'year':date.year,
    }
    return render(request, 'mainapp/contacts.html', context)


def catalog(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()


    context = {
        'page_title': 'Каталог',
        'products': products,
        'year':date.year,
        'categories':categories,
    }

    return render(request, 'mainapp/catalog.html', context)
