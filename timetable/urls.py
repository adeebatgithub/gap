from django.urls import path

from .views import (
    TimetableView, TimetableUpsertView
)

app_name = "timetable"

urlpatterns = [
    path('', TimetableView.as_view(), name='index'),
    path('add/', TimetableUpsertView.as_view(), name='create'),
]
