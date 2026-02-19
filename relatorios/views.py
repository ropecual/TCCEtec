from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from accounts.mixins import AdminRequiredMixin
from residuos.models import RegistroColeta, TipoResiduo


class AdminOnlyView(AdminRequiredMixin, TemplateView):
    template_name = "admin_area.html"

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
import json



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile

        queryset = RegistroColeta.objects.all()

        if profile.tipo == "MORADOR":
            queryset = queryset.filter(morador=user)

        # Agrupar por mês e tipo
        dados = (
            queryset
            .annotate(mes=TruncMonth('data'))
            .values('mes', 'tipo_residuo')
            .annotate(total=Sum('quantidade'))
            .order_by('mes')
        )

        meses = sorted(set(item['mes'] for item in dados if item['mes']))

        labels = [mes.strftime('%b/%Y') for mes in meses]

        # Estrutura base
        datasets = {}

        for tipo, _ in TipoResiduo.choices:
            datasets[tipo] = [0] * len(meses)

        # Preencher dados
        for item in dados:
            mes_index = meses.index(item['mes'])
            datasets[item['tipo_residuo']][mes_index] = float(item['total'])

        # Converter para formato Chart.js
        chart_datasets = []

        cores = {
            'PAPEL': 'rgba(54, 162, 235, 0.7)',
            'PLASTICO': 'rgba(255, 99, 132, 0.7)',
            'VIDRO': 'rgba(75, 192, 192, 0.7)',
            'METAL': 'rgba(153, 102, 255, 0.7)',
            'ORGANICO': 'rgba(255, 206, 86, 0.7)',
            'OUTROS': 'rgba(201, 203, 207, 0.7)',
        }

        for tipo, valores in datasets.items():
            chart_datasets.append({
                'label': tipo.capitalize(),
                'data': valores,
                'backgroundColor': cores.get(tipo, 'rgba(0,0,0,0.5)')
            })

        context['labels'] = json.dumps(labels)
        context['datasets'] = json.dumps(chart_datasets)

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

