from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import RegistroColeta


class RegistroCreateView(LoginRequiredMixin, CreateView):
    model = RegistroColeta
    fields = ['tipo_residuo', 'quantidade']
    template_name = 'residuos/registro_form.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.tipo != "MORADOR":
            raise PermissionDenied("Apenas moradores podem registrar resíduos.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.morador = self.request.user
        return super().form_valid(form)



class RegistroListView(LoginRequiredMixin, ListView):
    model = RegistroColeta
    template_name = 'residuos/registro_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return RegistroColeta.objects.filter(
            morador=self.request.user
        ).order_by('-data')