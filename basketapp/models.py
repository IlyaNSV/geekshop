from django.db import models
from django.utils.functional import cached_property

from authapp.models import ShopUser
from mainapp.models import Product


# class BasketQuerySet(models.QuerySet): #own model manager
#     def delete(self):
#         for object in self:
#             # object.product.quantity += object.quantity
#             # object.product.save()
#             object.delete()
#         return super().delete()


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # objects = BasketQuerySet.as_manager()

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related().all()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.get_items_cached))
        # return sum(self.user.basket.values_list('quantity', flat=True))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.get_items_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     pass

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     return super(Basket, self).delete(using=None, keep_parents=False)
