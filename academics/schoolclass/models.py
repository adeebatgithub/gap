from django.db import models

from controller.models import TimeStampedModel
from teacher.teacher.models import Teacher


class SchoolClass(TimeStampedModel):
    name = models.CharField(max_length=100)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="home_room",  null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"