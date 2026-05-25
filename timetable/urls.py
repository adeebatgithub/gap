from django.urls import path

from .views import (
    TimetableView, TimetableUpsertView, TimetablePreview,
    TimeTableSubjectsPartialView
)

app_name = "timetable"

urlpatterns = [
    path('', TimetablePreview.as_view(), name='preview'),
    path('edit', TimetableView.as_view(), name='edit'),
    path('add/', TimetableUpsertView.as_view(), name='create'),
    path('partial/subject/', TimeTableSubjectsPartialView.as_view(), name='partial-subject'),
]
