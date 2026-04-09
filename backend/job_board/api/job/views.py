import django_filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from job_board.models.job import Job
from .serializers import JobSerializer


class JobFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['category', 'job_type', 'location', 'status']


def require_employer(user):
    if not user.is_authenticated:
        raise PermissionDenied('Authentication required.')
    if user.role != 'employer':
        raise PermissionDenied('Only employers can perform this action.')


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    filterset_class = JobFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Job.objects.filter(status="open").select_related('employer')

    def perform_create(self, serializer):
        require_employer(self.request.user)
        employer_profile = self.request.user.employer_profile
        serializer.save(employer=employer_profile)

class MyJobListView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_class = (IsAuthenticated,)

    def get_queryset(self):
        require_employer(self.request.user)
        return Job.objects.filter(employer=self.request.user.employer_profile).select_related('employer')

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Job.objects.all().select_related('employer')

    def get_object(self):
        try:
            job = Job.objects.select_related('employer').get(pk=self.kwargs['pk'])
        except Job.DoesNotExist:
            raise NotFound('Job not found.')

        if self.request.method not in ('GET', 'HEAD', 'OPTIONS'):
            require_employer(self.request.user)
            if job.employer != self.request.user.employer_profile:
                raise PermissionDenied('You can only edit your own job postings.')

        return job

    def perform_destroy(self, instance):
        instance.delete()