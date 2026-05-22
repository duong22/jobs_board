from django.urls import path
from .profile.views import CandidateProfileView, EmployerProfileView
from .job.views import JobDetailView, JobListCreateView, MyJobListView
from .application.views import ApplyJobView, ApplicationDetailView, ApplicationListView, ApplicationStatusUpdateView, ApplicationCVDownloadView

urlpatterns = [
	path('profile/candidate/', CandidateProfileView.as_view(), name='candidate_profile'),
	path('profile/employer/', EmployerProfileView.as_view(), name='employer_profile'),

    path('jobs/', JobListCreateView.as_view(), name='job_list_create'),
    path('jobs/<uuid:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/me/', MyJobListView.as_view(), name='my_job_list'),

    path('jobs/<uuid:pk>/apply/', ApplyJobView.as_view(), name='apply_job'),
    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/<uuid:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<uuid:pk>/status/', ApplicationStatusUpdateView.as_view(), name='application_status'),
    path('applications/<uuid:pk>/cv/', ApplicationCVDownloadView.as_view(), name='application_cv_download'),

]