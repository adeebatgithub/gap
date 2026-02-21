from django.urls import path, include

from . import views

urlpatterns = [
    path('maintenance/', views.MaintenanceView.as_view(), name='maintenance-mode'),
    path('somthing-went-wrong/contact-support/', views.ExceptionView.as_view(), name='exception-mode'),
]
