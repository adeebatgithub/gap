from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from academics.schoolclass.models import SchoolClass
from academics.subject.models import Subject
from academics.academicyear.models import AcademicYear


class Command(BaseCommand):
    CLASSES = (
        "Class 1A",
        "Class 2A",
        "Class 3A",
        "Class 4A",
        "Class 5A"
    )

    subjects = (
        "Mathematics",
        "Science",
        "English",
        "Social Studies",
        "Computer Science",
        "Hindi",
        "Malayalam"
    )

    def handle(self, *args, **options):
        for cls in self.CLASSES:
            if not SchoolClass.objects.filter(name__icontains=cls).exists():
                SchoolClass.objects.create(name=cls.strip())
        self.stdout.write(
            self.style.SUCCESS("Classes Created successfully")
        )

        for subject in self.subjects:
            if not Subject.objects.filter(name__icontains=subject).exists():
                Subject.objects.create(name=subject.strip())
        self.stdout.write(
            self.style.SUCCESS("Subjects Created successfully")
        )

        AcademicYear.objects.create(
            name="26-27",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() + timedelta(weeks=25),
        )
        self.stdout.write(
            self.style.SUCCESS("AcademicYear Created successfully")
        )
