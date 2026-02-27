from django.contrib import messages

from academics.models import AcademicYear


class CheckForAcademicYearMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if AcademicYear.objects.filter(is_active=True).count() == 0:
            request.session["is_academic_year_set"] = 0
            messages.info(request, "Set Academic Year")
            return self.get_response(request)

        request.session["is_academic_year_set"] = 1
        return self.get_response(request)
