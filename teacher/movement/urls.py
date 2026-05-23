from django.urls import path
from .views import (
    MovementListView,
    MovementCreateView,
    MovementUpdateView,
    MovementDeleteView,
)

app_name = "movement"

urlpatterns = [
    path("", MovementListView.as_view(), name="list"),
    path("create/", MovementCreateView.as_view(), name="create"),
    path("<int:pk>/update/", MovementUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", MovementDeleteView.as_view(), name="delete"),
]