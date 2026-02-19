from django.urls import path
from .views import (
    CondominioListView,
    CondominioCreateView,
    CondominioUpdateView,
    CondominioDeleteView,
)


urlpatterns = [
    path("condominios/", CondominioListView.as_view(), name="condominio_list"),
    path("condominios/novo/", CondominioCreateView.as_view(), name="condominio_create"),
    path("condominios/<int:pk>/editar/", CondominioUpdateView.as_view(), name="condominio_update"),
    path("condominios/<int:pk>/excluir/", CondominioDeleteView.as_view(), name="condominio_delete"),

]
