from django.views.generic import TemplateView
from users.mixins import GroupRequiredMixin

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Enrollment


class DashboardView(GroupRequiredMixin, TemplateView):
    group_name = "Admin"
    template_name = 'academics/dashboard.html'

    @staticmethod
    def _get_enrollments():
        return Enrollment.objects.filter(status=Enrollment.ACTIVE)

    def _get_total_enrollments_gender(self, gender):
        return self._get_enrollments().filter(student__gender=gender).count()

    def _get_total_on_leave(self):
        return self._get_enrollments().filter(on_leave=True).count()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "total_enrollments": self._get_enrollments().count(),
            "total_M": self._get_total_enrollments_gender(gender="M"),
            "total_F": self._get_total_enrollments_gender(gender="F"),
            "total_leave": self._get_total_on_leave(),
        })
        return context

    def get(self, request, *args, **kwargs):
        if AcademicYear.objects.all().count() == 0:
            request.session["is_academic_year_set"] = 0
        self.request.session["navbar"] = "admin"
        return super().get(request, *args, **kwargs)
