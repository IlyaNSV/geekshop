import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.conf import settings


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'),
              'r',
              encoding='utf-8'
              ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill database with data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        categories_objs = [ProductCategory(**category) for category in categories]
        ProductCategory.objects.bulk_create(categories_objs)

        products = load_from_json('products')

        products_objs = []
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            products_objs.append(Product(**product))
        Product.objects.bulk_create(products_objs)


        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='admin@geekshop.local', password='geekbrains')
