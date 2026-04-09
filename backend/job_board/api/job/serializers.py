from rest_framework import serializers
from job_board.models.job import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='employer.company_name', read_only=True)
    company_location = serializers.CharField(source='employer.location', read_only=True)

    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'location',
            'job_type',
            'job_type_display',
            'category',
            'category_display',
            'description',
            'status',
            'status_display',
            'company_name',
            'company_location',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'status': {'required': False},
        }