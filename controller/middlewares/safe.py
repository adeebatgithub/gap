import logging

from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class ExceptionRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.primary_error_path = reverse("landing:home")
        self.fallback_path = reverse("exception-mode")

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if settings.DEBUG:
            return None

        logger.exception(
            "Unhandled exception occurred",
            extra={
                "path": request.path,
                "method": request.method,
                "user": getattr(request.user, "id", None),
            },
        )

        # If we're already on the error page, do NOT redirect again
        if request.path == self.primary_error_path:
            return redirect(self.fallback_path)

        # Absolute last line of defense: avoid infinite redirects entirely
        if request.path == self.fallback_path:
            return HttpResponseServerError(
                "Something went wrong. Please try again later."
            )

        return redirect(self.primary_error_path)
