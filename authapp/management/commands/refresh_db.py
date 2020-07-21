import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategory, Product
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_to_update = ShopUser.objects.filter(shopuserprofile__isnull=True)
        for user in users_to_update:
            ShopUserProfile.objects.create(user=user)
