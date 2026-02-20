import json
from datetime import datetime

from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from dateutil.relativedelta import relativedelta

from residuos.models import RegistroColeta, TipoResiduo
from condominio.models import Condominio


class DashboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        tipo = self.request.user.profile.tipo

        if tipo == "MORADOR":
            return ["dashboard_morador.html"]
        elif tipo == "SINDICO":
            return ["dashboard_sindico.html"]
        elif tipo == "ADMIN":
            return ["dashboard_admin.html"]

        return ["dashboard_morador.html"]

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

        tipo = profile.tipo

        if tipo == "MORADOR":
            context.update(self._dashboard_morador(queryset_mes, user))

        elif tipo == "SINDICO":
            context.update(self._dashboard_sindico(queryset_mes, profile))

        elif tipo == "ADMIN":
            context.update(self._dashboard_admin(queryset_mes))

        return context

    # ============================================================
    # MORADOR
    # ============================================================

    def _dashboard_morador(self, queryset_mes, user):

        profile = user.profile
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

        percent_individual = (
            round((total_individual / total_unidade) * 100, 1)
            if total_unidade > 0 else 0
        )

        percent_unidade = (
            round((total_unidade / total_bloco) * 100, 1)
            if total_bloco > 0 else 0
        )

        # Ranking unidade no bloco
        ranking_unidades = (
            queryset_bloco
            .values("morador__profile__unidade__id")
            .annotate(total=Sum("quantidade"))
            .order_by("-total")
        )

        posicao = 0
        for index, item in enumerate(ranking_unidades, start=1):
            if item["morador__profile__unidade__id"] == unidade.id:
                posicao = index
                break

        return {
            "total_individual": round(total_individual, 2),
            "total_unidade": round(total_unidade, 2),
            "total_bloco": round(total_bloco, 2),
            "percent_individual": percent_individual,
            "percent_unidade": percent_unidade,
            "posicao_unidade": posicao,
        }

    # ============================================================
    # SÍNDICO
    # ============================================================

    def _dashboard_sindico(self, queryset_mes, profile):

        condominio = profile.condominio

        queryset_condominio = queryset_mes.filter(
            morador__profile__unidade__bloco__condominio=condominio
        )

        # =============================
        # TOTAL DO CONDOMÍNIO
        # =============================
        total_condominio = queryset_condominio.aggregate(
            total=Sum("quantidade")
        )["total"] or 0

        # =============================
        # RANKING DE BLOCOS
        # =============================
        ranking_blocos = list(
            queryset_condominio
            .values("morador__profile__unidade__bloco__nome")
            .annotate(total=Sum("quantidade"))
            .order_by("-total")
        )

        # =============================
        # RANKING DE UNIDADES
        # =============================
        ranking_unidades = list(
            queryset_condominio
            .values(
                "morador__profile__unidade__bloco__nome",
                "morador__profile__unidade__numero"
            )
            .annotate(total=Sum("quantidade"))
            .order_by("-total")
        )

        # =============================
        # GRÁFICO BLOCOS
        # =============================
        blocos_labels = [
            item["morador__profile__unidade__bloco__nome"]
            for item in ranking_blocos
        ]

        blocos_valores = [
            float(item["total"])
            for item in ranking_blocos
        ]

        # =============================
        # GRÁFICO UNIDADES
        # =============================
        unidades_labels = [
            f'{item["morador__profile__unidade__bloco__nome"]} - {item["morador__profile__unidade__numero"]}'
            for item in ranking_unidades
        ]

        unidades_valores = [
            float(item["total"])
            for item in ranking_unidades
        ]

        return {
            "total_condominio": round(total_condominio, 2),
            "ranking_blocos": ranking_blocos,
            "ranking_unidades": ranking_unidades,
            "blocos_labels": json.dumps(blocos_labels),
            "blocos_valores": json.dumps(blocos_valores),
            "unidades_labels": json.dumps(unidades_labels),
            "unidades_valores": json.dumps(unidades_valores),
        }

    # ============================================================
    # ADMIN
    # ============================================================

    def _dashboard_morador(self, queryset_mes, user):

        profile = user.profile
        unidade = profile.unidade
        bloco = unidade.bloco if unidade else None

        if not unidade:
            return {}

        queryset_unidade = queryset_mes.filter(
            morador__profile__unidade=unidade
        )

        queryset_bloco = queryset_mes.filter(
            morador__profile__unidade__bloco=bloco
        )

        # =============================
        # TOTAIS
        # =============================
        total_individual = queryset_mes.filter(
            morador=user
        ).aggregate(total=Sum("quantidade"))["total"] or 0

        total_unidade = queryset_unidade.aggregate(
            total=Sum("quantidade")
        )["total"] or 0

        total_bloco = queryset_bloco.aggregate(
            total=Sum("quantidade")
        )["total"] or 0

        percent_individual = (
            round((total_individual / total_unidade) * 100, 1)
            if total_unidade > 0 else 0
        )

        percent_unidade = (
            round((total_unidade / total_bloco) * 100, 1)
            if total_bloco > 0 else 0
        )

        # =============================
        # RANKING UNIDADE NO BLOCO
        # =============================
        ranking_unidades = (
            queryset_bloco
            .values(
                "morador__profile__unidade__id",
                "morador__profile__unidade__numero"
            )
            .annotate(total=Sum("quantidade"))
            .order_by("-total")
        )

        posicao = 0
        for index, item in enumerate(ranking_unidades, start=1):
            if item["morador__profile__unidade__id"] == unidade.id:
                posicao = index
                break

        # =============================
        # GRÁFICO 1 — UNIDADE POR MORADOR (STACKED)
        # =============================

        moradores = (
            queryset_unidade
            .values("morador__id", "morador__username")
            .distinct()
        )

        labels = [m["morador__username"] for m in moradores]

        cores = [
            "rgba(54, 162, 235, 0.7)",
            "rgba(255, 99, 132, 0.7)",
            "rgba(75, 192, 192, 0.7)",
            "rgba(153, 102, 255, 0.7)",
            "rgba(255, 206, 86, 0.7)",
            "rgba(201, 203, 207, 0.7)",
        ]

        datasets = []

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

        # =============================
        # GRÁFICO 2 — RANKING DE BLOCOS
        # =============================

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

        return {
            "total_individual": round(total_individual, 2),
            "total_unidade": round(total_unidade, 2),
            "total_bloco": round(total_bloco, 2),
            "percent_individual": percent_individual,
            "percent_unidade": percent_unidade,
            "posicao_unidade": posicao,
            "labels": json.dumps(labels),
            "datasets": json.dumps(datasets),
            "blocos_labels": json.dumps(blocos_labels),
            "blocos_valores": json.dumps(blocos_valores),
        }