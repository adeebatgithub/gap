from django.db import models

from academics.academicyear.models import AcademicYear
from academics.schoolclass.models import SchoolClass
from teacher.teacher.models import Teacher
from controller.models import TimeStampedModel


class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name.title()


class SubjectClass(TimeStampedModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="allocations")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name[:16]}-{self.school_class.name}"
