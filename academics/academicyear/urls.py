from django.urls import path

from .views import (
    AcademicYearListView,
    AcademicYearCreateView,
    AcademicYearUpdateView,
    AcademicYearDeleteView, AcademicYearSetActive
)

app_name = "academicyear"

urlpatterns = [
    path('', AcademicYearListView.as_view(), name='list'),
    path('create/', AcademicYearCreateView.as_view(), name='create'),
    path('<int:pk>/update/', AcademicYearUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AcademicYearDeleteView.as_view(), name='delete'),
    path('<int:pk>/set/', AcademicYearSetActive.as_view(), name='set'),
]
