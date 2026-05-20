import random

from django.core.management.base import BaseCommand

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student, Enrollment
from academics.schoolclass.models import SchoolClass


class Command(BaseCommand):
    help = "Enroll students"

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        classes = SchoolClass.objects.all()
        enrollments = []
        for student in students:
            enrollment = Enrollment(
                student=student,
                school_class=random.choice(classes),
                academic_year=AcademicYear.objects.get(is_active=True)
            )
            enrollments.append(enrollment)

        Enrollment.objects.bulk_create(enrollments)

        self.stdout.write(
            self.style.SUCCESS("Successfully Enrolled students")
        )
