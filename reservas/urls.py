from django.urls import path

from . import views

app_name = "reservas"

urlpatterns = [
    path("quadras/<int:quadra_id>/horarios/", views.horarios, name="horarios"),
    path("quadras/<int:quadra_id>/reservar/", views.reservar, name="reservar"),
    path("minhas/", views.minhas, name="minhas"),
    path("<int:reserva_id>/cancelar/", views.cancelar, name="cancelar"),
    path("<int:reserva_id>/editar/", views.editar, name="editar"),
]
