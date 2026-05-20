import random
import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from teacher.teacher.models import Teacher
from django.contrib.auth.models import Group

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Seed sample teachers data"

    DEPARTMENTS = [
        "Mathematics",
        "Science",
        "Language",
        "Computer Science",
        "History",
    ]

    BLOOD_GROUPS = [
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-",
    ]

    def handle(self, *args, **kwargs):
        created_count = 0
        group = Group.objects.get(name="Teacher")

        for i in range(1, 11):
            first_name = fake.first_name()
            last_name = fake.last_name()

            email = f"teacher{i}@school.com"

            # Create user
            user = User.objects.create_user(
                username=f"teacher{i}",
                email=email,
                password="password123",
                first_name=first_name,
                last_name=last_name,
            )

            user.groups.add(group)

            # Create teacher
            Teacher.objects.create(
                uid=uuid.uuid4(),
                code=f"TCH{i:04d}",
                user=user,
                address=fake.address(),
                qualifications=random.choice(
                    [
                        "B.Ed",
                        "M.Ed",
                        "MSc Mathematics",
                        "MA English",
                        "MCA",
                        "PhD Physics",
                    ]
                ),
                dob=fake.date_between(
                    start_date=date(1970, 1, 1),
                    end_date=date(1995, 12, 31),
                ),
                experiences=random.choice(
                    [
                        "2 years teaching experience",
                        "5 years teaching experience",
                        "10 years academic experience",
                        "Worked as HOD for 3 years",
                        "Specialized in child education",
                    ]
                ),
                department=random.choice(self.DEPARTMENTS),
                blood_type=random.choice(self.BLOOD_GROUPS),
            )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {created_count} teachers"
            )
        )