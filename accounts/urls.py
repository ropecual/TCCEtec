from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserListView, UserUpdateView

urlpatterns = [
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout/', CustomLogoutView.as_view(), name='logout'),

	path("usuarios/", UserListView.as_view(), name="user_list"),
	path("usuarios/<int:pk>/editar/", UserUpdateView.as_view(), name="user_update"),
]
