from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminProductCategoryUpdateForm, \
    AdminProductUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class ShopUserList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'title': 'пользователи/создание',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=int(pk))
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'пользователи/редактирование',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=int(pk))

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    categories = ProductCategory.objects.all()
    context = {
        'title': 'админка/категории',
        'object_list': categories,
    }
    return render(request, 'adminapp/categories_list.html', context)


class ProductCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'Новая категория'


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'категории/редактирование'
    #     print(context)
    #     return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)

class ProductCategoryDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all()
    context = {
        'title': f'продукты категории {category.name}',
        'object_list': object_list,
        'category': category,
    }
    return render(request, 'adminapp/category_products_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products', kwargs={'pk': category.pk}
            ))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
            }
        )

    context = {
        'title': 'продукты/создание',
        'form': form,
        'category': category,
    }

    return render(request, 'mainapp/product_form.html', context)


class ProductUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = Product
    form_class = AdminProductUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты/редактирование'
        context['object'] = self.get_object()
        return context

    def get_success_url(self):
        self.object = self.get_object()

        return reverse(
            'my_admin:category_products', kwargs={'pk': self.object.category.pk}
        )


class ProductDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = Product

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy(
            'my_admin:category_products', kwargs={'pk': self.object.category.pk}
        ))


class ProductDetailView(DetailView, PageTitleMixin, ):
    model = Product
    pk_url_kwarg = 'product_pk'


def db_profile_by_query_type(prefix, query_type, queries):
    update_queries = list(filter(lambda x: query_type in x['sql'], queries))
    print(f'db_profile {query_type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(post_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_query_type(sender, 'UPDATE', connection.queries)
# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': 'админка/пользователи',
#         'object_list': users_list,
#     }
#
#     return render(request, 'adminapp/index.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = AdminProductCategoryUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminProductCategoryUpdateForm()
#
#     context = {
#         'title': 'категории продуктов/создание',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_update(request, pk):
#     obj = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductCategoryUpdateForm(request.POST, request.FILES, instance=obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminProductCategoryUpdateForm(instance=obj)
#
#     context = {
#         'title': 'категории продуктов/создание',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


# class ProductCreateView(SuperUserOnlyMixin, CreateView):
#     model = Product
#     form_class = AdminProductUpdateForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Продукты/редактирование'
#         context['object'] = self.get_object()
#         context['object.category'] = kwargs['pk']
#         return context
#
#     def get_success_url(self):
#         return reverse(
#             'my_admin:categories'
#         )

# success_url = HttpResponseRedirect(reverse_lazy(
#     'my_admin:category_products'
# ))


# @user_passes_test(lambda x: x.is_superuser)
# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'my_admin:category_products', kwargs={'pk': product.category.pk}
#             ))
#     else:
#         form = AdminProductUpdateForm(instance=product)
#
#     context = {
#         'title': 'продукты/редактирование',
#         'form': form,
#         'category': product.category,
#     }
#
#     return render(request, 'adminapp/product_form.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def product_delete(request, pk):
#     obj = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         obj.is_active = not obj.is_active
#         obj.save()
#         return HttpResponseRedirect(reverse(
#             'my_admin:category_products', kwargs={'pk': obj.category.pk}
#         ))
#
#     context = {
#         'title': 'продукты/удаление',
#         'object': obj,
#     }
#
#     return render(request, 'adminapp/product_delete.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def product_read(request, pk):
#     obj = get_object_or_404(Product, pk=pk)
#
#
#     context = {
#         'title': 'продукты/просмотр',
#         'object': obj,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_delete(request, pk):
#     obj = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         obj.is_active = not obj.is_active
#         obj.save()
#         return HttpResponseRedirect(reverse('my_admin:categories'))
#
#     context = {
#         'title': 'категории/удаление',
#         'object': obj,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)
