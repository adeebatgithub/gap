from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import MovementForm
from .models import Movement


class MovementListView(PermissionRequiredMixin, ListView):
    permission_required = "teacher.view_movement"
    model = Movement
    template_name = "teacher/movement/list.html"
    context_object_name = "movements"


class MovementCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "teacher.add_movement"
    model = Movement
    form_class = MovementForm
    template_name = "teacher/movement/form.html"
    success_url = reverse_lazy("teacher:movement:list")
    success_message = "Leave added to movement register"


class MovementUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "teacher.change_movement"
    model = Movement
    form_class = MovementForm
    template_name = "teacher/movement/form.html"
    success_url = reverse_lazy("teacher:movement:list")
    success_message = "movement register updated"


class MovementDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "teacher.delete_movement"
    model = Movement
    success_url = reverse_lazy("teacher:movement:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Movement deleted")
        return super().delete(request, *args, **kwargs)
