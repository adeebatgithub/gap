from django.utils import timezone
from django.views.generic import TemplateView

from academics.models import Teacher
from academics.teacher.views import TeacherDetailView
from timetable.models import Timetable


class DashboardView(TeacherDetailView):
    template_name = "teacher/dashboard.html"

    def get_object(self, queryset=None):
        return Teacher.objects.get(user=self.request.user)


class TimetableView(TemplateView):
    template_name = "teacher/timetable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "timetable": Timetable.objects.last(),
        })
        return context
