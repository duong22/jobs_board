from rest_framework import generics, permissions
from job_board.models.candidate import CandidateProfile
from job_board.models.employer import EmployerProfile
from .serializers import CandidateProfileSerializer, EmployerProfileSerializer

class CandidateProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование профиля кандидата[cite: 51].
    """
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Находим профиль CandidateProfile по текущему юзеру [cite: 3]
        return CandidateProfile.objects.get(user=self.request.user)

class EmployerProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование профиля работодателя[cite: 51].
    """
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Находим профиль EmployerProfile по текущему юзеру [cite: 16]
        return EmployerProfile.objects.get(user=self.request.user)