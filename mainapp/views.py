from django.shortcuts import render
from datetime import datetime
# Create your views here.

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
    products = [
        {
            'name':'Carlione',
            'picture':'img/carlione.jpg',
            'price':'10000'
        },
        {
            'name': 'Palzileri',
            'picture': 'img/palzileri.jpg',
            'price': '12000'
        },
        {
            'name': 'Parlamenter',
            'picture': 'img/parlamenter.jpg',
            'price': '15000'
        },
    ]

    context = {
        'page_title': 'Каталог',
        'products': products,
        'year':date.year,
    }

    return render(request, 'mainapp/catalog.html', context)
