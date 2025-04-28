from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('kdsu.companies.orders.urls')),
    path("companies/", include("kdsu.companies.catalogs.urls")),
    path("", include("kdsu.companies.utils.urls")),
    path('api/', include('kdsu.companies.api_urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
