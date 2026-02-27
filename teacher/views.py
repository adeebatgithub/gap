from academics.models import Teacher
from academics.teacher.views import TeacherDetailView


class DashboardView(TeacherDetailView):
    template_name = "teacher/dashboard.html"

    def get_object(self, queryset=None):
        return Teacher.objects.get(user=self.request.user)
