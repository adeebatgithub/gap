from django.db import models

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student
from academics.subject.models import SubjectClass
from controller.models import TimeStampedModel


class Session(TimeStampedModel):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE, related_name="sessions")
    period = models.IntegerField()
    date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


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
