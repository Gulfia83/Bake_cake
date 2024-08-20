from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import index, lk, lk_order


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('lk', lk, name='lk'),
    path('lk-order', lk_order, name='lk-order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
