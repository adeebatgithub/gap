from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, RedirectView

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Enrollment
from teacher.attendance.models import Attendance
from users.mixins import GroupRequiredMixin


class DashboardView(GroupRequiredMixin, RedirectView):
    group_name = "Admin"
    url = reverse_lazy("academics:stats")

    def get(self, request, *args, **kwargs):
        if AcademicYear.objects.all().count() == 0:
            request.session["is_academic_year_set"] = 0
        else:
            request.session["academic_year"] = AcademicYear.objects.get(is_active=True).id

        if year := request.GET.get("academic_year"):
            request.session["academic_year"] = year

        self.request.session["navbar"] = "admin"
        return super().get(request, *args, **kwargs)


class StatsView(PermissionRequiredMixin, TemplateView):
    permission_required = "academics.view_stats"
    template_name = 'academics/dashboard.html'

    @staticmethod
    def _get_enrollments():
        return Enrollment.objects.filter(status=Enrollment.ACTIVE)

    def _get_enrollment_stats(self):
        stats = (
            self._get_enrollments()
            .aggregate(
                total_enrollments=Count('id'),
                total_M=Count('id', filter=Q(student__gender="M")),
                total_present_M=Count('id', filter=Q(student__gender="M", on_leave=False)),
                total_F=Count('id', filter=Q(student__gender="F")),
                total_present_F=Count('id', filter=Q(student__gender="F", on_leave=False)),
                total_leave=Count('id', filter=Q(on_leave=True)),
            )
        )
        return stats

    @staticmethod
    def _get_attendance_stats():
        return Attendance.objects.filter(session__period=0, session__date=timezone.localdate()).aggregate(
            total=Count('id'),
            total_M=Count('id', filter=Q(student__gender="M", status=Attendance.PRESENT)),
            total_F=Count('id', filter=Q(student__gender="F", status=Attendance.PRESENT)),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "enrollment_stats": self._get_enrollment_stats(),
            "attendance_stats": self._get_attendance_stats(),
        })
        return context
