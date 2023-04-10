from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Device(models.Model):
    DEVICE_CONDITION_CHOICES = (
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=DEVICE_CONDITION_CHOICES)
    checked_out_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    checked_out_datetime = models.DateTimeField(null=True, blank=True)
    returned_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
