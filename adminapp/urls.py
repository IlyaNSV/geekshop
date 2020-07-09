from django.contrib import admin
from django.urls import path, re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('category/list/', adminapp.categories, name='categories'),
    path('category/create/', adminapp.category_create, name='category_create'),
    path('category/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('category/<int:pk>/products/', adminapp.category_products, name='category_products'),
]
