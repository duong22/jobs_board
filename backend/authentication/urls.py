from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api.views import RegisterView, ChangePasswordView, LogoutView, LoginView

urlpatterns = [
	path('login/', LoginView.as_view(), name='token_obtain_pair'),
	path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('register/', RegisterView.as_view(), name='auth_register'),
	path('change_password/<uuid:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
	path('logout/', LogoutView.as_view(), name='auth_logout')
]