from django.db import models
from .base import BaseModel 
from authentication.models import User

class CandidateProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    resume_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"Candidate: {self.user.username}"
    