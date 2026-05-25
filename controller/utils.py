from academics.academicyear.models import AcademicYear

def get_academic_year(request=None):
    if request and request.session.get('academic_year'):
        return AcademicYear.objects.only("id").get(id=request.session.get('academic_year')).id

    return AcademicYear.objects.only("id").get(is_active=True).id

