from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.aggregates import Sum
from django.db.models.expressions import ExpressionWrapper, F
from django.db.models.fields import DurationField
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from controller.views import ExportAsXlsxView
from .forms import MovementForm
from .models import Movement
from ..teacher.models import Teacher


class MovementListView(PermissionRequiredMixin, ListView):
    permission_required = "teacher.view_movement"
    model = Movement
    template_name = "teacher/movement/list.html"
    context_object_name = "movements"
    ordering = "-date"

    def get_template_names(self):
        if self.request.htmx:
            return ["teacher/movement/partial_list.html"]
        return super().get_template_names()

    def get_filters(self) -> dict:
        filters = {}
        if self.request.GET.get("date"):
            filters["date"] = self.request.GET.get("date")
        if self.request.GET.get("teacher"):
            filters["teacher_id"] = self.request.GET.get("teacher")
        return filters

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(**self.get_filters())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "teachers": Teacher.objects.only("id"),
        })
        return context


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


class MovementExportView(PermissionRequiredMixin, ExportAsXlsxView):
    permission_required = "teacher.view_movement"
    workbook_title = "Movement Register"
    filename = "movement_register.xlsx"
    model = Movement
    fields = ["date", "teacher", "start_time", "end_time"]
    headers = ["date", "teacher", "from", "to"]

    def get_filters(self) -> dict:
        filters = {}
        if self.request.GET.get("date"):
            filters["date"] = self.request.GET.get("date")
        if self.request.GET.get("teacher"):
            filters["teacher_id"] = self.request.GET.get("teacher")
        return filters

    @staticmethod
    def get_total_durations():
        return (
            Movement.objects
            .annotate(
                duration=ExpressionWrapper(
                    F("end_time") - F("start_time"),
                    output_field=DurationField()
                )
            )
            .values("teacher__user__first_name", "teacher__user__last_name")
            .annotate(total_duration=Sum("duration"))
        )

    def get_sheet(self):
        workbook = super().get_sheet()
        total_sheet = workbook.create_sheet("Total")
        total_sheet.append(["teacher", "total hrs"])
        for duration in self.get_total_durations():
            hours = duration["total_duration"].total_seconds() / 3600
            total_sheet.append([f"{duration['teacher__user__first_name']} {duration['teacher__user__last_name']}", hours])
        return workbook
