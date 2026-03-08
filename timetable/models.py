from django.db import models

from academics.models import SchoolClass, SubjectClass
from controller.models import TimeStampedModel


class Timetable(TimeStampedModel):
    pass


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
