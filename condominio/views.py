from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.mixins import AdminRequiredMixin
from .models import Condominio, Bloco, UnidadeHabitacional
from .forms import CondominioForm, BlocoForm, UnidadeHabitacionalForm


class CondominioListView(AdminRequiredMixin, ListView):
	model = Condominio
	template_name = "condominio/condominio_list.html"
	context_object_name = "condominios"


class CondominioCreateView(AdminRequiredMixin, CreateView):
	model = Condominio
	form_class = CondominioForm
	template_name = "condominio/condominio_form.html"
	success_url = reverse_lazy("condominio_list")


class CondominioUpdateView(AdminRequiredMixin, UpdateView):
	model = Condominio
	form_class = CondominioForm
	template_name = "condominio/condominio_form.html"
	success_url = reverse_lazy("condominio_list")


class CondominioDeleteView(AdminRequiredMixin, DeleteView):
	model = Condominio
	template_name = "condominio/condominio_confirm_delete.html"
	success_url = reverse_lazy("condominio_list")


class BlocoListView(AdminRequiredMixin, ListView):
	model = Bloco
	template_name = "condominio/bloco_list.html"
	context_object_name = "blocos"


class BlocoCreateView(AdminRequiredMixin, CreateView):
	model = Bloco
	form_class = BlocoForm
	template_name = "condominio/bloco_form.html"
	success_url = reverse_lazy("bloco_list")


class BlocoUpdateView(AdminRequiredMixin, UpdateView):
	model = Bloco
	form_class = BlocoForm
	template_name = "condominio/bloco_form.html"
	success_url = reverse_lazy("bloco_list")


class BlocoDeleteView(AdminRequiredMixin, DeleteView):
	model = Bloco
	template_name = "condominio/bloco_confirm_delete.html"
	success_url = reverse_lazy("bloco_list")



class UnidadeListView(AdminRequiredMixin, ListView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_list.html"
    context_object_name = "unidades"


class UnidadeCreateView(AdminRequiredMixin, CreateView):
    model = UnidadeHabitacional
    form_class = UnidadeHabitacionalForm
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")


class UnidadeUpdateView(AdminRequiredMixin, UpdateView):
    model = UnidadeHabitacional
    form_class = UnidadeHabitacionalForm
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")


class UnidadeDeleteView(AdminRequiredMixin, DeleteView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_confirm_delete.html"
    success_url = reverse_lazy("unidade_list")