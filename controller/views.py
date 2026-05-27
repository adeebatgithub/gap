from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View
from openpyxl.workbook.workbook import Workbook


class MaintenanceView(TemplateView):
    template_name = "controller/maintenance.html"

    def get(self, request, *args, **kwargs):
        if not getattr(settings, "MAINTENANCE_MODE", False):
            return redirect(reverse_lazy("users:redirect-user"))
        return super().get(request, *args, **kwargs)


class UnderConstructionView(TemplateView):
    template_name = "controller/underdev.html"


class ExportAsXlsxView(View):
    workbook_title = "Export"
    filename = "export.xlsx"

    model = None
    fields = []
    headers = None

    def get_filters(self) -> dict:
        return {}

    def get_queryset(self):
        return self.model.objects.filter(**self.get_filters())

    def get_headers(self):
        """
        Return excel column headers.
        """
        return self.headers or self.fields

    def get_row(self, obj):
        """
        Return row values for a model instance.
        """
        row = []

        for field in self.fields:
            value = getattr(obj, field)
            if callable(value):
                value = value()

            row.append(str(value))
        return row

    def get_sheet(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = self.workbook_title
        worksheet.append(self.get_headers())

        queryset = self.get_queryset()
        for obj in queryset.iterator():
            worksheet.append(self.get_row(obj))
        return workbook

    def get(self, request, *args, **kwargs):
        if not self.model:
            raise ValueError("model is required")

        if not self.fields:
            raise ValueError("fields cannot be empty")

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{self.filename}"'
        )
        workbook = self.get_sheet()
        workbook.save(response)
        return response
