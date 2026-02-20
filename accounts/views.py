from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from accounts.mixins import AdminRequiredMixin, SindicoOrAdminMixin
from condominio.models import UnidadeHabitacional, Condominio
from .forms import UserCreateForm, ProfileForm, UserUpdateForm


# ------------------------
# LOGIN / LOGOUT
# ------------------------

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


# ------------------------
# LISTAGEM DE USUÁRIOS
# ------------------------

class UserListView(SindicoOrAdminMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return User.objects.all()

        # SINDICO
        return User.objects.filter(
            profile__unidade__bloco__condominio=user.profile.condominio
        )


# ------------------------
# CRIAÇÃO DE USUÁRIO
# ------------------------

class UserCreateView(SindicoOrAdminMixin, View):

    template_name = "accounts/user_create.html"

    def get(self, request):

        user_form = UserCreateForm()
        profile_form = ProfileForm()

        if request.user.profile.tipo == "SINDICO":
            # Síndico só pode criar moradores do próprio condomínio
            profile_form.fields["condominio"].queryset = Condominio.objects.filter(
                id=request.user.profile.condominio.id
            )

            profile_form.fields["unidade"].queryset = (
                UnidadeHabitacional.objects.filter(
                    bloco__condominio=request.user.profile.condominio
                )
            )

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })

    def post(self, request):

        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if request.user.profile.tipo == "SINDICO":
            profile_form.fields["unidade"].queryset = (
                UnidadeHabitacional.objects.filter(
                    bloco__condominio=request.user.profile.condominio
                )
            )

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            profile = user.profile
            profile.tipo = profile_form.cleaned_data["tipo"]
            profile.condominio = profile_form.cleaned_data["condominio"]
            profile.unidade = profile_form.cleaned_data["unidade"]

            # Regra de coerência
            if profile.tipo == "SINDICO":
                profile.unidade = None
            elif profile.tipo == "MORADOR":
                profile.condominio = None

            profile.save()

            return redirect("user_list")


# ------------------------
# EDIÇÃO DE USUÁRIO
# ------------------------

from django.core.exceptions import PermissionDenied
from condominio.models import UnidadeHabitacional, Condominio


class UserUpdateView(SindicoOrAdminMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_queryset(self):
        user = self.request.user

        if user.profile.tipo == "ADMIN":
            return User.objects.all()

        # Síndico só pode editar usuários do próprio condomínio
        return User.objects.filter(
            profile__unidade__bloco__condominio=user.profile.condominio
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_form = ProfileForm(instance=self.object.profile)

        request_user = self.request.user

        if request_user.profile.tipo == "SINDICO":

            # Síndico NÃO pode alterar condomínio
            profile_form.fields["condominio"].queryset = Condominio.objects.filter(
                id=request_user.profile.condominio.id
            )

            # Só unidades do próprio condomínio
            profile_form.fields["unidade"].queryset = (
                UnidadeHabitacional.objects.filter(
                    bloco__condominio=request_user.profile.condominio
                )
            )

            # Síndico não pode criar outro ADMIN
            profile_form.fields["tipo"].choices = [
                ('MORADOR', 'Morador'),
                ('SINDICO', 'Síndico'),
            ]

        context["profile_form"] = profile_form
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        user_form = UserUpdateForm(request.POST, instance=self.object)
        profile_form = ProfileForm(request.POST, instance=self.object.profile)

        request_user = request.user

        if request_user.profile.tipo == "SINDICO":

            profile_form.fields["condominio"].queryset = Condominio.objects.filter(
                id=request_user.profile.condominio.id
            )

            profile_form.fields["unidade"].queryset = (
                UnidadeHabitacional.objects.filter(
                    bloco__condominio=request_user.profile.condominio
                )
            )

            profile_form.fields["tipo"].choices = [
                ('MORADOR', 'Morador'),
                ('SINDICO', 'Síndico'),
            ]

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile = profile_form.save(commit=False)

            # Regras de coerência
            if profile.tipo == "SINDICO":
                profile.unidade = None
            elif profile.tipo == "MORADOR":
                profile.condominio = None

            profile.save()

            return redirect("user_list")

        context = self.get_context_data()
        context["form"] = user_form
        context["profile_form"] = profile_form
        return self.render_to_response(context)