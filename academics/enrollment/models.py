from django.db import models

from academics.schoolclass.models import SchoolClass
from controller.consts import BLOOD_GROUP_CHOICES
from controller.models import TimeStampedModel


def student_photo_path(instance, filename):
    return f"students/photos/{instance.name}/{filename}"


class Student(TimeStampedModel):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default="M", null=True, blank=True)
    reg_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_phone = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    health_issues = models.TextField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    photo = models.ImageField(upload_to=student_photo_path, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def health_issue_list(self):
        if not self.health_issues:
            return []
        return [e.strip() for e in self.health_issues.split(',') if e.strip()]


class Enrollment(TimeStampedModel):
    ACTIVE = 1
    GRADUATED = 2
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (GRADUATED, 'Graduated'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="enrollments")
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    on_leave = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name
