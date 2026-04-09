from rest_framework import serializers
from job_board.models.candidate import CandidateProfile
from job_board.models.employer import EmployerProfile

class CandidateProfileSerializer(serializers.ModelSerializer):
    # Добавляем данные из связанной модели User
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CandidateProfile
        # Поля: username и email теперь включены в список [cite: 51]
        fields = ('username', 'email', 'resume_url', 'linkedin_url')
        read_only_fields = ('username', 'email')

class EmployerProfileSerializer(serializers.ModelSerializer):
    # Добавляем данные из связанной модели User
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = EmployerProfile
        # Поля: включая username и email по просьбе супервайзера [cite: 51]
        fields = ('username', 'email', 'company_name', 'company_website', 'description', 'location')
        read_only_fields = ('username', 'email')