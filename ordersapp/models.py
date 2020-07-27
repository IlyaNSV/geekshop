from django.contrib.auth import get_user_model
from django.db import models
from authapp.models import ShopUser
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEED, 'оплачен'),
        (PAID, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменён'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now=True)
    status = models.CharField(verbose_name='Статус',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x:x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.all()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x:x.quantity*x.product.price, items)))

    # def delete(self):
    #     for item in self.orderitems.all():
    #         item.product.quantity += item.quantity
    #         item.product.save()
    #     self.is_active = False
    #     self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity
