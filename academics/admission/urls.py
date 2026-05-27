from django.urls import path

from .views import (
    AdmissionListView,
    AdmissionCreateView,
    AdmissionDetailView,
    AdmissionUpdateView,
    AdmissionDeleteView,
    AdmissionExportView
)

app_name = "admission"

urlpatterns = [
    path('', AdmissionListView.as_view(), name='list'),
    path('<int:pk>/', AdmissionDetailView.as_view(), name='detail'),
    path('create/', AdmissionCreateView.as_view(), name='create'),
    path('update/<int:pk>/', AdmissionUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', AdmissionDeleteView.as_view(), name='delete'),
    path('export/', AdmissionExportView.as_view(), name='export'),
]
