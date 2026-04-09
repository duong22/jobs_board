from django.urls import path
from .profile.views import CandidateProfileView, EmployerProfileView
from .job.views import JobDetailView, JobListCreateView, MyJobListView

urlpatterns = [
	path('profile/candidate/', CandidateProfileView.as_view(), name='candidate_profile'),
	path('profile/employer/', EmployerProfileView.as_view(), name='employer_profile'),
    path('jobs/', JobListCreateView.as_view(), name='job_list_create'),
    path('jobs/<uuid:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/me/', MyJobListView.as_view(), name='my_job_list')
]