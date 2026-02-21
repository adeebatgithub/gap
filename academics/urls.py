from django.urls import path, include

from academics import teacher
from academics.views import DashboardView

app_name = 'academics'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('teachers/', include('academics.teacher.urls')),
    path('schoolclass/', include('academics.schoolclass.urls')),
    path('subject/', include('academics.subject.urls')),
]