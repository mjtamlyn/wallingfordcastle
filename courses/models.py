import uuid

from django.db import models


class CourseSignup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    student_name = models.CharField(max_length=255)
    student_date_of_birth = models.DateField()
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    gdpr_consent = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name
