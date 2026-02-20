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

        mes_param = self.request.GET.get("mes")

        if mes_param:
            ano, mes = map(int, mes_param.split("-"))
            data_base = datetime(ano, mes, 1)
        else:
            data_base = timezone.now().replace(day=1)

        context["mes_anterior"] = (data_base - relativedelta(months=1)).strftime("%Y-%m")
        context["mes_proximo"] = (data_base + relativedelta(months=1)).strftime("%Y-%m")
        context["mes_selecionado"] = data_base.strftime("%Y-%m")

        queryset_mes = RegistroColeta.objects.filter(
            data__year=data_base.year,
            data__month=data_base.month
        )

        # ============================================================
        # VISÃO MORADOR
        # ============================================================
        if profile.tipo == "MORADOR":

            unidade = profile.unidade
            bloco = unidade.bloco if unidade else None

            queryset_unidade = queryset_mes.filter(
                morador__profile__unidade=unidade
            )

            queryset_bloco = queryset_mes.filter(
                morador__profile__unidade__bloco=bloco
            )

            total_individual = queryset_mes.filter(
                morador=user
            ).aggregate(total=Sum("quantidade"))["total"] or 0

            total_unidade = queryset_unidade.aggregate(
                total=Sum("quantidade")
            )["total"] or 0

            total_bloco = queryset_bloco.aggregate(
                total=Sum("quantidade")
            )["total"] or 0

            context["total_individual"] = round(total_individual, 2)
            context["total_unidade"] = round(total_unidade, 2)
            context["total_bloco"] = round(total_bloco, 2)

            # ===============================
            # PERCENTUAIS
            # ===============================
            context["percent_individual"] = (
                round((total_individual / total_unidade) * 100, 1)
                if total_unidade > 0 else 0
            )

            context["percent_unidade"] = (
                round((total_unidade / total_bloco) * 100, 1)
                if total_bloco > 0 else 0
            )

            # ===============================
            # RANKING DE UNIDADES NO BLOCO
            # ===============================
            ranking_unidades = (
                queryset_bloco
                .values("morador__profile__unidade__id",
                        "morador__profile__unidade__numero")
                .annotate(total=Sum("quantidade"))
                .order_by("-total")
            )

            posicao = 0
            for index, item in enumerate(ranking_unidades, start=1):
                if item["morador__profile__unidade__id"] == unidade.id:
                    posicao = index
                    break

            context["posicao_unidade"] = posicao

            # ===============================
            # GRÁFICO MORADORES (mantido)
            # ===============================
            moradores = (
                queryset_unidade
                .values("morador__id", "morador__username")
                .distinct()
            )

            labels = [m["morador__username"] for m in moradores]

            datasets = []

            cores = [
                "rgba(54, 162, 235, 0.7)",
                "rgba(255, 99, 132, 0.7)",
                "rgba(75, 192, 192, 0.7)",
                "rgba(153, 102, 255, 0.7)",
                "rgba(255, 206, 86, 0.7)",
                "rgba(201, 203, 207, 0.7)",
            ]

            for index, (tipo, nome_legivel) in enumerate(TipoResiduo.choices):
                valores = []
                for morador in moradores:
                    total = queryset_unidade.filter(
                        morador__id=morador["morador__id"],
                        tipo_residuo=tipo
                    ).aggregate(total=Sum("quantidade"))["total"] or 0
                    valores.append(float(total))

                datasets.append({
                    "label": nome_legivel,
                    "data": valores,
                    "backgroundColor": cores[index % len(cores)],
                })

            context["labels"] = json.dumps(labels)
            context["datasets"] = json.dumps(datasets)

            # ===============================
            # RANKING DE BLOCOS (para gráfico)
            # ===============================
            ranking_blocos = (
                queryset_mes
                .values("morador__profile__unidade__bloco__nome")
                .annotate(total=Sum("quantidade"))
                .order_by("-total")
            )

            blocos_labels = [
                item["morador__profile__unidade__bloco__nome"]
                for item in ranking_blocos
            ]

            blocos_valores = [
                float(item["total"]) for item in ranking_blocos
            ]

            context["blocos_labels"] = json.dumps(blocos_labels)
            context["blocos_valores"] = json.dumps(blocos_valores)

        return context