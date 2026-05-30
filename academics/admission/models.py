from django.db import models

from controller.models import TimeStampedModel


class Admission(TimeStampedModel):
    full_name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    dob = models.DateField()
    mother_tongue = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    house_name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_1 = models.CharField(max_length=100)
    phone_2 = models.CharField(max_length=100, null=True, blank=True)
    center = models.CharField(max_length=100)