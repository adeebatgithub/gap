from django.urls import path
from .views import (
    NotificationListView,
    NotificationCreateView,
    NotificationUpdateView,
    NotificationDeleteView,
)

app_name = 'notification'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('create/', NotificationCreateView.as_view(), name='create'),
    path('<int:pk>/update/', NotificationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', NotificationDeleteView.as_view(), name='delete'),
]