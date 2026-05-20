from django.contrib import messages
from django.views.generic import TemplateView

from teacher.teacher.models import Teacher
from teacher.teacher.views import TeacherDetailView
from timetable.models import Timetable


class DashboardView(TeacherDetailView):
    template_name = "teacher/dashboard.html"

    def get_object(self, queryset=None):
        self.request.session["navbar"] = "teacher"
        return Teacher.objects.get(user=self.request.user)


class TimetableView(TemplateView):
    template_name = "teacher/timetable.html"

    def get_table(self):
        if date := self.request.GET.get('date'):
            table = Timetable.objects.filter(created_at__date=date)
            if table:
                return table.first()
            else:
                messages.info(self.request, "Timetable not found")
        return Timetable.objects.last()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "timetable": self.get_table(),
        })
        return context
