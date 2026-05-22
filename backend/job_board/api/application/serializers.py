from rest_framework import serializers
from job_board.models.application import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title    = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.employer.company_name', read_only=True)
    candidate_username = serializers.CharField(source='candidate.user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Application
        fields = [
            'id',
            'job',
            'job_title',
            'company_name',
            'candidate_username',
            'cover_letter',
            'cv_file',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'job': {'read_only': True},
        }


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Application
        fields = ['status']