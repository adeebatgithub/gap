from django.db import models
from django.utils import timezone

from academics.models import SchoolClass, SubjectClass
from controller.models import TimeStampedModel


class Timetable(TimeStampedModel):
    date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.localdate()
        return super().save(*args, **kwargs)

class TimetableClass(TimeStampedModel):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='classes')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)


class TimetablePeriod(TimeStampedModel):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='periods')
    number = models.IntegerField()
    time_range = models.CharField(max_length=50)


class TimetableCell(TimeStampedModel):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='cells')
    period_number = models.IntegerField()
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE)
    is_marked = models.BooleanField(default=False)
