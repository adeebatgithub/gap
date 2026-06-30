from django.urls import path
from .views import (
    TimetableImageListView,
    TimetableImageCreateView,
    TimetableImageUpdateView,
)

app_name = "image"

urlpatterns = [
    path('images/', TimetableImageListView.as_view(), name='list'),
    path('images/create/', TimetableImageCreateView.as_view(), name='create'),
    path('images/<int:pk>/update/', TimetableImageUpdateView.as_view(), name='update'),
]