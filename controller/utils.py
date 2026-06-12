from academics.academicyear.models import AcademicYear

def get_academic_year(request=None):
    if request and not request.session.get('academic_year'):
        request.session['academic_year'] = AcademicYear.objects.only("id").get(is_active=True).id

    return request.session.get('academic_year')

