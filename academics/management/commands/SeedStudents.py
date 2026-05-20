import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from academics.enrollment.models import Student

fake = Faker()


class Command(BaseCommand):
    help = "Seed sample students data"

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
        students = []

        for i in range(1, 31):
            gender = random.choice(["M", "F"])

            # Random DOB between 2005 and 2015
            dob = fake.date_between(
                start_date=date(2005, 1, 1),
                end_date=date(2015, 12, 31),
            )

            admission_date = dob + timedelta(days=random.randint(1500, 4000))

            student = Student(
                name=fake.name_male() if gender == "M" else fake.name_female(),
                gender=gender,
                reg_number=f"REG{i:04d}",
                father_name=fake.name_male(),
                father_phone=fake.phone_number()[:15],
                mother_name=fake.name_female(),
                address=fake.address(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:15],
                dob=dob,
                health_issues=random.choice(
                    [
                        "",
                        "Asthma",
                        "Diabetes",
                        "Peanut Allergy",
                        "",
                        "",
                    ]
                ),
                blood_group=random.choice(self.BLOOD_GROUPS),
                admission_date=admission_date,
            )

            students.append(student)

        Student.objects.bulk_create(students)

        self.stdout.write(
            self.style.SUCCESS("Successfully seeded 30 students")
        )