from academics.academicyear.models import AcademicYear


def get_academic_year():
    year = AcademicYear.objects.filter(is_active=True)
    if year:
        return year.first().name
    return None


def global_data(request):
    return {
        "ACADEMIC_YEAR": get_academic_year(),
        "ACADEMIC_YEARS": AcademicYear.objects.only("id", "name", "is_active"),
    }
