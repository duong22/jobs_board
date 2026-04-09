from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from .serializers import CandidateProfileSerializer, EmployerProfileSerializer

class CandidateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateProfileSerializer

    def get_object(self):
        if self.request.user.role != "candidate":
            raise PermissionDenied("Only candidate can access this profile.")
        return self.request.user.candidate_profile


class EmployerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployerProfileSerializer

    def get_object(self):
        if self.request.user.role != "employer":
            raise PermissionDenied("Only employer can access this profile.")
        return self.request.user.employer_profile