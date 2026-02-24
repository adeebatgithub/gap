from django.urls import path

from .views import (
    SessionListView,
    SessionDetailView,
    SessionCreateView,
    SessionUpdateView,
    SessionDeleteView,
    MarkAttendance
)

app_name = "attendance"

urlpatterns = [
    path('', SessionListView.as_view(), name='list'),
    path('<int:pk>/', SessionDetailView.as_view(), name='detail'),
    path('create/', SessionCreateView.as_view(), name='create'),
    path('<int:pk>/update/', SessionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', SessionDeleteView.as_view(), name='delete'),

    path('<int:pk>/mark/', MarkAttendance.as_view(), name='mark'),
]
