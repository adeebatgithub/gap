from django.urls import path

from .views import (
    SubjectListView,
    SubjectDetailView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
)

app_name = 'subject'

urlpatterns = [
    path('', SubjectListView.as_view(), name='list'),
    path('<int:pk>/', SubjectDetailView.as_view(), name='detail'),
    path('create/', SubjectCreateView.as_view(), name='create'),
    path('<int:pk>/update/', SubjectUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', SubjectDeleteView.as_view(), name='delete'),
]
