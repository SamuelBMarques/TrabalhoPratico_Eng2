from django.urls import path

from . import views

app_name = "reservas"

urlpatterns = [
    path("quadras/<int:quadra_id>/horarios/", views.horarios, name="horarios"),
    path("quadras/<int:quadra_id>/reservar/", views.reservar, name="reservar"),
]
