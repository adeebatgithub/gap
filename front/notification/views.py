from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import NotificationForm
from front.models import Notification


class NotificationListView(PermissionRequiredMixin, ListView):
    permission_required = 'front.view_notification'
    model = Notification
    template_name = 'front/notification/list.html'
    context_object_name = 'notifications'
    ordering = ['-date']


class NotificationCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'front.add_notification'
    model = Notification
    form_class = NotificationForm
    template_name = 'front/notification/form.html'
    success_url = reverse_lazy('notification:list')


class NotificationUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'front.change_notification'
    model = Notification
    form_class = NotificationForm
    template_name = 'front/notification/form.html'
    success_url = reverse_lazy('notification:list')


class NotificationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'front.delete_notification'
    model = Notification
    success_url = reverse_lazy('notification:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)
