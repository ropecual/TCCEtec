from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.mixins import AdminRequiredMixin
from .models import UnidadeHabitacional


class UnidadeListView(AdminRequiredMixin, ListView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_list.html"
    context_object_name = "unidades"


class UnidadeCreateView(AdminRequiredMixin, CreateView):
    model = UnidadeHabitacional
    fields = ["numero", "condominio"]
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")


class UnidadeUpdateView(AdminRequiredMixin, UpdateView):
    model = UnidadeHabitacional
    fields = ["numero", "condominio"]
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")


class UnidadeDeleteView(AdminRequiredMixin, DeleteView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_confirm_delete.html"
    success_url = reverse_lazy("unidade_list")
