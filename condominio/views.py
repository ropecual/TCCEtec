from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.mixins import AdminRequiredMixin
from .models import Condominio


class CondominioListView(AdminRequiredMixin, ListView):
    model = Condominio
    template_name = "condominio/condominio_list.html"
    context_object_name = "condominios"


class CondominioCreateView(AdminRequiredMixin, CreateView):
    model = Condominio
    fields = ["nome", "endereco"]
    template_name = "condominio/condominio_form.html"
    success_url = reverse_lazy("condominio_list")


class CondominioUpdateView(AdminRequiredMixin, UpdateView):
    model = Condominio
    fields = ["nome", "endereco"]
    template_name = "condominio/condominio_form.html"
    success_url = reverse_lazy("condominio_list")


class CondominioDeleteView(AdminRequiredMixin, DeleteView):
    model = Condominio
    template_name = "condominio/condominio_delete.html"
    success_url = reverse_lazy("condominio_list")
