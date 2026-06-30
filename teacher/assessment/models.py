from django.db import models

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student
from academics.subject.models import SubjectClass
from controller.models import TimeStampedModel


class Assessment(TimeStampedModel):
    CHOICES = (
        ("assignment", "Assignment"),
        ("viva", "Viva"),
        ("seminar", "Seminar"),
        ("written exam", "Written exam"),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE)
    date = models.DateField()
    assessment_type = models.CharField(choices=CHOICES, max_length=20)
    mark = models.IntegerField()

    def __str__(self):
        return self.subject_class


class Grade(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
