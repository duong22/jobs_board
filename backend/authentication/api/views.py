from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.models import User
from job_board.models.candidate import CandidateProfile
from job_board.models.employer import EmployerProfile
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    CandidateProfileSerializer,
    EmployerProfileSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,) 
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,) 
    serializer_class = ChangePasswordSerializer

class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Находим профиль, принадлежащий текущему залогиненному пользователю
        return CandidateProfile.objects.get(user=self.request.user)

class EmployerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Находим профиль работодателя, привязанный к текущему пользователю [cite: 16]
        return EmployerProfile.objects.get(user=self.request.user)