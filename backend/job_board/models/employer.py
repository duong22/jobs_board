from django.db import models
from .base import BaseModel 
from authentication.models import User

class EmployerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Employer: {self.user.username}"