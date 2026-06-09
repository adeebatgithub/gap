from django.db import models

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student
from academics.subject.models import SubjectClass
from controller.models import TimeStampedModel


class Session(TimeStampedModel):
    subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE, related_name="sessions")
    period = models.IntegerField()
    date = models.DateField()


class Attendance(TimeStampedModel):
    PENDING = 0
    PRESENT = 1
    ABSENT = 2
    LEAVE = 3
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LEAVE, 'Leave'),
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
