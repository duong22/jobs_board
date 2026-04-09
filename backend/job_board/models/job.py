from django.db import models
from .base import BaseModel
from .employer import EmployerProfile


class Job(BaseModel):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
    ]

    TYPE_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("internship", "Internship"),
    ]

    CATEGORY_CHOICES = [
    ("engineering", "Engineering & Technology"),
    ("design", "Design & Creative"),
    ("marketing", "Marketing & Communications"),
    ("sales", "Sales & Business Development"),
    ("finance", "Finance & Accounting"),
    ("hr", "Human Resources"),
    ("customer_service", "Customer Service & Support"),
    ("operations", "Operations & Logistics"),
    ("healthcare", "Healthcare & Medical"),
    ("education", "Education & Training"),
    ("legal", "Legal"),
    ("data", "Data & Analytics"),
    ("product", "Product Management"),
    ("admin", "Administrative & Clerical"),
    ("other", "Other"),
]

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")

    class Meta:
        app_label = "job_board"
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.title} — {self.employer.company_name}"