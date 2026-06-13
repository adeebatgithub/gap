import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from controller.consts import BLOOD_GROUP_CHOICES
from controller.models import TimeStampedModel


def teacher_photo_path(instance, filename):
    return f"teachers/%Y/{instance.name}/photos/{filename}"


def teacher_cv_path(instance, filename):
    return f"teachers/%Y/{instance.name}/cvs/{filename}"


class Teacher(TimeStampedModel):
    uid = models.CharField(max_length=50, unique=True, null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    experiences = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    blood_type = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    photo = models.ImageField(upload_to=teacher_photo_path, null=True, blank=True)
    cv = models.FileField(upload_to=teacher_cv_path, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        return super(Teacher, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return any(
            group.name == "Admin"
            for group in self.user.groups.all()
        )

    @property
    def is_exam(self):
        return any(
            group.name == "Exam"
            for group in self.user.groups.all()
        )

    @property
    def qualification_list(self):
        if not self.qualifications:
            return []
        return [q.strip() for q in self.qualifications.split(',') if q.strip()]

    @property
    def experience_list(self):
        if not self.experiences:
            return []
        return [e.strip() for e in self.experiences.split(',') if e.strip()]
