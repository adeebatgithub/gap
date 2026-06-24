from django.urls import path, include

from academics.views import StatsView, DashboardView

app_name = 'academics'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('stats/', StatsView.as_view(), name='stats'),

    path('schoolclasses/', include('academics.schoolclass.urls')),
    path('subjects/', include('academics.subject.urls')),
    path('enrolments/', include('academics.enrollment.urls')),
    path('academicyear/', include('academics.academicyear.urls')),
    path('admission/', include('academics.admission.urls')),
]