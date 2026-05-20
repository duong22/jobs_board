from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from job_board.models.job import Job
from job_board.models.application import Application
from .serializers import ApplicationSerializer, ApplicationStatusSerializer

def require_candidate(user):
    if user.role != 'candidate':
        raise PermissionDenied('Only candidates can apply for jobs.')

def require_employer(user):
    if user.role != 'employer':
        raise PermissionDenied('Only employers can perform this action.')

class ApplyJobView(generics.CreateAPIView):
    serializer_class   = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        require_candidate(self.request.user)

        try:
            job = Job.objects.get(pk=self.kwargs['pk'])
        except Job.DoesNotExist:
            raise NotFound('Job not found.')

        if job.status != 'open':
            raise ValidationError('This job is no longer accepting applications.')

        candidate = self.request.user.candidate_profile

        if Application.objects.filter(job=job, candidate=candidate).exists():
            raise ValidationError('You have already applied for this job.')

        serializer.save(job=job, candidate=candidate)

class ApplicationListView(generics.ListAPIView):
    serializer_class   = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Application.objects.filter(
                candidate=user.candidate_profile
            ).select_related('job', 'job__employer')
        elif user.role == 'employer':
            return Application.objects.filter(
                job__employer=user.employer_profile
            ).select_related('job', 'candidate', 'candidate__user')
        return Application.objects.none()


class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class   = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            app = Application.objects.select_related(
                'job', 'job__employer', 'candidate', 'candidate__user'
            ).get(pk=self.kwargs['pk'])
        except Application.DoesNotExist:
            raise NotFound('Application not found.')

        user = self.request.user
        if user.role == 'candidate' and app.candidate != user.candidate_profile:
            raise PermissionDenied()
        if user.role == 'employer' and app.job.employer != user.employer_profile:
            raise PermissionDenied()

        return app

class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class   = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names  = ['patch']

    def get_object(self):
        require_employer(self.request.user)
        try:
            app = Application.objects.select_related('job__employer').get(pk=self.kwargs['pk'])
        except Application.DoesNotExist:
            raise NotFound('Application not found.')

        if app.job.employer != self.request.user.employer_profile:
            raise PermissionDenied('You can only update applications for your own jobs.')

        return app