from django.conf import settings
from django.shortcuts import redirect


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "MAINTENANCE_MODE", False) or getattr(settings, "DEBUG", True):
            return self.get_response(request)

        if request.path.startswith("/controller/"):
            return self.get_response(request)

        user = getattr(request, "user", None)
        # if user and user.is_authenticated and user.is_superuser:
        #     return self.get_response(request)

        return redirect("maintenance-mode")
