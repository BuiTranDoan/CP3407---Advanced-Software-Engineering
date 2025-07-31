from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} ({self.position})"
