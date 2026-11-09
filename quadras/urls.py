from django.urls import path

from . import views

app_name = "quadras"

urlpatterns = [
    path("gerenciar/", views.gerenciar, name="gerenciar"),
    path("", views.lista, name="lista"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/desativar/", views.desativar, name="desativar"),
    path("<int:pk>/reativar/", views.reativar, name="reativar"),
    path("<int:quadra_id>/horarios/", views.horarios, name="horarios"),
    path("<int:quadra_id>/horarios/cadastro/", views.cadastrar_horario_view, name="cadastrar_horario"),
    path("horarios/<int:pk>/editar/", views.editar_horario_view, name="editar_horario"),
]
