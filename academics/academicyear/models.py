from django.db import models

from controller.models import TimeStampedModel


class AcademicYear(TimeStampedModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.start_date.strftime("%B %Y")