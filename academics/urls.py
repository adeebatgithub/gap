from django.urls import path

from academics.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]