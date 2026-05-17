from django.urls import path
from .views import (
    TeacherListView,
    TeacherDetailView,
    TeacherCreateView,
    TeacherUpdateView,
    TeacherDeleteView,
    AddToAdmin, AddToExam,
    RemoveFromAdmin, RemoveFromExam
)

app_name = 'teacher'

urlpatterns = [
    path('', TeacherListView.as_view(), name='list'),
    path('<int:pk>/', TeacherDetailView.as_view(), name='detail'),
    path('create/', TeacherCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TeacherUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TeacherDeleteView.as_view(), name='delete'),


    path('<int:pk>/add/admin', AddToAdmin.as_view(), name='add-admin'),
    path('<int:pk>/add/exam', AddToExam.as_view(), name='add-exam'),
    path('<int:pk>/remove/admin', RemoveFromAdmin.as_view(), name='remove-admin'),
    path('<int:pk>/remove/exam', RemoveFromExam.as_view(), name='remove-exam'),
]