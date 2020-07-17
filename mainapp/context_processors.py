from mainapp.models import ProductCategory


def menu(request):
    menu = ProductCategory.objects.filter(is_active=True)
    return {
        'categories': menu,
    }
