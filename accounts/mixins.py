from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.profile.tipo != "ADMIN":
            raise PermissionDenied("Você não tem permissão para acessar esta área.")

        return super().dispatch(request, *args, **kwargs)



class SindicoOrAdminMixin:

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise PermissionDenied()

        if request.user.profile.tipo not in ["ADMIN", "SINDICO"]:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)