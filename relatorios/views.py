from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from accounts.mixins import AdminRequiredMixin
from residuos.models import RegistroColeta



class AdminOnlyView(AdminRequiredMixin, TemplateView):
    template_name = "admin_area.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile

        # Se for ADMIN → visão global
        if profile.tipo == "ADMIN":
            total_kg = RegistroColeta.objects.aggregate(
                total=Sum('quantidade')
            )['total'] or 0

            por_tipo = (
                RegistroColeta.objects
                .values('tipo_residuo')
                .annotate(total=Sum('quantidade'))
            )

        # Se for MORADOR → visão individual
        else:
            total_kg = RegistroColeta.objects.filter(
                morador=user
            ).aggregate(
                total=Sum('quantidade')
            )['total'] or 0

            por_tipo = (
                RegistroColeta.objects
                .filter(morador=user)
                .values('tipo_residuo')
                .annotate(total=Sum('quantidade'))
            )

        context['total_kg'] = total_kg
        context['por_tipo'] = por_tipo
        context['tipo_usuario'] = profile.tipo

        return context
