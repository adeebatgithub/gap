# urls.py
from django.urls import path
from .views import (
    GalleryListView,
    GalleryCreateView,
    GalleryUpdateView,
    GalleryDeleteView,
)

app_name = "gallery"

urlpatterns = [
    path("", GalleryListView.as_view(), name="list"),
    path("create/", GalleryCreateView.as_view(), name="create"),
    path("<int:pk>/update/", GalleryUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", GalleryDeleteView.as_view(), name="delete"),
]