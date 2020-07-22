from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from ordersapp.models import Order


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        # return self.model.objects.filter(user=self.request.user)
        return self.request.user.order_set.all()