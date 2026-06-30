from django.urls import path, include

from .views import (
    TimetableImageView,
)

app_name = "timetable"

urlpatterns = [
    path('', TimetableImageView.as_view(), name='preview'),
    path('', include("timetable.image.urls")),
]
