from django.urls import path

from .views import (
    TimetableView, TimetableUpsertView, TimetablePreview
)

app_name = "timetable"

urlpatterns = [
    path('', TimetablePreview.as_view(), name='preview'),
    path('edit', TimetableView.as_view(), name='edit'),
    path('add/', TimetableUpsertView.as_view(), name='create'),
]
