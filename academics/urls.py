from django.urls import path, include

from academics import teacher
from academics.views import DashboardView

app_name = 'academics'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('teachers/', include('academics.teacher.urls')),
    path('schoolclasses/', include('academics.schoolclass.urls')),
    path('subjects/', include('academics.subject.urls')),
    path('enrolments/', include('academics.enrollment.urls')),
    path('assignments/', include('academics.assignment.urls')),
    path('academicyear/', include('academics.academicyear.urls')),
]