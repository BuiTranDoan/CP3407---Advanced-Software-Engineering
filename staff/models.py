from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name if full_name else self.user.username} ({self.position})"

class Shift(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    staff_members = models.ManyToManyField(StaffProfile, blank=True, related_name='shifts')

    def __str__(self):
        return f'{self.name} ({self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")})'

    def duration_hours(self):
        """Returns duration of the shift in hours."""
        delta = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
        return round(delta.total_seconds() / 3600, 2)

class WorkLog(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='work_logs')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='work_logs')
    date = models.DateField(default=date.today)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField()
    is_substitute = models.BooleanField(default=False)
    is_overtime = models.BooleanField(default=False)

    def hours_worked(self):
        if self.clock_out_time:
            return round((self.clock_out_time - self.clock_in_time).total_seconds() / 3600,2)
        return 0

    def __str__(self):
        return f"{self.staff.user.get_full_name()} worked on {self.date} for {self.hours_worked()} hours"

"""This might need to be modified"""
class SalaryLog(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)

    total_hours_worked = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    total_absent_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    salary_paid = models.DecimalField(max_digits=7, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.month}/{self.year} :${self.salary_paid}"
