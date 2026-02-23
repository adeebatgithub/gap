from django.urls import path
from .views import (
    SchoolClassListView,
    SchoolClassDetailView,
)

app_name = 'schoolclass'

urlpatterns = [
    path('', SchoolClassListView.as_view(), name='list'),
    path('<int:pk>/', SchoolClassDetailView.as_view(), name='detail'),
]