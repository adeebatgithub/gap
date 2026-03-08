from django.urls import path, include

from teacher.views import DashboardView, TimetableView

app_name = 'teacher'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('attendance/', include("teacher.attendance.urls")),
    path('schoolclass/', include("teacher.schoolclass.urls")),
]