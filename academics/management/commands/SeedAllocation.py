import random

from django.core.management.base import BaseCommand

from academics.schoolclass.models import SchoolClass
from academics.subject.models import SubjectClass, Subject
from teacher.teacher.models import Teacher


class Command(BaseCommand):
    help = "Allocate subjects to teachers"

    def handle(self, *args, **kwargs):
        teachers = Teacher.objects.all()
        classes = SchoolClass.objects.all()
        subjects = Subject.objects.all()
        allocations = []
        for teacher in teachers:
            allocation = SubjectClass(
                teacher=teacher,
                school_class=random.choice(classes),
                subject=random.choice(subjects)
            )
            allocations.append(allocation)

        SubjectClass.objects.bulk_create(allocations)
        self.stdout.write(
            self.style.SUCCESS("Successfully Allocated subjects to teachers")
        )
