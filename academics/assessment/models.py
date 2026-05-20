from django.db import models

from controller.models import TimeStampedModel
from academics.subject.models import Subject
from academics.schoolclass.models import SchoolClass
from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student

class Assessment(TimeStampedModel):
    CHOICES = (
        ("sem written exam", "sem written Exam"),
        ("sem viva exam", "sem viva Exam"),

        ("internal exam", "Internal exam"),
        ("assignment", "Assignment"),
        ("project", "Project"),
        ("viva", "Viva"),
        ("seminar", "Seminar"),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.subject.name

    def save(self, *args, **kwargs):
        if not self.academic_year:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Grade(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)