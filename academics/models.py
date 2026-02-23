from django.contrib.auth import get_user_model
from django.db import models

from controller.models import TimeStampedModel


class Teacher(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class SchoolClass(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubjectClass(TimeStampedModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Student(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AcademicYear(TimeStampedModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.start_date.strftime("%B %Y")


class Enrollment(TimeStampedModel):
    ACTIVE = 1
    GRADUATED = 2
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (GRADUATED, 'Graduated'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Session(TimeStampedModel):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.academic_year_id:
            self.academic_year = AcademicYear.objects.get(is_active=True)
        return super().save(*args, **kwargs)


class Attendance(TimeStampedModel):
    PENDING = 0
    PRESENT = 1
    ABSENT = 2
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
