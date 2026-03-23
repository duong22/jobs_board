from django.urls import path
from .api.views import RegisterView, ChangePasswordView, LogoutView, LoginView

urlpatterns = [
	path('login/', LoginView.as_view(), name='token_obtain_pair'),
	path('register/', RegisterView.as_view(), name='auth_register'),
	path('change_password/<uuid:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
	path('logout/', LogoutView.as_view(), name='auth_logout')
]