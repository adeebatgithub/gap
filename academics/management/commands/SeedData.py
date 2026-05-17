from django.core.management import BaseCommand

from academics.models import SchoolClass, Subject


class Command(BaseCommand):
    CLASSES = (
        "ILP H1", "ILP C1",
        "ILP H2", "ILP C2",
        "ILP 3 SOC", "ILP 3 BCA",
        "ILP 4 ARB", "ILP 4 BCA", "ILP 4 SOC", "ILP 4 BCOM",
        "ILP 5",
        "ILS 1", "ILS 2"
    )

    subjects = (
        "AQD",
        "ARB",
        "BLF",
        "CLA.LIT",
        "COR&AU",
        "DS",
        "EFC",
        "ENG",
        "FIQ",
        "FMGNT",
        "HAD",
        "ISS&C",
        "MOD.ARB",
        "NCPUL DIP",
        "PWP",
        "QUR",
        "RHETC",
        "RWE",
        "S&MA",
        "SOC",
        "SOC IN",
        "USOC",
        "SOFTE",
        "URDU"
    )

    def handle(self, *args, **options):
        for cls in self.CLASSES:
            if not SchoolClass.objects.filter(name__icontains=cls).exists():
                SchoolClass.objects.create(name=cls.strip())
        self.stdout.write("Classes Created successfully")

        for subject in self.subjects:
            if not Subject.objects.filter(name__icontains=subject).exists():
                Subject.objects.create(code=subject.strip())
        self.stdout.write("Subjects Created successfully")
