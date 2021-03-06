from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.models import OrderItem


@login_required
def index(request):
    return render(request, 'basketapp/index.html')


@login_required
def add_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    # basket = request.user.basket_set.filter(product.pk = pk).first()

    if not basket:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        # basket.quantity += 1
        basket.quantity = F('quantity')+1
        # basket.product.quantity -= 1
        # basket.product.save()
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_product(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(reverse('basket:index'))


@login_required
def change(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = get_object_or_404(Basket, pk=int(pk))
        if quantity <= 0:
            basket.delete()
        else:
            basket.quantity = quantity
            basket.save()

        context = {
            'basket': request.user.basket.all(),
        }

        result = render_to_string('basketapp/includes/inc__basket_list.html', context)

        return JsonResponse({'result': result})
        # return JsonResponse({
        #     'total_cost': basket.total_cost,
        #     'total_quantity' : basket.total_quantity,
        #     'product_cost' : basket.product_cost,
        # })


# @receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    print(f' instance:{instance}, kwargs:{kwargs}')
    if instance.pk:
        instance.product.quantity -= instance.quantity - \
                                     sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


# @receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
