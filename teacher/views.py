from academics.teacher.views import TeacherDetailView


class DashboardView(TeacherDetailView):
    template_name = "teacher/dashboard.html"
