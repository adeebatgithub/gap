import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from academics.enrollment.models import Enrollment
from academics.subject.models import SubjectClass
from teacher.attendance.models import Session, Attendance


class Command(BaseCommand):
    help = "Seed Attendance"

    def handle(self, *args, **kwargs):
        allocations = SubjectClass.objects.all()
        for allocation in allocations:
            count = 0
            for i in range(1, 31):
                session = Session.objects.create(
                    subject_class=allocation,
                    period=i,
                    date=timezone.localdate()
                )
                count += 1
                enrollments = Enrollment.objects.filter(school_class=allocation.school_class)
                attendances = []
                for enrollment in enrollments:
                    attendance = Attendance(
                        session=session,
                        student=enrollment.student,
                        status=random.choice((Attendance.PRESENT, Attendance.ABSENT))
                    )
                    attendances.append(attendance)
                Attendance.objects.bulk_create(attendances)

            self.stdout.write(
                self.style.SUCCESS(f"Successfully seeded for {allocation.subject}: {count}")
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully seeded attendance")
        )
