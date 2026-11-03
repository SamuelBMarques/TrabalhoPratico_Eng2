from django.urls import path

from . import views

app_name = "quadras"

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("<int:pk>/editar/", views.editar, name="editar"),
]
