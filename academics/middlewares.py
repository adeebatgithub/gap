from django.contrib import messages


class CheckForAcademicYearMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get("is_academic_year_set") == 0:
            messages.info(request, "Set Academic Year")
            return self.get_response(request)
        return self.get_response(request)
