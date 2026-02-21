from django.urls import path
from .views import (
    SchoolClassListView,
    SchoolClassDetailView,
    SchoolClassCreateView,
    SchoolClassUpdateView,
    SchoolClassDeleteView,
)

app_name = 'schoolclass'

urlpatterns = [
    path('', SchoolClassListView.as_view(), name='list'),
    path('<int:pk>/', SchoolClassDetailView.as_view(), name='detail'),
    path('create/', SchoolClassCreateView.as_view(), name='create'),
    path('<int:pk>/update/', SchoolClassUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', SchoolClassDeleteView.as_view(), name='delete'),
]