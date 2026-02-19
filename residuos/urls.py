from django.urls import path
from .views import RegistroCreateView, RegistroListView

urlpatterns = [
    path('registrar/', RegistroCreateView.as_view(), name='registrar_residuo'),
    path('meus-registros/', RegistroListView.as_view(), name='meus_registros'),
]
