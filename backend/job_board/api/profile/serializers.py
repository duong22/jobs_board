from rest_framework import serializers
from job_board.models.candidate import CandidateProfile
from job_board.models.employer import EmployerProfile

class CandidateProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = CandidateProfile
        fields = ('id', 'username', 'email', 'role', 'resume_url', 'linkedin_url')
        read_only_fields = ('id', 'username', 'email', 'role')

class EmployerProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = EmployerProfile
        fields = (
            'id', 'username', 'email', 'role', 
            'company_name', 'company_website', 'description', 'location'
        )
        read_only_fields = ('id', 'username', 'email', 'role')