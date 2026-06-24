from django.urls import path, include

from teacher.views import DashboardView, TimetableView, ProfileView

app_name = 'teacher'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include('teacher.teacher.urls')),
    path('allocation/', include('teacher.assignment.urls')),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('attendance/', include("teacher.attendance.urls")),
    path('schoolclass/', include("teacher.schoolclass.urls")),
    path('movement/', include("teacher.movement.urls")),
    path('assessments/', include('teacher.assessment.urls')),
]