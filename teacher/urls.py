from django.urls import path, include

from teacher.views import DashboardView

app_name = 'teacher'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('attendance/', include("teacher.attendance.urls")),
    path('schoolclass/', include("teacher.schoolclass.urls")),
]