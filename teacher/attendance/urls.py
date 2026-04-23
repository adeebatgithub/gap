from django.urls import path

from .views import (
    SessionDetailView,
    SessionDeleteView,
    AttendanceSheetUpsertView,
    MarkAttendance
)

app_name = "attendance"

urlpatterns = [
    path('<int:pk>/', SessionDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', SessionDeleteView.as_view(), name='delete'),

    path('<int:pk>/add', AttendanceSheetUpsertView.as_view(), name='upsert'),
    path('<int:pk>/mark/', MarkAttendance.as_view(), name='mark'),
]
