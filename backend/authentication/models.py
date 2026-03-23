import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CANDIDATE = 'candidate'
    EMPLOYER = 'employer'
    ROLE_CHOICES = [
        (CANDIDATE, 'Candidate'),
        (EMPLOYER, 'Employer'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
