from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from users.mixins import GroupRequiredMixin

from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Enrollment

@method_decorator(cache_page(60*15), name="dispatch")
class DashboardView(GroupRequiredMixin, TemplateView):
    group_name = "Admin"
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "enrollment_stats": self._get_enrollment_stats(),
        })
        return context

    def get(self, request, *args, **kwargs):
        if AcademicYear.objects.all().count() == 0:
            request.session["is_academic_year_set"] = 0
        else:
            request.session["academic_year"] = AcademicYear.objects.get(is_active=True).id

        if year:=request.GET.get("academic_year"):
            request.session["academic_year"] = year

        self.request.session["navbar"] = "admin"
        return super().get(request, *args, **kwargs)
