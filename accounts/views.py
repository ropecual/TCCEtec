from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts.mixins import AdminRequiredMixin
from django.contrib.auth.models import User
from .forms import ProfileForm, UserUpdateForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')




class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "usuarios"


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