from django.urls import path

from .views import (
    SubjectClassCreateView,
    SubjectClassUpdateView,
    SubjectClassDeleteView,
)

app_name = "assignment"

urlpatterns = [
    path('create/', SubjectClassCreateView.as_view(), name='create'),
    path('<int:pk>/update/', SubjectClassUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', SubjectClassDeleteView.as_view(), name='delete'),
]
