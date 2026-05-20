from django.db import models

from controller.models import TimeStampedModel


class SchoolClass(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"