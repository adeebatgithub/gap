from django.db import models

from controller.models import TimeStampedModel


class Admission(TimeStampedModel):
    COURSE_CHOICES = (
        ('ilp', 'Integrated Learning Programme (ILP | Boys) — 5 Years'),
        ('ils', 'Islamic Life Solutions (ILS | Girls) — 3 Years'),
        ('lateral entry', 'ILP Lateral Entry (Degree | Boys) — 3 Years'),
    )

    CENTERS_CHOICES = (
        ('mjr', 'Manjeri'),
        ('klm', 'Kollam'),
        ('alv', 'Aluva'),
        ('tsy', 'Thalassery'),
    )

    full_name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    dob = models.DateField()
    mother_tongue = models.CharField(max_length=100)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    house_name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_1 = models.CharField(max_length=100)
    phone_2 = models.CharField(max_length=100, null=True, blank=True)
    center = models.CharField(max_length=100, choices=CENTERS_CHOICES)