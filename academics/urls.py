from django.urls import path, include

from academics.views import DashboardView

app_name = 'academics'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('schoolclasses/', include('academics.schoolclass.urls')),
    path('subjects/', include('academics.subject.urls')),
    path('enrolments/', include('academics.enrollment.urls')),
    path('academicyear/', include('academics.academicyear.urls')),
    path('assessments/', include('academics.assessment.urls')),
]