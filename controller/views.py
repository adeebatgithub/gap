from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView


class MaintenanceView(TemplateView):
    template_name = "controller/maintenance.html"

    def get(self, request, *args, **kwargs):
        if not getattr(settings, "MAINTENANCE_MODE", False):
            return redirect(reverse_lazy("users:redirect-user"))
        return super().get(request, *args, **kwargs)

