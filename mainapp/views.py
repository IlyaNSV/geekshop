from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', context)


def contacts(request):
    context = {
        'page_title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context)


def catalog(request):
    context = {
        'page_title': 'Каталог',
    }
    return render(request, 'mainapp/catalog.html', context)
