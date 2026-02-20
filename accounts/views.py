from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from accounts.mixins import AdminRequiredMixin
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

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "usuarios"


# ------------------------
# CRIAÇÃO DE USUÁRIO
# ------------------------

class UserCreateView(AdminRequiredMixin, View):

    template_name = "accounts/user_create.html"

    def get(self, request):
        user_form = UserCreateForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })

    def post(self, request):
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Criar usuário
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            # Atualizar profile criado pelo signal
            profile = user.profile
            profile.tipo = profile_form.cleaned_data["tipo"]
            profile.unidade = profile_form.cleaned_data["unidade"]
            profile.save()

            return redirect("user_list")

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })


# ------------------------
# EDIÇÃO DE USUÁRIO
# ------------------------

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = ProfileForm(instance=self.object.profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        user_form = UserUpdateForm(request.POST, instance=self.object)
        profile_form = ProfileForm(request.POST, instance=self.object.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("user_list")

        context = self.get_context_data()
        context["form"] = user_form
        context["profile_form"] = profile_form
        return self.render_to_response(context)