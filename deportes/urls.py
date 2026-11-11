from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # login/ y logout/ de Django (django.contrib.auth)
    path("cuentas/", include("django.contrib.auth.urls")),
    path("", include("reservas.urls")),
]
