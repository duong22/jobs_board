from rest_framework import generics, permissions
from job_board.models.candidate import CandidateProfile
from job_board.models.employer import EmployerProfile
from .serializers import CandidateProfileSerializer, EmployerProfileSerializer

class CandidateProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CandidateProfile.objects.get(user=self.request.user)

class EmployerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)