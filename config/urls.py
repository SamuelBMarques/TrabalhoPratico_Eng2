from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quadras/", include("quadras.urls")),
    path("reservas/", include("reservas.urls")),
    path("", include("usuarios.urls")),
]