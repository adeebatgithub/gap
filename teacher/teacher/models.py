import uuid

from django.contrib.auth import get_user_model
from django.db import models

from controller.consts import BLOOD_GROUP_CHOICES
from controller.models import TimeStampedModel


def teacher_photo_path(instance, filename):
    return f"teachers/%Y/{instance.name}/photos/{filename}"


def teacher_cv_path(instance, filename):
    return f"teachers/%Y/{instance.name}/cvs/{filename}"


class Teacher(TimeStampedModel):
    uid = models.UUIDField(editable=False)
    code = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.TextField()
    qualifications = models.TextField()
    dob = models.DateField()
    experiences = models.TextField()
    department = models.CharField(max_length=50)
    blood_type = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    photo = models.ImageField(upload_to=teacher_photo_path, null=True, blank=True)
    cv = models.FileField(upload_to=teacher_cv_path, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        return super(Teacher, self).save(*args, **kwargs)

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
