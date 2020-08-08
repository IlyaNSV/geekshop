from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('имя категории', max_length=64)
    description = models.TextField('описание категории', blank=True)
    is_active = models.BooleanField(db_index=True, default=True)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='категория продукта', on_delete=models.CASCADE)
    name = models.CharField('имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField('краткое описание', max_length=64, blank=True)
    desc = models.TextField('описание товара', blank=True)
    price = models.DecimalField('цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('количество на складе', default=0)
    is_active = models.BooleanField(db_index=True, default=True)

    @staticmethod
    def get_active_items(self):
        return Product.objects.filter(category__is_active=True, is_active=True)
