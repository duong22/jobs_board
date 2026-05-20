from django.db import models
from .base import BaseModel
from .job import Job
from .candidate import CandidateProfile

class Application(BaseModel):
    STATUS_CHOICES  = [
        ('pending',  'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(blank=True)

    class Meta:
        app_label = 'job_board'
        ordering  = ['-created_at']
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate} → {self.job.title} ({self.status})"