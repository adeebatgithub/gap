from django.views.generic import TemplateView
from users.mixins import GroupRequiredMixin

from academics.models import AcademicYear


class DashboardView(GroupRequiredMixin, TemplateView):
    group_name = "Admin"
    template_name = 'academics/dashboard.html'

    def get(self, request, *args, **kwargs):
        if AcademicYear.objects.all().count() == 0:
            request.session["is_academic_year_set"] = 0
        return super().get(request, *args, **kwargs)
