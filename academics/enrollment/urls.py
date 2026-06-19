from django.urls import path

from .views import (
    EnrollmentListView,
    EnrollmentDetailView,
    EnrollmentCreateView,
    EnrollmentUpdateView,
    EnrollmentDeleteView,
    EnrollmentChangeLeaveStatusView,
    StudentImportView,
    StudentImportTemplateView,
)

app_name = 'enrollment'

urlpatterns = [
    path('', EnrollmentListView.as_view(), name='list'),
    path('<int:pk>/', EnrollmentDetailView.as_view(), name='detail'),
    path('create/', EnrollmentCreateView.as_view(), name='create'),
    path('<int:pk>/update/', EnrollmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='delete'),

    path('<int:pk>/onleave/', EnrollmentChangeLeaveStatusView.as_view(), name='onleave'),
    path('<int:pk>/import/', StudentImportView.as_view(), name='import'),
    path('download/template/', StudentImportTemplateView.as_view(), name='template'),
]
