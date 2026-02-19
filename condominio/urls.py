from django.urls import path
from .views import (
    UnidadeListView,
    UnidadeCreateView,
    UnidadeUpdateView,
    UnidadeDeleteView,
)

urlpatterns = [
    path("unidades/", UnidadeListView.as_view(), name="unidade_list"),
    path("unidades/nova/", UnidadeCreateView.as_view(), name="unidade_create"),
    path("unidades/<int:pk>/editar/", UnidadeUpdateView.as_view(), name="unidade_update"),
    path("unidades/<int:pk>/excluir/", UnidadeDeleteView.as_view(), name="unidade_delete"),
]
