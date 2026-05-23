from django.db import models

from controller.models import TimeStampedModel
from teacher.teacher.models import Teacher


class Movement(TimeStampedModel):
    date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()