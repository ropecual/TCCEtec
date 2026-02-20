from django.urls import path
from .views import (
	CondominioListView,
	CondominioCreateView,
	CondominioUpdateView,
	CondominioDeleteView,
	BlocoListView,
	BlocoCreateView,
	BlocoUpdateView,
	BlocoDeleteView,
	UnidadeListView,
	UnidadeCreateView,
	UnidadeUpdateView,
	UnidadeDeleteView,
)

urlpatterns = [
	path("condominios/", CondominioListView.as_view(), name="condominio_list"),
	path("condominios/novo/", CondominioCreateView.as_view(), name="condominio_create"),
	path("condominios/<int:pk>/editar/", CondominioUpdateView.as_view(), name="condominio_update"),
	path("condominios/<int:pk>/excluir/", CondominioDeleteView.as_view(), name="condominio_delete"),

	path("blocos/", BlocoListView.as_view(), name="bloco_list"),
	path("blocos/novo/", BlocoCreateView.as_view(), name="bloco_create"),
	path("blocos/<int:pk>/editar/", BlocoUpdateView.as_view(), name="bloco_update"),
	path("blocos/<int:pk>/excluir/", BlocoDeleteView.as_view(), name="bloco_delete"),

	path("unidades/", UnidadeListView.as_view(), name="unidade_list"),
	path("unidades/nova/", UnidadeCreateView.as_view(), name="unidade_create"),
	path("unidades/<int:pk>/editar/", UnidadeUpdateView.as_view(), name="unidade_update"),
	path("unidades/<int:pk>/excluir/", UnidadeDeleteView.as_view(), name="unidade_delete"),

]
