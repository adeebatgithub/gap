from django.urls import path, include

from . import views

urlpatterns = [
    path('maintenance/', views.MaintenanceView.as_view(), name='maintenance-mode'),
    path('underdev/', views.UnderConstructionView.as_view(), name='underdev-mode'),
]
