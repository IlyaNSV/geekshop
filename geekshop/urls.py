from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import mainapp.views as mainapp

urlpatterns = [
    path('', include('mainapp.urls', namespace='main')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('my/admin/', include('adminapp.urls', namespace='my_admin')),
    path('auth/register/', include('social_django.urls', namespace='social')),
    path('orders/', include('ordersapp.urls', namespace='orders')),

    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
