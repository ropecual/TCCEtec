import json
from datetime import datetime

from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from accounts.mixins import AdminRequiredMixin
from residuos.models import RegistroColeta, TipoResiduo


class AdminOnlyView(AdminRequiredMixin, TemplateView):
    template_name = "admin_area.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile

        queryset = RegistroColeta.objects.all()

        if profile.tipo == "MORADOR":
            queryset = queryset.filter(morador=user)

        mes_param = self.request.GET.get("mes")

        if mes_param:
            ano, mes = map(int, mes_param.split("-"))
            data_base = datetime(ano, mes, 1)
        else:
            data_base = timezone.now().replace(day=1)

        # Filtrar mês selecionado
        queryset = queryset.filter(
            data__year=data_base.year,
            data__month=data_base.month
        )

        # ===== CALCULAR NAVEGAÇÃO =====
        mes_anterior = (data_base - relativedelta(months=1)).strftime("%Y-%m")
        mes_proximo = (data_base + relativedelta(months=1)).strftime("%Y-%m")

        context["mes_anterior"] = mes_anterior
        context["mes_proximo"] = mes_proximo
        context["mes_selecionado"] = data_base.strftime("%Y-%m")

        # ===== AGRUPAR POR TIPO =====
        dados = (
            queryset
            .values('tipo_residuo')
            .annotate(total=Sum('quantidade'))
        )

        labels = []
        valores = []

        for tipo, _ in TipoResiduo.choices:
            labels.append(tipo.capitalize())
            total = next((item['total'] for item in dados if item['tipo_residuo'] == tipo), 0)
            valores.append(float(total) if total else 0)

        context["labels"] = json.dumps(labels)
        context["valores"] = json.dumps(valores)

        return context



class RankingView(AdminRequiredMixin, TemplateView):
    template_name = 'relatorios/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ranking = (
            RegistroColeta.objects
            .values('morador__username')
            .annotate(total=Sum('quantidade'))
            .order_by('-total')
        )

        context['ranking'] = ranking
        return context

