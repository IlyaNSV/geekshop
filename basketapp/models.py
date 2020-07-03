from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # _items = self.user.basket_set.all()
        # _items = self.user.basket.all()
        #return sum(map(lambda x: x.quantity, self.user.basket.all()))
        return sum(self.user.basket.values_list('quantity', flat=True))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.user.basket.all()))
