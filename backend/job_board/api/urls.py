from .profile.views import CandidateProfileView, EmployerProfileView
from django.urls import path

urlpatterns = [
	path('profile/candidate/', CandidateProfileView.as_view(), name='candidate_profile'),
	path('profile/employer/', EmployerProfileView.as_view(), name='employer_profile'),
]