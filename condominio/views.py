from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.mixins import AdminRequiredMixin, SindicoOrAdminMixin
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


class BlocoListView(SindicoOrAdminMixin, ListView):
    model = Bloco
    template_name = "condominio/bloco_list.html"
    context_object_name = "blocos"

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return Bloco.objects.all()

        # SINDICO
        return Bloco.objects.filter(
            condominio=user.profile.condominio
        )


class BlocoCreateView(SindicoOrAdminMixin, CreateView):
    model = Bloco
    form_class = BlocoForm
    template_name = "condominio/bloco_form.html"
    success_url = reverse_lazy("bloco_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.user.profile.tipo == "SINDICO":
            form.fields["condominio"].queryset = Condominio.objects.filter(
                id=self.request.user.profile.condominio.id
            )

        return form


class BlocoUpdateView(SindicoOrAdminMixin, UpdateView):
    model = Bloco
    form_class = BlocoForm
    template_name = "condominio/bloco_form.html"
    success_url = reverse_lazy("bloco_list")

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return Bloco.objects.all()

        return Bloco.objects.filter(
            condominio=user.profile.condominio
        )


class BlocoDeleteView(AdminRequiredMixin, DeleteView):
	model = Bloco
	template_name = "condominio/bloco_confirm_delete.html"
	success_url = reverse_lazy("bloco_list")



class UnidadeListView(SindicoOrAdminMixin, ListView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_list.html"
    context_object_name = "unidades"

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return UnidadeHabitacional.objects.all()

        return UnidadeHabitacional.objects.filter(
            bloco__condominio=user.profile.condominio
        )


class UnidadeCreateView(SindicoOrAdminMixin, CreateView):
    model = UnidadeHabitacional
    form_class = UnidadeHabitacionalForm
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.user.profile.tipo == "SINDICO":
            form.fields["bloco"].queryset = Bloco.objects.filter(
                condominio=self.request.user.profile.condominio
            )

        return form


class UnidadeUpdateView(SindicoOrAdminMixin, UpdateView):
    model = UnidadeHabitacional
    form_class = UnidadeHabitacionalForm
    template_name = "condominio/unidade_form.html"
    success_url = reverse_lazy("unidade_list")

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return UnidadeHabitacional.objects.all()

        return UnidadeHabitacional.objects.filter(
            bloco__condominio=user.profile.condominio
        )


class UnidadeDeleteView(AdminRequiredMixin, DeleteView):
    model = UnidadeHabitacional
    template_name = "condominio/unidade_confirm_delete.html"
    success_url = reverse_lazy("unidade_list")